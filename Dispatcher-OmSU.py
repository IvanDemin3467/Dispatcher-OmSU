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

# periods_dict translates hour of the day into period of the day
periods_dict = {"08" : 1, "09" : 2, "11" : 3, "13" : 4, "15" : 5, "17" : 6, "18" : 7}

# timeteble stores all scheduled events (pairs)
class Timetable:
    def __init__(self, name="Other"):
        self.timetable = [[["" for period in range(7)]
                               for day in range(7)]
                               for week in range(52)]
        self.name = name

    def put(self, value, period, day, week):
        self.timetable[week-1][day-1][period-1] = value

    def get(self, period, day, week):
        return self.timetable[week-1][day-1][period-1]

    def print(self):
        # .print() - prints timetable to the screen
        for week in range(52):
            empty_week = True
            to_print = ""
            to_print += "######   Week: " + str(week+1) + "   ######\n"
            to_print += "Periods: 1 2 3 4 5 6 7\n"
            for day in range(7):
                to_print += "     " + days_dict[day] + ":"
                empty_day = True
                for period in range(7):
                    if self.timetable[week][day][period] != "":
                        to_print += " *"
                        empty_day = False
                    else:
                        to_print += "  "
                to_print += " :" + days_dict[day] + "\n"
                if not empty_day:
                    empty_week = False
            to_print += "         1 2 3 4 5 6 7\n"
            if not empty_week:
                print(to_print)
                    


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
    calendar_list = get_calendar_dict()

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
    # (Cyrillic letters are accepted)
    # Also searches all calendars for given user
    # Prints name of calendar, name of event and event date-time
    # Prints day of the week, week of the year and period of the day
    page_token = None

    # init timetable
    timetable = Timetable(options["group"])

    # get calendar list
    calendar_dict = get_calendar_dict()

    # get events
    print("********************\nList of evens for group:", options["group"])
    for calendar in calendar_dict:
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
                        print("********************")
                        event_tutor = calendar_dict[calendar]
                        print("Tutor: ", event_tutor)
                        print("Event_name: ", event_name)
                        print("Event_start: ", event_start)
                        week = int(event_start.strftime("%W").lstrip("0"))
                        print("Week: ", week)
                        day = event_start.strftime("%A")
                        print("Day: ", day)
                        period = event_start.strftime("%H")
                        try:
                            period = periods_dict[period]
                        except:
                            period = "other"
                        print("Period: ", period, " ", event_start.strftime("%H:%M:%S"))
                        data = event_tutor + " : " + event_name
                        print(data)
                        timetable.put(value=data, period=period, day=day, week=week)
                        print(timetable.get(period=period, day=day, week=week))
                    #print(event['id'])
                except:
                    #pass
                    print("Some error", event_tutor, event_name, period, day, week)
            page_token = events.get('nextPageToken')
            if not page_token:
                break
    #timetable.print()
    return timetable

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

def get_calendar_dict():
    # This function retrieves list of calendars for user
    # Returns dict if calendar_ID: calenar_summary
    page_token = None
    calendar_dict = {}
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        #print(calendar_list_entry['summary'])
          calendar_dict[calendar_list_entry['id']] = calendar_list_entry['summary']
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    return calendar_dict


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
