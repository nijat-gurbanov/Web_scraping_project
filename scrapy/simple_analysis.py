#####################################################################################
#####################     Web scraping using     ####################################
######################     Scrapy (part 3)     ######################################
#####################################################################################

# Simple data analysis
import pandas as pd
from statistics import mean, mode

# Preparing data for simple analysis
player_table = pd.read_csv(r'Project/Project_Scrapy/players.csv')
player_table = player_table[['name', 'curr_team', 'age', 'national', 'height', 'weight']]
player_table.rename(columns = 
{'name':'Name', 
'curr_team':'Current Team',
'age':'Age',
'national':'Nationality',
'height':'Height (in cm)',
'weight':'Weight (in kg)'}, inplace = True)

# Simple analysis
print("Simple data analysis")
print("Average age:", mean(player_table["Age"]))
print("Average height:", mean(player_table["Height (in cm)"]), "cm")
print("Average weight:", mean(player_table["Weight (in kg)"]), "kg")
print("The team with most strongest players is", mode(player_table["Current Team"]))

print(player_table)