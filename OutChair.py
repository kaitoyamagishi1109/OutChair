#Copyright 2019, Kaito Yamagishi, all rights reserved

#imports for sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#make sure to update this with your own json folder downloaded from the google cloud API website
credentials = ServiceAccountCredentials.from_json_keyfile_name('OutChair-46ffa5a5c89a.json', scope)
gc = gspread.authorize(credentials)
#This will be the name of your spreadsheet: share this via google sheets to the given client email in your json file
attendance = gc.open('JSA_Attendance').sheet1

#imports for slack API
from slackclient import SlackClient

#other imports
import datetime


#global variable declerations
#find date right now, format it the same as in spreadsheet
timenow = datetime.datetime.now()
date = timenow.strftime("%m" + '/' + "%d")
#find todays date's row from spreadsheet
datecol = (attendance.find(date).col)

def excused():
    #marks some absenst students excused from absense form/spreadsheet
    absform = gc.open('AbsenceForm_Responses').sheet1
    #find every user absent for todays meeting
    numabsense = absform.findall(date)
    #for loop through all those user
    for user in range(0, len(numabsense)):
        row = (numabsense[user].row)
        email = absform.cell(row,2).value
        #split email by delimiter and recieve username
        username = email.split("@")[0]
        userrow = (attendance.find(username).row)
        #update cell with E for excused
        attendance.update_cell(userrow, datecol, 'E')
        

def swipe(buid):
    #find the users row within the spreadsheet, print name
    userrow = (attendance.find(buid).row)
    print(attendance.cell(userrow, 1).value + " was marked present.")
    #find the users slack username, return values
    username = (attendance.cell(userrow, 2).value)
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
        as_user='false')


def write(userrow):
    #find todays date from the columns, and put a P for present in the users corresponding frame
    attendance.update_cell(userrow, datecol, 'P')


def strike():
    #after appending everyones attendance, put strikes for people who havent showed up
    numMember = len(attendance.col_values(1))+1
    #due to google sheets 1 start counting system of cells, numMember needs an increment
    for user in range(1,numMember):
        if (attendance.cell(user, datecol).value == ''):
            attendance.update_cell(user, datecol, 'S')


if __name__ == '__main__':
    #user is able to keep swiping until ;q is called
    excused()
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
        write(datalist[0])
    strike()
    print('Exiting Program...')