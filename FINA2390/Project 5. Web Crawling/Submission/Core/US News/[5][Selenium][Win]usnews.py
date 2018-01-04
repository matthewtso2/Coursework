
# coding: utf-8

# In[3]:


import csv
import pandas as pd
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

############################################################################################
#Initial variables
#This part of the code is used to set the inital parameters for the web crawler
############################################################################################
START_PAGE = 51
END_PAGE = 125
PROJECT_ABBR = "usnews"
PROJECT_NAME = "Project 5"
URL = "https://www.usnews.com/education/best-global-universities/rankings"

#Main window
driver =webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')
driver.get(URL)

#Secondary window
driver2 = webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')

df_columns = ['Ranking',
              'University Name',
              'Country',
              'Address',
              'Website',
              'No. of Students',
              'Source']

df_etf = pd.DataFrame(columns=df_columns)

############################################################################################
#Class
#This particular class to define the conditions for explict wait
#The condition states that the crawler will jump to next page if and only if the webpage can find the text presented
############################################################################################
class text_appear(object):
  def __init__(self, locator1, locator2, locator3):
    self.locator1 = locator1
    self.locator2 = locator2
    self.locator3 = locator3

  def __call__(self, driver):
    element1 = driver.find_element(*self.locator1) 
    element2 = driver.find_element(*self.locator2)
    element3 = driver.find_element(*self.locator3)
    if len(element1.text) != 0 and len(element2.text) !=0 and len(element3.text) !=0:
        return True
    else:
        return False

def go_to_page(page):
    if page != 1:
        print 'GOING TO PAGE' + str(page)
        driver.get('https://www.usnews.com/education/best-global-universities/rankings?page='+str(page))
        print 'ARRIVED PAGE' + str(page)
    else:
        return

def save_file(state, CURRENT_PAGE):
    if state == 'backup':
        filename = '['+ PROJECT_ABBR +'][Intrim Backup][' + str(CURRENT_PAGE) + ']' + PROJECT_NAME + ' PAGE ' + str(START_PAGE) + ' to PAGE ' + str(CURRENT_PAGE) + ' Records.csv'
        df_etf.to_csv(filename, index=False,  encoding='utf-8')
        print '[Intrim Backup]Saved First '+ str(CURRENT_PAGE) + 'Pages Records to CSV'
    elif state == 'all':
        filename = '['+ PROJECT_ABBR +']'+ PROJECT_NAME +' PAGE ' + str(START_PAGE) + 'to PAGE ' + str(END_PAGE) + 'Records.csv'
        df_etf.to_csv(filename, index=False, encoding='utf-8')
        print 'Exported to csv'
        
    
def dig(link, row_index):
    
    #Open a new window
    driver2.get(link.get_attribute('href'))
    time.sleep(1)
    try:    
        element = WebDriverWait(driver2, 5).until(           
            text_appear((By.XPATH, '//*[@id="directoryPageSection-institution-data"]/div[1]/div[1]'), (By.XPATH, '//*[@id="content"]/div[3]/div[1]/div[1]/div[4]/div[2]/a'),(By.XPATH, '//*[@id="content"]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]')))
    except TimeoutException as ex:
        return False
    except StaleElementReferenceException as sx:
        return False
    finally:
        #find fields on the new driver
        time.sleep(1)
        if len(driver2.find_elements_by_xpath('//*[@id="directoryPageSection-institution-data"]/div[1]/div[1]')) != 0:
            df_etf.loc[row_index, 'No. of Students'] = driver2.find_element_by_xpath('//*[@id="directoryPageSection-institution-data"]/div[1]/div[1]').text
        if len(driver2.find_elements_by_xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[4]/div[2]/a')) != 0:
            df_etf.loc[row_index, 'Website']         = driver2.find_element_by_xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[4]/div[2]/a').text
        if len(driver2.find_elements_by_xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]')) != 0:    
            df_etf.loc[row_index, 'Address']         = driver2.find_element_by_xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]').text
############################################################################################
#Main
#This part is the main function of the program
############################################################################################
def main():
    time.sleep(2)
    
    go_to_page(START_PAGE)
    time.sleep(1)
    print 'Start at PAGE'+ str(START_PAGE)
    
    n = 1
    for CURRENT_PAGE in range(START_PAGE,END_PAGE+1):
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' START--------------------'
        START_TIMESTAMP = time.time()
        for row in driver.find_elements_by_xpath('//*[@id="resultsMain"]/div[1]/div'):
            df_etf.loc[n, 'Ranking']         = row.find_element_by_xpath('div[2]/span').text
            df_etf.loc[n, 'University Name'] = row.find_element_by_xpath('div[3]/h2/a').text
            df_etf.loc[n, 'Country']         = row.find_element_by_xpath('div[3]/div/span[1]').text
            link = row.find_element_by_xpath('div[3]/h2/a')
            
            #open the univesity profile to get other fields
            dig(link, n)
            print '--------------------ROW ' + str(n)+ ' FINISHED--------------------'
            n = n + 1
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' FINISH--------------------'
        END_TIMESTAMP = time.time()
        print '-TIME USED:' + str(START_TIMESTAMP-END_TIMESTAMP) + '-'
        
        #store every first 5,10,15... pages to CSV for backup purpose
        if(CURRENT_PAGE % 5) == 0:
            save_file('backup', CURRENT_PAGE)
            
        go_to_page(CURRENT_PAGE + 1)
        
    #set Source as QS for every row as this is crawl from QS
    df_etf['Source'] = PROJECT_ABBR
    
    #export the file to CSV
    save_file('all', CURRENT_PAGE)
    
    #close the driver
    driver.quit()
if __name__ == "__main__":
    main()



# In[33]:


df_etf

