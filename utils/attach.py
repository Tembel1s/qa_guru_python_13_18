import allure
from allure_commons.types import AttachmentType
from requests import Response
import json


def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')


def response_attach(response: Response):
    allure.attach(body=str(response.status_code), name="Status Code", attachment_type=AttachmentType.TEXT)
    allure.attach(body=json.dumps(dict(response.cookies), indent=4), name="Cookies",
                  attachment_type=AttachmentType.JSON)
