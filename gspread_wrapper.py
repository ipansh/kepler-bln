from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
import os
import json

credentials = os.environ.get['GOOGLE_APPLICATION_CREDENTIALS']
print('Got credentials from env...')
credentials_json = json.loads(credentials)
print('Converted to json...')


def get_master_spreadsheet():
    gspread_scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    gspread_credentials = ServiceAccountCredentials.from_service_account_info(credentials_json)
    print('Credentials step 1...')

    gc = gspread.authorize(gspread_credentials)
    print('Authorized!')
    spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/11kcKN_enesAjM4ASHg2-kpwqMtco2A19D407fz3UXHE/edit#gid=0')

    sh1 = spreadsheet.sheet1
    return pd.DataFrame(sh1.get_all_records())