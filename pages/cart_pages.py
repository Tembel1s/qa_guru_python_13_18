import allure
from selene import browser, have
import requests
from test_data.products import product_info
from allure_commons.types import AttachmentType
import json
from utils import attach

class Cart:
    def __init__(self):
        self.product_info = product_info
        self.cookies = {}

    @allure.step ('Получить cookie новой корзины')
    def get_cookies(self):
        CART_URL = 'https://demowebshop.tricentis.com/cart'
        response = requests.get(url=CART_URL)
        self.cookies['Nop.customer'] = response.cookies.get('Nop.customer')

        allure.attach(body=str(response.status_code), name="Status Code", attachment_type=AttachmentType.TEXT)
        allure.attach(body=json.dumps(dict(response.cookies), indent=4), name="Cookies",
                      attachment_type=AttachmentType.JSON)

        return self

    @allure.step ('Добавить товар в корзину через API')
    def add_product(self, quantity, product):
        product_data = self.product_info[product]
        API_URL = f'https://demowebshop.tricentis.com/addproducttocart/details/{product_data["id"]}/1'
        if 'attributes' in product_data:
            payload = product_data['attributes'].copy()
        else:
            payload = {}
        payload[f'addtocart_{product_data["id"]}.EnteredQuantity'] = quantity
        response = requests.post(url=API_URL, data=payload, cookies={'Nop.customer': self.cookies['Nop.customer']})
        self.cookies['Nop.customer'] = response.cookies.get('Nop.customer')

        allure.attach(body=str(response.status_code), name="Status Code", attachment_type=AttachmentType.TEXT)
        allure.attach(body=json.dumps(dict(response.cookies), indent=4), name="Cookies",
                      attachment_type=AttachmentType.JSON)

        assert response.status_code == 200

        return self

    @allure.step ('Проверить через UI наличие в корзине добавленного товара')
    def check_if_product_in_cart(self, product):
        product_name = self.product_info[product]
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.driver.add_cookie({'name': 'Nop.customer', 'value': self.cookies['Nop.customer']})
        browser.driver.refresh()
        browser.element('.order-summary-content').should(have.text(f'{product_name['name']}'))

        attach.add_screenshot(browser)
        attach.add_html(browser)

        return self

    @allure.step ('Проверить через UI корректное количество добавленного товара')
    def check_quantity(self, quantity):
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.driver.add_cookie({'name': 'Nop.customer', 'value': self.cookies['Nop.customer']})
        browser.driver.refresh()
        browser.element('.cart-qty').should(have.text(str(quantity)))

        attach.add_screenshot(browser)
        attach.add_html(browser)

        return self

    @allure.step('Удалить через UI товар из корзины')
    def remove_product (self):
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.driver.add_cookie({'name': 'Nop.customer', 'value': self.cookies['Nop.customer']})
        browser.driver.refresh()
        browser.element('.cart').element('[name=removefromcart]').click()
        browser.element('[name=updatecart]').click()
        browser.element('.order-summary-content').should(have.exact_text('Your Shopping Cart is empty!'))

        attach.add_screenshot(browser)
        attach.add_html(browser)

cart = Cart()
