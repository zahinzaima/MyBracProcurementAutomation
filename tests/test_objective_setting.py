# tests/test_objective_setting.py

import pytest
from playwright.sync_api import sync_playwright
from rich.traceback import install

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.objective_setting_page import ObjectiveSettingPage
from resources.resource_file import TestResources

install()

@pytest.fixture(scope='session', autouse=True)
def resource():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()

def test_objective_setting_entry(resource):
    print("🔐 Logging in...")
    login = LoginPage(resource)
    login.navigate_to_url(TestResources.test_url)
    login.perform_login(TestResources.test_user_name, TestResources.test_user_pass)

    print("🧼 Closing popup and navigating to ePMS...")
    dashboard = DashboardPage(resource)
    dashboard.closing_add()
    dashboard.goto_ePMS()

    print("📝 Opening Objective Setting and submitting form...")
    obj_page = ObjectiveSettingPage(resource)
    obj_page.go_to_self_opening_year()
    obj_page.fill_objective_form()

    print("✅ Objective successfully submitted!")
