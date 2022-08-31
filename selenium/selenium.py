#####################################################################################
#####################     Web scraping using     ####################################
##########################     Selenium     #########################################
#####################################################################################

###  Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as BS
import pandas as pd
import re
from statistics import mean, mode

# Hide the warning of append method
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Storing start time to calculate the running time later
total_start_time = time.time()

# Creating a boolean variable for limiting the scraped pages to 100
minrequirement = bool(True)

###  Scraping player information
URL = "https://basketball.realgm.com/nba/stats"

# Start the Driver
driver = webdriver.Firefox()

# Hit the url of web site
driver.get(URL)

# Creating a table for storing player information
player_table = pd.DataFrame({'Name':[], 'Current Team':[], 'Age':[], 'Nationality':[], 'Height (in cm)':[], 'Weight (in kg)':[]})

scraped_pages = 0

for i in range(100):
    # Going to the profile of a player
    try:
        driver.find_elements(by = By.XPATH, value = "//tbody/tr/td/a[starts-with(@href, '/player')]")[i].click()
    except:
        pass

    time.sleep(3)

    # Click "Agree" button to continue
    try:
        driver.find_element(by = By.XPATH, value = "//button[starts-with(@title,'Scroll to the')]").click()
    except:
        pass
    
    # Extracting html of the website
    bs = BS(driver.page_source, 'html.parser')

    # Extracting player information
    try:
        name = bs.find('div', {'class': 'profile-box'}).find('h2').next_element.replace('\xa0','')
    except:
        name = ''
    
    try:
        curr_team = bs.find(text='Current Team:').findNext('a').text
    except:
        curr_team = ''

    try:
        age = bs.find(text='Born:').findNext('a').next_element.next_element[2:4]
    except:
        age = ''

    try:
        national = bs.find(text='Nationality:').findNext('a').text
    except:
        national = ''

    try:
        height = bs.find(text='Height:').parent.next_sibling
        height = re.findall(r'\((.*?)\)', height)[0].replace('cm','')
    except:
        height = ''

    try:
        weight = bs.find(text='Weight:').parent.next_sibling
        weight = re.findall(r'\((.*?)\)', weight)[0].replace('kg','')
    except:
        weight = ''

    # Storing information in a dictionary for appending it to the table later
    player = {'Name':name, 'Current Team':curr_team, 'Age':int(age), 'Nationality':national, 
    'Height (in cm)':int(height), 'Weight (in kg)':int(weight)}

    # Appending each players' information to "player_table" table
    player_table = player_table.append(player, ignore_index = True)
    
    # Going back to main page
    driver.back()
    time.sleep(2)

    scraped_pages += 1

    # Checking minrequirement for limiting the number of sraped pages to 100
    if minrequirement == True:
        if scraped_pages == 100:
            break
        else:
            pass
    else:
        pass

driver.close()
total_end_time = time.time()

# Printing the table and number of pages scraped
print(player_table)
print("Number of pages scraped is:", scraped_pages)

# Analyzing the performance
print("Analyzing the performance of the scraper")
print("Total time spent for running the whole program is %.2f seconds" % (total_end_time - total_start_time))

###  Simple data analysis
print("Simple data analysis")
print("Average age:", mean(player_table["Age"]))
print("Average height:", mean(player_table["Height (in cm)"]), "cm")
print("Average weight:", mean(player_table["Weight (in kg)"]), "kg")
print("The team with most strongest players is", mode(player_table["Current Team"]))
