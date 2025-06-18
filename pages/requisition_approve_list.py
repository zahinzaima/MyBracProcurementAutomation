# this is an object of samplePage to automate, which contains all elementsAdd commentMore actions
# and actions could be performed, like input, verify etc.
import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class RequisitionApproveList(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.search_box = page.get_by_placeholder("Search Requisition No")
        self.checkbox=page.locator("//*[@class='requisition_proposal_list']")
        self.approve= page.get_by_role("button", name=re.compile("Approve", re.IGNORECASE))
        self.requisition_number="REQ20250004394"

    def search_requisition(self, requisition_number):
        self.input_in_element(self.search_box, requisition_number)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(2000)

    def select_requisition(self):
        # Select the checkbox for the requisition
        self.checkbox.click()
        self.page.wait_for_timeout(1000)

    def approve_requisition(self):
        # Click the approve button
        self.approve.click()
        self.page.wait_for_timeout(1000)
        # Verify the requisition number is displayed in the message
        #expect(self.page.locator('//div[@class="message"]')).to_contain_text(self.requisition_number)
        #self.page.wait_for_timeout(2000)