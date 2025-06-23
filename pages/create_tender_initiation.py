import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class CreateTenderInitiation(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        self.search_box_for_list = page.get_by_placeholder("Please enter item name or REQ. No. to filter")
        self.select_all_checkbox = page.get_by_role("link", name="Select All", exact=True)
        self.unselect_all_checkbox = page.get_by_role("link", name="Unselect All", exact=True)
        # self.select_item=
        self.select_method_dropdown = page.locator("#purchaseMethodIdDiv_input")
        self.select_method_dropdown_options_dpm = page.get_by_text("Direct Purchase-(DPM)")
        self.remarks= page.get_by_placeholder("Max size of remarks 250 characters")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.save_button = page.get_by_role("button", name="Save")
    

    def search_requisition(self, requisition_number: str) -> None:
        self.search_box_for_list.fill(requisition_number)
        self.wait_for_timeout(1000)  # Wait for the search results to load
        # self.search_box_for_list.press("Enter")
        self.get_full_page_screenshot(f"search_requisition_{requisition_number}")
        # expect(self.search_box_for_list).to_have_value(requisition_number)
      
def select_all_items(self) -> None:
        self.select_all_checkbox.click()
        self.get_full_page_screenshot("select_all_items")
        self.wait_for_timeout(1000)  # Wait for the selection to be processed

def unselect_all_items(self) -> None:
        self.unselect_all_checkbox.click()
        self.get_full_page_screenshot("unselect_all_items")
        self.wait_for_timeout(1000)  # Wait for the unselection to be processed

def select_purchase_method(self, method: str) -> None:
        self.select_method_dropdown.fill(method)
        self.get_full_page_screenshot("select_purchase_method_dropdown")
        if method == "DPM":
            self.select_method_dropdown_options_dpm.click()
        else:
            raise ValueError(f"Unsupported purchase method: {method}")
        self.get_full_page_screenshot(f"select_purchase_method_{method}")
        expect(self.select_method_dropdown).to_have_text(re.compile(method))
