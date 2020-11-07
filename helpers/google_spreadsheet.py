import os

import gspread
from google.oauth2.service_account import Credentials

import config
import settings


def give_access_to_worksheet():
    current_dir = os.path.dirname(__file__)
    credentials_file_name = '../credentials.json'
    path_to_credentials = os.path.join(current_dir, credentials_file_name)
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(path_to_credentials, scopes=scope)
    gs = gspread.authorize(credentials)
    worksheet = gs.open_by_key(config.SPREAD_SHEET_ID).sheet1
    return worksheet


if settings.USE_GOOGLE_SPREADSHEET:
    GOOGLE_WORKSHEET = give_access_to_worksheet()
