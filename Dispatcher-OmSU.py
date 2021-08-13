from os import environ

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from datetime import datetime

#import pprint
#pp = pprint.PrettyPrinter(indent=2)

# periods_dict translates hour of the day into period of the day
periods_dict = {"08" : 1, "09" : 2, "10" : 2, "11" : 3, "12" : 3, "13" : 4,
                "14" : 4, "15" : 5, "16" : 5, "17" : 6, "18" : 7, "19" : 7}
# days_dict translates day of the week into locl name of the day
days_dict = {0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб", 6: "Вс"}

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
            to_print += "########    Week: " + str(week+1) + "   ########\n"
            to_print += "Periods: 1 2 3 4 5 6 7 :Periods\n"
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

    def get_list(self):
        # .get_list() - prepares list to load into spreadsheet
        complete_list = []
        for week in range(52):
            empty_week = True
            complete_list.append(["Неделя: " + str(week+1), "", "", "", "", "", "", ""])
            complete_list.append(["", "Пара 1", "Пара 2", "Пара 3", "Пара 4", "Пара 5", "Пара 6", "Пара 7"])
            for day in range(7):
                row = []
                row.append(days_dict[day])
                for period in range(7):
                    value = self.timetable[week][day][period]
                    if value == "": value = " "
                    else: empty_week = False
                    row.append(value)
                    
                complete_list.append(row)
            if empty_week:
                del complete_list[-9:]
        return complete_list


def load_into_spreadsheet(service, options, timetable):
    # Input is: spreadsheet service, options dict and timetable object
    # Call the Sheets API, creates new spreadsheet
    # and loads data from timetable into spreadsheet
    # Outputs link to created spreadsheet on the screen
    sheet = service.spreadsheets()
    spreadsheet = {
        'properties': {
            'title': timetable.name +
            datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                        fields='spreadsheetId').execute()
    spreadsheetId = spreadsheet.get('spreadsheetId')

    range_name = "Лист1!A1"

    values = timetable.get_list()
    
    body = {
        'values': values
    }
    
    value_input_option = "USER_ENTERED"
    
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))
        
    print("https://docs.google.com/spreadsheets/d/" + spreadsheetId)


def get_authenticated_services():
    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret.
    CLIENT_SECRETS_FILE = "client_secret.json"

    # This access scope grants read-only access to the authenticated user's Calendar
    # account.
    SCOPES = ['https://www.googleapis.com/auth/calendar',
              'https://www.googleapis.com/auth/spreadsheets']
    API_SERVICE_NAME = 'calendar'
    API_VERSION = 'v3'

    # Do auth
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    service_calendar = build('calendar', 'v3', credentials = credentials)
    service_sheets = build('sheets', 'v4', credentials = credentials)
    return service_calendar, service_sheets

##def list_calendar_events(service):
##    page_token = None
##    
##    while True:
##        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
##        #print(events)
##        for event in events['items']:
##            try:
##                print(event['summary'])
##                #print(event['id'])
##            except:
##                print("Some error with 'summary' field")
##        page_token = events.get('nextPageToken')
##        if not page_token:
##            break


##def del_all_calendar_events(service, options):
##    # This function deletes all events before given date
##    # Also searches through all calendars for given user
##    page_token = None
##
##    # get calendar list
##    calendar_list = get_calendar_dict()
##
##    # del events
##    for calendar in calendar_list:
##        while True:
##            events = service.events().list(calendarId=calendar, pageToken=page_token).execute()
##            for event in events['items']:
##                try:
##                    if event_start < options["lower_date"]:
##                        service.events().delete(calendarId=calendar,
##                                                eventId=event['id']).execute()
##                except:
##                    print("Can not delete")
##            page_token = events.get('nextPageToken')
##            if not page_token:
##                break

def simple_print_event(event_tutor, event_name, event_start, week, day, period):
    print("********************")
    print("Tutor: ", event_tutor)
    print("Event_name: ", event_name)
    print("Event_start: ", event_start)
    print("Week: ", week)
    print("Day: ", day)
    print("Period: ", period, " ", event_start.strftime("%H:%M:%S"))
    return

