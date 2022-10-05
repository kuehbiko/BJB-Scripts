# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:28:43 2022

@author: u56313
"""

import win32com.client

portfolio = input("Enter Portfolio Number: ")
if len(portfolio) != 13: portfolio = input("Enter Portfolio Number: ")

subject = portfolio + ' New Account - FYA on New Ebanking'
recipient = '***' #email redacted for privacy
body = "Hi Mailing Team, \
        <br><br>FYA. \
        <br><br>Thank you. \
        <br><br>Best Regards, \
        <br>Elizabeth Lim"

def sendEmail(recipient, subject, body):
    #Create and send email
    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.To = recipient
    newMail.Subject = subject
    newMail.HTMLBody  = body

    newMail.display()

sendEmail(recipient, subject, body)
