import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from prettytable import PrettyTable
from time import strptime
import os
import constants as const

class Verge_scraper(webdriver.Chrome):
    def __init__(self, year,month,keyword='',driver_path="D:\Free Code Camp\Selenium\chromedriver_win64",teardown=False):
    
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        super(Verge_scraper,self).__init__(options=options)

        self.year = year
        str_month = str(strptime(month, '%b').tm_mon)
        self.month = str_month
        self.keyword = keyword.lower()
        self.teardown = teardown
        self.maximize_window()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
    
    def parse_url(self):
        int_key = self.keyword + '/'
        parsed_url = const.base_url + int_key + self.year + '/' + self.month
        return parsed_url
    
    def land_req_page(self):
        self.get(self.parse_url())

    def scrolling_func(self):
        # Get scroll height
        last_height = self.execute_script("return document.body.scrollHeight")
        while True:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # ActionChains(self).key_down(Keys.CONTROL).send_keys(
            #     'END').key_up(Keys.CONTROL).perform()

            # Wait to load page
            load_button = WebDriverWait(self, 3).until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'c-archives-load-more__button')))
            load_button.click()
            
            if len(self.keyword) == 0:
                time.sleep(10)
            elif len(self.keyword)>0:
                time.sleep(1)
            
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def load_more(self):
        done = True
        while done:
            try:
                self.scrolling_func()
            except:
                print('Whattt')
                done = False
    
    def date_extractor(self,date_elem):
        return date_elem.text.strip()
    def text_extractor(self,title_elem):
        return title_elem.text.strip()

    def link_extractor(self, title_elem):
        s = str(title_elem)[str(title_elem).find("href")+5:]
        return s[:s.find(">")]

    def info_extractor(self):
        soup = BeautifulSoup(self.page_source, 'lxml')
        titles = soup.find_all("h2", class_="c-entry-box--compact__title")
        dates = soup.find_all("time", class_="c-byline__item")
        total = soup.find('h1', class_="p-page-title")

        self.total = total.text.strip().split('(')[1].split(')')[0]
        self.final_headlines = []
        self.final_dates = []
        self.final_links = []

        headlines_results = map(self.text_extractor, titles)
        dates_results = map(self.date_extractor, dates)
        links_results = map(self.link_extractor, titles)

        def list_process(gens):
            return [gen for gen in gens]

        headlines = list_process(headlines_results)
        dates = list_process(dates_results)
        links = list_process(links_results)

        self.final_headlines.extend(headlines)
        self.final_dates.extend(dates)
        self.final_links.extend(links)

    def write_to_csv(self):
        dict_data = {'Date':self.final_dates,'Headlines':self.final_headlines,'links':self.final_links}

        df = pd.DataFrame(dict_data,columns = list(dict_data.keys()))
        df = df.iloc[::-1]
        print(f'The dataframe size is {len(df)} and total number of links is {self.total}')
        df.to_csv(f'{self.keyword.capitalize()}_{self.month}_{self.year}.csv')
    
    def print_table(self):
        collections = []
        for d,h,l in zip(self.final_dates,self.final_headlines,self.final_links):
            collections.append((d,h,l))
        
        table = PrettyTable(
            ["Dates", "Headlines", "Links"]
        )
        table.add_rows(collections)
        print(table)
        self.teardown = True

        



        
        
        
            
                        



    
