from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import URL, DRIVER, CLASSNAME_DENY_SUBS

DRIVER.get(URL)

sleep(2)
DRIVER.find_element(By.CLASS_NAME,CLASSNAME_DENY_SUBS).click()

containers = DRIVER.find_elements(By.CLASS_NAME, 'el-input__inner')
containers = containers[:2]

from_country = containers[0]
to_country = containers[1]

from_country.send_keys('Arequipa')
sleep(1)
element = DRIVER.find_element(By.XPATH, '//li[contains(text(), "Arequipa")]')
element.click()

DRIVER.close()
sleep(3)
