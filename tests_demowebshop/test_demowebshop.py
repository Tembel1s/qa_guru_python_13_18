from pages.cart_pages import cart
from test_data.products import expensive_computer, cheap_computer, smartphone
import allure

@allure.story('Проверка добавления товара в корзину')
def test_add_product_to_cart():
    cart.get_cookies()
    cart.add_product(product=expensive_computer, quantity=1)
    cart.check_if_product_in_cart(product=expensive_computer)
    cart.check_quantity(quantity=1)

@allure.story('Проверка добавления двух единиц одного товара в корзину')
def test_add_two_same_products_to_cart():
    cart.get_cookies()
    cart.add_product(product=cheap_computer, quantity=2)
    cart.check_if_product_in_cart(cheap_computer)
    cart.check_quantity(quantity=2)

@allure.story('Проверка добавления двух разных товаров в корзину')
def test_add_two_different_products_to_cart():
    cart.get_cookies()
    cart.add_product(product=cheap_computer, quantity=1)
    cart.add_product(product=expensive_computer, quantity=1)
    cart.check_if_product_in_cart(cheap_computer)
    cart.check_if_product_in_cart(expensive_computer)
    cart.check_quantity(quantity=2)

@allure.story('Проверка удаления товара из корзины')
def test_remove_product_from_cart():
    cart.get_cookies()
    cart.add_product(product=smartphone, quantity=1)
    cart.remove_product()







