import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class RequisitionAcceptList(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # self.assigned_to = page.get_by_label("Assigned To")
        self.req_no = page.get_by_role("textbox", name="Requisition No.")
        self.find = page.get_by_role("button", name="Find")
        self.select_all = page.get_by_role("link", name="Select All", exact=True)
        self.approve = page.get_by_role("button", name=re.compile("Approve", re.IGNORECASE))
        self.confirmation_message_approve = page.get_by_role("button", name=re.compile("Approve", re.IGNORECASE))
        

    def search_requisition(self, requisition_number):
        self.input_in_element(self.req_no, requisition_number + " ") # adding a trailing space to ensure the input is recognized
        self.page.wait_for_timeout(1000)
        self.req_no.click()  # focus the input field
        self.page.keyboard.press("End")  # move cursor to the end
        self.page.keyboard.press("Backspace")  # delete trailing space
        
        self.page.wait_for_timeout(2000)
        # self.find.click()
        self.page.wait_for_timeout(4000)
        #self.page.wait_for_timeout(2000)
        # self.select_all.click()
        # self.approve.click()
        # self.confirmation_message_approve.click()
        #self.page.wait_for_timeout(5000)
        
