#####################################################################################
#####################     Web scraping using     ####################################
#######################     Beautiful soap     ######################################
#####################################################################################

###  Importing necessary libraries
import re
from urllib import request
from bs4 import BeautifulSoup as BS
from numpy import integer
import pandas as pd
from statistics import mean, mode
import time

# Hide the warning of append method
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Storing start time to calculate the running time later
total_start_time = time.time()

# Creating a boolean variable for limiting the scraped pages to 100
minrequirement = bool(True)

###  Getting the links for the profile of each basketball player
url = 'https://basketball.realgm.com/nba/stats' 
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

# Information about the players are inside the table.
tags = bs.find('tbody').find_all('tr')
# We are creating the real links for the profile of each player
links = ['https://basketball.realgm.com' + tag.a['href'] for tag in tags]

# Adding links to the list
player_links = []
player_links.extend(links)

###  Scraping player information
# Creating a table for storing player information
player_table = pd.DataFrame({'Name':[], 'Current Team':[], 'Age':[], 'Nationality':[], 'Height (in cm)':[], 'Weight (in kg)':[]})

scraped_pages = 0

# Storing start time of player information extraction to calculate the running time later
player_start_time = time.time()

# Extracting player information
for link in player_links:
    url = link 
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')

    name = bs.find('div', {'class': 'profile-box'}).find('h2').next_element.replace('\xa0','')
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
    scraped_pages += 1

    # Checking minrequirement for limiting the number of sraped pages to 100
    if minrequirement == True:
        if scraped_pages == 100:
            break
        else:
            pass
    else:
        pass

total_end_time = time.time()

# Printing the table and number of pages scraped
print(player_table)
print("Number of pages scraped is:", scraped_pages)

# Analyzing the performance
print("Analyzing the performance of the scraper")
print("Total time spent for running the whole program is %.2f seconds" % (total_end_time - total_start_time))
print("Total time spent for running the main part of the program is %.2f seconds" % (total_end_time - player_start_time))

###  Simple data analysis
print("Simple data analysis")
print("Average age:", mean(player_table["Age"]))
print("Average height:", mean(player_table["Height (in cm)"]), "cm")
print("Average weight:", mean(player_table["Weight (in kg)"]), "kg")
print("The team with most strongest players is", mode(player_table["Current Team"]))