##Importing pickle, reading in and unpickling file

import pickle

filename = "./data/ids.pickle"
infile = open(filename,'rb')
new_dict = pickle.load(infile)
infile.close()

##Transforming IDs to strings, this way 0 can be added to beginning
##If an ID is only 13 characters long, that means the 0 was cut off from the beginning
##Therefore if an ID is only 13 characters, I add a 0 to the beginning
##This way I obtain correct IDs

for n in new_dict:
    n = str(n)
    if len(n) == 13:
        n = "0" + n
        
##Creating an empty list for county codes
##Through a for loop, I add the 3rd and 4th digits from every code to the list
##I obtain a list of the county codes

counties = []
for m in new_dict:
    counties.append(m[2:4])
    
##Importing the Pandas package in order to use data frames sufficiently

import pandas as pd

##Loading the translation table for further use

trans = pd.read_csv('./data/id-to-county.csv')

##My next task is to change the county codes in the translation table to strings
##Furthermore add 0 to beginning when necessary
##In the next for loop I obtain the county codes necessary for the correct translation table

codes = []
for i in range(1,21):
    i = str(i)
    if len(i)==1:
        i = "0" + i
    if i=="20":
        i = "00"
    codes.append(i)
    
##Changing the Sorszám column in the translation table to the correct county codes

trans['Sorszám'] = codes

##The next task is to count how many IDs belong to each county
##I do this by sorting county codes into an increasing order
##To facilitate calculations I import groupby from Itertools package
##Then I grouped the county codes accordingly (same county codes in one group)
##Then I summed how many counties are in each group
##Then I added an "IDs per county" column to the data frame for further use

counties.sort()

from itertools import groupby

num_codes = [len(list(j)) for i, j in groupby(counties)]

trans['IDs per County'] = num_codes

##In our final table we only need the names of the counties, not the registry court
##Therefore, I split the "Bíróság" names to before and after the colon
##I only kept the half with the county name (first half) and added a new column "County" to the data frame for further use

names = []
for i in range(0,20):
    names.append(trans['Bíróság'][i].split(":")[0])

trans['County'] = names

##Making a new data frame with only 2 columns, the county name and the number of IDs per county

id_count_by_county = trans[['County','IDs per County']]

##Exporting results to a .csv file in data folder:

id_count_by_county.to_csv('./data/id-count-by-county')
