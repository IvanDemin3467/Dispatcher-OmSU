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
``` 
