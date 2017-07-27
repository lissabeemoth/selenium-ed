# -*- coding: UTF-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def get_element(driver, *args):
    try:
        return driver.find_element(*args)
    except NoSuchElementException:
        return False


def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    WebDriverWait(driver, 5).until(ec.title_is("Test Selenium Store"))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    cursor = True
    while cursor:
        if get_element(driver, By.CSS_SELECTOR, '#box-apps-menu .selected'):
            current = get_element(driver, By.CSS_SELECTOR, '#box-apps-menu .selected + li')
        else:
            current = get_element(driver, By.CSS_SELECTOR, '#box-apps-menu > li:first-child')
        if current:
            current.click()
            driver.find_element(By.TAG_NAME, "h1")
        else:
            cursor = False