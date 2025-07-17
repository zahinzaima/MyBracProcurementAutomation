# pages/login_page.py

from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page

    def navigate_to_url(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000)  # Wait for scripts

    def perform_login(self, username, password):
        try:
            # Wait for input field
            self.page.wait_for_selector("input", timeout=5000)

            # Try using label text if available
            if self.page.locator("input[name='userName']").count():
                self.page.fill("input[name='userName']", username)
            else:
                self.page.get_by_placeholder("Username").fill(username)

            if self.page.locator("input[name='password']").count():
                self.page.fill("input[name='password']", password)
            else:
                self.page.get_by_placeholder("Password").fill(password)

            # Try clicking using visible text
            if self.page.locator("button:has-text('Login')").count():
                self.page.click("button:has-text('Login')")
            else:
                self.page.get_by_role("button").nth(0).click()

            self.page.wait_for_timeout(3000)

        except Exception as e:
            self.page.screenshot(path="login_error.png")
            print("❌ Login failed. Screenshot saved.")
            raise e


