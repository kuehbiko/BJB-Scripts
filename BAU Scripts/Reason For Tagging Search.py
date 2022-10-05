# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:31:29 2022

@author: u56313
"""

import os
import pandas as pd

inp = input("Enter Tag ID: ") #Input in the forms: SGTAG-00xxx, 00xxx or xxx

bcf = pd.read_excel("I:/BJB_Data/Robotics/ACM SG Static/RPA Manual Tagging/Maker/Files/ConfigurationFile/Business Config File - DDM Copy.xlsx", "Tag Table", usecols="A,C")
tag_ID = bcf['Tag ID']
tag_message = bcf['Tag Message']

def addToClipBoard(text): #Function to auto-copy output to clipboard
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)
    
def r4t(inp): #Function to find tag message
    inp = str(inp).upper()
    for i in range(len(tag_ID)):
        if inp in tag_ID[i]:
            #True if Tag exists
            if pd.isnull(tag_message[i]):
                #True if Tag Message is blank    
                return tag_ID[i] + "\n\n<This tag ID has no tag message.>" 
            addToClipBoard(tag_message[i]) #Calls auto-copy function
            return tag_ID[i] + '\n' + tag_message[i] + "\n\n<This tag message has been copied to your clipboard!>"
            break
        else:
            continue
    return inp + '\n' + "\n\n<This tag ID does not exist.>"

print(r4t(inp))
