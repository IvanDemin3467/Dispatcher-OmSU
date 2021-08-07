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


def del_all_calendar_events(service, options):
    # This function deletes all events before given date
    # Also searches through all calendars for given user
    page_token = None

    # get calendar list
    calendar_list = get_calendar_list()

    # del events
    for calendar in calendar_list:
        while True:
            events = service.events().list(calendarId=calendar, pageToken=page_token).execute()
            for event in events['items']:
                try:
                    if event_start < options["lower_date"]:
                        service.events().delete(calendarId=calendar,
                                                eventId=event['id']).execute()
                except:
                    print("Can not delete")
            page_token = events.get('nextPageToken')
            if not page_token:
                break


def list_events_by_param(service, options):
    # lists all events in main calendar which are between dates, given in options
    # Also it filters events by name. Choses events that contain give string in name
    # It is implemented to get all events for given group e.g. DAN-909, DTN-809 etc.
    # Also searches all calendars for given user
    page_token = None

    # get calendar list
    calendar_list = get_calendar_list()

    # get events
    for calendar in calendar_list:
        while True:
            events = service.events().list(calendarId=calendar, pageToken=page_token).execute()
            for event in events['items']:
                try:
                    event_name = event['summary']
                    event_start = datetime.strptime(event['start']['dateTime'],
                                                    "%Y-%m-%dT%H:%M:%S+06:00")
                    if event_start > options["lower_date"] and \
                       event_start < options["upper_date"] and \
                       options["group"] in event_name:
                        print("calendar: ", calendar)
                        print("event_name: ", event_name)
                        print("event_start: ", event_start)
                        print("Group and date are ok")
                    #print(event['id'])
                except:
                    print("Some error")
            page_token = events.get('nextPageToken')
            if not page_token:
                break


def get_options():
    # It reads parameters from file: lower_date, upper_date, group
    # Those params are to be passed to function list_events_by_param
    # That function will list events, filtered by params
    options = {}
    stream = open("options.txt", "rt", encoding = "utf-8")
    lower_date = stream.readline().rstrip()
    options["lower_date"] = datetime.strptime(lower_date, "%Y-%m-%d %H:%M:%S")
    upper_date = stream.readline().rstrip()
    options["upper_date"] = datetime.strptime(upper_date, "%Y-%m-%d %H:%M:%S")
    group = stream.readline().rstrip()
    options["group"] = group
    stream.close()
    return options

def get_calendar_list():
    # This function retrieves list of calendars for user
    # Returns list if calendar IDs
    page_token = None
    cal_list = []
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        #print(calendar_list_entry['summary'])
          cal_list.append(calendar_list_entry['id'])
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    return cal_list


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    while True:
        Input = input("Next task: ")
        options = get_options()
        if Input == "list" or Input == "List" or Input == "LIST":
            list_calendar_events(service)
        if Input == "byparam":
            list_events_by_param(service, options)
        if Input == "cal_list":
            get_calendar_list()
        if Input == "q" or Input == "quit" or Input == "Quit" or Input == "QUIT":
            break
        if Input == "del -all" or Input == "quit" or Input == "Quit" or Input == "QUIT":
            if(input("Are you sure?") == "Yes"):
                del_all_calendar_events(service, options)
    service.close()
