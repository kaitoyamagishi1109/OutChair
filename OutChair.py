#Copyright 2019, Kaito Yamagishi, all rights reserved

#imports for sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#make sure to update this with your own json folder downloaded from the google cloud API website
credentials = ServiceAccountCredentials.from_json_keyfile_name('OutChair-46ffa5a5c89a.json', scope)
gc = gspread.authorize(credentials)
#This will be the name of your spreadsheet: share this via google sheets to the given client email in your json file
wks = gc.open('JSA_Attendance').sheet1

#imports for slack API
from slackclient import SlackClient

#other imports
import datetime

#find date right now, format it the same as in spreadsheet
timenow = datetime.datetime.now()
date = timenow.strftime("%m" + '/' + "%d")

def swipe(buid):
    #find the users row within the spreadsheet, print name
    userrow = (wks.find(buid).row)
    print('Name: ' + wks.cell(userrow, 1).value)
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
    return datecol

def strike(datecol):
    #after appending everyones attendance, put strikes for people who havent showed up
    numMember = len(wks.col_values(1))+1
    for x in range(1,numMember):
        if (wks.cell(x,datecol).value == ''):
            wks.update_cell(x, datecol, 'S')

if __name__ == '__main__':
    #user is able to keep swiping until ;q is called
    while True:
        #ID input and simple error check
        swiper_input = input("Swipe BUID: ")
        while swiper_input == '' or swiper_input[0] != ';':
            swiper_input = input("Invalid. Swipe a valid BUID: ")
        #keep swiping, to quit, type ;q
        if swiper_input == ';q':
            break
        buid = swiper_input[2:10]
        #recieve slack username from the swipe function
        datalist = swipe(buid)
        #pass the recieved slack username into the notify function 
        notify(datalist[1])
        #pass the users row number to the write function to append presence
        datecol = write(datalist[0])
    strike(datecol)
    print('Exiting Program...')