# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 16:39:36 2022

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
                                               'Address Type',
                                               'Address - Country'))

#Clean up:
#New column 'Party Name Cleanup', 'PartyNameDOB'
#Replace blank cells with 'None'
#Remove duplicates, sort
df['Inconsistency Type'] = "Same Name, DOB, Add Type;  Diff Address Country"
df['Party Name Cleanup'] = df['Party Name'].str.replace('\W','').str.lower()
df['PartyNameDOB'] = df['Date of Birth'].dt.strftime('%d%m%Y').astype(str) + df['Party Name Cleanup']
df['Address - Country'].fillna('None', inplace = True)
df = df.drop_duplicates().sort_values(['Party Name Cleanup', 'Party ID'])

#Filter by:
#Party Type == Natural Person and Address Type == Existing Residential Address
df_addc = df[(df['Party Type'] == 'Natural Person') & (df['Address Type'] == 'Existing Residential Address')]

#For every party, get a set of all the corresponding entries under 'Address - Country'
#Add to finaldf if there is more than 1 value
finaldf_addc = pd.DataFrame()
for name in df_addc["PartyNameDOB"]:
    tempdf = df_addc[df_addc['PartyNameDOB'] == name]
    setof_addresscountry = {country for country in tempdf['Address - Country'].unique()}
    if len(setof_addresscountry) == 1:
        continue
    else:
        finaldf_addc = finaldf_addc.append(df_addc[df_addc['PartyNameDOB'] == name])


#Cleanup final product and save as excel spreadsheet
if finaldf_addc.empty == False:
    finaldf_addc = finaldf_addc.drop(axis=1, columns=(['Party Name Cleanup', 'PartyNameDOB'])).drop_duplicates()
finaldf_addc.to_excel('15.xlsx', index=False)
print('Completed.')
