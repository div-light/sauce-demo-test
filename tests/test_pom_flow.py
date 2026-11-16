from pathlib import Path

from playwright.sync_api import Page

from config.config import PASSWORD, SAUCE_USERNAME
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductPage


def test_pom_flow(page: Page, tmp_path: Path):
    lp = LoginPage(page)
    lp.load()
    lp.login(SAUCE_USERNAME, PASSWORD)
    lp.is_present()

    pp = ProductPage(page)
    pp.add_all_products_to_cart()
    assert pp.cart_badge_count() == "6"
    pp.click_cart_link()

    cp = CheckoutPage(page)
    cp.checkout_with_details("Test", "User", "12345")
    download, saved_path = cp.download_order_pdf(tmp_path)
    assert download.suggested_filename.endswith(".pdf")
    assert saved_path.exists()
    assert saved_path.stat().st_size > 0
    assert download.failure() is None
