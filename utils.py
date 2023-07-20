import logging
import requests
import re
import pandas as pd
from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

from selenium.common.exceptions import ElementNotInteractableException
from settings import URL_FORMATTED, DRIVER, CLASSNAME_DENY_SUBS

logging.basicConfig(level=logging.INFO, filename='utils.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class Airline_scraper:

    def __init__(self) -> None:
        self.get_data_from_flight('AQP', 'LIM', '2023-07-20', '2023-07-23')
        

    def get_data_from_flight(self,from_country_code, to_country_code, departure_date, return_date):
        # 'YYYY-MM-DD'
    
        self.url = URL_FORMATTED.format(from_country_code=from_country_code, to_country_code=to_country_code, departure_date=departure_date, return_date=return_date )
        
        self.setting_up_webpage_to_extract()

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        logging.info('Getting page source from: {from_country_code} to: {to_country_code}, Staying: {departure_date} to {return_date}'.format(to_country_code=to_country_code, from_country_code=from_country_code, departure_date=departure_date, return_date=return_date))
        
        df= self.df_prices_per_date(soup)
        print(df.head())
        print(df.shape)

        self.driver.quit()
        return soup
    def setting_up_webpage_to_extract(self,month=6):

        self.driver = DRIVER
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)
        self.skip_add()
        self.driver.implicitly_wait(5)
        next_button_push = month*5
        for _ in range(next_button_push):
            self.next_page_date_prices()
            sleep(0.25)

        sleep(10)


    def df_prices_per_date(self,page_source):
        container_prices_and_date = page_source.find('ul', class_='slider')
        items_prices_and_date = container_prices_and_date.find_all('li', class_='date-slider-item')

        data_date_prices_dict = self.items_prices_and_date_loop(items_prices_and_date)
        logging.info('Prices and dates extracted')

        df= pd.DataFrame(data_date_prices_dict)
        return df

        
    def items_prices_and_date_loop(self, items_prices_and_date):
        data_date_prices = {
            'date': [],
            'prices $': []
        }

        for item in items_prices_and_date:
            month_name = item.find('span', class_='month').text
            days = item.find('span', class_='day').text
            days = re.findall(r'\d+', days)[0]
            date_formatted = month_name + days
            
            prices_container = item.find('div', class_='price')
            prices = prices_container.find('span').text
            prices = prices.replace('USD ', '')

            data_date_prices['date'].append(date_formatted)
            data_date_prices['prices $'].append(prices)

        return data_date_prices


    def next_page_date_prices(self):
        
        buttons= self.driver.find_elements(By.CLASS_NAME,'slider-button')
        from_button_next = buttons[1]
        sleep(1)
        from_button_next.click()
      

    def skip_add(self):
        
        try:
            skipping_add = self.driver.find_element(By.ID,'pa-deny-btn')
            skipping_add.click()
            sleep(3)
            self.driver.execute_script("window.scrollTo(0, 100);")

            logging.info('Add skipped')
        except ElementNotInteractableException:
            logging.info('Add not found')
            pass

        return logging.info('Scraping started')

    

Airline_scraper()


# class Airline_scraper:

    
    # def __init__(self):
    #     self.driver = DRIVER

    #     self.init_scrap()
    #     self.select_from_to_country('Arequipa', 'Lima')

    # def init_scrap(self):
    #     self.driver.get(URL)
    #     self.driver.implicitly_wait(5)
    #     logging.info('Waiting for add')
        
    #     try:
    #         WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, CLASSNAME_DENY_SUBS))
    #         )
    #         skipping_add = self.driver.find_element(By.CLASS_NAME,CLASSNAME_DENY_SUBS)
    #         skipping_add.click()
    #         logging.info('Add skipped')
            

    #     except ElementNotInteractableException:
    #         logging.info('Add not found')
    #         pass

    #     return logging.info('Scraping started')
        



    # def select_from_to_country(self, input_from_country, input_to_country):
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, 'el-input__inner'))
    #     )
    #     main_containers = self.driver.find_elements(By.CLASS_NAME, 'el-input__inner')
    #     main_containers = main_containers[:2]

    #     from_country = main_containers[0]
    #     to_country = main_containers[1]

    #     from_country.send_keys(input_from_country)
    #     from_country.send_keys(Keys.ENTER)
    #     logging.info(f'From country : {input_from_country}')

    #     to_country.send_keys(input_to_country)
    #     to_country.send_keys(Keys.ENTER)
    #     logging.info(f'To country : {input_to_country}')
    #     sleep(5)



# Airline_scraper()