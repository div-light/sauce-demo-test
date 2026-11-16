import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from testdata.invalid_crendentials import INVALID_CREDENTIALS


@pytest.mark.parametrize("username, password, expected_message", INVALID_CREDENTIALS)
def test_invalid_login(page: Page, username, password, expected_message):
    lp = LoginPage(page)
    lp.load()
    lp.login(username, password)
    expect(lp.error_message).to_have_text(expected_message)
