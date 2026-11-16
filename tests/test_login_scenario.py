from playwright.sync_api import Page

from config.config import PASSWORD, SAUCE_USERNAME
from pages.login_page import LoginPage


def test_login_scenario(page: Page):
    login_page = LoginPage(page)
    login_page.load()
    login_page.login(SAUCE_USERNAME, PASSWORD)
    login_page.is_present()
