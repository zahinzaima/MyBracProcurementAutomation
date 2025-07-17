# pages/dashboard_page.py
class DashboardPage:
    def __init__(self, page):
        self.page = page

    def closing_add(self):
        try:
            self.page.click("button[aria-label='Close']")  # Update this selector if needed
            self.page.wait_for_timeout(1000)
        except:
            print("No popup found or already closed.")

    def goto_ePMS(self):
        self.page.click("text=PMS")
        self.page.wait_for_timeout(2000)
