# -*- coding: UTF-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.get("http://localhost/litecart/admin/")
    WebDriverWait(wd, 5).until(EC.title_is("Test Selenium Store"))
    wd.find_element_by_name("username").send_keys("admin")
    wd.find_element_by_name("password").send_keys("admin")
    wd.find_element_by_name("login").click()
    request.addfinalizer(wd.quit)
    return wd


# first part of assignment
def test_first(driver):
    countries = []
    zones_urls = []

    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")

    # checking alphabetical order for countries list
    rows = driver.find_elements(By.CSS_SELECTOR, ".dataTable .row")

    for row in rows:
        country = row.find_element(By.CSS_SELECTOR, "td:nth-child(5) a")
        countries.append(country.get_attribute("innerText"))
        if row.find_element(By.CSS_SELECTOR, "td:nth-child(6)").get_attribute("innerText") != "0":
            zones_urls.append(country.get_attribute("href"))

    if countries == sorted(countries):
        print "Countries are sorted in alphabetical order"
    else:
        print "Countries are not in alphabetical order"

    # checking alphabetical order for zones list
    if not zones_urls:
        print "there are no zones specified for any country"
    else:
        zones = []
        for zone_page in zones_urls:
            driver.get(zone_page)
            zones_rows = driver.find_elements(By.CSS_SELECTOR,".dataTable td:nth-child(3)")

            for single_zone in zones_rows:
                if single_zone.get_attribute("innerText") != "":
                    zones.append(single_zone.get_attribute("innerText"))

            if zones == sorted(zones):
                print "Zones are sorted in alphabetical order"
            else:
                print "Zones are not in alphabetical order"


#second part of assignment
def test_second(driver):
    countries_urls = []
    zones = []

    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    rows = driver.find_elements(By.CSS_SELECTOR, ".dataTable .row")

    for row in rows:
        country_url = row.find_element(By.CSS_SELECTOR, "td:nth-child(3) a").get_attribute("href")
        countries_urls.append(country_url)

    print '============================================================'
    print '============================================================'

    for country_page in countries_urls:
        driver.get(country_page)
        zone_rows = driver.find_elements(By.CSS_SELECTOR, ".dataTable  td:nth-child(3) option[selected=selected]")

        for single_zone in zone_rows:
            if single_zone.get_attribute("innerText") != "":
                zones.append(single_zone.get_attribute("innerText"))

        if zones == sorted(zones):
            print "Zones are sorted in alphabetical order"
        else:
            print "Zones are not in alphabetical order"
