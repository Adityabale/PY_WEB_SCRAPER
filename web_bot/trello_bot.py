from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date
import os
import json


CHROME_DRIVER_PATH = os.path.join(os.getcwd(),"chromedriver.exe") #Driver for all browsers-https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
OP = webdriver.ChromeOptions()
OP.add_argument('__headless')
DRIVER = webdriver.Chrome(CHROME_DRIVER_PATH)


def login():
    with open('config.json') as configfile:
        credentials = json.load(configfile)
        #credentials["PASSWORD"]
        #credentials['USENAME']
        time.sleep(2) 
        DRIVER.find_element(By.XPATH, value="//a[@href='/login']").click() #// means anywhere in the whole Html
        #XPath can be used to navigate through elements and attributes in an XML document.
        time.sleep(2)
        username = DRIVER.find_element(By.CSS_SELECTOR, value="input[name='user']")
        username.clear()
        username.send_keys(credentials["USERNAME"])
        DRIVER.find_element(By.CSS_SELECTOR, value="input[type='submit']").click()
        time.sleep(2)
        password = DRIVER.find_element(By.CSS_SELECTOR, value="input[name='password']")
        password.clear()
        password.send_keys(credentials["PASSWORD"])
        DRIVER.find_element(By.XPATH, value="//*[@type='submit']").click()
        time.sleep(2)
    

def navigateToBoard():
    time.sleep(5)
    DRIVER.find_element(By.XPATH, value="//div[@class='{}']/ancestor::a".format('board-tile-details-name')).click()
    time.sleep(5)


def addtask():
    time.sleep(5)
    DRIVER.find_element(By.XPATH, value="//textarea[@aria-label='To Do']/ancestor::div/descendant::div[@class='card-composer-container js-card-composer-container']/child::a").click()
    time.sleep(5)
    task_text_area = DRIVER.find_element(By.XPATH, value="//div[@class='card-composer']/descendant::textarea")
    task_text_area.clear()
    task_text_area.send_keys("Bot Added Task")
    DRIVER.find_element(By.XPATH, value="//input[@value='Add card']").click()
    time.sleep(5)


def screenshotPage():
    time.sleep(5)
    date_str = date.today().strftime("%m-%d-%Y")
    file_path = os.path.join(os.getcwd(), 'downloads/{}.png'.format(date_str))
    DRIVER.get_screenshot_as_file(file_path)

def main():
    try:        
        DRIVER.get('https://trello.com')
        login()
        navigateToBoard()
        addtask()
        screenshotPage()
        input("Bot operations complete. Press any key....")
        DRIVER.close()
    except Exception as e:  
        print(e)
        DRIVER.close()


if __name__=='__main__':
    main()

