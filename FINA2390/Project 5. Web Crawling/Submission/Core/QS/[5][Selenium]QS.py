
# coding: utf-8

# In[8]:


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
START_PAGE = 38
END_PAGE = 39
PROJECT_ABBR = "QS"
PROJECT_NAME = "Project 5"
URL = "https://www.topuniversities.com/university-rankings/world-university-rankings/2018"

#Main window
driver =webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')
driver.get(URL)

#Secondary window
driver2 = webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')

df_columns = ['Ranking',
              'University Name',
              'Country',
              'Source',
              'No. of Students',
              'Public/Private University',
              'Focus']

df_etf = pd.DataFrame(columns=df_columns)
df_links = pd.DataFrame(columns=['link'])

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
        for i in range(page-1):
            next_page()
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
        
def next_page():
    #click next page
    driver.find_element_by_xpath('//*[@id="qs-rankings_next"]').click()
    time.sleep(2)
    
def dig(link, row_index):
    #open a new window
    #driver2 = webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')
    driver2.get(link.get_attribute('href'))
    time.sleep(2)
    try:    
        element = WebDriverWait(driver2, 10).until(           
            text_appear((By.XPATH, '//*[@id="uni-info"]/li[3]/div/h4/span'), (By.XPATH, '//*[@id="uni-info"]/li[5]/div/h4/span'),(By.XPATH, '//*[@id="uni-info"]/li[1]/h4/span')))
    except TimeoutException as ex:
        return False
    except StaleElementReferenceException as sx:
        return False
    finally:
        #find fields on the new driver
        time.sleep(1)
        if len(driver2.find_elements_by_xpath('//*[@id="uni-info"]/li[1]/h4/span')) != 0:
            df_etf.loc[row_index, 'No. of Students'] = driver2.find_element_by_xpath('//*[@id="uni-info"]/li[1]/h4/span').text
        if len(driver2.find_elements_by_xpath('//*[@id="uni-info"]/li[3]/div/h4/span')) != 0:
            df_etf.loc[row_index, 'Public/Private University'] = driver2.find_element_by_xpath('//*[@id="uni-info"]/li[3]/div/h4/span').text
        if len(driver2.find_elements_by_xpath('//*[@id="uni-info"]/li[5]/div/h4/span')) != 0:    
            df_etf.loc[row_index, 'Focus'] = driver2.find_element_by_xpath('//*[@id="uni-info"]/li[5]/div/h4/span').text
    
    #close the driver
    #driver2.close()

############################################################################################
#Main
#This part is the main function of the program
############################################################################################
def main():
    time.sleep(5)
    go_to_page(START_PAGE)
    time.sleep(1)
    print 'Start at PAGE'+ str(START_PAGE)
    
    n = 1
    for CURRENT_PAGE in range(START_PAGE,END_PAGE+1):
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' START--------------------'
        START_TIMESTAMP = time.time()
        for row in driver.find_elements_by_xpath('//*[@id="qs-rankings"]/tbody/tr'):
            df_etf.loc[n, 'Ranking']         = row.find_element_by_xpath('td[1]/div/div/span[2]').text
            df_etf.loc[n, 'University Name'] = row.find_element_by_xpath('td[2]/div/a').text
            df_etf.loc[n, 'Country']         = row.find_element_by_xpath('td[3]/div/img').get_attribute('alt')
            
            link = row.find_element_by_xpath('td[2]/div/a')
            #open the page to get other fields
            dig(link, n)
            print '--------------------ROW ' + str(n)+ ' FINISHED--------------------'
            n = n + 1
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' FINISH--------------------'
        END_TIMESTAMP = time.time()
        print '-TIME USED:' + str(START_TIMESTAMP-END_TIMESTAMP) + '-'
        
        #store every first page to CSV for backup purpose
        save_file('backup', CURRENT_PAGE)
            
        #turn to next page
        next_page()  
    #set Source as QS for every row as this is crawl from QS
    df_etf['Source'] = PROJECT_ABBR
    
    #export the file to CSV
    save_file('all', CURRENT_PAGE)
    
    #close the driver
    driver.quit()
if __name__ == "__main__":
    main()



# In[15]:







# In[32]:





# In[9]:


df_links

