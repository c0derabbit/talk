from datetime import datetime as d

def stringify_date(date):
    try:
        return '{0}-{1}-{2}-{3}-{4}'.format(date.year, date.month, date.day, date.hour, date.minute)
    except ValueError:
        raise ValueError('Invalid date format', date)

def parse_date(date):
    try:
        return d.strptime(date, '%Y-%m-%d-%H-%M')
    except ValueError:
        raise ValueError('Could not convert string to date', date)
