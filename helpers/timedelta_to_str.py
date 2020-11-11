from datetime import datetime, timedelta


def timedelta_to_time_string(timedelta_period, full_format):
    days, seconds = timedelta_period.days, timedelta_period.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if full_format:
        result_string = f'{hours} часов, {minutes} минут, {seconds} секунд'
    else:
        result_string = f'{hours}:{minutes}:{seconds}'
    return result_string