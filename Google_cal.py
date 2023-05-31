from __future__ import print_function
from datetime import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

temp_table = np.array([[0,0]])
table = pd.DataFrame(columns = ["date", "event"])

calendars = ['sehra.rajpreet@gmail.com','en.judaism#holiday@group.v.calendar.google.com','addressbook#contacts@group.v.calendar.google.com']

def calendar_events(temp_table,table):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    for item in calendars:

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = service.events().list(calendarId=item, timeMin=now,
                                                  maxResults=5, singleEvents=True,
                                                  orderBy='startTime').execute()
            
            events = events_result.get('items', [])
            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                temp_table = np.append(temp_table,[[datetime.strptime(start[:10], '%Y-%m-%d').date(), event['summary']]],axis=0)



        except HttpError as error:
            print('An error occurred: %s' % error)

        table = pd.concat([table,pd.DataFrame(temp_table, columns = ['date','event'])])
        table = table[ (table['date'] != 0)]

    table.sort_values(by = 'date', inplace=False)
    return table

