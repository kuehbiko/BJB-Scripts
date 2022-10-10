# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:33:31 2022

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
                                               'Identification Document Issue Country',
                                               'Nationality'))


#Clean up:
#New column 'Party Name Cleanup', 'PartyNameDOB'
#Replace blank cells with 'None'
df['Party Name Cleanup'] = df['Party Name'].str.replace('\W','').str.lower()
df['PartyNameDOB'] = df['Date of Birth'].dt.strftime('%d%m%Y').astype(str) + df['Party Name Cleanup']
df['Identification Document Type'].fillna('None', inplace = True)
df['Identification Document Issue Country'].fillna('None', inplace = True)


#Different dataframes for Passport, NRIC, National ID based on their different filtering criteria:
#- Passport: Identification Document Type == Passport
#- NRIC: Identification Document Type == SG Pink NRIC
#- National ID: Identification Document Type == National ID; Issue Country == Switzerland/Italy/Germany/France/Liechtenstein
#Query out all cases where Issue Country = Nationality
country_list = ['Switzerland','Italy','Germany','France','Liechtenstein']
#Passport:
df_pass = df[(df['Party Type'] == 'Natural Person') & (df['Identification Document Type'] == 'Passport')]
finaldf_pass = df_pass.query('`Identification Document Issue Country` != Nationality')
#SG Pink NRIC:
df_NRIC = df[(df['Party Type'] == 'Natural Person') & (df['Identification Document Type'] == 'SG Pink NRIC')]
finaldf_NRIC = df_NRIC.query('`Identification Document Issue Country` != Nationality')
#National ID:
df_NID = df[(df['Party Type'] == 'Natural Person') & (df['Identification Document Type'] == 'National ID') & 
            (df['Identification Document Issue Country'].isin(country_list) | df['Nationality'].isin(country_list))]
finaldf_NID = df_NID.query('`Identification Document Issue Country` != Nationality')


#Add Inconsistency Type columns for Passport, NRIC, National ID dataframes
finaldf_pass['Inconsistency Type'] = "Passport ID Doc Ctry <> Nationality"
finaldf_NRIC['Inconsistency Type'] = "Same Name, DOB; Nationality <> ID proof"
finaldf_NID['Inconsistency Type'] = "Same Name, DOB; Nationality <> ID proof"
#Then combine them
df_all = pd.concat([finaldf_pass, finaldf_NRIC, finaldf_NID])


#Filter for dual citizenship
finaldf_12 = pd.DataFrame()
for name in df_all["PartyNameDOB"]:
    tempdf = df_all[df_all['PartyNameDOB'] == name]
    setof_countries = {country for country in tempdf['Identification Document Issue Country'].unique()}
    setof_nationalities = {country for country in tempdf['Nationality'].unique()}
    if setof_countries == setof_nationalities:
        continue
    else:
        finaldf_12 = finaldf_12.append(df_all[df_all['PartyNameDOB'] == name])


#Cleanup final product and save as excel spreadsheet
if finaldf_12.empty == False:
    finaldf_12 = finaldf_12.sort_values(['Party Name Cleanup', 'Inconsistency Type', 'Party ID']). \
                      drop(axis=1, columns=(['Party Name Cleanup', 'PartyNameDOB'])).drop_duplicates()
finaldf_12.to_excel('12.xlsx', index=False)
print('Completed.')
