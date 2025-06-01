# this page contains all the common actions to be performed in this project
from playwright.sync_api import expect
import os


class BasicActions:
    def __init__(self, page):
        self.page = page

    def get_screen_shot(self, name):
        self.page.screenshot(path=os.getcwd() + "/screenshots/" + name + ".png")

    def navigate_to_url(self, given_url):
        self.page.goto(given_url)

    def verify_by_title(self, title):
        expect(self.page).to_have_title(title)

    @staticmethod
    def wait_to_load_element(elem):
        elem.wait_for(state='visible')
        print('waited for the elem')

    @staticmethod
    def click_on_btn(btn):
        btn.click()

    @staticmethod
    def input_in_element(elem, input_text):
        #elem.to_be_visible()
        elem.click()
        elem.fill(input_text)

    @staticmethod
    def select_from_list_by_value(elem, value):
        elem.click()
        elem.select_option(value)