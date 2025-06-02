# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify etc.
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class CreateRequisitionPage(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.proc_item_requisition_for_self = page.locator('input[type="radio"][id="self"]')
        self.proc_item_requisition_for_other = page.locator('input[type="radio"][id="other"]')
        self.proc_item_project = page.locator('css=#projectInfoDiv_input')
        # self.proc_item_project = page.locator('css=#projectInfoDiv_ctr')
        # projectInfoDiv_ctr
        self.proc_item_project_dropdown = page.locator('#projectInfoDiv_arrow')
        self.proc_item_source_of_fund = page.locator('css=#sourceOfFundDiv_arrow')
        self.proc_item_information = page.get_by_role("input", name='itemInfoName')
        self.proc_item_tor = page.get_by_role("textarea", name='itemSpecification')
        self.proc_item_quantity = page.get_by_role("input", name='quantity')
        self.proc_item_unit_price = page.get_by_role("input", name='unitPrice')
        self.requisition_for_single_project = page.locator('input[type="radio"][id="singleProjectRadio"]')
        self.requisition_for_multiple_project = page.locator('input[type="radio"][id="multiProjectRadio"]')
        self.requisition_cost_quantity = page.locator('input[type="radio"][id="itemCostQuantity"]')
        self.requisition_cost_amount = page.locator('input[type="radio"][id="itemCostAmount"]')
        self.requisition_item_gl_code = page.locator('css=#glInfo_0Div_arrow')
        self.requisition_item_qty_amount = page.get_by_role("textbox", name="amountQty_0")
        self.requisition_add_button = page.get_by_role("button", name='addToGrid')
        self.save_button = page.get_by_role("button", name='Save')
        self.submit_button = page.get_by_role("button", name='Submit')


    def select_requisition_for_self(self):
        self.proc_item_requisition_for_self.click()

    def select_requisition_for_other(self):
        self.proc_item_requisition_for_other.click()

    def input_project_name(self, project_name):
        self.select_from_dropdown(self.proc_item_project_dropdown, project_name)
        #self.proc_item_project.wait_for(state='visible')
        #self.select_from_list_by_text(self.proc_item_project, project_name)
        #self.press_button("Enter")
        # self.proc_item_project_dropdown.click()
        # self.page.get_by_text(project_name).click()
        # self.page.keyboard.press("Enter")
        # self.page.wait_for_timeout(5000)

    def input_source_of_fund(self, source_of_fund):
        self.select_from_dropdown(self.proc_item_source_of_fund, source_of_fund)

    def input_item_information(self, item_information):
        self.input_in_element(self.proc_item_information, item_information)
        self.press_button("Enter")
        expect(self.proc_item_tor).to_have_text('Glue (any type of glue)')

    def input_item_quantity(self, quantity):
        self.input_in_element(self.proc_item_quantity, quantity)
        if self.requisition_cost_quantity.is_checked():
            expect(self.requisition_item_qty_amount).to_have_text(quantity)

    def input_item_unit_price(self, unit_price):
        self.input_in_element(self.proc_item_unit_price, unit_price)
        if self.requisition_cost_amount.is_checked():
            qty = self.proc_item_quantity.get_attribute("value")
            expect(self.requisition_item_qty_amount).to_have_value(qty*unit_price)

    def add_item_to_grid(self):
        self.click_on_btn(self.requisition_add_button)

    def save_requisition(self):
        self.click_on_btn(self.save_button)

    def submit_requisition(self):
        self.click_on_btn(self.submit_button)