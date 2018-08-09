import datetime


def test_date(datetime_str):
    try:
        datetime.datetime.strptime(datetime_str, '%Y-%m-%d')
        return True
    except:
        return False
