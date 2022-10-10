# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:55:52 2022

@author: u56313
"""

import pandas as pd
import warnings
warnings.simplefilter("ignore")

df = pd.read_excel('party_data.xlsx', usecols=('Party ID',
                                               'Party Type',
                                               'Relationship (Party Role)',
                                               'Portfolio RM UID',
                                               'Portfolio RM Name',
                                               'Party RM UID',
                                               'Party RM Name'))

#Clean up:
df['Inconsistency Type'] = "Party ID tagged to 2 portfolio RMs (Party Role = AH & BO only)"


#Filter by:
#Party Type == Natural Person
#Party Role == Account Holder or Beneficial Owner
df_27 = df[(df['Party Type'] == 'Natural Person') & (
       (df['Relationship (Party Role)'] == 'Account Holder') | (df["Relationship (Party Role)"] == "Beneficial Owner"))]

#For every party ID, get a set of all the corresponding entries under 'Portfolio RM UID'
#Add to finaldf if there is more than 1 value
finaldf_27 = pd.DataFrame()
for partyID in df_27["Party ID"]:
    tempdf = df_27[df_27['Party ID'] == partyID]
    setof_pfRMs = {RM for RM in tempdf['Portfolio RM UID'].unique()}
    if len(setof_pfRMs) == 1:
        continue
    else:
        finaldf_27 = finaldf_27.append(df_27[df_27['Party ID'] == partyID])

#Can i just do if: pf RM != party RM?

#Cleanup final product and save as excel spreadsheet
if finaldf_27.empty == False:
    finaldf_27 = finaldf_27.drop_duplicates()
finaldf_27.to_excel('27.xlsx', index=False)
print('Completed.')
