from playwright.sync_api import Page

from utils.logger import logger


class ProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.invetory_list = page.locator("div.inventory_item")
        self.cart_badge = page.locator("span.shopping_cart_badge")
        self.cart_link = page.locator("a.shopping_cart_link")

    def add_all_products_to_cart(self):
        self.inv_list = self.invetory_list.all()
        for inv in self.inv_list:
            self.name = inv.locator("div.inventory_item_name").text_content()
            inv.get_by_text("Add to cart", exact=True).click()
            logger.info(" %s is added to cart 🛒 ", self.name)

    def cart_badge_count(self):
        return self.cart_badge.text_content()

    def click_cart_link(self):
        self.cart_link.click()
