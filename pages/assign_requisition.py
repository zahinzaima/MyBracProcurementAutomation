# this is an object of samplePage to automate, which contains all elementsAdd commentMore actions
# and actions could be performed, like input, verify etc.
import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class AssignRequisition(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # self.assigned_to = page.get_by_label("Assigned To")
        self.assigned_to = page.locator("#employeeInfoDiv_input")


    def assigning_person(self, assigned_person):
        self.input_in_element(self.assigned_to, assigned_person)
        #self.page.wait_for_load_state("networkidle")
        #self.press_button("Enter")
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)
