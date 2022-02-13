import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

# get local path
local_path = os.path.dirname(__file__)

# set options
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    executable_path=f"{local_path}/chromedriver.exe",
    options=options)

try:
    # Open page
    print("Open drive.google.com")
    driver.get("https://drive.google.com")
    time.sleep(5)
    
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()