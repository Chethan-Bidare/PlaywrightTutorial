import json

from playwright.sync_api import Playwright

with open("data/credentials.json") as file_data:
    test_data = json.load(file_data)

class ApiUtils:


    def auth_token(self, playwright : Playwright) -> str:
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com/")
        response = api_request_context.post(url="/api/ecom/auth/login",
                                 data={"userEmail":"chethan.bidare12@gmail.com","userPassword":"Bidare@123"})
        response_result = response.json()
        return response_result["token"]

    def get_all_products(self, playwright: Playwright) :
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com/")
        response = api_request_context.post(url="/api/ecom/product/get-all-products",
                                headers={"Authorization": self.auth_token(playwright),
                                         "Content-Type": "application/json"},
                                            data={"productName":"","minPrice":"null","maxPrice":"null","productCategory":[],"productSubCategory":[],"productFor":[]})
        print("Product Response Status:", response.status)
        print("Product Response Text:", response.text())
        json_data = response.json()
        product_names = [product ["productName"] for product in json_data["data"] ]
        print(product_names)
        return product_names


    def create_order_api(self, playwright : Playwright):
        token = self.auth_token(playwright)
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com/")
        response = api_request_context.post(url="/api/ecom/order/create-order",
                                 data={"orders":[{"country":"India","productOrderedId":"67a8dde5c0d3e6622a297cc8"}]},
                                 headers={"Authorization": token,
                                          "Content-Type": "application/json"})
        return response.json()

def test_check_api(playwright: Playwright):
    #result = ApiUtils().create_order_api(playwright)
    #order_id = result["orders"]
    #print(result)
    #print(order_id)
    api_utils = ApiUtils()
    result1 = api_utils.get_all_products(playwright)
    print(result1)