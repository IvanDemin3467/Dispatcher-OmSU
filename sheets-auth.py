from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def get_authenticated_service_sheets():
    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret.
    CLIENT_SECRETS_FILE = "client_secret.json"

    # This access scope grants read-only access to the authenticated user's Calendar
    # account.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'

    # Do auth
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
##    if os.path.exists('token.json'):
##        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
##    # If there are no (valid) credentials available, let the user log in.
##    if not creds or not creds.valid:
##        if creds and creds.expired and creds.refresh_token:
##            creds.refresh(Request())
##        else:
##            flow = InstalledAppFlow.from_client_secrets_file(
##                'credentials.json', SCOPES)
##            creds = flow.run_local_server(port=0)
##        # Save the credentials for the next run
##        with open('token.json', 'w') as token:
##            token.write(creds.to_json())

    service = get_authenticated_service_sheets()

    # Call the Sheets API
    sheet = service.spreadsheets()
    spreadsheet = {
        'properties': {
            'title': "DTN-809"
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                        fields='spreadsheetId').execute()
    print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))

##    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
##                                range=SAMPLE_RANGE_NAME).execute()
##    values = result.get('values', [])
##
##    if not values:
##        print('No data found.')
##    else:
##        print('Name, Major:')
##        for row in values:
##            # Print columns A and E, which correspond to indices 0 and 4.
##            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()
