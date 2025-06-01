from utils.basic_actions import BasicActions


class DashboardPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # self.myDashboardItem_modal = page.locator('id=modal')
        self.myDashboardItem_procurement = page.locator('xpath=//*[contains(text(),"PROCUREMENT")]')

    def goto_procurement(self) -> None:
        self.page.keyboard.press('Enter')
        self.click_on_btn(self.myDashboardItem_procurement)
