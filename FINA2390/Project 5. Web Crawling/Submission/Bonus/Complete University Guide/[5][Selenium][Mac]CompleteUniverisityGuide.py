
# coding: utf-8

# In[17]:


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

#As there only one page for this ranking, we can simply set both start page and end page to 1
START_PAGE = 1
END_PAGE = 1

#For file naming
PROJECT_ABBR = "CompleteUniverisityGuide"
PROJECT_NAME = "Project 5"

#Base URL
URL = "https://www.thecompleteuniversityguide.co.uk/league-tables/rankings"

#Main window
driver = webdriver.Firefox()
driver.get(URL)

#Secondar Window
driver2 = webdriver.Firefox()

df_columns = ['Ranking',
              'University Name',
              'Country',
              'Source']

#Create new dataframe with a the fields above
df_etf = pd.DataFrame(columns=df_columns)

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
        for row in driver.find_elements_by_xpath('//*[@id="top"]/div[2]/div[6]/div/div[1]/table/tbody/tr[contains(@class, "expandable")]'):     
            #Extracting the fields ranking, university name, country and also no. of students
            df_etf.loc[n, 'Ranking']         = row.find_element_by_xpath('td[2]').text
            df_etf.loc[n, 'University Name'] = row.find_element_by_xpath('td[4]/a').text
            
            link = row.find_element_by_xpath('td[4]/a')
            
            n = n + 1
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' FINISH--------------------'
        END_TIMESTAMP = time.time()
        
        #Print the time used for each page so as to estimate the remaining time of the program
        print '-TIME USED:' + str(START_TIMESTAMP-END_TIMESTAMP) + '-'
        
    #set Source 
    df_etf['Source'] = PROJECT_ABBR
    
    #set Country as UK as this ranking is merely about university in UK
    df_etf['Country'] = 'UK'
    
    #export the file to CSV
    save_file('all', CURRENT_PAGE)
    
    #close the driver after the program finished
    driver.quit()

############################################################################################
#This part is of the code is to tell the program to start function main() when it launches
############################################################################################
if __name__ == "__main__":
    main()



# In[18]:



df_etf


