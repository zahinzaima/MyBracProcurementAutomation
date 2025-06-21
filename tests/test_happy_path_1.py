# this page contains all the test cases for the samplePage
import pytest

from rich.traceback import install

from pages.create_requisition_page import CreateRequisitionPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.procurement_home_page import ProcurementHomePage
from resources.resource_file import TestResources
from pages.requisition_approve_list import RequisitionApproveList
from pages.assign_requisition import AssignRequisition
from pages.requisition_accept_list import RequisitionAcceptList
from utils.basic_actions import BasicActions       
from playwright.sync_api import sync_playwright


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
    s_page  = LoginPage(resource)
    s_page.navigate_to_url(TestResources.test_url)
    s_page.perform_login(
        user_name=TestResources.test_user_name,
        pass_word=TestResources.test_user_pass
    )
    #s_page.get_screen_shot('modular_test_1')

# def test_two(resource):
#     d_page = DashboardPage(resource)
#     d_page.goto_procurement()
#     #d_page.get_screen_shot('modular_test_2')

# def test_three(resource):
#     p_page = ProcurementHomePage(resource)
#     p_page.navigate_to_create_requisition()
#     #p_page.get_screen_shot('modular_test_3')

# def test_four(resource):
#     c_page = CreateRequisitionPage(resource)
#     try:
#         c_page.verify_by_title("Create Requisition")
#         #c_page.get_screen_shot('modular_test_4')
#         c_page.select_requisition_for_self()
#         c_page.input_project_name("[H04] - Procurement-BRAC")
#         c_page.input_source_of_fund("BRAC")
#         c_page.input_item_information("[19190]-Glue-(Supplies and Stationeries->Supplies and Stationeries->Stationery)", "BAG")
#         c_page.wait_for_timeout(10000)
#         c_page.input_item_quantity("10")
#         c_page.input_item_unit_price("100")
#         c_page.set_delivery_schedule()
#         c_page.set_requisition_details()        # Providing GL details also
#         c_page.wait_for_timeout(5000)
#         c_page.get_full_page_screenshot('modular_test_5')
#         c_page.add_item_to_grid()
#         c_page.get_full_page_screenshot('modular_test_6')
#         c_page.save_requisition()
#         #c_page.confirm_submit_requisition()
#         c_page.get_full_page_screenshot('modular_test_7')
#         c_page.wait_for_timeout(5000)
#         c_page.track_requisition_number()
#         c_page.get_full_page_screenshot('modular_test_8')
#     except Exception as e:
#         c_page.get_full_page_screenshot('test_four_error')
#         raise e
# def test_five(resource):
#     r_page = RequisitionApproveList(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/authorizationList")
#         r_page.search_requisition(r_page.requisition_number)
#         r_page.select_requisition()
#         r_page.approve_requisition()
#         r_page.confirmation_message_aprrove()
#         r_page.get_full_page_screenshot('modular_test_10')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_four_error')
#         raise e
# def test_six(resource):
#     r_page = RequisitionApproveList(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/authorizationList")
#         r_page.search_requisition(r_page.requisition_number)
#         r_page.navigate_to_requisition_detail_page()
#         r_page.approve_requisition_from_details_page()
#         r_page.get_full_page_screenshot('modular_test_11')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_four_error')
#         raise e
# def test_seven(resource):
#     r_page = AssignRequisition(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/assignRequisitions")
#         r_page.assigning_person(assigned_person=TestResources.test_requisition_assignee)
#         r_page.search_requisition_for_assigning(requisition_number=TestResources.test_requisition_number)
#         r_page.get_full_page_screenshot('modular_test_12')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_12_error')
#         raise e
    
def test_eight(resource):
    r_page = RequisitionAcceptList(resource)
    try:
        r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/dashboard#!/requisition/assignedRequisitionShowList")
        r_page.search_requisition(requisition_number=TestResources.test_requisition_number)
        r_page.get_full_page_screenshot('modular_test_12')
    except Exception as e:
        r_page.get_full_page_screenshot('test_12_error')
        raise e
        
