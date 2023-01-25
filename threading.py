from requests import *
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

f = open('data.json')
index = 0
data = json.load(f)[index:]

from time import sleep
from csv import writer
from threading import *

lock = Lock()

def func(users):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome("chromedriver", options = chrome_options)
    for user in users:
        try:
            driver.get("https://dreammaker.ph/signup")
            username = user['username']
            password = user['password']
            email = username + '@' + user['email']
            try:
                cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Allow all cookies']")))
                cookies.click()
            except:
                pass
            email_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Email']")))
            email_input.send_keys(email)

            verify_email = driver.find_element(By.XPATH, "//button[text()='Verify email']") 
            verify_email.click()

            sleep(4)
            msg_id = -1
            while 1:
                try:
                    sleep(1)
                    msg_id = get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={user["email"]}').json()[0]["id"]
                    break
                except:
                    continue
            msg = get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={user["email"]}&id={msg_id}').json()["body"]

            soup = BeautifulSoup(msg, "html.parser")
            code = soup.find('div', {'class': 'otpCode'}).text

            verification_code = driver.find_element(By.XPATH, "//input[@placeholder='Enter 6-digit verification code']")
            verification_code.send_keys(code)

            pw_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Password']")))
            pw_input.send_keys(password)

            next_button = driver.find_element(By.XPATH, "//button[text()='Next']")  
            next_button.click()

            pw_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Re-enter your password']")))
            pw_input.send_keys(password)

            next_button = driver.find_element(By.XPATH, "//button[text()='Next']")  
            next_button.click()

            sleep(2)

            chk_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Agree to all']")))
            chk_box.click()

            confirm = driver.find_element(By.XPATH, "//button[text()='Confirm']")   
            confirm.click()

            un_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter your nickname']")))
            un_input.send_keys(username)

            confirm = driver.find_element(By.XPATH, "//button[text()='Confirm']")   
            confirm.click()

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Congratulations! You are now a member!']")))
                lock.acquire()
                with open('account.csv', 'a', newline='') as f:
                    writer_object = writer(f)
                    writer_object.writerow([email, password])
                    f.close()
                lock.release()
            except:
                print("BRUH",index)
                #driver.save_screenshot(f"sc{index}.jpg")
                driver.delete_all_cookies()
                driver.execute_script('window.localStorage.clear();')
                index += 1
                continue
            #driver.save_screenshot(f"sc{index}.jpg")
            driver.delete_all_cookies()

            print(username,password,email,index)
            index += 1
        except:
            pass


number_of_threads = 5

threads = []

for number in range(number_of_threads):
    t = Thread(target=func, args=(data[number::number_of_threads], )) # get number for place in list `buttons`
    t.start()
    threads.append(t)

for t in threads:
    t.join()
