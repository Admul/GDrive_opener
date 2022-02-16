import os
import time
import pickle
import logging
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from fake_useragent import UserAgent

# get local path
local_path = os.path.dirname(__file__)

# 
file_login = ""
file_password = ""

# Function for enter and check login
def login(driver):
    print("Enter your telephone number or yandex email...")
    login_enter(driver)

    try:
        while(driver.find_element(By.ID, "field:input-login:hint")):
            print("Incorrent telephone number or yandex email, please try again...")
            login_enter(driver)
    except NoSuchElementException:
        pass

# Function contain main code for enter data
def login_enter(driver):
    if(check_auth_file()):
        log = get_auth_log()
    else:
        log = input()
        global file_login
        file_login = log

    login_form = driver.find_element(By.ID, "passp-field-login")
    login_form.clear()
    login_form.send_keys(log)
    time.sleep(2)

    driver.find_element(By.ID, "passp:sign-in").click()
    time.sleep(2)
    
def password(driver):
    print("Please enter your password...")
    password_enter(driver)

    try:
        while(driver.find_element(By.ID, "field:input-passwd:hint")):
            print("Incorrent passwrod, please try again...")
            password_enter(driver)
    except NoSuchElementException:
        pass
    
def password_enter(driver):
    if(check_auth_file()):
        pas = get_auth_pas()
    else:
        pas = input()
        global file_password
        file_password = pas

    password_form = driver.find_element(By.ID, "passp-field-passwd")
    password_form.clear()
    password_form.send_keys(pas)
    time.sleep(2)

    driver.find_element(By.ID, "passp:sign-in").click()
    time.sleep(2)
    
def create_auth_file():
    auth_info = {
            "login": file_login,
            "password": file_password
        }   
    with open(f"{local_path}/auth.json", "w") as file:
        json.dump(auth_info, file)
        
def check_auth_file():
    test = False
    
    for file in os.listdir(f"{local_path}"):
        if file == "auth.json":
            test = True
            
    try: 
        get_auth_log()
    except json.JSONDecodeError:
        test = False
            
    return test


def get_auth_log():
    with open(f"{local_path}/auth.json", "r", encoding="utf8") as file:
        data = json.load(file)["login"]
        
    return data
        

def get_auth_pas():
    with open(f"{local_path}/auth.json", "r", encoding="utf8") as file:
        pas = json.load(file)["password"]

    return pas

def main():
    # set options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    #options.add_argument("--headless")

    driver = webdriver.Chrome(
        executable_path=f"{local_path}/chromedriver.exe",
        options=options)
    
    os.remove(f"{local_path}/ydrive_opener.log")
    logging.basicConfig(level=logging.DEBUG, filename=f"{local_path}/ydrive_opener.log")

    try:
        # Open page
        print("Open yandex drive")
        driver.get("https://disk.yandex.ru/client/disk")
        time.sleep(2)
        
        # Enter login
        print("Enter on yandex drive")
        login(driver)
        time.sleep(2)
        
        # Enter password
        password(driver)
        time.sleep(2)
        
        print("Succesful enter on yandex drive!")
        if(check_auth_file() == False):
            create_auth_file()
            
        while driver.window_handles:
            pass
             
    except Exception as ex:
        logging.exception("Exception: ")
    finally:
        if(NoSuchWindowException == False):
            driver.close()
        driver.quit()
    
if __name__ == "__main__":
    main()