from selenium import webdriver
import selenium.webdriver.common.keys as Keys
import time
import threading
from capture import capture_feed
 
# change this to point to chromedriver location
driver = webdriver.Chrome('C:/Users/jochagas/Documents/Selenium/Driver/Chrome/chromedriver.exe')

# internet connection must be off
driver.get('https://chromedino.com/')
time.sleep(2)

driver.maximize_window();
page = driver.find_element_by_tag_name('body')
page.send_keys(u'\ue00d')

capture_feed.start()

while True:
    pass