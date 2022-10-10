# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 19:16:57 2022

@author: u56313
"""
import pandas as pd
import warnings
warnings.simplefilter("ignore")

df = pd.read_excel('party_data.xlsx', usecols=('Party RM UID',
                                               'Party RM Name',
                                               'Party ID',
                                               'Party Name',
                                               'Party Type',
                                               'Date of Birth',
                                               'Identification Document Type',
                                               'Identification Document Issue Country'))

#Clean up:
#New column 'Party Name Cleanup', 'PartyNameDOB'

df['Party Name Cleanup'] = df['Party Name'].str.replace('\W','').str.lower()
df['PartyNameDOB'] = df['Date of Birth'].dt.strftime('%d%m%Y').astype(str) + df['Party Name Cleanup']



#Filter by:
#Party Type == Natural Person
df_26 = df[(df['Party Type'] == 'Natural Person')]

#Find cases:
#Case 1: Type = Blank; Country != Blank
#Case 2: Type != Blank; Country = Blank
finaldf_26 = df[(df['Identification Document Type'].isnull()) & (df['Identification Document Issue Country'].notnull()) |
                (df['Identification Document Type'].notnull()) & (df['Identification Document Issue Country'].isnull())]

#Cleanup final product and save as excel spreadsheet
finaldf_26['Inconsistency Type'] = "ID Doc Issue Country/Type is Blank"
if finaldf_26.empty == False:
    finaldf_26 = finaldf_26.sort_values(['Party Name Cleanup', 'Inconsistency Type', 'Party ID']). \
                      drop(axis=1, columns=(['Party Name Cleanup', 'PartyNameDOB'])).drop_duplicates()
finaldf_26.to_excel('26.xlsx', index=False)
print('Completed.')
