# -*- coding: UTF-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
from selenium.webdriver.common.by import By

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    #wd = webdriver.Firefox()
    #wd = webdriver.Safari()
    #print(wd.capabilities)
    wd.get("http://localhost/litecart/")
    WebDriverWait(wd, 5).until(EC.title_is("Online Store | Test Selenium Store"))
    request.addfinalizer(wd.quit)
    return wd


def test_first(driver):
    # product parameters
    title = driver.find_element_by_css_selector("#box-campaigns .name").get_attribute("innerText")
    campaign_price = driver.find_element_by_css_selector("#box-campaigns .campaign-price").get_attribute("innerText")
    regular_price = driver.find_element_by_css_selector("#box-campaigns .regular-price").get_attribute("innerText")
    regular_price_colour = driver.find_element_by_css_selector("#box-campaigns .regular-price").value_of_css_property("color")
    # added for Safari
    if (driver.capabilities['browserName'] == "safari"):
        style_name = "text-decoration"
    else:
        style_name = "text-decoration-line"
    # get css styles
    regular_price_style = driver.find_element_by_css_selector("#box-campaigns .regular-price").value_of_css_property(style_name)
    regular_price_font = driver.find_element_by_css_selector("#box-campaigns .regular-price").value_of_css_property("font-size")
    campaign_price_colour = driver.find_element_by_css_selector("#box-campaigns .campaign-price").value_of_css_property("color")
    campaign_price_style = driver.find_element_by_css_selector("#box-campaigns .campaign-price").value_of_css_property("font-weight")
    campaign_price_font = driver.find_element_by_css_selector("#box-campaigns .campaign-price").value_of_css_property("font-size")

    # check styles
    regular_price_colour = Color.from_string(regular_price_colour)
    campaign_price_colour = Color.from_string(campaign_price_colour)

    if regular_price_colour.red == regular_price_colour.blue == regular_price_colour.green:
        print "regular price colour is grey"
    else:
        print "error! regular price colour is wrong"

    if regular_price_style == "line-through":
        print "regular price style is ok"
    else:
        print "error! regular price style is wrong"

    if regular_price_font < campaign_price_font:
        print "fonts are ok"
    else:
        print "error! fonts are wrong"

    if (campaign_price_colour.blue == 0) & (campaign_price_colour.green == 0):
        print "campaign price colour is red"
    else:
        print "error! campaign price colour is wrong"

    # added for FF
    if (driver.capabilities['browserName'] == "firefox"):
        if int(campaign_price_style) >= 400:
            print "campaign price style is ok"
        else:
            print "error! campaign price style is wrong"
    elif campaign_price_style == "bold":
        print "campaign price style is ok"
    else:
        print "error! campaign price style is wrong"

    # second part of task
    driver.find_element_by_css_selector("#box-campaigns .link").click()
    print "================================================================"
    print "================================================================"

    # added for Safari
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

    # get product parameters
    title_inner = driver.find_element_by_css_selector("h1").get_attribute("innerText")
    campaign_price_inner = driver.find_element_by_css_selector("#box-product .campaign-price").get_attribute("innerText")
    regular_price_inner = driver.find_element_by_css_selector("#box-product .regular-price").get_attribute("innerText")
    regular_price_colour = driver.find_element_by_css_selector("#box-product .regular-price").value_of_css_property("color")

    # added for Safari
    if (driver.capabilities['browserName'] == "safari"):
        style_name = "text-decoration"
    else:
        style_name = "text-decoration-line"

    regular_price_style = driver.find_element_by_css_selector("#box-product .regular-price").value_of_css_property(style_name)
    regular_price_font = driver.find_element_by_css_selector("#box-product .regular-price").value_of_css_property("font-size")
    campaign_price_colour = driver.find_element_by_css_selector("#box-product .campaign-price").value_of_css_property("color")
    campaign_price_style = driver.find_element_by_css_selector("#box-product .campaign-price").value_of_css_property("font-weight")
    campaign_price_font = driver.find_element_by_css_selector("#box-product .campaign-price").value_of_css_property("font-size")
    regular_price_colour = Color.from_string(regular_price_colour)
    campaign_price_colour = Color.from_string(campaign_price_colour)

    # check product parameters
    if regular_price_colour.red == regular_price_colour.blue == regular_price_colour.green:
        print "regular price colour is grey"
    else:
        print "error! regular price colour is wrong"
        print regular_price_colour[1]

    if regular_price_style == "line-through":
        print "regular price style is ok"
    else:
        print "error! regular price style is wrong"

    if regular_price_font < campaign_price_font:
        print "fonts are ok"
    else:
        print "error! fonts are wrong"

    if (campaign_price_colour.blue == 0) & (campaign_price_colour.green == 0):
        print "campaign price colour is red"
    else:
        print "error! campaign price colour is wrong"

    # added for FF
    if (driver.capabilities['browserName'] == "firefox"):
        if int(campaign_price_style) >= 400:
            print "campaign price style is ok"
        else:
            print "error! campaign price style is wrong"
    elif campaign_price_style == "bold":
        print "campaign price style is ok"
    else:
        print "error! campaign price style is wrong"

    # check if there are differences between home and product pages
    if title == title_inner:
        print "Titles are the same"
    else:
        print "Titles are not the same"

    if campaign_price == campaign_price_inner:
        print "Campaign prices are the same"
    else:
        print "Campaign prices are not the same"

    if regular_price == regular_price_inner:
        print "Regular prices are the same"
    else:
        print "Regular prices are not the same"
