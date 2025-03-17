from playwright.sync_api import Page, Playwright, expect

from api_practice import ApiUtils

mock_payload_response = {"data":[],"message":"No Orders"}
def intercept_response(route):
    route.fulfill(
        json=mock_payload_response
    )

def test_network_1(page: Page):
    page.goto("https://rahulshettyacademy.com/client")
    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*", intercept_response)
    page.get_by_placeholder("email@example.com").fill("chethan.bidare12@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Bidare@123")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="ORDERS").click()
    order_text = page.locator(".mt-4").text_content()
    print(order_text)


def intercept_request(route):
    route.continue_(url="https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=67d25324c019fb1ad62415c0")

def test_network_2(page : Page):
    page.goto("https://rahulshettyacademy.com/client")
    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*", intercept_request)
    page.get_by_placeholder("email@example.com").fill("chethan.bidare12@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Bidare@123")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="ORDERS").click()
    page.get_by_role("button", name="View").first.click()
    order_text = page.locator(".blink_me").text_content()
    print(order_text)

def test_session_storage(playwright : Playwright):
    api_utils = ApiUtils()
    token_value = api_utils.auth_token(playwright)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.add_init_script(f"""localStorage.setItem('token', '{token_value}')""")
    page.goto("https://rahulshettyacademy.com/client")
    page.get_by_role("button", name="ORDERS").click()
    expect(page.get_by_text("Your Orders")).to_be_visible()

