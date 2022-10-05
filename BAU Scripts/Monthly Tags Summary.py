# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:23:53 2022

@author: u56313
"""

import re
import pandas as pd
import warnings
warnings.simplefilter("ignore")

#Inputs
inp = input("File location: ") #Please include the file name in your path
inp2 = int(input("Find the top X number of tags. (Enter 0 to see all tags.) X = "))

df = pd.read_excel(f"{inp}.xlsx", usecols=["Last Remark"])

df["new"] = df["Last Remark"].str.replace(' ','').str.upper() #remove all spaces

#set variables to be used later:
sgtag = re.compile('SGTAG-.....') #wildcard regex search for SGTAG-00xxx
last_remark = df["new"].to_numpy().flatten().tolist() #Last Remark column flattened into a list. 1 element per row.

#Find all instances of "SGTAG-xxxxx" in each row
temp_list = []
for i in last_remark:
    temp_list.append(re.findall(sgtag, i))

#Flatten list of tags
#Sort list and calculate count, % frequency of tags
all_tags = [item for sublist in temp_list for item in sublist]
top_tags = sorted([[j, all_tags.count(j), round(100*all_tags.count(j)/len(all_tags), 2)] for j in set(all_tags)], key = lambda x: x[1], reverse=True)
if inp2 == 0: inp2 = len(all_tags)
top_tags_var = sorted(top_tags, key = lambda x: x[1], reverse=True)[0:inp2]

#Output:
for k in top_tags_var:
    print(f"{k[0]} - Count: {k[1]}, {k[2]}%")
print(f"The top 3 tags are {top_tags[0][0]} ({top_tags[0][2]}%); {top_tags[1][0]} ({top_tags[1][2]}%); {top_tags[2][0]} ({top_tags[2][2]}%)")
print(f"Total number of tags: {len(all_tags)}")
