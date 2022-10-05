# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 18:20:56 2022

@author: u56313
"""
import pandas as pd
import warnings
warnings.simplefilter("ignore")

df = pd.read_excel('party_data.xlsx', usecols=('RM UID',
                                               'RM Name',
                                               'Party ID',
                                               'Party Name',
                                               'Party Type',
                                               'Date of Birth',
                                               'Place of Birth'))

#Clean up:
#New column 'Party Name Cleanup', 'PartyNameDOB'
#Replace blank cells with 'None'
#Remove duplicates, sort
df['Inconsistency Type'] = "Same Name, DOB; Diff Place of Birth"
df['Party Name Cleanup'] = df['Party Name'].str.replace('\W','').str.lower()
df['PartyNameDOB'] = df['Date of Birth'].dt.strftime('%d%m%Y').astype(str) + df['Party Name Cleanup']
df['Place of Birth'].fillna('None', inplace = True)
df = df.drop_duplicates().sort_values(['Party Name Cleanup', 'Party ID'])

#Filter by:
#Party Type == Natural Person
df_pob = df[(df['Party Type'] == 'Natural Person')]

#For every party, get a set of all the corresponding entries under 'Place of Birth'
#Add to finaldf if there is more than 1 value
finaldf_pob = pd.DataFrame()
for name in df_pob["PartyNameDOB"]:
    tempdf = df_pob[df_pob['PartyNameDOB'] == name]
    setof_placeofbirth = {place for place in tempdf['Place of Birth'].unique()}
    if len(setof_placeofbirth) == 1:
        continue
    else:
        finaldf_pob = finaldf_pob.append(df_pob[df_pob['PartyNameDOB'] == name])


#Cleanup final product and save as excel spreadsheet
if finaldf_pob.empty == False:
    finaldf_pob = finaldf_pob.drop(axis=1, columns=(['Party Name Cleanup', 'PartyNameDOB'])).drop_duplicates()
finaldf_pob.to_excel('14.xlsx', index=False)
print('Completed.')
