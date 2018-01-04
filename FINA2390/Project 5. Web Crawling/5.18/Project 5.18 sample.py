import csv
import pandas as pd
import os
from time import sleep
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


df_columns = ['Date',
              'Year of Study',
              'Subject',
              'Sex',
              'Location',
              'Time',
              'Salary']

#Create new dataframe with a the fields above
df = pd.DataFrame(columns=df_columns)

def get_data():
    chrome_path = r"E:\Project\Prospectus\Prospectus\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)
    driver.get("http://www.kits-tutor.com/2015/index.php")
    sleep(3)
    #assert "No results found." not in driver.page_source
    #try:
    num = 1
    rowCount=len(driver.find_elements_by_xpath('//*[@id="content"]/table/tbody/tr'))
    for row in driver.find_elements_by_xpath('//*[@id="content"]/table/tbody/tr'):
        print('Current Progress:' + str(round(num/rowCount*100,2)) + '%' ,end='\r')
        df.loc[num,'Location']= row.find_element_by_xpath('td[1]/a/strong').text
        df.loc[num,'Year of Study']= row.find_element_by_xpath('td[2]').text
        df.loc[num,'Sex']= row.find_element_by_xpath('td[3]').text
        df.loc[num,'Subject']= row.find_element_by_xpath('td[4]').text
        df.loc[num,'Time']= row.find_element_by_xpath('td[5]').text
        df.loc[num,'Salary']= row.find_element_by_xpath('td[6]').text
        df.loc[num,'Date']= row.find_element_by_xpath('td[7]').text
        num+=1
    #except NoSuchElementException:
    driver.quit()
    date =datetime.date.today()
    df.to_csv('kitstutor_'+str(date)+'.csv',index=False, encoding='utf-8')
    print('Data is successfully saved!')
get_data()