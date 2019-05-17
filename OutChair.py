#Copyright 2019, Kaito Yamagishi, all rights reserved
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1c6lJb77s5RkQhiui4v9Nl5WPkTApTmW2Znd1FvstP1s'
SAMPLE_RANGE_NAME = '!A:S'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    #OutChair functionality
    swiper_input = raw_input("Swipe ID: ")
    while swiper_input == '' or swiper_input[0] != ';':
        swiper_input = raw_input("Invalid ID. Swipe ID: ")
    #change hardcode to 8 digits after U character
    buid = swiper_input[2:10]
    date='4/3' #hardcoded date
    mydict = dict()

    print("BUID: U"+buid)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            #append BUID to name on dictionary
            mydict[row[1]] = row[0]
        for col in values[0]:
            if col == date:
                print(date)
    #find and print the name corresponding to BUID
    name = mydict[buid]
    print("Name: "+name)

if __name__ == '__main__':
    main()