# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify etc.
import re
from utils.basic_actionsdm import BasicActionsDM

class LoginPage(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # self.commonLogin = page.get_by_role('button')
        # self.openLoginFormBtn = page.get_by_role('button', name=re.compile("Common Login", re.IGNORECASE))
       # self.commonLogin = page.get_by_label('button', name=re.compile("Common Login", re.IGNORECASE))
        self.first_common_login_btn = page.locator("//div[@class='componentStyle']//following-sibling::button")
        self.userName = page.get_by_label('Username')
        self.passWord = page.get_by_placeholder('password')
        #self.commonLogin = page.get_by_role('button', name=re.compile("Common Login", re.IGNORECASE))
        self.second_common_login_btn = page.locator("//button[@type='submit']")


    # write down all the necessary actions performed in this page as def
    def perform_login(self, user_name, pass_word):
        # self.first_common_login_btn.click()
        # # self.userName.fill(user_name)
        # # self.passWord.fill(pass_word)
        # #self.second_common_login_btn.click()
        self.click_on_btn(self.first_common_login_btn)
        self.input_in_element(self.userName, user_name)
        self.input_in_element(self.passWord, pass_word)
        self.click_on_btn(self.second_common_login_btn)

