class OrderPage :

    def __init__(self, page):
        self.page = page

    def click_first_order(self):
        self.page.get_by_role("button", name="View").first.click()