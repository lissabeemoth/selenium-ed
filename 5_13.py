# -*- coding: UTF-8 -*-
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def element_exists(driver, *args):
    try:
        driver.find_element(*args)
        return True
    except NoSuchElementException:
        return False


def add_item_to_cart(driver):
    # open first product from list
    driver.get("http://localhost/litecart/")
    WebDriverWait(driver, 5).until(EC.title_is("Online Store | Test Selenium Store"))
    driver.find_element_by_css_selector(".content a.link").click()

    # add item to cart
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name=add_cart_product]")))
    # select a size if it is the yellow duck
    if driver.find_element(By.CSS_SELECTOR, "h1.title").get_attribute("innerText") == "Yellow Duck":
        driver.find_element_by_css_selector("select[name='options[Size]']").click()
        driver.find_element_by_css_selector("select[name='options[Size]'] option:nth-child(2)").click()

    driver.find_element_by_css_selector("button[name=add_cart_product]").click()


def test_first(driver):
    i = 1
    wait = WebDriverWait(driver, 10)
    while i < 4:
        add_item_to_cart(driver)
        # wait until counter changed
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart .quantity"), str(i)))
        i += 1

    # checkout
    driver.find_element_by_css_selector("#cart-wrapper .link").click()

    while True:
        # remove item
        if element_exists(driver, By.CSS_SELECTOR, ".shortcuts .shortcut:first-child"):
            driver.find_element_by_css_selector(".shortcuts .shortcut:first-child").click()

        summary_block_element = driver.find_element_by_css_selector("#box-checkout-summary")
        driver.find_element_by_css_selector(".viewport .item:first-child button[name=remove_cart_item]").click()
        # waiting for DOM to change
        wait.until(EC.staleness_of(driver.find_element_by_css_selector("#checkout-cart-wrapper .viewport")))

        if not element_exists(driver, By.CSS_SELECTOR, "#checkout-cart-wrapper .viewport"):
            break

        # check table
        wait.until(EC.staleness_of(summary_block_element))

