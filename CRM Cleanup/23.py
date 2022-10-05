# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 16:23:08 2022

@author: u56313
"""

import pandas as pd
import datetime as dt
import warnings
warnings.simplefilter("ignore")


df = pd.read_excel('party_data.xlsx', usecols=('RM UID',
                                               'RM Name',
                                               'Party ID',
                                               'Party Name',
                                               'Party Type',
                                               'Date of Birth',
                                               'Identification Document Type',
                                               'Identification Document Expiry Date',
                                               'Identification Date of Issue'))

#Filter by:
#Party Type == Natural Person
#Identification Document Type == Declaration of Nationality
df = df[(df['Party Type'] == 'Natural Person') & (df['Identification Document Type'] == 'Declaration of Nationality')]

#Clean up:
#New column 'Party Name Cleanup', 'PartyNameDOB'
#Convert date to string
#Drop duplicates
df['Party Name Cleanup'] = df['Party Name'].str.replace('\W','').str.lower()
df['PartyNameDOB'] = df['Date of Birth'].astype(str) + df['Party Name Cleanup']
df['Identification Date of Issue'] = df['Identification Date of Issue'].dt.strftime('%d%m%Y')
df['Identification Document Expiry Date'] = df['Identification Document Expiry Date'].dt.strftime('%d%m%Y')
df.drop_duplicates()
    
#Identifying Missing Values:
#Missing Issue Date or Expiry Date
#Place them in a separate dataframe missing_values
#Remove rows in missing_values from original df
issue_missing = df[df['Identification Date of Issue'].isna()]
expiry_missing = df[df['Identification Document Expiry Date'].isna()]
missing_values = pd.concat([issue_missing, expiry_missing], ignore_index=True, axis=0).sort_values(by=['PartyNameDOB'])
df = df.dropna()

#Identifying Wrong Values:
df['Date Diff'] = df['Identification Document Expiry Date'].astype(int) - df['Identification Date of Issue'].astype(int)

#Cleanup and save to excel
df['Inconsistency Type'] = 'DON expiry - issue date = 2 years'
finaldf_don = pd.concat([missing_values, df[df['Date Diff'] != 2]], ignore_index=True, axis=0)
if finaldf_don.empty == False:
    finaldf_don = finaldf_don.sort_values(['Party Name Cleanup', 'Party ID']). \
                              drop(axis=1, columns=(['Party Name Cleanup','PartyNameDOB'])).drop_duplicates()
finaldf_don.to_excel('23.xlsx', index=False)
print('Completed.')
