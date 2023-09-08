import numpy as np
import time
import operator
from operator import itemgetter
import urllib
import json
import urllib.parse
from urllib import request
import re
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import lxml
from lxml import etree
from fuzzywuzzy import fuzz
from utils import load_from_mongodb
from utils import store_to_mongodb
from Prototype1_final import ResourceRecommendation
import json

SCROLL_PAUSE_TIME = 0.5

obj = ResourceRecommendation()
list_of_KPs = obj.load_KPs()
KP_List = list_of_KPs
list_of_names = obj.load_KP_names()
KP_names = list_of_names
KP_metadata = pd.DataFrame(columns = ['KP_name'], index = KP_List, data = KP_names)

driver = webdriver.Firefox(executable_path= r'C:\Users\nguyennamminhquan\work\geckodriver.exe')
#driver.get(r"https://www.youtube.com/playlist?list=PLCd8j6ZYo0lY8ZFrhrAyzCzuo5x9YIrAm")
driver.get(r"https://www.youtube.com/playlist?list=PLCd8j6ZYo0lbwm8pL2Dvr7xs23FovsKXI")
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


def get_youtube_title(youtube_id):
   youtube_watch_url = r'https://www.youtube.com/watch?v='
   youtube_watch_url += youtube_id
   youtube = etree.HTML(request.urlopen(youtube_watch_url).read().decode(r'utf-8'))
   video_title = youtube.xpath(r"//title")[0].text 
   return video_title

user_data = driver.find_elements_by_xpath(r'//*[@id="video-title"]')
links = []
for i in user_data:
  links.append(i.get_attribute('href'))

resource_kp = pd.DataFrame(columns = ['title', 'link', 'KP_available'])

def getIndexes(dfObj, value):
    ''' Get index positions of value in dataframe i.e. dfObj.'''
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append(row)
            
    # Return a list of tuples indicating the positions of value in the dataframe
            
    return listOfPos[0]
#sorting resources
def classify(x):
  KP_contained = list()
  str2 = x
  for i in range(len(KP_names)):
    str1 = KP_names[i]
    ratio = fuzz.token_sort_ratio(str1.lower(), str2.lower())
    if ratio >= 50:
      KP_contained.append(getIndexes(KP_metadata, str1))
  return KP_contained

wait = WebDriverWait(driver, 10)

  
for x in links: 
    driver.get(x)
    v_id = x[32:]
    #v_title = driver.find_element_by_xpath('//*[@id="video-title"]').text
    v_title = get_youtube_title(v_id)
    final_title = v_title[25:-9]
    KP_available = classify(final_title)
    v_link = r'https://www.youtube.com/watch?v='+ v_id
    resource_kp.loc[len(resource_kp)] = [v_title, v_link, KP_available]

resource_kp.to_csv(r'C:\Users\nguyennamminhquan\Desktop\Assignments\Work stuffs\lop_6_hinh.csv')
