# this page contains all the test cases for the samplePage
from resources.resource_file import TestResources
from pages.cr3_page import CreateReqPage
from pages.login_page import LoginPage

from rich.traceback import install
install()

tr = TestResources()

def test_one(page):
    s_page  = LoginPage(page)
    try:
        s_page.navigate_to_url(TestResources.test_url)
        s_page.perform_login(
            user_name=TestResources.test_user_name,
            pass_word=TestResources.test_user_pass
        )
    except Exception as e:
        #s_page.get_full_page_screenshot('test_one_error')
        raise e


def test_four(page):
    c_page = CreateReqPage(page)
    try:
        c_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/create")
        c_page.verify_by_title("Create Requisition")
        c_page.setting_requisition_for("[H04] - Procurement-BRAC")
        c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
        c_page.setting_requisition_details("glue","[19193]-Glue Stick (Fevi Stick)-(Supplies and Stationeries->Supplies and Stationeries->Stationery)","BAG", "Tor for Item","1000","25")
        c_page.setting_requisition_for_details("[5102010107-05] Remuneration","gl remarks","30-07-2025", "Head Office", "ABC Road")
        c_page.get_full_page_screenshot('full_page_screenshot_1')
        c_page.save_requisition()
        c_page.get_full_page_screenshot('full_page_screenshot_2')
    except Exception as e:
        c_page.get_full_page_screenshot('test_four_error')
        raise e