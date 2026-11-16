from playwright.sync_api import Page

from config.config import BASE_URL
from utils.logger import logger


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.user_name_field = page.locator("#user-name")
        self.password_field = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.product_title = page.locator("span.title")
        self.error_message = page.locator('[data-test="error"]')

    def load(self):
        self.page.goto(BASE_URL)

    def login(self, username, password):
        self.user_name_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()

    def is_present(self):
        assert self.product_title.text_content() == "Products"
        logger.info("log in successfull!")
