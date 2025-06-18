from rich.traceback import install
install()

import pytest
import os
import shutil
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='function')
def resource(request):
    test_name = request.node.name

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--start-maximized"], headless=True)

        context = browser.new_context(
            viewport=None,
            record_video_dir="videos/"
        )

        # ✅ Start tracing
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.set_default_timeout(30000)
        page.set_default_navigation_timeout(30000)

        yield page  # Test runs here

        test_failed = request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False

        # ✅ Stop tracing and save if failed
        if test_failed:
            os.makedirs("traces", exist_ok=True)
            trace_path = f"traces/{test_name}.zip"
            context.tracing.stop(path=trace_path)
            print(f"[Trace saved] {trace_path}")
        else:
            context.tracing.stop()

        # ✅ Rename video file to test name
        try:
            video_path = page.video.path()
            new_video_path = f"videos/{test_name}.webm"
            os.makedirs("videos", exist_ok=True)
            page.close()  # must close page before accessing video file
            shutil.move(video_path, new_video_path)
            print(f"[Video saved] {new_video_path}")
        except Exception as e:
            print(f"[Video error] {e}")
            page.close()

        context.close()
        browser.close()


# the following hook is for detecting test status
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Get the report and attach to the test `item`
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)