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
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


df_columns = ['Agency',
              'Date',
              'Year of Study',
              'Subject',
              'Sex',
              'Location',
              'Time',
              'Salary',
              'Remark']

#Create new dataframe with the fields above
df = pd.DataFrame(columns=df_columns)

def get_data():
    chrome_path = r"E:\Project\Prospectus\Prospectus\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)
    driver.get("http://www.tutorok.com/")
    #wait 3 seconds to load the website completely before crawling
    sleep(3)
    num = 1
    #get the total page number of the website
    page_no = int((driver.find_elements_by_id('span_page_no')[0].text).split('/')[1])
    try:
        for i in range(page_no):
            count = 1
            skip = True
            print('Extracting data from page ' + str(i+1))
            #extract the data from the table
            rowCount=len(driver.find_elements_by_xpath('/html/body/div/div[3]/div[2]/div/div[3]/table/tbody/tr'))
            for row in driver.find_elements_by_xpath('/html/body/div/div[3]/div[2]/div/div[3]/table/tbody/tr'):
                #skip the first title row
                if skip == True:
                    skip = False
                    continue
                #data extraction
                df.loc[num,'Agency']='TutorOK'
                df.loc[num,'Location']= row.find_element_by_xpath('td[2]').text
                df.loc[num,'Year of Study']= row.find_element_by_xpath('td[3]').text
                df.loc[num,'Sex']= row.find_element_by_xpath('td[5]').text
                df.loc[num,'Subject']= row.find_element_by_xpath('td[4]').text
                df.loc[num,'Time']= row.find_element_by_xpath('td[7]').text
                df.loc[num,'Salary']= row.find_element_by_xpath('td[6]').text
                df.loc[num,'Date']= row.find_element_by_xpath('td[9]').text
                df.loc[num,'Remark']= row.find_element_by_xpath('td[8]').text
                num+=1
                count+=1
                #progress percentage counting
                print('Current Progress:' + str(round(count/rowCount*100,2)) + '%' ,end='\r')
            #click to next page
            driver.find_element_by_xpath('//*[@id="a_next"]').click()
            sleep(2)
    #no next page exception
    except ElementNotVisibleException:   
            driver.quit()
    driver.quit()
    
    #get current date
    date =datetime.date.today()
    #save the data to csv
    df.to_csv('TutorOK_'+str(date)+'.csv',index=False, encoding='utf_8_sig')
    print('Data is successfully saved!')

#main function
get_data()