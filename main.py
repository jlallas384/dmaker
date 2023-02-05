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
from random import *
import datetime

f = open('data.json')
data = json.load(f)

with open("log.txt",'w') as file:
    pass

lock = Lock()

def func(users):
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    while True:
        try:
            driver = webdriver.Chrome(".\\chromedriver",options = chrome_options)
            break
        except Exception as E:
            print(E)
            continue
    for user in users:
        try:
            while True:
                driver.get("https://dreammaker.ph/login")
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
                take = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Take Survey']")))
                take.click()

                for i in range(10):
                    vote = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='10. JOM']")))
                    s2 = """
                    var xpath = "//div[text()='10. JOM']";
                    var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    matchingElement.click()
                    """
                    driver.execute_script(s2)
                    nextBtn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Next']")))
                    s2 = """
                    xpath = "//button[text()='Next']";
                    matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    matchingElement.click()
                    """
                    driver.execute_script(s2)
                    sleep(1.2)
                vote = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Disagree']")))
                s2 = """
                var xpath = "//div[text()='Disagree']";
                var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                matchingElement.click()
                """
                driver.execute_script(s2)
                try:
                    nextBtn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Submit']")))
                except:
                    print("OOF",index)
                    driver.quit()
                    while True:
                        try:
                            driver = webdriver.Chrome(".\\chromedriver",options = chrome_options)
                            break
                        except:
                            continue
                    continue

                s2 = """
                xpath = "//button[text()='Submit']";
                matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                matchingElement.click()
                """
                driver.execute_script(s2)
                sleep(1)

                try:
                    nextBtn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Cancel']")))
                    s2 = """
                    xpath = "//button[text()='Cancel']";
                    matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    matchingElement.click()
                    """
                    driver.execute_script(s2)
                except:
                    pass
                print("NICE")
                lock.acquire()
                with open('log.txt', 'a') as f:
                    f.write(f"{username},{password},{user['email']},{datetime.datetime.now()}\n")
                lock.release()
                driver.delete_all_cookies()
                break
        except Exception as e:
            print("NOO", e)
            driver.quit()
            while True:
                try:
                    driver = webdriver.Chrome(".\\chromedriver",options = chrome_options)
                    break
                except:
                    continue
            continue
    driver.quit()


with open('setup.txt') as f:
    number_of_threads = int([line.rstrip('\n') for line in f][0])


threads = []

for number in range(number_of_threads):
    t = Thread(target=func, args=(data[number::number_of_threads], )) # get number for place in list `buttons`
    t.start()
    threads.append(t)

for t in threads:
    t.join()



print("OKAY NAAAAAAAAAAAAAAA")