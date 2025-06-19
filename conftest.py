import pytest
import os
import shutil
from datetime import datetime
from playwright.sync_api import sync_playwright, Page
from typing import Generator

# Required for HTML reporting
try:
    from pytest_html import extras
except ImportError:
    extras = None

# Constants
VIDEO_DIR = "videos"
TRACE_DIR = "traces"
REPORT_DIR = "report"
DEFAULT_TIMEOUT = 30000  # 30 seconds


class TestConfig:
    PROJECT = os.getenv("PROJECT_NAME", "Playwright Automation")
    TESTER = os.getenv("TESTER_NAME", "Mahbubur Rahman")
    ENVIRONMENT = os.getenv("ENV", "Staging")
    BROWSER = os.getenv("BROWSER", "Chromium")
    HEADLESS = not bool(os.getenv("HEADFUL", False))
#    HEADLESS = not bool(os.getenv("HEADFUL", True))



# Ensure directories exist
for directory in [VIDEO_DIR, TRACE_DIR, REPORT_DIR]:
    os.makedirs(directory, exist_ok=True)


def pytest_configure(config):
    """Configure pytest and HTML reporting."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")
    config.option.htmlpath = report_path

    # Metadata configuration
    if not hasattr(config.option, "html_metadata"):
        config.option.html_metadata = {}

    config.option.html_metadata.update({
        "Project": TestConfig.PROJECT,
        "Tester": TestConfig.TESTER,
        "Environment": TestConfig.ENVIRONMENT,
        "Browser": TestConfig.BROWSER,
        "Execution Time": timestamp
    })

    print(f"\n[✅] HTML report will be generated at: {report_path}")


def pytest_html_report_title(report):
    report.title = "🧪 Test Report | Playwright"


def pytest_html_results_table_header(cells):
    cells.insert(1, '<th class="status">Status</th>')


def pytest_html_results_table_row(report, cells):
    """Customize test status in report."""
    status_icons = {
        "passed": '<span style="color: green;">✔ PASSED</span>',
        "failed": '<span style="color: red;">✖ FAILED</span>',
        "skipped": '<span style="color: orange;">⚠ SKIPPED</span>'
    }
    if report.outcome in status_icons:
        cells.insert(1, f'<td class="col-status">{status_icons[report.outcome]}</td>')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Collect artifacts for failed tests."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed and extras:
        test_name = item.name
        report_extras = getattr(report, "extras", [])

        # Add video link if exists
        video_path = os.path.join(VIDEO_DIR, f"{test_name}.webm")
        if os.path.exists(video_path):
            report_extras.append(extras.html(f'<a href="{video_path}">🎥 Video</a>'))

        # Add trace link if exists
        trace_path = os.path.join(TRACE_DIR, f"{test_name}.zip")
        if os.path.exists(trace_path):
            report_extras.append(extras.html(f'<a href="{trace_path}">📝 Trace</a>'))

        report.extras = report_extras


@pytest.fixture(scope="session", autouse=True)
def resource(request):
    """Playwright page fixture with automatic tracing and video recording."""
    test_name = request.node.name

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=TestConfig.HEADLESS,
            args=["--start-maximized"]
        )

        context = browser.new_context(
#            no_viewport=True,
            viewport=None, #{"width": 1920, "height": 1080},
            record_video_dir=VIDEO_DIR,
            ignore_https_errors=True
        )

        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        page.set_default_navigation_timeout(DEFAULT_TIMEOUT)

        yield page

        test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

        trace_path = os.path.join(TRACE_DIR, f"{test_name}.zip")
        context.tracing.stop(path=trace_path if test_failed else None)

        if test_failed:
            print(f"\n[🔍] Trace saved: {trace_path}")

        try:
            if page.video:
                video_path = page.video.path()
                new_video_path = os.path.join(VIDEO_DIR, f"{test_name}.webm")
                shutil.move(video_path, new_video_path)
                print(f"\n[🎥] Video saved: {new_video_path}")
        except Exception as e:
            print(f"\n[⚠️] Video error: {str(e)}")

        page.close()
        context.close()
        browser.close()