from selenium import webdriver
import selenium.webdriver.common.keys as Keys
import time
import threading
from capture import capture_feed
from network import ai_player

# Altere este diretório para onde está o driver do selenium
driver = webdriver.Chrome('C:/Users/jochagas/Documents/Selenium/Driver/Chrome/chromedriver.exe')

# Chama pagina web
driver.get('https://chromedino.com/')
time.sleep(2)
driver.maximize_window();

# Seleciona um elemento específico para receber os comandos
page = driver.find_element_by_tag_name('body')

# Inicia
page.send_keys(u'\ue00d')

# Controla o objeto
while True:
   ai_player.predict(page)
