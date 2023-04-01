'''Utils'''
import regex
import pandas as pd
from datetime import datetime, timedelta
from calendar import monthrange
from pathlib import Path


DATE_FORMAT = '%Y-%m-%d'

def write_log_simple(path, mode, msg):
    '''Writes log

    params:
    ---
        path: str - full path (including filename)
        msg: str - message
    '''
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, mode) as logfile:
        logfile.write(msg)


def write_text_data(path, mode, data: str, encoding="utf-8"):
    '''Writes text data
    '''
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, mode, encoding=encoding) as textfile:
        textfile.write(data)
    print(f"Wrote data to {path}")


def date_to_str(d: datetime, format=DATE_FORMAT):
    '''Date to str of format
    '''
    return d.strftime(format)


def generate_dates(start: str, end: str, format=DATE_FORMAT):
    '''Generates dates between two dates (inclusive)

    params:
    ---
    start: date as string (eg '2022-01-01')
    end: date as string (eg '2022-01-01')

    Useful when getting daily data (e.g., event_date = ...)
    '''
    start_date = datetime.strptime(start, format)
    end_date = datetime.strptime(end, format)
    check = end_date >= start_date
    if not check:
        raise ValueError

    current_date = start_date
    dates = [current_date]
    while current_date < end_date:
        current_date = current_date + timedelta(days = 1)
        dates.append(current_date)
    return dates


def generate_yearMonths(start: str, end: str, format=DATE_FORMAT):
    '''Generates pairs of year-month strings between two dates (inclusive)
    
    E.g., start='2022-11-01', end='2023-01-01', output will have:
    [(2022,11), (2022,12), (2023,1)]
    '''
    year_month_str = pd.date_range(start, end, freq='MS').strftime("%Y-%m").to_list()
    return [tuple(map(lambda x: int(x), s.split("-"))) for s in year_month_str]


def month_start_end(year: int, month: int, format=DATE_FORMAT):
    '''Generates a tuple of strings representing the first
    and last day of the month
    '''
    date = datetime(year=year, month=month, day=1)
    month_last_day = monthrange(year, month)[1]
    month_last_date = datetime(year=year, month=month, day=month_last_day)

    return (date.strftime(DATE_FORMAT), month_last_date.strftime(DATE_FORMAT))


def days_back(start, end, step):
    '''Generates delta days to go back
    
    For example, if we want to go back 364 days using 6-step incrementals,
    expected output will be:
    [(6, 0), (13, 7), ..., (364, 357)]
    '''
    upper_ = range(start, end, step + 1) # upper numbers
    result = []
    for idx, num in enumerate(upper_):
        if idx == len(upper_) - 1:
            result.append((end, num))
        else:
            result.append(((num + step), num))
    return result


def sanitize_filename(filename: str, illegal_pattern=r"[\<\>\:\"\/\|\?\*\\]+", alt="_"):
    '''Sanitizes file name as per Windows standard

    :params:
    ---
        alt: alternative character/string for anything that matches the illegal pattern
    '''
    return regex.sub(illegal_pattern, alt, filename)


if __name__ == "__main__":
    # print(generate_dates('2022-01-01', '2022-01-05'))
    # print(date_to_str(generate_dates('2022-01-01', '2022-01-05')[0]))
    # write_log_simple("test.txt", "a", "test")
    print(month_start_end(2020, 2))
