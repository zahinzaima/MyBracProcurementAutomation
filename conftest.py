import pytest
from rich.traceback import install
from playwright.sync_api import sync_playwright

install()
# Optional: Customize browser context args
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "ignore_https_errors": True,
        "record_video_dir": "videos/"
    }

@pytest.fixture(scope='session', autouse=True)
def resource():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--start-maximized"], headless=False)
        context = browser.new_context(viewport=None)
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()