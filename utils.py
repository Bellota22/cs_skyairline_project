import re
import os
import logging
import requests
import pandas as pd
from time import sleep
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

from selenium.common.exceptions import ElementNotInteractableException
from settings import URL_FORMATTED, DRIVER, CLASSNAME_DENY_SUBS, MONTH_MAP

logging.basicConfig(level=logging.INFO, filename='utils.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class Airline_scraper:

    def __init__(self) -> None:
        self.from_cc = ['IQT','AQP','JAU']
        self.to_cc = ['LIM']
        self.departure_date = '2023-07-20' # 'YYYY-MM-DD'
        self.return_date = '2023-07-23'
        
        for from_cc in self.from_cc:
            for to_cc in self.to_cc:
                self.get_data_from_flight(from_cc, to_cc, self.departure_date, self.return_date)
        




    def get_data_from_flight(self,from_country_code, to_country_code, departure_date, return_date):
    
        self.url = URL_FORMATTED.format(from_country_code=from_country_code, to_country_code=to_country_code, departure_date=departure_date, return_date=return_date )
        
        if not self.setting_up_webpage_to_extract():

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            logging.info('Getting page source from: {from_country_code} to: {to_country_code}, Staying: {departure_date} to {return_date}'.format(to_country_code=to_country_code, from_country_code=from_country_code, departure_date=departure_date, return_date=return_date))
            
            df= self.data_processed(soup)

            print(df.head())
            print(df.shape)

            self.driver.quit()
            return soup
        else:
            logging.info('No flights found_2')
            self.driver.quit()
            return False
    
    def setting_up_webpage_to_extract(self,month=1):

        self.driver = DRIVER
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)

        self.skip_add()
        self.driver.implicitly_wait(5)

        no_flights= self.driver.find_element(By.CLASS_NAME,'flight_info_label').text
        
        if not no_flights:
            next_button_push = month*5

            for _ in range(next_button_push):
                self.next_page_date_prices()
                sleep(0.25)

            sleep(3)
            logging.info('Page source extracted')
            return True

        else:
            logging.info('No flights found_1')
            self.driver.quit()

            return False

    def data_processed(self,page_source):
        container_prices_and_date = page_source.find('ul', class_='slider')
        items_prices_and_date = container_prices_and_date.find_all('li', class_='date-slider-item')

        data_date_prices_dict = self.items_prices_and_date_loop(items_prices_and_date)

        logging.info('Prices and dates extracted')

        df= pd.DataFrame(data_date_prices_dict)
        df = self.structured_df(df)
        logging.info('Dataframe structured')

        self.save_data(df)
        
        return df
    
    def structured_df(self,df):
        
        df = self.structured_date_column(df)
        df['prices $'] = df['prices $'].astype(float)
        df['from_country'] = self.from_cc
        df['to_country'] = self.to_cc
        df['departure_date'] = self.departure_date
        df['return_date'] = self.return_date
        df.sort_values(by=['date'], inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df
        
    def structured_date_column(self, df):
        current_year = datetime.now().year
        self.month_map = MONTH_MAP

        df['date'] = df['date'].str.strip()
        df['date'] = df['date'].apply(self.convert_month_cc)
        df['date'] = pd.to_datetime(df['date'] + f' {current_year}', format='%b %d %Y')

        df['is_month_reset'] = df['date'].dt.month < df['date'].dt.month.shift()
        df['date'] = df.apply(lambda x: x['date'].replace(year=x['date'].year+1) if x['is_month_reset'] else x['date'], axis=1)

        df = df.drop(columns=['is_month_reset'])

        logging.info('Date column converted')
        return df
    
    def convert_month_cc(self, date_str):
        for esp, eng in self.month_map.items():
            if esp in date_str:
                return date_str.replace(esp, eng)
        return date_str

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

    def save_data(self, df):
        
        if not os.path.exists('data'):
            os.makedirs('data')
            df.to_csv(f'data/data_{self.from_cc}_{self.to_cc}.csv', index=False)
            logging.info('Dataframe saved')
        else:
            df.to_csv(f'data/data_{self.from_cc}_{self.to_cc}.csv', index=False)
            logging.info('Dataframe saved')

        return True

        

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

