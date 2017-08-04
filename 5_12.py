# -*- coding: UTF-8 -*-
import os
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.get("http://localhost/litecart/admin")
    WebDriverWait(wd, 5).until(EC.title_is("Test Selenium Store"))
    wd.find_element_by_name("username").send_keys("admin")
    wd.find_element_by_name("password").send_keys("admin")
    wd.find_element_by_name("login").click()
    request.addfinalizer(wd.quit)
    return wd


def check_element(driver, *args):
    try:
        driver.find_element(*args)
        return True
    except NoSuchElementException:
        return False


def test_first(driver):
    image_path = str(os.path.abspath("sunglassed-rubber-duck.jpg"))
    product_category = "Rubber Ducks"
    product_name = "Swag duck"

    driver.find_element(By.PARTIAL_LINK_TEXT, "Catalog").click()
    driver.find_element(By.PARTIAL_LINK_TEXT, "Add New Product").click()
    WebDriverWait(driver, 5).until(EC.title_is("Add New Product | Test Selenium Store"))

    # adding of new product
    driver.find_element_by_css_selector("input[name='name[en]']").send_keys(product_name)
    driver.find_element_by_css_selector("input[name=code]").send_keys("123456")
    # changing of current category to desired one
    driver.find_element_by_css_selector("input[name='categories[]'][checked=checked]").click()
    category_selector = 'input[name="categories[]"][data-name="' + product_category + '"]'
    driver.find_element(By.CSS_SELECTOR, category_selector).click()
    driver.find_element(By.CSS_SELECTOR, "input[name='product_groups[]'][value='1-3']").click()
    driver.find_element_by_css_selector("input[name=quantity]").clear()
    driver.find_element_by_css_selector("input[name=quantity]").send_keys("100")
    driver.find_element_by_css_selector("input[name='new_images[]']").send_keys(image_path)
    driver.find_element_by_css_selector("input[name=date_valid_from]").send_keys(Keys.HOME + "08/01/2017")
    driver.find_element_by_css_selector("input[name=date_valid_to]").send_keys(Keys.HOME + "08/01/2020")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Information")))

    # information tab
    driver.find_element(By.LINK_TEXT, "Information").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "manufacturer_id")))
    driver.find_element_by_css_selector("select[name=manufacturer_id]").click()
    driver.find_element_by_css_selector("select[name=manufacturer_id] option:nth-child(2)").click()
    driver.find_element_by_css_selector("input[name=keywords]").send_keys("duck, rubber, swag, glasses")
    driver.find_element_by_css_selector("input[name='short_description[en]']").send_keys("cool duck with dark glasses")
    driver.find_element_by_css_selector(".trumbowyg-textarea").send_keys("Eco-friendly rubber duck with cool dark sunglasses")
    driver.find_element_by_css_selector("input[name='head_title[en]']").send_keys("cool duck")
    driver.find_element_by_css_selector("input[name='meta_description[en]']").send_keys("cool duck with dark glasses")

    # prices tab
    driver.find_element(By.LINK_TEXT, "Prices").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "purchase_price")))
    driver.find_element_by_css_selector("input[name=purchase_price]").clear()
    driver.find_element_by_css_selector("input[name=purchase_price]").send_keys("25")
    driver.find_element_by_css_selector("select[name=purchase_price_currency_code]").click()
    driver.find_element_by_css_selector("select[name=purchase_price_currency_code] option:nth-child(2)").click()

    driver.find_element_by_css_selector("input[name='prices[USD]']").send_keys("25")
    driver.find_element_by_css_selector("input[name='prices[EUR]']").send_keys("22")

    # submit
    driver.find_element_by_css_selector("button[name=save]").click()

    # check product in the catalog
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog")
    WebDriverWait(driver, 5).until(EC.title_is("Catalog | Test Selenium Store"))
    driver.find_element(By.LINK_TEXT, product_category).click()

    if check_element(driver, By.LINK_TEXT, product_name):
        print "Product added successfully"
    else:
        print "Something went wrong"









