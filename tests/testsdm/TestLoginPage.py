# this page contains all the test cases for the samplePage
import pytest

from rich.traceback import install

from pages.create_requisition_page import CreateRequisitionPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.procurement_home_page import ProcurementHomePage
from resources.DMResourceFile import TestResourcesDM
from resources.resource_file import TestResources
from pages.requisition_approve_list import RequisitionApproveList
from pages.assign_requisition import AssignRequisition
from pages.requisition_accept_list import RequisitionAcceptList
from pages.main_navigation_bar import MainNavigationBar
from utils.basic_actions import BasicActions
from playwright.sync_api import sync_playwright
from pages.procurement_page_navigation_bar import ProcurementPageNavigationBar
from pages.create_tender_initiation import CreateTenderInitiation
from pages.create_direct_purchase import CreateDirectPurchase
from pages.direct_purchase_list import DirectPurchaseList

# Variables used to run this test
# purchase_order_number = ''

install()

@pytest.fixture(scope='session', autouse=True)
def resource():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--start-maximized"], headless=False)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()


def test_one(resource):
    print("Test One")
    s_page  = LoginPage(resource)
    s_page.navigate_to_url(TestResourcesDM.test_url)
    # s_page.click_on_btn()

    # s_page.click_on_btn(TestResourcesDM.test_commonLogin)
    s_page.perform_login(
        user_name=TestResourcesDM.test_username,
        pass_word=TestResourcesDM.test_userpass
    )
    #s_page.get_screen_shot('modular_test_1')