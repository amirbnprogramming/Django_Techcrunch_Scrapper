from datetime import datetime


def get_correct_date(date):
    datetime_object = datetime.fromisoformat(date)
    return datetime_object
