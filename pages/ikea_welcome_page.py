from playwright.sync_api import expect


class IkeaWelcomePage:
    def __init__(self, page):
        self.page = page
        self.inter_button = page.get_by_role("button", name="Inter IKEA, Non Ingka")

    def click_inter_button(self):
        expect(self.inter_button).to_be_visible()
        self.inter_button.click()
