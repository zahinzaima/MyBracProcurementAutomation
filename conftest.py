import pytest
from pathlib import Path
import shutil
import time
from datetime import datetime
from typing import Optional
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

# Configuration
ARTIFACTS_DIR = Path("artifacts")
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TRACES_DIR = ARTIFACTS_DIR / "traces"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"

# Global variables
global_browser: Optional[Browser] = None
global_context: Optional[BrowserContext] = None
global_page: Optional[Page] = None


def pytest_configure(config):
    """Clear artifacts directory before test run"""
    if ARTIFACTS_DIR.exists():
        shutil.rmtree(ARTIFACTS_DIR, ignore_errors=True)  # Added ignore_errors
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(exist_ok=True)
    TRACES_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)


def safe_file_operation(file_path, operation, max_retries=3, delay=1):
    """Helper function to handle file operations with retries"""
    for attempt in range(max_retries):
        try:
            return operation(file_path)
        except (PermissionError, OSError) as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    global global_browser
    if global_browser is None:
        global_browser = playwright.chromium.launch(headless=False, slow_mo=500)
    yield global_browser

    if global_browser:
        global_browser.close()
        global_browser = None


@pytest.fixture
def context(browser: Browser, request) -> BrowserContext:
    global global_context
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=VIDEOS_DIR,
        record_video_size={"width": 1920, "height": 1080}
    )

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    yield context

    # Save trace on test failure
    if request.node.rep_call.failed:
        trace_path = TRACES_DIR / f"{timestamp}_{test_name}_trace.zip"
        context.tracing.stop(path=trace_path)

        # Handle video files with retries
        for page in context.pages:
            if page.video:
                video_path = Path(page.video.path())
                new_video_path = VIDEOS_DIR / f"{timestamp}_{test_name}.webm"

                def rename_op(_):
                    video_path.rename(new_video_path)

                safe_file_operation(video_path, rename_op)
    else:
        context.tracing.stop()
        # Delete videos for passed tests
        for page in context.pages:
            if page.video:
                video_path = Path(page.video.path())

                def delete_op(_):
                    video_path.unlink(missing_ok=True)

                safe_file_operation(video_path, delete_op)

    context.close()


@pytest.fixture
def page(context: BrowserContext, request) -> Page:
    global global_page
    if global_page is None:
        global_page = context.new_page()

    yield global_page

    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = SCREENSHOTS_DIR / f"{timestamp}_{test_name}.png"

        def screenshot_op(_):
            global_page.screenshot(path=screenshot_path, full_page=True)

        safe_file_operation(screenshot_path, screenshot_op)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# import pytest
