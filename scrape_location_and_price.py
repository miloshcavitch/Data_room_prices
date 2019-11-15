import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time

df = pd.read_csv('nyc_room_prices.csv', index_col=0)


driver = webdriver.Chrome()

prices = []
longitudes = []
latitudes = []
for i, link in enumerate(df['href']):
    try:
        print(link)
        driver.get(link)
        price = driver.find_elements_by_xpath('/html/body/section/section/h2/span/span[1]')[0].text
        latitude = 0
        longitude = 0
        map = driver.find_element_by_id('map')
        latitude = map.get_attribute('data-latitude')
        longitude = map.get_attribute('data-longitude')
        prices.append(price)
        longitudes.append(longitude)
        latitudes.append(latitude)
    except:
        print('error occured, continuing')
    print(i)
    if i > 2999:
        break

df = pd.DataFrame(prices, columns=['price'])
df['longitude'] = longitudes
df['latitude'] = latitudes
df.to_csv('map_data.csv')
