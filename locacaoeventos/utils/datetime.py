import datetime


def test_date(datetime_str):
    try:
        datetime.datetime.strptime(datetime_str, '%Y-%m-%d')
        return True
    except:
        return False


def translate_month(month_eng):
	if month_eng == "January":
		month_pt = "Janeiro"
	elif month_eng == "February":
		month_pt = "Fevereiro"
	elif month_eng == "March":
		month_pt = "Março"
	elif month_eng == "April":
		month_pt = "Abril"
	elif month_eng == "May":
		month_pt = "Maio"
	elif month_eng == "June":
		month_pt = "Junho"
	elif month_eng == "July":
		month_pt = "Julho"
	elif month_eng == "August":
		month_pt = "Agosto"
	elif month_eng == "September":
		month_pt = "Setembro"
	elif month_eng == "October":
		month_pt = "Outubro"
	elif month_eng == "November":
		month_pt = "Novembro"
	elif month_eng == "December":
		month_pt = "Dezembro"
	return month_pt



def convert_to_time(str_time):
	time = datetime.datetime.strptime(str_time, "%Hh%M")
	return time 

def convert_time_to_string(time):
	time_str = time.strftime("%Hh%M")
	return time_str