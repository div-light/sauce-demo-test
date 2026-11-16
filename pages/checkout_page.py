from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.generate_pdf_button = page.locator("#generate-pdf-order")

    def checkout_with_details(self, firstname, lastname, zipcode):
        self.checkout_button.click()
        self.first_name.fill(firstname)
        self.last_name.fill(lastname)
        self.postal_code.fill(zipcode)
        self.continue_button.click()
        self.finish_button.click()

    def download_order_pdf(self, tmp_path):
        with self.page.expect_download() as download_info:
            self.generate_pdf_button.click()
        download = download_info.value
        saved_path = tmp_path / "order.pdf"
        download.save_as(saved_path)
        return download, saved_path
