#Copyright 2019, Kaito Yamagishi, all rights reserved

#imports for sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('OutChair-46ffa5a5c89a.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('JSA_Attendance').sheet1

#imports for slack API
from slackclient import SlackClient

#other imports
import datetime

#find date right now, format it the same as in spreadsheet
timenow = datetime.datetime.now()
date = timenow.strftime("%m" + '/' + "%d")

def swipe():
    #read swipes from users and append the attendance data to the dictionary
    #ID input and simple error check
    swiper_input = input("Swipe ID: ")
    while swiper_input == '' or swiper_input[0] != ';':
        swiper_input = input("Invalid ID. Swipe ID: ")
    #initialize buid as 8 integers
    buid = swiper_input[2:10]
    #find the users row within the spreadsheet, print name
    userrow = (wks.find(buid).row)
    print('Name: '+wks.cell(userrow, 1).value)
    #find the users slack username, return values
    username = (wks.cell(userrow, 2).value)
    return [userrow, username]


def notify(username):
    #send a slack notification to the user
    #input argument: username (BU email before @ e.g. kaitoy)
    token = "xoxb-593052545734-641598667014-ZXrCx7gjRFsM4yYDffBe15Xi"
    sc = SlackClient(token)
    sc.api_call(
        "chat.postMessage",
        channel='@'+username,
        text='You have been marked present for ' + date + '\'s meeting. Thank you for coming! :sushi:',
        username='OutChair Attendane Bot',
        icon_emoji=':jp:',
        as_user='false'
    )

def write(userrow):
    #find todays date from the columns, and put a P for present in the users corresponding frame
    datecol = (wks.find(date).col)
    wks.update_cell(userrow, datecol, 'P')

if __name__ == '__main__':
    #recieve slack username from the swipe function
    datalist = swipe()
    #pass the recieved slack username into the notify function 
    notify(datalist[1])
    #pass the users row number to the write function to append presence
    write(datalist[0])