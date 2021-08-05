import os
import pprint

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from datetime import datetime

pp = pprint.PrettyPrinter(indent=2)

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This access scope grants read-only access to the authenticated user's Calendar
# account.
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def list_calendar_events(service):
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        #print(events)
        for event in events['items']:
            try:
                print(event['summary'])
                #print(event['id'])
            except:
                print("Some error with 'summary' field")
        page_token = events.get('nextPageToken')
        if not page_token:
            break


def del_all_calendar_events():
    page_token = None
    while True:
        
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            try:
                Id = event['id']
            except:
                print("No id")
            try:
                service.events().delete(calendarId='primary', eventId=event['id']).execute()
            except:
                print("Can not delete")
        page_token = events.get('nextPageToken')
        if not page_token:
            break


def list_events_by_param(service, options):
    page_token = None

    # get events
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            try:
                event_name = event['summary'])
                event_start = datetime.strptime(event['start']['dateTime'],
                                                "%Y-%m-%dT%H:%M:%S+06:00")
                print(event_name)
                print(event_start)
                if event_start > options["lower_date"] and
                   event_start < options["upper_date"] and
                   options["group"] in event_name:
                    print("Date in desired interval")
                #print(event['id'])
            except:
                print("Some error with 'summary' field")
        page_token = events.get('nextPageToken')
        if not page_token:
            break


def get_options():
    # get options
    options = {}
    stream = open("options.txt", "rt")
    lower_date = stream.readline().rstrip()
    options["lower_date"] = datetime.strptime(lower_date, "%Y-%m-%d %H:%M:%S")
    upper_date = stream.readline().rstrip()
    options["upper_date"] = datetime.strptime(upper_date, "%Y-%m-%d %H:%M:%S")
    group = stream.readline().rstrip()
    print(group)
    options["group"] = group
    stream.close()


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    options = get_options()
    while True:
        Input = input("Next task: ")
        if Input == "list" or Input == "List" or Input == "LIST":
            list_calendar_events(service)
        if Input == "byparam":
            list_events_by_param(service, options)
        if Input == "q" or Input == "quit" or Input == "Quit" or Input == "QUIT":
            break
        if Input == "del -all" or Input == "quit" or Input == "Quit" or Input == "QUIT":
            if(input("Are you sure?") == "Yes"):
                del_all_calendar_events()
    service.close()
