import json
import time

import pytest
from playwright.sync_api import Page, expect, Playwright

from conftest import user_credentials, browser_instance
from pageObjects.LoginPage import LoginPage

with open("data/credentials.json") as file_data:
    test_data = json.load(file_data)
    user_credentials_list = test_data['user_credentials']

def test_playwright_basics(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://flipkart.com")

def test_playwright_basics1(playwright:Playwright):
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://flipkart.com")

def test_playwright_direct(page : Page):
    page.goto("https://flipkart.com")

def test_locators(page : Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_label("Username").fill("rahulshettyacademy")
    page.get_by_label("Password").fill("learning")
    page.get_by_role("combobox").select_option("stud")
    page.locator("#terms").check() #locator can be used to pass css, xpath etc
    page.get_by_role("link", name="terms and conditions").click()
    page.get_by_role("button", name="Sign In").click()
    #expect(page.get_by_text("Incorrect Username/Password")).to_be_visible() # using expect asserts whether visible
    #Below code searches the blocks which has app-card tag and filters iphone 16 and returns matching block
    iphone_product = page.locator("app-card").filter(has_text="iphone X")
    iphone_product.get_by_role("button").click()
    samsung_product = page.locator("app-card").filter(has_text="Samsung Note 8")
    samsung_product.get_by_role("button").click()
    page.get_by_text("Checkout").click()
    print(page.locator(".media-body").count())
    #Aserts whether the cart page has 2 items
    result = expect(page.locator(".media-body")).to_have_count(2)

def test_child_window_handle(page:Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    with page.expect_popup() as new_window:
        page.locator(".blinkingText").click()
        child_window = new_window.value
        red_content = child_window.locator(".red").text_content()
        assert "mentor@rahulshettyacademy.com" in red_content


def test_ui_checks(page : Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice")
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible()
    page.get_by_role("button", name="Hide").click()
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden()

def test_handle_alerts(page: Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice")
    page.on("dialog", lambda dialog:dialog.accept())
    page.get_by_role("button", name="Confirm").click()
    time.sleep(5)

def test_frames(page: Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice")
    page_frame = page.frame_locator("#courses-iframe")
    page_frame.get_by_role("link", name="All Access Plan").click()
    actual_text = page_frame.locator("body").text_content()
    #using 2 ways
    assert "Happy Subscribers" in actual_text
    expect(page_frame.locator("body")).to_contain_text("Happy Subscribers")

def test_web_tables(page: Page):
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/offers")
    price_col_num = ''
    for index in range(page.locator("th").count()):
        if page.locator("th").nth(index).filter(has_text="Price").count()>0 :
            price_col_num = index
            break
    rice_row = page.locator("tr").filter(has_text="Rice")
    expect(rice_row.locator("td").nth(price_col_num)).to_have_text("37")
    #Mouse hover method
    #page.locator("#mousehover").hover()

@pytest.mark.parametrize("user_credentials", user_credentials_list)
def test_login_ecommerce_app(user_credentials, browser_instance):
    login_page = LoginPage(browser_instance)
    login_page.navigate_To()
    dashboard_page = login_page.login(user_credentials["userEmail"], user_credentials["password"])
    orders_page = dashboard_page.select_orders()
    orders_page.click_first_order()
    #order_text = page.locator(".blink_me").text_content()