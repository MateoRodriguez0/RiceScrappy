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
    price_selector = ".vtex-product-price-1-x-currencyInteger.vtex-product-price-1-x-currencyInteger--summary"
    name_selector = ".vtex-store-components-3-x-productBrand.vtex-store-components-3-x-productBrand--quickview"
    image_selector = ".vtex-store-components-3-x-productImageTag"
    url = "https://www.megatiendas.co/arroz-diana-x-500-g-7702511000014/p"

    service = Service(ChromeDriverManager().install())

    options = Options()
    options.add_argument("--headless=new")
        
    driver = webdriver.Chrome(service=service, options=options)

    addressItemName = "selectedAddress"
    address = {
        "address": {
            "postalCode": "",
            "geoCoordinates": [-75.5187403961301, 10.4045894371466],
            "city": "Cartagena De Indias",
            "state": "Bolívar",
            "country": "COL",
            "addressType": "residential",
            "receiverName": "",
            "addressId": "onlyWhiteLabel",
            "complement": "",
            "neighborhood": "Bruselas",
            "street": "7726CF3JWH",
            "number": ""
        },
        "isNecessaryVerifyAtCheckout": "true"
    }

    try:
        driver.get(url)
        sleep(2)

        # Inject address and refresh
        driver.execute_script(
            "localStorage.setItem(arguments[0], arguments[1]);",
            addressItemName,
            json.dumps(address)
        )
        driver.refresh()

        wait = WebDriverWait(driver, 15)

        def all_ready(d):
            try:
                n = d.find_element(By.CSS_SELECTOR, name_selector)
                im = d.find_element(By.CSS_SELECTOR, image_selector)
                pr = d.find_elements(By.CSS_SELECTOR, price_selector)
                return (n, pr, im) if n and im and pr else False
            except:
                return False

        name_el, price_els, image_el = wait.until(all_ready)

        # Build result
        name_text = name_el.text.strip()

        # Concatenate price parts without a dot and remove separators
        parts = [p.text.strip() for p in price_els]
        price_concat =  "".join(parts).replace(".", "").replace(",", "") 

        image_url = image_el.get_attribute("src")

        return {
            "name": name_text,
            "price": price_concat,
            "image": image_url,
            "store": "Megatiendas",
            "url": url
        }
    finally:
        driver.quit()
