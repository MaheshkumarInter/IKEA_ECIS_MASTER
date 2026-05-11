# from playwright.sync_api import expect
#
#
# class IkeaLoginPage:
#     def __init__(self, page):
#         self.page = page
#         self.username_input = page.locator("#userNameInput")
#         self.password_input = page.locator("#passwordInput")
#         self.sign_in = page.locator("#submitButton")
#
#     def login(self, username: str, password: str):
#         expect(self.username_input).to_be_visible()
#         self.username_input.fill(username)
#         self.password_input.fill(password)
#         self.sign_in.click()


from playwright.sync_api import expect



class IkeaLoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#userNameInput")
        self.password_input = page.locator("#passwordInput")
        self.sign_in = page.locator("#submitButton")
        self.logout = page.locator("#btnLogout")

    def login(self, username: str, password: str):
        expect(self.username_input).to_be_visible()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.sign_in.click()

    def logout_ecis(self):
        self.logout.click()