# -*- coding: UTF-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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


def get_new_window(driver, windows_list):
    new_windows_list = driver.window_handles
    new_window = list(set(new_windows_list) - set(windows_list))
    if new_window:
        return new_window[0]
    else:
        return False


def test_first(driver):
    wait = WebDriverWait(driver,5)

    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    wait.until(EC.title_is("Countries | Test Selenium Store"))

    # let's check country creation page
    driver.find_element_by_css_selector(".button").click()
    wait.until(EC.title_is("Add New Country | Test Selenium Store"))

    # basic list of windows
    basic_windows_list = driver.window_handles
    main_window = driver.current_window_handle

    # get list of external links
    external_links_list = driver.find_elements(By.CSS_SELECTOR, "#content .fa-external-link")

    for external_link in external_links_list:
        external_link.click()
        # wait until new window opens
        wait.until(EC.new_window_is_opened(basic_windows_list))
        # find out id of a new window
        new_window_id = get_new_window(driver, basic_windows_list)
        driver.switch_to_window(new_window_id)
        driver.close()
        driver.switch_to_window(main_window)


