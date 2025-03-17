from playwright.sync_api import Playwright, sync_playwright, expect

def test_run(pw: Playwright) -> None:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.flipkart.com/")
    page.get_by_label("Mobiles").click()
    expect(page.get_by_role("img", name="BSD Header").nth(1)).to_be_visible()
    page.get_by_role("link", name="a a").first.click()
    expect(page.get_by_text("Coming Soon")).to_be_visible()
    page.get_by_text("5% Unlimited Cashback on").click()
    page.locator("div").filter(has_text="Back to top").nth(3).click()
    page.locator(".XqNaEv").click()
    page.get_by_role("link", name="COMPARE 1").click()
    page.get_by_text("Choose Brand").first.click()
    page.get_by_text("Apple").first.click()
    page.get_by_text("RETRY").click()
    page.get_by_text("Apple").first.click()
    page.get_by_text("Apple").nth(1).click()
    page.get_by_text("Choose a Product").first.click()
    page.get_by_text("Choose Brand").first.click()
    page.get_by_text("Acer").nth(1).click()
    page.get_by_text("Choose a Product").first.click()
    page.get_by_text("Choose a Product").first.click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
