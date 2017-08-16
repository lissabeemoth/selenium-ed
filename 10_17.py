# -*- coding: UTF-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_logger(driver):
    # admin login
    driver.get("http://localhost/litecart/admin/")
    WebDriverWait(driver, 5).until(EC.title_is("Test Selenium Store"))

    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    # open category page
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    WebDriverWait(driver, 5).until(EC.title_is("Catalog | Test Selenium Store"))

    # let's count products
    product_list_count = len(driver.find_elements(By.CSS_SELECTOR, ".dataTable tr.row a[href*='product_id']:first-child"))

    # main part of test
    i = 0
    while i != product_list_count:
        driver.find_elements(By.CSS_SELECTOR, ".dataTable tr.row a[href*='product_id']:first-child")[i].click()
        i += 1

        # print log if there is something or "ok" message instead
        if driver.get_log("browser"):
            for l in driver.get_log("browser"):
                print(l)
        else:
            print 'ok'

        # back to catalog
        driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
