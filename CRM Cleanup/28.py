# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 18:22:19 2022

@author: u56313
"""

import pandas as pd
import warnings
warnings.simplefilter("ignore")

df = pd.read_excel('party_data.xlsx', usecols=('Party RM UID',
                                               'Party RM Name',
                                               'Party Type',
                                               'Party ID'))

#Clean up:
#New column 'Party Name Cleanup', 'PartyNameDOB'
#Replace blank cells with 'None'
#Remove duplicates, sort
df['Inconsistency Type'] = "Party ID tagged to multiple Party RMs"
df = df.drop_duplicates().sort_values(['Party ID'])

#Filter by:
#Party Type == Natural Person and Address Type == Existing Residential Address
df_28 = df[(df['Party Type'] == 'Natural Person')]

#For every party, get a set of all the corresponding entries under 'Address - Country'
#Add to finaldf if there is more than 1 value
finaldf_28 = pd.DataFrame()
for partyID in df_28["Party ID"]:
    tempdf = df_28[df_28['Party ID'] == partyID]
    setof_partyRMs = {RM for RM in tempdf['RM UID'].unique()}
    if len(setof_partyRMs) == 1:
        continue
    else:
        finaldf_28 = finaldf_28.append(df_28[df_28['Party ID'] == partyID])


#Cleanup final product and save as excel spreadsheet
if finaldf_28.empty == False:
    finaldf_28 = finaldf_28.drop_duplicates()
finaldf_28.to_excel('28.xlsx', index=False)
print('Completed.')
