# Dispatcher-OmSU
Application for the dispatcher to work with the Google Calendar via Web API

**uses**
``` 
import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
``` 

Uses googleapiclient library from
https://github.com/googleapis/google-api-python-client

**Requres**
```
pip install google-api-python-client
```

**Setup**

There are a few setup steps you need to complete before you can use this library:

1.  If you don't already have a Google account, [sign up](https://www.google.com/accounts).
2.  If you have never created a Google APIs Console project, read the [Managing Projects page](http://developers.google.com/console/help/managing-projects) and create a project in the [Google API Console](https://console.developers.google.com/).
3.  [Install](http://developers.google.com/api-client-library/python/start/installation) the library.
4.  To add new tester while app is in test mode -> go to your [Google APIs Console] (https://console.cloud.google.com/apis/credentials/consent)

**Features**
```
list - lists all events in main calendar
quit - quits program
del -all - deletes all events in main calendar
           Also searches through all calendars for given user
byparam - lists all events in main calendar which are between dates, given in options
          Also it filters events by name. Choses events that contain give string in name
          It is implemented to get all events for given group e.g. DAN-909, DTN-809 etc.
          Also searches all calendars for given user
          Also accepts cyrillic letters
          Prints name of calendar, name of event and event date-time
          Prints day of the week, week of the year and period of the day
cal_list - lists calendars for user
```
**Functions**
```
def get_options():
    # It reads parameters from file: lower_date, upper_date, group
    # Those params are to be passed to function list_events_by_param
    # That function will list events, filtered by params
    
def get_calendar_dict():
    # This function retrieves list of calendars for user
    # Returns dict if calendar_ID: calenar_summary
    
def del_all_calendar_events(service, options):
    # This function deletes all events before given date
    # Also searches through all calendars for given user

def load_into_spreadsheet(service, options, timetable):
    # Input is: spreadsheet service, options dict and timetable object
    # Call the Sheets API, creates new spreadsheet
    # and loads data from timetable into spreadsheet
    # Outputs link to created spreadsheet on the screen
``` 
**structures**
```
periods_dict
    # translates hour of the day into period of the day

days_dict
    # days_dict translates day of the week into locl name of the day

class Timetable
    # timeteble stores all scheduled events (pairs)
    # .print() - prints timetable to the screen
```
**usefull parameters for query**
```
Events: list
calendarId - string from calendarList: List
singleEvents = True - to expand recurring events into instances. False - to only return single one-off events and instances of recurring events, but not the underlying recurring events themselves. Optional. The default is False. 
```
