
# coding: utf-8

# In[13]:


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
START_PAGE = 1
END_PAGE = 11

#For file naming
PROJECT_ABBR = "webmetrics"
PROJECT_NAME = "Project 5"

#Base URL
#Directly load start page
if START_PAGE != 1:
    URL = 'http://www.webometrics.info/en/world?page='+str(START_PAGE)
else:
    URL = 'http://www.webometrics.info/en/world'

#Main window
driver =webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')
driver.get(URL)

df_columns = ['Ranking',
              'University Name',
              'Country',
              'Source']

#Create new dataframe with a the fields above
df_etf = pd.DataFrame(columns=df_columns)

def get_country(href):
    #This part of the programme show how to get the country from the image href
    #This website doenst not provide the text description of the country image href with country abbr
    #e.g. http://www.webometrics.info/sites/default/files/logos/ca.png
    #it is obvious that 'ca' in 'ca.jpg' is the country name Canda
    
    #use the split function to seperate different part of the string by delimter '/'
    string = href.split('/')
    
    #string[-1] will refer to the last element of the array (ca.png)
    #we split ca.png again and use sub_string[0] to get 'ca'
    sub_string = string[-1].split('.')
    
    #return CA back to the main function
    return sub_string[0].upper()
    
############################################################################################
#save_file
#This function is to save the file, where the file will be named different according to different state
############################################################################################
def save_file(state, CURRENT_PAGE):
    if state == 'backup':
        filename = '['+ PROJECT_ABBR +'][Intrim Backup][' + str(CURRENT_PAGE) + ']' + PROJECT_NAME + ' PAGE ' + str(START_PAGE) + ' to PAGE ' + str(CURRENT_PAGE) + ' Records.csv'
        df_etf.to_csv(filename, index=False,  encoding='utf-8')
        print '[Intrim Backup]Saved First '+ str(CURRENT_PAGE) + 'Pages Records to CSV'
    elif state == 'all':
        filename = '['+ PROJECT_ABBR +']'+ PROJECT_NAME +' PAGE ' + str(START_PAGE) + 'to PAGE ' + str(END_PAGE) + 'Records.csv'
        df_etf.to_csv(filename, index=False, encoding='utf-8')
        print 'Exported to csv'

#Turn to next page
def next_page():
    #click next page
    if START_PAGE == 1:
        driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/ul/li[11]/a').click()
    else:
        driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/ul/li[13]/a').click()
        
    time.sleep(2)
    
############################################################################################
#Main
#This part is the main function of the program
############################################################################################
def main():
    #Ensure the page is completely load            
    time.sleep(2)
                
    print 'Start at PAGE'+ str(START_PAGE)
    
    #n in the row index for the dataframe
    n = 1
    
    #This is a loop to loop over every page of the website
    for CURRENT_PAGE in range(START_PAGE,END_PAGE+1):
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' START--------------------'
        START_TIMESTAMP = time.time()
        
        #As all the <td> are wrapped by <tr>, we can use a loop to get the <td> inside a <td>
        for row in driver.find_elements_by_xpath('//*[@id="block-system-main"]/div/table[2]/tbody/tr'):
            #Extracting the fields ranking, university name, country
            df_etf.loc[n, 'Ranking']         = row.find_element_by_xpath('td[1]').text
            df_etf.loc[n, 'University Name'] = row.find_element_by_xpath('td[2]/a').text
            df_etf.loc[n, 'Country']         = get_country(row.find_element_by_xpath('td[4]/center/img').get_attribute('src'))

            n = n + 1
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' FINISH--------------------'
        END_TIMESTAMP = time.time()
        
        #Print the time used for each page so as to estimate the remaining time of the program
        print '-TIME USED:' + str(START_TIMESTAMP-END_TIMESTAMP) + '-'
        
        #store every first 5,10,15... pages to CSV for backup purpose
        if(CURRENT_PAGE % 10) == 0:
            save_file('backup', CURRENT_PAGE)
                
        #turn to next page(Not necessarily to use in this crawler)
        next_page()
        
    #set Source as Times for every row as this is crawler for QS
    df_etf['Source'] = PROJECT_ABBR
    
    #export the file to CSV
    save_file('all', CURRENT_PAGE)
    
    #close the driver after the program finished
    driver.quit()

############################################################################################
#This part is of the code is to tell the program to start function main() when it launches
############################################################################################
if __name__ == "__main__":
    main()



# In[14]:


df_etf


