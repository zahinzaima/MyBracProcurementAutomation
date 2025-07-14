from utils.basic_actionsdm import BasicActionsDM


class HomePage(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # self    = page
        # write down all the elements here with locator format
        # self.myDashboardItem_HRM = page.locator('xpath=//*[contains(text(),"HRM")]')
        self.userHomePageItem_ShowFrameworkAgreementList = page.locator(
            'xpath=//*[contains(text(),"All Framework Agreements")]')
        self.userHomePageItem_ShowAllVendors = page.locator('xpath=//*[contains(text(),"All Vendors ")]')
        self.userHomePageItem_showAllCategories = page.locator('xpath=//*[contains(text(),"All Categories")]')

        # Locator: find the span with class "cart-label" and text "Shopping cart"
        self.shopping_cart1 = page.locator('a:has-text("Shopping cart")')
        # self.shopping_cart = page.locator('span.cart-label', has_text='Shopping cart')
        # self.userHomePageItem_showShoppingCartList = page.locator('/html/body/div[6]/div[2]/div[1]/div[2]/div[1]/ul/a/span[1]')

    def click_shopping_cart(self):
        # self.shopping_cart1.click()
        self.click_on_btn(self.shopping_cart1)
        # def goto_shoppingcart(self):
        #     (self.click_on_btn(self.userHomePageItem_showShoppingCartList)
        # userHomePageItem_showShoppingCartList.click())
