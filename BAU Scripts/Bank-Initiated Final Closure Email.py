# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:09:24 2022

@author: u56313
"""

import win32com.client

portfolio = input("Enter Portfolio Number: ")
if len(portfolio) != 13: portfolio = input("Enter Portfolio Number: ")

subject = 'Portfolio Closure ' + portfolio
recipient = ''
copied = '***' #email redacted for privacy
body = "Hi All, \
        <br><br>Portfolio has been closed. \
        <br>You may retrieve the closing letter via eDelivery Portfolio Letters in Doxter. \
        <br>Saved Searches -> Search Templates -> E-Delivery Portfolio Letters -> Input Account Number -> Click Search -> Closure of Account \
        <br><br>Regards, \
        <br>Data Management - Static"

def sendEmail(recipient, copied, subject, body):
    #Create and send email
    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.To = recipient
    newMail.CC = copied
    newMail.Subject = subject
    newMail.HTMLBody  = body

    newMail.display()

sendEmail(recipient, copied, subject, body)
