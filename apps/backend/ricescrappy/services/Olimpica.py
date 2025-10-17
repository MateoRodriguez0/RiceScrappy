from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json

def get_product_info(driver_path: str = 'chromedriver.exe') -> dict:
    price_selector = "span.olimpica-dinamic-flags-0-x-currencyContainer"
    name_selector = "span.vtex-store-components-3-x-productBrand.vtex-store-components-3-x-productBrand--quickview"
    image_selector = "img.vtex-store-components-3-x-productImageTag--main"
    url = "https://www.olimpica.com/arroz-diana-500-gr-7702511000014-518231/p"

    service = Service(ChromeDriverManager().install())

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        sleep(2)

        wait = WebDriverWait(driver, 15)

        def all_ready(d):
            try:
                n = d.find_element(By.CSS_SELECTOR, name_selector)
                im = d.find_element(By.CSS_SELECTOR, image_selector)
                pr = d.find_element(By.CSS_SELECTOR, price_selector)
                return (n, pr, im) if n and im and pr else False
            except:
                return False

        name_el, price_el, image_el = wait.until(all_ready)

        name_text = name_el.text.strip()
        price_clean = price_el.text.strip().replace(".", "").replace(",", "")
        image_url = image_el.get_attribute("src")

        return {
            "name": name_text,
            "price": price_clean,
            "image": image_url,
            "store": "Olímpica",
            "url": url
        }

    finally:
        driver.quit()
