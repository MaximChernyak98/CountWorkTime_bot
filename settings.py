from datetime import datetime, timedelta

IS_MAN_AT_WORKPLACE = False
IS_WORKDAY_STARTED = False
IS_BREAK = False

HITS_TO_START_WORK = 2
HITS_TO_BREAK = 2

LAST_TIME_STAMP = datetime.now()
SUMMARY_WORK_TIME = timedelta()
SUMMARY_BREAK_TIME = timedelta()
