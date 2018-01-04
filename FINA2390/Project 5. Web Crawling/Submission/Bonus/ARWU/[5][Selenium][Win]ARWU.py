
# coding: utf-8

# In[14]:


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

#there are two tabs for the website, first tab is page 1 and second tab is page 2
START_PAGE = 1
END_PAGE = 2

#For file naming
PROJECT_ABBR = "arwu"
PROJECT_NAME = "Project 5"

#Base URL
URL = "http://www.shanghairanking.com/ARWU2017.html"

#Main window
driver =webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')
driver.get(URL)

driver2 = webdriver.Firefox(executable_path=r'D:\git\FINA2390-Programs\geckodriver.exe')
df_columns = ['Ranking',
              'University Name',
              'Country',
              'Website',
              'Address',
              'Year of foundation',
              'Source']

#Create new dataframe with a the fields above
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
    
############################################################################################
#save_file
#This function is to save the file, where the file will be named different according to different state
############################################################################################
def save_file(state, CURRENT_PAGE):
    if state == 'backup':
        filename = '['+ PROJECT_ABBR +'][Intrim Backup][' + str(CURRENT_PAGE) + ']' + PROJECT_NAME + ' PAGE ' + str(START_PAGE) + ' to PAGE ' + str(CURRENT_PAGE) + ' Records.csv'
        df_etf.to_csv(filename, index=False,  encoding='utf-8')
        print '[Intrim Backup]Saved First '+ str(CURRENT_PAGE) + 'Records to CSV'
    elif state == 'all':
        filename = '['+ PROJECT_ABBR +']'+ PROJECT_NAME +' PAGE ' + str(START_PAGE) + 'to PAGE ' + str(END_PAGE) + 'Records.csv'
        df_etf.to_csv(filename, index=False, encoding='utf-8')
        print 'Exported to csv'

############################################################################################
#get_country
#get country name from the image href
############################################################################################
def get_country(href):
    #This part of the programme show how to get the country from the image href
    #This website doenst not provide the text description of the country image href with country abbr
    #e.g. image/flag/USA.png
    #it is obvious that 'USA' in 'USA.png' is the country name USA
    
    #use the split function to seperate different part of the string by delimter '/'
    string = href.split('/')
    
    #string[-1] will refer to the last element of the array (USA.png)
    #we split USA.png again and use sub_string[0] to get 'USA'
    sub_string = string[-1].split('.')
    
    #return USA back to the main function
    return sub_string[0]

############################################################################################
#next_tab
#turn to next tab
############################################################################################
def next_tab():
    #swtich to next tab to crawl the university from 501 to 800
    driver.get('http://www.shanghairanking.com/ARWU2017Candidates.html')

############################################################################################
#dig
#open another window to get the fields inside the university profile
############################################################################################
def dig(link, row_index):
    #open a new window   
    driver2.get(link.get_attribute('href'))
    time.sleep(2)
    
    #xpath for the fields to be extracted
    xyear_of_foundation = '//*[@id="tab1"]/table/tbody/tr[4]/td[2]' #Year of foundation
    xaddress = '//*[@id="tab1"]/table/tbody/tr[5]/td[2]' #Address
    xwebsite = '//*[@id="tab1"]/table/tbody/tr[6]/td[2]/a' #Website
    
    try:    
        element = WebDriverWait(driver2, 5).until(           
            text_appear((By.XPATH, xyear_of_foundation), (By.XPATH, xaddress),(By.XPATH, xwebsite)))
    except TimeoutException as ex:
        return False
    except StaleElementReferenceException as sx:
        return False
    finally:
        #find fields on the new driver
        time.sleep(1)
        
        #get the fields
        if len(driver2.find_elements_by_xpath(xyear_of_foundation)) != 0:
            df_etf.loc[row_index, 'Year of foundation'] = driver2.find_element_by_xpath(xyear_of_foundation).text
        if len(driver2.find_elements_by_xpath(xwebsite)) != 0:
            df_etf.loc[row_index, 'Website'] = driver2.find_element_by_xpath(xwebsite).text
        if len(driver2.find_elements_by_xpath(xaddress)) != 0:    
            df_etf.loc[row_index, 'Address'] = driver2.find_element_by_xpath(xaddress).text

############################################################################################
#Main
#This part is the main function of the program
############################################################################################
def main():
    #Ensure the page is completely load            
    time.sleep(2)
    
    if(START_PAGE == 2):
        next_tab()
    
    print 'Start at PAGE'+ str(START_PAGE)
    
    #n in the row index for the dataframe
    n = 1
    
    #This is a loop to loop over every page of the website
    for CURRENT_PAGE in range(START_PAGE,END_PAGE+1):
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' START--------------------'
        START_TIMESTAMP = time.time()
        
        #As all the <td> are wrapped by <tr>, we can use a loop to get the <td> inside a <td>
        #loop over each record
        for row in driver.find_elements_by_xpath('//*[@id="UniversityRanking"]/tbody/tr')[1:]:
            #Extracting the fields ranking, university name, country
            df_etf.loc[n, 'Ranking']         = row.find_element_by_xpath('td[1]').text
            
            #The layout on two tab of the website are different, from record 1 to 500, there is a hyperlink for each univeristy name. That's why we need to find td[2]/a for tab 1 and td[2] only for tab 2
            if(START_PAGE == 1): #if it starts on tab 1
                df_etf.loc[n, 'University Name'] = row.find_element_by_xpath('td[2]/a').text
                df_etf.loc[n, 'Country']         = get_country(row.find_element_by_xpath('td[3]/a/img').get_attribute('src'))
                
                 #open the page to get other fields that are not listed on the table
                 #Remarks: this website doesnt provide university profile for the universities in tab 2
                link = row.find_element_by_xpath('td[2]/a')
                dig(link, n)
                
            else: #if it starts on tab 2
                df_etf.loc[n, 'University Name'] = row.find_element_by_xpath('td[2]').text
                df_etf.loc[n, 'Country']         = get_country(row.find_element_by_xpath('td[3]/img').get_attribute('src'))
                     
            print '--------------------ROW ' + str(n)+ ' FINISHED--------------------'
            n = n + 1
            
        #Backup each page
        save_file('backup', n)
            
        print '--------------------PAGE ' + str(CURRENT_PAGE) +' FINISH--------------------'
        END_TIMESTAMP = time.time()
        
        #Print the time used for each page so as to estimate the remaining time of the program
        print '-TIME USED:' + str(START_TIMESTAMP-END_TIMESTAMP) + '-'
        
        if(START_PAGE != 2):
            #swtich to next tab
            next_tab()
        
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






