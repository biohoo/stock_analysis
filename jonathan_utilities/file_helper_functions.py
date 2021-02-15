import datetime
import os

FILE = '../images/you_are_being_audited.jpg'

timeframes = ['year','day','month']

def file_modified_date_difference(filename, timeframe='year'):
    '''
    Given a file and the current year, calculates
    the elapsed time since the file has been modified, in years.
    '''

    if timeframe == 'year':

        return file_year_difference(filename)

    elif timeframe == 'month':

        return (file_year_difference(filename) * 12) + file_month_difference(filename)

    elif timeframe == 'day':

        return (file_year_difference(filename) * 365) + (file_month_difference(filename) * 30) + file_day_difference(filename)

    else:
        return None


def file_year_difference(filename):
    now = datetime.datetime.now().year
    file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filename)).year
    time_from_modified = now - file_modified

    return time_from_modified


def file_month_difference(filename):
    now = datetime.datetime.now().month
    file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filename)).month
    time_from_modified = now - file_modified
    return time_from_modified


def file_day_difference(filename):
    now = datetime.datetime.now().day
    file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filename)).day
    time_from_modified = now - file_modified
    return time_from_modified




