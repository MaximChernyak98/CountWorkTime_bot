from datetime import datetime, timedelta


def timedelta_to_time_string(timedelta_period, full_format):
    days, seconds = timedelta_period.days, timedelta_period.seconds
    hours = days * 24 + seconds // 3600
    minutes_for_print = (seconds % 3600) // 60
    seconds_for_print = seconds % 60
    if full_format:
        result_string = f'{hours} часов, {minutes_for_print} минут, {seconds_for_print} секунд'
    else:
        result_string = f'{hours}:{minutes_for_print}:{seconds_for_print}'
    return result_string
