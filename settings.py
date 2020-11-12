from datetime import datetime, timedelta
from telegram.ext import Updater
import config

MYBOT = Updater(token=config.TOKEN, use_context=True)

USE_GOOGLE_SPREADSHEET = True

REST_TIME_TYPE = 'rest'

IS_MAN_AT_WORKPLACE = False
IS_WORKDAY_STARTED = False

SECONDS_TO_START_WORK = 5
SECONDS_TO_BREAK = 5
HOURS_FOR_WORK_AT_DAY = timedelta(hours=6)

LAST_TIME_STAMP = datetime.now()
SUMMARY_WORK_TIME = timedelta()
SUMMARY_BREAK_TIME = timedelta()
SUMMARY_DINNER_TIME = timedelta()
RAW_BREAK_TIME = timedelta()