def list_events_by_param(service, options):
    # lists all events in main calendar which are between dates, given in options
    # Also it filters events by name. Choses events that contain give string in name
    # It is implemented to get all events for given group e.g. DAN-909, DTN-809 etc.
    # (Cyrillic letters are accepted)
    # Also searches all calendars for given user
    # Prints name of calendar, name of event and event date-time
    # Prints day of the week, week of the year and period of the day
    # Creates google spreadsheet and loads timetable into it
    # Shows link to the created sheet on a screen
    page_token = None

    # init timetables
    list_timetable = []
    for group in options["groups"]:
        timetable = Timetable(group)
        list_timetable.append(timetable)
    
    # init timetable
    # timetable = Timetable(options["group"])

    # get calendar list
    calendar_dict = get_calendar_dict(service)

    # get events
    # print("********************\nWorking on: timetable for group:", options["group"])
    for calendar in calendar_dict:
        while True:
            events = service.events().list(calendarId=calendar, pageToken=page_token, singleEvents = True).execute()
            for event in events['items']:
                try:
                    event_name = event['summary']
                    event_start = datetime.strptime(event['start']['dateTime'],
                                                    "%Y-%m-%dT%H:%M:%S+06:00")
                    for timetable in list_timetable:
                        if event_start > options["lower_date"] and \
                           event_start < options["upper_date"] and \
                           timetable.name in event_name:
                            event_tutor = calendar_dict[calendar]
                            week = int(event_start.strftime("%W").lstrip("0"))
                            day = int(event_start.strftime("%w"))
                            period = event_start.strftime("%H")
                            try: period = periods_dict[period]
                            except: period = "other"
                            
                            # simply print valuable info on event
                            # simple_print_event(event_tutor, event_name, event_start, week, day, period)

                            data = event_tutor + " : " + event_name
                            #print(data)
                            try: timetable.put(value=data, period=period, day=day, week=week)
                            except: print("error while put()")

                            # get event that was just in timetable (for testing)
                            #try: print(timetable.get(period=period, day=day, week=week))
                            #except: print("error while get()")
                        #print(event['id'])
                except:
                    pass
                    #print("Some error", event_tutor, event_name, period, day, week)
            page_token = events.get('nextPageToken')
            if not page_token:
                break
    if len(options["groups"]) == 1:
        timetable.print()

    ##
    for timetable in list_timetable:
        print(timetable.name)
        load_into_spreadsheet(service_sheets, options, timetable)
    
    return timetable

def get_options():
    # It reads parameters from file: lower_date, upper_date, group
    # Those params are to be passed to function list_events_by_param
    # That function will list events, filtered by params
    options = {}
    s = open("options.txt", "rt", encoding = "utf-8")
    stream = list(s)
    s.close()
    lower_date = stream[0].rstrip()
    options["lower_date"] = datetime.strptime(lower_date, "%Y-%m-%d %H:%M:%S")
    upper_date = stream[1].rstrip()
    options["upper_date"] = datetime.strptime(upper_date, "%Y-%m-%d %H:%M:%S")

    groups = []
    for i in range(2, len(stream)):
        nextline = stream[i].rstrip()
        groups.append(nextline)
    
    options["groups"] = groups
    return options

def get_calendar_dict(service):
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
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service_calendar, service_sheets = get_authenticated_services()
    first_run = True
    while True:
        if first_run:
            Input = "byparam"
            first_run = False
        else:
            Input = input("Next task: ")
        options = get_options()
        if Input == "list" or Input == "List" or Input == "LIST":
            list_calendar_events(service_calendar)
        if Input == "byparam":
            timetable = list_events_by_param(service_calendar, options)
        if Input == "cal_list":
            get_calendar_list()
        if Input == "q" or Input == "quit" or Input == "Quit" or Input == "QUIT":
            break
        if Input == "del -all" or Input == "quit" or Input == "Quit" or Input == "QUIT":
            if(input("Are you sure?") == "Yes"):
                del_all_calendar_events(service_calendar, options)
    service_calendar.close()
