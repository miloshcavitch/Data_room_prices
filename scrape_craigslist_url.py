import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time

url = 'https://newyork.craigslist.org/search/roo?min_price=500'
driver = webdriver.Chrome()
driver.get(url)

hrefs = []
still_results = True
while still_results == True:
    results = driver.find_elements_by_class_name('result-row')
    if len(results) == 0:
        still_results = False
        break
    for result in results:
        hrefs.append(result.find_element_by_css_selector('a').get_attribute('href'))
    btn = driver.find_elements_by_xpath('//*[@id="searchform"]/div[3]/div[3]/span[2]/a[3]')
    if len(hrefs) < 2990:
        btn[0].click()
    else:
        still_results = False
    #time.sleep(2)


df = pd.DataFrame(hrefs, columns=['href'])

df.to_csv('nyc_room_prices.csv')
