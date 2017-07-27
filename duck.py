# -*- coding: UTF-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_check_ducks(driver):
    driver.get("http://localhost/litecart/")
    products = driver.find_elements(By.CSS_SELECTOR, ".products .product")
    if len(products) > 0:
        count = 0
        for product in products:
            if len(product.find_elements(By.CLASS_NAME, "sticker")) != 1:
                count += 1
        if count > 0:
            print count, " of ducks have none or more then one sticker"
        else:
            print "All of the ducks have only one sticker"
    else:
        print("Sorry. No ducks today.")