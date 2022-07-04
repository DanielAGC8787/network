from selenium import webdriver
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('http://127.0.0.1:8000/')
login = driver.find_element_by_id("login")
login.click()
username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")

username.send_keys('Carl')
password.send_keys('D@niel0606')
submit = driver.find_element_by_id("loginButton")
submit.click()

for i in range(25):
    textSpace = driver.find_element_by_id("id_body")
    textSpace.send_keys('test post from bot')
    postButton = driver.find_element_by_id("post")
    postButton.click()

time.sleep(3)
assert 'admin' in driver.page_source

