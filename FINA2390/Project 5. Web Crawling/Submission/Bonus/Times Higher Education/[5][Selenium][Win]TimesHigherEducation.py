
# coding: utf-8

# In[19]:


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
END_PAGE = 1

#For file naming
PROJECT_ABBR = "times"
PROJECT_NAME = "Project 5"

#Base URL
#Note:
#the url below contain a parameter -1 that all records will be shown in one page thus it is not neccessary to turn to next page and so on.
URL = "https://www.timeshighereducation.com/world-university-rankings/2017/world-ranking#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/statss"

#Main window
driver =webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')
driver.get(URL)

df_columns = ['Ranking',
              'University Name',
              'Country',
              'No. of Students',
              'Source']

#Create new dataframe with a the fields above
df_etf = pd.DataFrame(columns=df_columns)
    
############################################################################################
#go_to_page
#This function is control the program to go to the start page
#The implementation is quite simple that we press a number of click of button 'next_page'
#As we have set all records in one page, it not necessarily for to use this function
############################################################################################
def go_to_page(page):
    if page != 1:
        print 'GOING TO PAGE' + str(page)
        driver.get('https://www.timeshighereducation.com/world-university-rankings/2017/world-ranking#!/page/'+str(page-1)+'/length/25/sort_by/rank/sort_order/asc/cols/statss')
        time.sleep(1)
        print 'ARRIVED PAGE' + str(page)
    else:
        return

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

#As we have set all records in one page, it not necessarily for to use this function
#Turn to next page
def next_page():
    #click next page
    driver.find_element_by_xpath('//*[@id="datatable-1_next"]/a').click()
    time.sleep(3)
    
############################################################################################
#Main
#This part is the main function of the program
############################################################################################
def main():
    #Ensure the page is completely load            
    time.sleep(2)
                
    #Go to the start page
    go_to_page(START_PAGE)
                
    #Ensure the page is loaded after going to the destination page
    time.sleep(2)
                
    print 'Start at PAGE'+ str(START_PAGE)
    
    #n in the row index for the dataframe
    n = 1
    
    #This is a loop to loop over every page of the website
    for CURRENT_PAGE in range(START_PAGE,END_PAGE+1):
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' START--------------------'
        START_TIMESTAMP = time.time()
        
        #As all the <td> are wrapped by <tr>, we can use a loop to get the <td> inside a <td>
        #loop over every row
        for row in driver.find_elements_by_xpath('//*[@id="datatable-1"]/tbody/tr'):
            #Extracting the fields ranking, university name, country and also no. of students
            df_etf.loc[n, 'Ranking']         = row.find_element_by_xpath('td[1]/center').text
            df_etf.loc[n, 'University Name'] = row.find_element_by_xpath('td[2]/a').text
            df_etf.loc[n, 'Country']         = row.find_element_by_xpath('td[2]/div/span').text
            df_etf.loc[n, 'No. of Students'] = row.find_element_by_xpath('td[3]').text
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



# In[ ]:






