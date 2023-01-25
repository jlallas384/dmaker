import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from time import *
from threading import *
f = open('data.json')
data = json.load(f)

def func(users, num):
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options = options)
    for user in users:
        driver.get(url)
        username = user['username']
        password = user['password']
        email = username + '@' + user['email']

        try:
            cookies = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Allow all cookies']")))
            cookies.click()
        except:
            pass

        un_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter email address']")))
        un_input.send_keys(email)

        pw_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter password']")))
        pw_input.send_keys(password)

        confirm = driver.find_element(By.XPATH, "//button[text()='Log in']")    
        confirm.click()

        card = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "BaseCard_title__BEzWQ")))
        card.click()
        sleep(3)
        s = driver.find_elements(By.XPATH, "//button[text()='View My Responses']")
        if len(s):
            print("OK", num)
        else:
            print("NO", username)
        driver.delete_all_cookies()

url = 'https://dreammaker.ph/login'

number_of_threads = 2

threads = []

for number in range(number_of_threads):
    t = Thread(target=func, args=(data[number::number_of_threads],number, )) # get number for place in list `buttons`
    t.start()
    threads.append(t)

for t in threads:
    t.join()



