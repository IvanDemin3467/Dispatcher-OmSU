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

**Features**
```
list - lists all events in main calendar
bydate - lists all events in main calendar which are between dates, given in options.txt
quit - quits program
del -all - deletes all events in main calendar
```
**update**
New function implemented - get_options
It reads parameters from file: lower_date, upper_date, group