# import os
# import shutil
# from datetime import datetime
# from playwright.sync_api import sync_playwright
# from typing import Generator
# import glob
#
# try:
#     from pytest_html import extras
# except ImportError:
#     extras = None
#
# # Constants
# ARTIFACT_ROOT = "artifacts"
# REPORT_DIR = "report"
# DEFAULT_TIMEOUT = 30000  # in ms
#
#
# class TestConfig:
#     PROJECT = os.getenv("PROJECT_NAME", "Playwright Automation")
#     TESTER = os.getenv("TESTER_NAME", "Mahbubur Rahman")
#     ENVIRONMENT = os.getenv("ENV", "Staging")
#     BROWSER = os.getenv("BROWSER", "Chromium")
#
#
# os.makedirs(REPORT_DIR, exist_ok=True)
# os.makedirs(ARTIFACT_ROOT, exist_ok=True)
#
#
# def pytest_sessionstart(session):
#     if os.path.exists(ARTIFACT_ROOT):
#         shutil.rmtree(ARTIFACT_ROOT)
#     os.makedirs(ARTIFACT_ROOT)
#     print(f"\n[🧹] Cleaned old artifacts in: {ARTIFACT_ROOT}")
#
#
# def pytest_configure(config):
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")
#     config.option.htmlpath = report_path
#
#     if not hasattr(config.option, "html_metadata"):
#         config.option.html_metadata = {}
#
#     config.option.html_metadata.update({
#         "Project": TestConfig.PROJECT,
#         "Tester": TestConfig.TESTER,
#         "Environment": TestConfig.ENVIRONMENT,
#         "Browser": TestConfig.BROWSER,
#         "Execution Time": timestamp
#     })
#
#     print(f"\n[✅] HTML report will be generated at: {report_path}")
#
#
# def pytest_html_report_title(report):
#     report.title = "🧪 Playwright Test Report"
#
#
# def pytest_html_results_table_header(cells):
#     cells.insert(1, '<th class="status">Status</th>')
#
#
# def pytest_html_results_table_row(report, cells):
#     status_icons = {
#         "passed": '<span style="color: green;">✔ PASSED</span>',
#         "failed": '<span style="color: red;">✖ FAILED</span>',
#         "skipped": '<span style="color: orange;">⚠ SKIPPED</span>'
#     }
#     if report.outcome in status_icons:
#         cells.insert(1, f'<td>{status_icons[report.outcome]}</td>')
#
#
# test_artifacts = {}
#
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     setattr(item, f"rep_{report.when}", report)
#
#     if report.when == "call":
#         test_id = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
#         trace_file = test_artifacts.get(test_id, {}).get("trace")
#         video_file = test_artifacts.get(test_id, {}).get("video")
#
#         if extras:
#             extras_list = getattr(report, "extras", [])
#             if video_file and os.path.exists(video_file):
#                 extras_list.append(extras.html(f'<a href="{video_file}">🎥 Video</a>'))
#             if trace_file and os.path.exists(trace_file):
#                 extras_list.append(extras.html(f'<a href="{trace_file}">📝 Trace</a>'))
#             report.extras = extras_list
#
#
# # ─────────────────────────────────────────────────────────────
# # Shared browser instance
# # ─────────────────────────────────────────────────────────────
# @pytest.fixture(scope="session")
# def browser():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         yield browser
#         browser.close()
#
#
# # ─────────────────────────────────────────────────────────────
# # Per-test context and page with tracing and video
# # ─────────────────────────────────────────────────────────────
# @pytest.fixture
# def context(browser, request):
#     test_id = request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     artifact_dir = os.path.join(ARTIFACT_ROOT, f"{test_id}_{timestamp}")
#     os.makedirs(artifact_dir, exist_ok=True)
#
#     context = browser.new_context(
#         no_viewport=True,
#         record_video_dir=artifact_dir,
#         ignore_https_errors=True,
#     )
#     context.tracing.start(screenshots=True, snapshots=True, sources=True)
#
#     yield context
#
#     # Save trace for all tests, not just failed ones
#     trace_path = os.path.join(artifact_dir, "trace.zip")
#     context.tracing.stop(path=trace_path)
#
#     test_artifacts[test_id] = {
#         "trace": trace_path,
#         "video": None  # Will be updated by page fixture
#     }
#
#
# @pytest.fixture
# def page(context, request):
#     page = context.new_page()
#     page.set_default_timeout(DEFAULT_TIMEOUT)
#     page.set_default_navigation_timeout(DEFAULT_TIMEOUT)
#
#     if hasattr(request, "cls"):
#         request.cls.page = page
#
#     yield page
#
#     # Handle video capture
#     test_id = request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
#     video_path = os.path.join(ARTIFACT_ROOT, f"{test_id}_*", "video.webm")
#
#     try:
#         if page.video:
#             video_files = glob.glob(video_path)
#             if video_files:
#                 test_artifacts[test_id]["video"] = video_files[0]
#     except Exception as e:
#         print(f"[⚠️] Video handling error: {e}")
#
#     page.close()
#
#
#
# # import pytest
# # import os
# # import shutil
# # from datetime import datetime
# # from playwright.sync_api import sync_playwright, Page
# # from typing import Generator
# #
# # try:
# #     from pytest_html import extras
# # except ImportError:
# #     extras = None
# #
# # # Constants
# # ARTIFACT_ROOT = "artifacts"
# # REPORT_DIR = "report"
# # DEFAULT_TIMEOUT = 30000  # ms
# #
# # class TestConfig:
# #     PROJECT = os.getenv("PROJECT_NAME", "Playwright Automation")
# #     TESTER = os.getenv("TESTER_NAME", "Mahbubur Rahman")
# #     ENVIRONMENT = os.getenv("ENV", "Staging")
# #     BROWSER = os.getenv("BROWSER", "Chromium")
# #
# # os.makedirs(REPORT_DIR, exist_ok=True)
# # os.makedirs(ARTIFACT_ROOT, exist_ok=True)
# #
# # # ─────────────────────────────────────────────────────────────
# # # CLEANUP OLD ARTIFACTS
# # # ─────────────────────────────────────────────────────────────
# # def pytest_sessionstart(session):
# #     if os.path.exists(ARTIFACT_ROOT):
# #         shutil.rmtree(ARTIFACT_ROOT)
# #     os.makedirs(ARTIFACT_ROOT)
# #     print(f"\n[🧹] Cleaned old artifacts in: {ARTIFACT_ROOT}")
# #
# # # ─────────────────────────────────────────────────────────────
# # # HTML REPORT CONFIGURATION
# # # ─────────────────────────────────────────────────────────────
# # def pytest_configure(config):
# #     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #     report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")
# #     config.option.htmlpath = report_path
# #
# #     if not hasattr(config.option, "html_metadata"):
# #         config.option.html_metadata = {}
# #
# #     config.option.html_metadata.update({
# #         "Project": TestConfig.PROJECT,
# #         "Tester": TestConfig.TESTER,
# #         "Environment": TestConfig.ENVIRONMENT,
# #         "Browser": TestConfig.BROWSER,
# #         "Execution Time": timestamp
# #     })
# #
# #     print(f"\n[✅] HTML report will be generated at: {report_path}")
# #
# # def pytest_html_report_title(report):
# #     report.title = "🧪 Playwright Test Report"
# #
# # def pytest_html_results_table_header(cells):
# #     cells.insert(1, '<th class="status">Status</th>')
# #
# # def pytest_html_results_table_row(report, cells):
# #     status_icons = {
# #         "passed": '<span style="color: green;">✔ PASSED</span>',
# #         "failed": '<span style="color: red;">✖ FAILED</span>',
# #         "skipped": '<span style="color: orange;">⚠ SKIPPED</span>'
# #     }
# #     if report.outcome in status_icons:
# #         cells.insert(1, f'<td>{status_icons[report.outcome]}</td>')
# #
# # # ─────────────────────────────────────────────────────────────
# # # CAPTURE TEST RESULTS
# # # ─────────────────────────────────────────────────────────────
# # test_artifact_info = {}  # Global dict to track per-test trace/video
# #
# # @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# # def pytest_runtest_makereport(item, call):
# #     outcome = yield
# #     report = outcome.get_result()
# #     setattr(item, f"rep_{report.when}", report)
# #
# #     if report.when == "call":
# #         test_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
# #         status = report.outcome
# #         test_artifact_info[test_name]["status"] = status
# #
# #         if extras:
# #             trace = test_artifact_info[test_name]["trace"]
# #             video = test_artifact_info[test_name]["video"]
# #             report_extras = getattr(report, "extras", [])
# #
# #             if os.path.exists(trace):
# #                 report_extras.append(extras.html(f'<a href="{trace}">📝 Trace</a>'))
# #             if os.path.exists(video):
# #                 report_extras.append(extras.html(f'<a href="{video}">🎥 Video</a>'))
# #
# #             report.extras = report_extras
# #
# # # ─────────────────────────────────────────────────────────────
# # # SHARED SESSION FIXTURE — One browser/page for all tests
# # # ─────────────────────────────────────────────────────────────
# # @pytest.fixture(scope="session")
# # def resource(request) -> Generator[Page, None, None]:
# #     with sync_playwright() as playwright:
# #         browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
# #         context = browser.new_context(
# #             no_viewport=True,
# #             record_video_dir=ARTIFACT_ROOT,
# #             ignore_https_errors=True
# #         )
# #
# #         context.tracing.start(screenshots=True, snapshots=True, sources=True)
# #
# #         page = context.new_page()
# #         page.set_default_timeout(DEFAULT_TIMEOUT)
# #         page.set_default_navigation_timeout(DEFAULT_TIMEOUT)
# #
# #         yield page
# #
# #         # Save traces only if any test failed
# #         for test_name, info in test_artifact_info.items():
# #             trace_path = info["trace"]
# #             context.tracing.stop(path=trace_path)
# #             print(f"\n[📦] Trace saved: {trace_path}")
# #             break  # Stop after first one — Playwright only allows 1 stop()
# #
# #         try:
# #             if page.video:
# #                 raw_video = page.video.path()
# #                 shutil.move(raw_video, info["video"])
# #                 print(f"[🎥] Video saved: {info['video']}")
# #         except Exception as e:
# #             print(f"[⚠️] Video error: {str(e)}")
# #
# #         page.close()
# #         context.close()
# #         browser.close()
# #
# # # ─────────────────────────────────────────────────────────────
# # # AUTOSETUP PER-TEST ARTIFACT PATHS
# # # ─────────────────────────────────────────────────────────────
# # @pytest.fixture(autouse=True)
# # def test_setup(request):
# #     test_name = request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
# #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# #     artifact_path = os.path.join(ARTIFACT_ROOT, f"{test_name}_{timestamp}")
# #     os.makedirs(artifact_path, exist_ok=True)
# #
# #     trace_path = os.path.join(artifact_path, "trace.zip")
# #     video_path = os.path.join(artifact_path, "video.webm")
# #
# #     test_artifact_info[test_name] = {
# #         "trace": trace_path,
# #         "video": video_path,
# #         "status": None
# #     }
# #
# #
# # # import pytest
# # # import os
# # # import shutil
# # # from datetime import datetime
# # # from playwright.sync_api import sync_playwright
# # # from typing import Generator
# # #
# # # # Optional HTML report extras
# # # try:
# # #     from pytest_html import extras
# # # except ImportError:
# # #     extras = None
# # #
# # # # Constants
# # # ARTIFACT_ROOT = "artifacts"
# # # REPORT_DIR = "report"
# # # DEFAULT_TIMEOUT = 30000  # ms
# # #
# # # # Test Metadata Configuration
# # # class TestConfig:
# # #     PROJECT = os.getenv("PROJECT_NAME", "Playwright Automation")
# # #     TESTER = os.getenv("TESTER_NAME", "Mahbubur Rahman")
# # #     ENVIRONMENT = os.getenv("ENV", "Staging")
# # #     BROWSER = os.getenv("BROWSER", "Chromium")
# # #
# # # # Ensure necessary folders exist
# # # os.makedirs(REPORT_DIR, exist_ok=True)
# # # os.makedirs(ARTIFACT_ROOT, exist_ok=True)
# # #
# # # # ─────────────────────────────────────────────────────────────
# # # # CLEANUP OLD ARTIFACTS
# # # # ─────────────────────────────────────────────────────────────
# # # def pytest_sessionstart(session):
# # #     if os.path.exists(ARTIFACT_ROOT):
# # #         shutil.rmtree(ARTIFACT_ROOT)
# # #     os.makedirs(ARTIFACT_ROOT)
# # #     print(f"\n[🧹] Cleaned old artifacts in: {ARTIFACT_ROOT}")
# # #
# # # # ─────────────────────────────────────────────────────────────
# # # # HTML REPORT CONFIGURATION
# # # # ─────────────────────────────────────────────────────────────
# # # def pytest_configure(config):
# # #     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# # #     report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")
# # #     config.option.htmlpath = report_path
# # #
# # #     if not hasattr(config.option, "html_metadata"):
# # #         config.option.html_metadata = {}
# # #
# # #     config.option.html_metadata.update({
# # #         "Project": TestConfig.PROJECT,
# # #         "Tester": TestConfig.TESTER,
# # #         "Environment": TestConfig.ENVIRONMENT,
# # #         "Browser": TestConfig.BROWSER,
# # #         "Execution Time": timestamp
# # #     })
# # #
# # #     print(f"\n[✅] HTML report will be generated at: {report_path}")
# # #
# # # def pytest_html_report_title(report):
# # #     report.title = "🧪 Playwright Test Report"
# # #
# # # def pytest_html_results_table_header(cells):
# # #     cells.insert(1, '<th class="status">Status</th>')
# # #
# # # def pytest_html_results_table_row(report, cells):
# # #     status_icons = {
# # #         "passed": '<span style="color: green;">✔ PASSED</span>',
# # #         "failed": '<span style="color: red;">✖ FAILED</span>',
# # #         "skipped": '<span style="color: orange;">⚠ SKIPPED</span>'
# # #     }
# # #     if report.outcome in status_icons:
# # #         cells.insert(1, f'<td>{status_icons[report.outcome]}</td>')
# # #
# # # # ─────────────────────────────────────────────────────────────
# # # # CAPTURE TEST RESULTS
# # # # ─────────────────────────────────────────────────────────────
# # # @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# # # def pytest_runtest_makereport(item, call):
# # #     outcome = yield
# # #     report = outcome.get_result()
# # #     setattr(item, f"rep_{report.when}", report)
# # #
# # #     if report.when == "call" and extras:
# # #         test_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
# # #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# # #         artifact_path = os.path.join(ARTIFACT_ROOT, f"{test_name}_{timestamp}")
# # #
# # #         trace_file = os.path.join(artifact_path, "trace.zip")
# # #         video_file = os.path.join(artifact_path, "video.webm")
# # #
# # #         report_extras = getattr(report, "extras", [])
# # #
# # #         if os.path.exists(video_file):
# # #             report_extras.append(
# # #                 extras.html(f'<a href="{video_file}">🎥 Video</a>')
# # #             )
# # #         if os.path.exists(trace_file):
# # #             report_extras.append(
# # #                 extras.html(f'<a href="{trace_file}">📝 Trace</a>')
# # #             )
# # #
# # #         report.extras = report_extras
# # #
# # # # ─────────────────────────────────────────────────────────────
# # # # MAIN FIXTURE — One page per test with video & trace
# # # # ─────────────────────────────────────────────────────────────
# # # @pytest.fixture(scope="function", autouse=True)
# # # def resource(request) -> Generator:
# # #     test_name = request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
# # #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# # #     artifact_path = os.path.join(ARTIFACT_ROOT, f"{test_name}_{timestamp}")
# # #     os.makedirs(artifact_path, exist_ok=True)
# # #
# # #     trace_file = os.path.join(artifact_path, "trace.zip")
# # #     video_final_path = os.path.join(artifact_path, "video.webm")
# # #
# # #     with sync_playwright() as playwright:
# # #         browser = playwright.chromium.launch(headless=True, args=["--start-maximized"])
# # #         context = browser.new_context(
# # #             no_viewport=True,
# # #             record_video_dir=artifact_path,
# # #             ignore_https_errors=True
# # #         )
# # #
# # #         context.tracing.start(screenshots=True, snapshots=True, sources=True)
# # #
# # #         page = context.new_page()
# # #         page.set_default_timeout(DEFAULT_TIMEOUT)
# # #         page.set_default_navigation_timeout(DEFAULT_TIMEOUT)
# # #
# # #         yield page  # HAND OVER TO TEST
# # #
# # #         # After test completes
# # #         context.tracing.stop(path=trace_file)
# # #         print(f"\n[📦] Trace saved: {trace_file}")
# # #
# # #         try:
# # #             if page.video:
# # #                 raw_video_path = page.video.path()
# # #                 shutil.move(raw_video_path, video_final_path)
# # #                 print(f"[🎥] Video saved: {video_final_path}")
# # #         except Exception as e:
# # #             print(f"[⚠️] Video error: {str(e)}")
# # #
# # #         page.close()
# # #         context.close()
# # #         browser.close()
# # #
# # #
# # # # import pytest
# # # # import os
# # # # import shutil
# # # # from datetime import datetime
# # # # from playwright.sync_api import sync_playwright
# # # # from typing import Generator
# # # #
# # # # # Optional HTML report extras
# # # # try:
# # # #     from pytest_html import extras
# # # # except ImportError:
# # # #     extras = None
# # # #
# # # # # Constants
# # # # VIDEO_DIR = "videos"
# # # # TRACE_DIR = "traces"
# # # # REPORT_DIR = "report"
# # # # DEFAULT_TIMEOUT = 30000  # in milliseconds
# # # #
# # # # class TestConfig:
# # # #     PROJECT = os.getenv("PROJECT_NAME", "Playwright Automation")
# # # #     TESTER = os.getenv("TESTER_NAME", "Mahbubur Rahman")
# # # #     ENVIRONMENT = os.getenv("ENV", "Staging")
# # # #     BROWSER = os.getenv("BROWSER", "Chromium")
# # # #
# # # # # Ensure required directories exist
# # # # for directory in [VIDEO_DIR, TRACE_DIR, REPORT_DIR]:
# # # #     os.makedirs(directory, exist_ok=True)
# # # #
# # # # # Optional: Clean old artifacts before new run
# # # # def pytest_sessionstart(session):
# # # #     """Clean up old traces and videos before test run."""
# # # #     for folder in [TRACE_DIR, VIDEO_DIR]:
# # # #         for file in os.listdir(folder):
# # # #             file_path = os.path.join(folder, file)
# # # #             if os.path.isfile(file_path):
# # # #                 os.remove(file_path)
# # # #     print("\n[🧹] Old traces and videos cleaned.")
# # # #
# # # # def pytest_configure(config):
# # # #     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# # # #     report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")
# # # #     config.option.htmlpath = report_path
# # # #
# # # #     if not hasattr(config.option, "html_metadata"):
# # # #         config.option.html_metadata = {}
# # # #
# # # #     config.option.html_metadata.update({
# # # #         "Project": TestConfig.PROJECT,
# # # #         "Tester": TestConfig.TESTER,
# # # #         "Environment": TestConfig.ENVIRONMENT,
# # # #         "Browser": TestConfig.BROWSER,
# # # #         "Execution Time": timestamp
# # # #     })
# # # #
# # # #     print(f"\n[✅] HTML report will be generated at: {report_path}")
# # # #
# # # # def pytest_html_report_title(report):
# # # #     report.title = "🧪 Test Report | Playwright"
# # # #
# # # # def pytest_html_results_table_header(cells):
# # # #     cells.insert(1, '<th class="status">Status</th>')
# # # #
# # # # def pytest_html_results_table_row(report, cells):
# # # #     status_icons = {
# # # #         "passed": '<span style="color: green;">✔ PASSED</span>',
# # # #         "failed": '<span style="color: red;">✖ FAILED</span>',
# # # #         "skipped": '<span style="color: orange;">⚠ SKIPPED</span>'
# # # #     }
# # # #     if report.outcome in status_icons:
# # # #         cells.insert(1, f'<td class="col-status">{status_icons[report.outcome]}</td>')
# # # #
# # # # @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# # # # def pytest_runtest_makereport(item, call):
# # # #     outcome = yield
# # # #     report = outcome.get_result()
# # # #     setattr(item, f"rep_{report.when}", report)
# # # #
# # # #     if report.when == "call" and report.failed and extras:
# # # #         test_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
# # # #         matching_trace = [f for f in os.listdir(TRACE_DIR) if f.startswith(test_name)]
# # # #         matching_video = [f for f in os.listdir(VIDEO_DIR) if f.startswith(test_name)]
# # # #         report_extras = getattr(report, "extras", [])
# # # #
# # # #         if matching_video:
# # # #             report_extras.append(extras.html(f'<a href="{os.path.join(VIDEO_DIR, matching_video[0])}">🎥 Video</a>'))
# # # #
# # # #         if matching_trace:
# # # #             report_extras.append(extras.html(f'<a href="{os.path.join(TRACE_DIR, matching_trace[0])}">📝 Trace</a>'))
# # # #
# # # #         report.extras = report_extras
# # # #
# # # # @pytest.fixture(scope="session", autouse=True, name="resource")
# # # # def resource(request) -> Generator:
# # # #     test_name = request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
# # # #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# # # #     trace_path = os.path.join(TRACE_DIR, f"{test_name}_{timestamp}.zip")
# # # #     video_file_name = f"{test_name}_{timestamp}.webm"
# # # #     video_path_final = os.path.join(VIDEO_DIR, video_file_name)
# # # #
# # # #     with sync_playwright() as playwright:
# # # #         browser = playwright.chromium.launch(
# # # #             headless=False,
# # # #             args=["--start-maximized"]
# # # #         )
# # # #
# # # #         context = browser.new_context(
# # # #             no_viewport=True,
# # # #             record_video_dir=VIDEO_DIR,
# # # #             ignore_https_errors=True
# # # #         )
# # # #
# # # #         context.tracing.start(
# # # #             screenshots=True,
# # # #             snapshots=True,
# # # #             sources=True
# # # #         )
# # # #
# # # #         page = context.new_page()
# # # #         page.set_default_timeout(DEFAULT_TIMEOUT)
# # # #         page.set_default_navigation_timeout(DEFAULT_TIMEOUT)
# # # #
# # # #         yield page
# # # #
# # # #         test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
# # # #
# # # #         if test_failed:
# # # #             context.tracing.stop(path=trace_path)
# # # #             print(f"\n[🔍] Trace saved (test failed): {trace_path}")
# # # #         else:
# # # #             context.tracing.stop()
# # # #             print(f"\n[ℹ️] Trace discarded (test passed): {test_name}")
# # # #
# # # #         try:
# # # #             if page.video:
# # # #                 raw_video_path = page.video.path()
# # # #                 shutil.move(raw_video_path, video_path_final)
# # # #                 print(f"\n[🎥] Video saved: {video_path_final}")
# # # #         except Exception as e:
# # # #             print(f"\n[⚠️] Video error: {str(e)}")
# # # #
# # # #         page.close()
# # # #         context.close()
# # # #         browser.close()
# # # #
# # # # # import pytest
# # # # # import os
# # # # # import shutil
# # # # # from datetime import datetime
# # # # # from playwright.sync_api import sync_playwright, Page
# # # # # from typing import Generator
# # # # #
# # # # # # Required for HTML reporting
# # # # # try:
# # # # #     from pytest_html import extras
# # # # # except ImportError:
# # # # #     extras = None
# # # # #
# # # # # # Constants
# # # # # VIDEO_DIR = "videos"
# # # # # TRACE_DIR = "traces"
# # # # # REPORT_DIR = "report"
# # # # # DEFAULT_TIMEOUT = 30000  # 30 seconds
# # # # #
# # # # #
# # # # # class TestConfig:
# # # # #     PROJECT = os.getenv("PROJECT_NAME", "Playwright Automation")
# # # # #     TESTER = os.getenv("TESTER_NAME", "Mahbubur Rahman")
# # # # #     ENVIRONMENT = os.getenv("ENV", "Staging")
# # # # #     BROWSER = os.getenv("BROWSER", "Chromium")
# # # # #     #HEADLESS = not bool(os.getenv("HEADFUL", False))
# # # # # #    HEADLESS = not bool(os.getenv("HEADFUL", True))
# # # # #
# # # # #
# # # # #
# # # # # # Ensure directories exist
# # # # # for directory in [VIDEO_DIR, TRACE_DIR, REPORT_DIR]:
# # # # #     os.makedirs(directory, exist_ok=True)
# # # # #
# # # # #
# # # # # def pytest_configure(config):
# # # # #     """Configure pytest and HTML reporting."""
# # # # #     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# # # # #     report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")
# # # # #     config.option.htmlpath = report_path
# # # # #
# # # # #     # Metadata configuration
# # # # #     if not hasattr(config.option, "html_metadata"):
# # # # #         config.option.html_metadata = {}
# # # # #
# # # # #     config.option.html_metadata.update({
# # # # #         "Project": TestConfig.PROJECT,
# # # # #         "Tester": TestConfig.TESTER,
# # # # #         "Environment": TestConfig.ENVIRONMENT,
# # # # #         "Browser": TestConfig.BROWSER,
# # # # #         "Execution Time": timestamp
# # # # #     })
# # # # #
# # # # #     print(f"\n[✅] HTML report will be generated at: {report_path}")
# # # # #
# # # # #
# # # # # def pytest_html_report_title(report):
# # # # #     report.title = "🧪 Test Report | Playwright"
# # # # #
# # # # #
# # # # # def pytest_html_results_table_header(cells):
# # # # #     cells.insert(1, '<th class="status">Status</th>')
# # # # #
# # # # #
# # # # # def pytest_html_results_table_row(report, cells):
# # # # #     """Customize test status in report."""
# # # # #     status_icons = {
# # # # #         "passed": '<span style="color: green;">✔ PASSED</span>',
# # # # #         "failed": '<span style="color: red;">✖ FAILED</span>',
# # # # #         "skipped": '<span style="color: orange;">⚠ SKIPPED</span>'
# # # # #     }
# # # # #     if report.outcome in status_icons:
# # # # #         cells.insert(1, f'<td class="col-status">{status_icons[report.outcome]}</td>')
# # # # #
# # # # #
# # # # # @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# # # # # def pytest_runtest_makereport(item, call):
# # # # #     """Collect artifacts for failed tests."""
# # # # #     outcome = yield
# # # # #     report = outcome.get_result()
# # # # #     setattr(item, f"rep_{report.when}", report)
# # # # #
# # # # #     if report.when == "call" and report.failed and extras:
# # # # #         test_name = item.name
# # # # #         report_extras = getattr(report, "extras", [])
# # # # #
# # # # #         # Add video link if exists
# # # # #         video_path = os.path.join(VIDEO_DIR, f"{test_name}.webm")
# # # # #         if os.path.exists(video_path):
# # # # #             report_extras.append(extras.html(f'<a href="{video_path}">🎥 Video</a>'))
# # # # #
# # # # #         # Add trace link if exists
# # # # #         trace_path = os.path.join(TRACE_DIR, f"{test_name}.zip")
# # # # #         if os.path.exists(trace_path):
# # # # #             report_extras.append(extras.html(f'<a href="{trace_path}">📝 Trace</a>'))
# # # # #
# # # # #         report.extras = report_extras
# # # # #
# # # # #
# # # # # @pytest.fixture(scope="session", autouse=True)
# # # # # def resource(request):
# # # # #     """Playwright page fixture with automatic tracing and video recording."""
# # # # #     test_name = request.node.name
# # # # #
# # # # #     with sync_playwright() as playwright:
# # # # #         browser = playwright.chromium.launch(
# # # # #             headless=False, #TestConfig.HEADLESS,
# # # # #             args=["--start-maximized"]
# # # # #         )
# # # # #
# # # # #         context = browser.new_context(
# # # # #             no_viewport=True,
# # # # #             #viewport=None, #{"width": 1920, "height": 1080},
# # # # #             record_video_dir=VIDEO_DIR,
# # # # #             ignore_https_errors=True
# # # # #         )
# # # # #
# # # # #         context.tracing.start(
# # # # #             screenshots=True,
# # # # #             snapshots=True,
# # # # #             sources=True
# # # # #         )
# # # # #
# # # # #         page = context.new_page()
# # # # #         page.set_default_timeout(DEFAULT_TIMEOUT)
# # # # #         page.set_default_navigation_timeout(DEFAULT_TIMEOUT)
# # # # #
# # # # #         yield page
# # # # #
# # # # #         test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
# # # # #
# # # # #         trace_path = os.path.join(TRACE_DIR, f"{test_name}.zip")
# # # # #         context.tracing.stop(path=trace_path if test_failed else None)
# # # # #
# # # # #         if test_failed:
# # # # #             print(f"\n[🔍] Trace saved: {trace_path}")
# # # # #
# # # # #         try:
# # # # #             if page.video:
# # # # #                 video_path = page.video.path()
# # # # #                 new_video_path = os.path.join(VIDEO_DIR, f"{test_name}.webm")
# # # # #                 shutil.move(video_path, new_video_path)
# # # # #                 print(f"\n[🎥] Video saved: {new_video_path}")
# # # # #         except Exception as e:
# # # # #             print(f"\n[⚠️] Video error: {str(e)}")
# # # # #
# # # # #         page.close()
# # # # #         context.close()
# # # # #         browser.close()