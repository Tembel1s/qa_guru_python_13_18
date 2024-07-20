import pytest
from selene import browser
from selenium import webdriver
from utils import attach


@pytest.fixture(scope="function", autouse=True)
def browser_settings():
    browser.config.window_height = 1080
    browser.config.window_width = 1920
    browser.config.base_url = 'https://demowebshop.tricentis.com'

    options = webdriver.ChromeOptions()
    browser.config.driver_options = options

    yield

    attach.add_screenshot(browser)
    attach.add_html(browser)

    browser.quit()