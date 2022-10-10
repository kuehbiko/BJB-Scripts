# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 19:40:22 2022

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
                                               'Vulnerable Client'))

#Clean up:
#New column 'Party Name Cleanup', 'PartyNameDOB'
#Replace blank cells with 'None'
#Remove duplicates, sort
df['Inconsistency Type'] = "Same Name, DOB; Diff VC status"
df['Party Name Cleanup'] = df['Party Name'].str.replace('\W','').str.lower()
df['PartyNameDOB'] = df['Date of Birth'].dt.strftime('%d%m%Y').astype(str) + df['Party Name Cleanup']
df['Vulnerable Client'].fillna('None', inplace = True)
df = df.drop_duplicates().sort_values(['Party Name Cleanup', 'Party ID'])

#Filter by:
#Party Type == Natural Person
df_vc = df[(df['Party Type'] == 'Natural Person')]

#For every party, get a set of all the corresponding entries under 'Vulnerable Client'
#Add to finaldf if there is more than 1 value
finaldf_vc = pd.DataFrame()
for name in df_vc["PartyNameDOB"]:
    tempdf = df_vc[df_vc['PartyNameDOB'] == name]
    setof_VCstatus = {status for status in tempdf['Vulnerable Client'].unique()}
    if len(setof_VCstatus) == 1:
        continue
    else:
        finaldf_vc = finaldf_vc.append(df_vc[df_vc['PartyNameDOB'] == name])


#Cleanup final product and save as excel spreadsheet
if finaldf_vc.empty == False:
    finaldf_vc = finaldf_vc.drop(axis=1, columns=(['Party Name Cleanup', 'PartyNameDOB'])).drop_duplicates()
finaldf_vc.to_excel('13.xlsx', index=False)
print('Completed.')
