import re
from resources.resource_file import TestResources
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class CreateVendorBillPayable(ProcurementHomePage, BasicActions):
    
    def __init__(self, page):
        super().__init__(page)
        self.purchase_order_type = page.locator("#dpmNo")
        self.vendor_info = page.get_by_role("textbox", name="Search by vendor name(Example")
        self.search_result = page.get_by_text(TestResources.test_vendor_name)
        self.order_no = page.locator("#woIdDiv_input")
        self.challan_no = page.locator("#challanIdDiv_input")
        self.bill_no = page.locator("#billNo")
        self.remarks = page.get_by_role("textbox", name="Max size of remarks 500")
        self.bill_date = page.locator("#billDate")
        self.bill_receive_date = page.locator("#billReceiveDate")
        self.select_all = page.get_by_role("link", name="Select All", exact=True)
        self.unselect_all = page.get_by_role("link", name="Unselect All")
        self.bill_recommender = page.locator("#poRecommenderIdDiv_input")
        self.bill_recommender_selection = page.get_by_text(TestResources.test_bill_recommender)
        self.submit = page.get_by_role("button", name="Submit")
        self.submit_confirmation = page.get_by_label("Submit Confirmation").get_by_role("button", name="Submit")
 

    def search_vendor(self, vendor_name: str):
        self.vendor_info.fill(vendor_name)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")
        self.page.keyboard.press("Backspace") 
        self.search_result.wait_for(state="visible", timeout=5000)
        self.search_result.hover()
        self.search_result.click()
    
    def bill_number(self, bill_no: str):
        self.bill_no.fill(bill_no)

    def bill_date_with_text(self, date: str):
        # Fill the estimated delivery date input field
        self.bill_date.scroll_into_view_if_needed()
        self.bill_date.fill(date)

    def bill_receive_date_with_text(self, date: str):
        # Fill the estimated delivery date input field
        self.bill_receive_date.scroll_into_view_if_needed()
        self.bill_receive_date.fill(date)

    def select_all_items(self):
        self.select_all.scroll_into_view_if_needed()
        self.select_all.click()
        self.wait_for_timeout(1000)

    def unselect_all_items(self): 
        self.unselect_all.click()
        self.wait_for_timeout(1000)

    def Bill_recommender_selecting(self, recommender: str):
        self.bill_recommender.scroll_into_view_if_needed()
        self.bill_recommender.fill(recommender)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")
        self.page.keyboard.press("Backspace")
        self.bill_recommender_selection.wait_for(state="visible", timeout=5000)
        self.bill_recommender_selection.hover()
        self.bill_recommender_selection.click()

    def submit_bill(self):
        self.submit.scroll_into_view_if_needed()
        self.submit.click()
        self.wait_for_timeout(2000)

    def confirm_submission(self):
        self.submit_confirmation.scroll_into_view_if_needed()
        self.submit_confirmation.click()
        self.wait_for_timeout(5000)