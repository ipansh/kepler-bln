from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
import os

g_private_key_id = os.environ.get("G_PRIVATE_KEY_ID")
g_private_key = os.environ.get("G_PRIVATE_KEY")
g_client_email = os.environ.get("G_CLIENT_EMAIL")
g_client_id = os.environ.get("G_CLIENT_ID")
g_client_x509_cert_url = os.environ.get("G_CLIENT_X509_CERT_URL")

def get_master_spreadsheet():
    gspread_scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    gspread_credentials = ServiceAccountCredentials.from_json_keyfile_dict({
    "type": "service_account",
    "project_id": "kepler-bln",
    "private_key_id": g_private_key_id,
    "private_key": g_private_key,
    "client_email": g_client_email,
    "client_id": g_client_id,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": g_client_x509_cert_url
    })

    gc = gspread.authorize(gspread_credentials)
    spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/11kcKN_enesAjM4ASHg2-kpwqMtco2A19D407fz3UXHE/edit#gid=0')

    sh1 = spreadsheet.sheet1
    return pd.DataFrame(sh1.get_all_records())