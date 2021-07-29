# Dispatcher-OmSU
Application for the dispatcher to work with the Google Calendar via Web API

**uses**
``` 
import os
import pprint

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
``` 

Uses googleapiclient library from
https://github.com/googleapis/google-api-python-client
