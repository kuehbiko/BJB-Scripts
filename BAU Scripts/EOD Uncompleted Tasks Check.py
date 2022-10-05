# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:13:37 2022

@author: u56313
"""

import os
import datetime

base = datetime.datetime.today()
yyyy = base.strftime("%Y")
mmm_yyyy = base.strftime("%b %Y").upper()
dd_mmm_yyyy = base.strftime("%d %b %Y")

folder_list = ['AGENT','CIP','COUNTERPARTY','NAME SEARCHES','NEW PORTFOLIO OPENING','PORTFOLIO CLOSURE','PRICING','SERVICE TERMINATION','STATIC MAINTENANCE OTHERS','SWITCH OF SERVICE MODEL']
temp = [f"I:/BJB_Data/Acct Mgt/Data Management/Data Mgmt - Static/WFH/{folder_name}/{yyyy}/{mmm_yyyy}/{dd_mmm_yyyy}" for folder_name in folder_list]
path_list = []

#Check if each folder path exists
for path in temp:
    if os.path.isdir(path):
        path_list.append(path)
    else:
        continue

#Compiles a list of all tasks that are not labeled 'checked'
for path in path_list:
    print(f"\nPath: {path}")
    unchecked = []
    checked = []
    tasks = os.listdir(path)
    
    for task_name in tasks:
        if 'checked' in task_name.lower():
            checked.append(task_name)
        else:
            unchecked.append(task_name)
    
    print('UNCHECKED:')
    print(*unchecked, sep='\n')
