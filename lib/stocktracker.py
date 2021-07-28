#!usr/bin/python

import sys, re, os, glob, platform

import datetime
import tempfile
import unicodedata

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from db_common import *
from common import *
from stockdb import *


class StockTracker:
    default_website = "https://finance.vietstock.vn"
    browser = ''
    actions = ''
    def __init__(self, default):
        self.config = default["config"]
        self.stockdb = default["stockdb"]

    def open_browser(self):
        global browser
        opts = webdriver.FirefoxOptions()
        if not self.config.gui:
            opts.set_headless()
        self.browser = webdriver.Firefox(firefox_options=opts)
        return None

    def wait_until_element_load(self, timeout, xpath_element):
        global browser
        WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.XPATH, '{}'.format(xpath_element)))
        )
        return None
        

    def google_data(self, key):
        global browser
        self.browser.get('https://google.com')
        try:
            self.browser.find_element_by_xpath("//*[text()='English']").click()
        except:
            print("Default language is already English")
        search_key = self.browser.find_element_by_xpath("//input[@title='Search']")
        search_key.send_keys(key)
        search_key.send_keys(Keys.ENTER)
        # Wait until searching complete, result page fully loaded
        self.wait_until_element_load(20, "//div[@class='hdtb-mitem']")

    def search_code(self, web_base):
        global browser
        self.google_data('co phieu vietnam {}'.format(self.config.stock_code))
        try:
            web_element = self.browser.find_element_by_xpath(r"//*[contains(text(), '{}')]".format(web_base))
            stock_element = web_element.find_element_by_xpath(r"//span[contains(text(), '{}')]".format(self.config.stock_code))
            return stock_element
        except:
            print("Can't find {} or {} in web_base".format(web_base, self.config.stock_code))
            return False
    
    # Access the element in google searching result and wait until the new page loaded
    def access_element(self, element, confirm_xpath_element):
        global browser
        if (element):
            element.click()
        self.wait_until_element_load(10, confirm_xpath_element)
        return None

    def capture_element_text(self, capture_key):
        global browser
        return self.browser.find_element_by_xpath(capture_key).text

    def update_stock_info(self, price, name):
        global browser


    def scrap_data_from_web(self): 
        global browser
        self.browser.get('https://finance.vietstock.vn')
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'close-popup-icon-x-account'))
        )
        self.browser.find_elements(By.CLASS_NAME, 'close-popup-icon-x-account')[2].click()
        self.browser.find_element(By.ID, 'txt-top-filter').send_keys('POW')
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tt-suggestion'))
        )
        self.browser.find_elements(By.CLASS_NAME, 'tt-suggestion')[0].click()
        print(self.browser.current_url)

    def main(self):
        global browser
        self.open_browser()
        element = self.search_code('https://finance.vietstock.vn')
        self.access_element(element, "//h2[@id='stockprice']")
        if (platform.system() == 'Windows'):
            price = self.capture_element_text("//h2[@id='stockprice']").replace(',','.')
            name = self.capture_element_text("//h1[contains(@class, 'h1-title')]/b[1]")
        else:
            price = unicode_to_str(self.capture_element_text("//h2[@id='stockprice']")).replace(',','.')
            name = unicode_to_str(self.capture_element_text("//h1[contains(@class, 'h1-title')]/b[1]"))
        path = self.browser.current_url
        print(path)
        if not self.stockdb.is_code_exist(self.config.stock_code):
            print("Insert DB")
            self.stockdb.insert_stock_db([self.config.stock_code, name, path, price])
        else:
            print("Update DB")
            self.stockdb.update_stock_db([self.config.stock_code, name, path, price])

        return None

