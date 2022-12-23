import time
import random
import lib.headers
import lib.config
import asyncio
import selenium_async
import asyncselenium

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class SavePage:
    def __init__(self, url: str, page: str):
        self.url = url
        self.page = page

    def get_sourse_html(self):
        persona = self.get_headers_proxy()

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={persona['user-agent']}")
        options.add_argument("--disable=blink-features=AutomationControlled")
        options.add_argument("--headless")
        # set proxy
        proxy_options = {
            "proxy": {
                "https": persona["https"],
                "no-proxy": "localhost,127.0.0.1:8080"
            }
        }
        driver = webdriver.Chrome(
            options=options,
            executable_path=r"D:\pycharm_projects\scraping_wildberries\chromedriver\chromedriver.exe",
            seleniumwire_options=proxy_options
        )

        try:
            driver.request_interceptor = lib.headers.interceptor
            driver.get(self.url)
            time.sleep(random.randrange(2, 5))
            while True:
                find_review_block = driver.find_element(By.CLASS_NAME, "product-page__bottom")

                if driver.find_elements(By.XPATH, "//*[contains(text(), 'Смотреть все отзывы')]"):
                    html_product = driver.page_source
                    with open(f"data/products/{self.page}", "w", encoding="utf-8") as file:
                        file.write(html_product)
                    break
                else:
                    actions = ActionChains(driver)
                    actions.move_to_element(find_review_block).perform()
        except Exception as ex_:
            print(ex_)
        finally:
            driver.close()
            driver.quit()

    def get_headers_proxy(self):
        try:
            users = lib.config.USER_AGENTS_PROXY_LIST
            persona = random.choice(users)
        except ImportError:
            persona = None

        return persona