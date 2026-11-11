from pathlib import Path

from playwright.sync_api import Page, expect

from config.config import BASE_URL, PASSWORD, USERNAME


def test_e2e_flow(page: Page, tmp_path: Path):
    page.goto(BASE_URL)
    page.fill('input[data-test="username"]', USERNAME)
    page.fill('input[data-test="password"]', PASSWORD)
    page.click('input[data-test="login-button"]')
    page.wait_for_selector("div.inventory_item")
    invetory_list = page.locator("div.inventory_item").all()
    try:
        for item in invetory_list:
            name = item.locator("div.inventory_item_name").text_content()
            price = item.locator("div.inventory_item_price").text_content()
            item.get_by_text("Add to cart", exact=True).click()
    except Exception as e:
        print(f"An error occurred: {e}")

    expect(page.locator("span.shopping_cart_badge")).to_have_text("6")
    page.locator("a.shopping_cart_link").click()
    page.wait_for_timeout(7000)
    page.get_by_role("button", name="Checkout").click()
    page.locator("#first-name").fill("Test")
    page.locator("#last-name").fill("User")
    page.locator("#postal-code").fill("12345")
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Finish").click()
    with page.expect_download() as download_info:
        page.locator("#generate-pdf-order").click()
    download = download_info.value
    saved_path = tmp_path / "order.pdf"  # this is the key line that defines temp_path
    download.save_as(saved_path)

    assert download.suggested_filename.endswith(".pdf")
    assert saved_path.exists()
    assert saved_path.stat().st_size > 0
    assert download.failure() is None
