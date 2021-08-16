from os import environ

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow

from datetime import datetime

import webbrowser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

import win32clipboard
import time
from pynput.keyboard import Key, Controller

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
##flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES,
##                                     redirect_uri='urn:ietf:wg:oauth:2.0:oob')

# Open in Google Chrome
auth_url, _ = flow.authorization_url(prompt='consent')
auth_url += "&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob"

driver = webdriver.Chrome()
driver.get(auth_url)
assert "Вход" in driver.title

elem = driver.find_element_by_name('identifier')
elem.clear()
elem.send_keys("deminie@college.omsu.ru")
elem.send_keys(Keys.RETURN)
#continue_link = driver.find_element_by_name('deminie@college.omsu.ru')
#driver.tap(continue_link)
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
driver.implicitly_wait(2)
elem = driver.find_element_by_name('password')
elem.clear()
elem.send_keys("sometimethumbnoractual")
elem.send_keys(Keys.RETURN)

## Продолжить

wait = WebDriverWait(driver, 10)
while True:
    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "VfPpkd-vQzf8d")))
        elem = driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[2]/div/div/button/span')
        elem.click()
        break
    except StaleElementReferenceException as e:
        print(e)
    except: print("Waiting too long for Продолжить")

print("VfPpkd-vQzf8d clicked")

## Принять 1

while True:
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectioni1"]')))
        elem = driver.find_element_by_xpath('//*[@id="selectioni1"]')
        elem.click()
        break
    except StaleElementReferenceException as e:
        print(e)
    except: print("Waiting too long for Принять 1")

print("Принять 1 clicked")

## Принять 2

while True:
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectioni4"]')))
        elem = driver.find_element_by_xpath('//*[@id="selectioni4"]')
        elem.click()
        break
    except StaleElementReferenceException as e:
        print(e)
    except: print("Waiting too long for Принять 2")

print("Принять 2 clicked")

## Продолжить после принятия

while True:
    try:
        elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit_approve_access"]/div/button')))
        #elem = driver.find_element_by_xpath('//*[@id="submit_approve_access"]/div/button')
        elem.click()
        break
    except StaleElementReferenceException as e:
        print(e)
    except: print("Waiting too long for Продолжить после принятия")

print("Продолжить после принятия clicked")


## Скопировать

while True:
    try:
        elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/span/div/div/button')))
        #elem = driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/span/div/div/button')
        elem.click()
        break
    except StaleElementReferenceException as e:
        print(e)
    except: print("Waiting too long for Скопировать")

print("Скопировать clicked")

time.sleep(1)

win32clipboard.OpenClipboard()
from_clipboard = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()

print("Got code: ", from_clipboard)

driver.close()

flow.run_local_server()

# flow.fetch_token(code=from_clipboard)

##actions = ActionChains(driver)
##actions.move_to_element(elem)
##actions.pause(1)
##actions.click_and_hold(elem)
##actions.pause(1)
##actions.release(elem)
##actions.perform()

##keyboard = Controller()

##with keyboard.pressed(Key.alt):
##    keyboard.press(Key.tab)
##    keyboard.release(Key.tab)

##keyboard.type(from_clipboard)

credentials = flow.credentials
service_calendar = build('calendar', 'v3', credentials = credentials)
service_sheets = build('sheets', 'v4', credentials = credentials)
