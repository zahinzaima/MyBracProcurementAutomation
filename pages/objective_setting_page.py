# pages/objective_setting_page.py
class ObjectiveSettingPage:
    def __init__(self, page):
        self.page = page

    def go_to_self_opening_year(self):
        self.page.click("text=Objective Setting")
        self.page.click("text=Self")
        self.page.click("text=Opening Year")
        self.page.wait_for_timeout(2000)

    def fill_objective_form(self):
        self.page.select_option("select[formcontrolname='objectiveType']", label="Operational")
        self.page.fill("textarea[formcontrolname='objective']", "Efficiency target")
        self.page.fill("input[formcontrolname='weightage']", "90")
        self.page.fill("input[placeholder='Start Date']", "12-02-2025")
        self.page.fill("input[placeholder='End Date']", "31-03-2025")
        self.page.fill("textarea[formcontrolname='measure']", "a")
        self.page.click("button:has-text('Save')")
        self.page.wait_for_timeout(2000)
