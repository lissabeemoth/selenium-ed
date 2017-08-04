# -*- coding: UTF-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    #print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_first(driver):
    driver.get("http://localhost/litecart/en/create_account")
    WebDriverWait(driver, 5).until(EC.title_is("Create Account | Test Selenium Store"))

    # generation of unique email address
    letters = ['a', 'b', 'c', 'd', 'e']
    generated_email = random.choice(letters) + str(random.randint(0,1000)) + '@' + 'test.test'
    password = '123456'

    # new user registration - USA, New Jersey
    driver.find_element_by_css_selector("input[name=tax_id]").send_keys("123456")
    driver.find_element_by_css_selector("input[name=company]").send_keys("Company Test")
    driver.find_element_by_css_selector("input[name=firstname]").send_keys("FName")
    driver.find_element_by_css_selector("input[name=lastname]").send_keys("LName")
    driver.find_element_by_css_selector("input[name=address1]").send_keys("26 Merry Lane MK01")
    driver.find_element_by_css_selector("input[name=postcode]").send_keys("07936")
    driver.find_element_by_css_selector("input[name=city]").send_keys("East Hanover")

    # select magic
    country_select = driver.find_element_by_css_selector("select[name=country_code]")
    driver.execute_script("arguments[0].selectedIndex = 224; arguments[0].dispatchEvent(new Event('change'))", country_select)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "zone_code")))

    zone_select = driver.find_element_by_css_selector("select[name=zone_code]")
    driver.execute_script("arguments[0].selectedIndex = 40; arguments[0].dispatchEvent(new Event('change'))", zone_select)

    driver.find_element_by_css_selector("input[name=email]").send_keys(generated_email)
    driver.find_element_by_css_selector("input[name=phone]").send_keys("+380000000001")
    driver.find_element_by_css_selector("input[name=password]").send_keys(password)
    driver.find_element_by_css_selector("input[name=confirmed_password]").send_keys(password)

    # submit
    driver.find_element_by_css_selector("button[name=create_account]").click()

    # logout
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
    driver.find_element(By.LINK_TEXT, "Logout").click()

    # login
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "login")))
    driver.find_element_by_css_selector("input[name=email]").send_keys(generated_email)
    driver.find_element_by_css_selector("input[name=password]").send_keys(password)
    driver.find_element_by_css_selector("button[name=login]").click()
    WebDriverWait(driver, 5).until(EC.title_is("Online Store | Test Selenium Store"))

    #logout
    driver.find_element(By.LINK_TEXT, "Logout").click()


