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
    try:
        time = datetime.datetime.strptime(str_time, "%Hh%M")
    except:
        time = datetime.datetime.strptime(str_time, "%H:%M")

    return time 

def convert_time_to_string(time):
    time_str = time.strftime("%H:%M")
    return time_str




def next_days(number_days, comparison):
    days_response = []
    for i in range(number_days):
        days_response.append(comparison + datetime.timedelta(days=i+1))
    return days_response



def unavailability_repeat(str_unavailability_repeat):
    if str_unavailability_repeat == "week":
        repeat = "Repete toda semana"
    elif str_unavailability_repeat == "biweek":
        repeat = "A cada quinze dias"
    elif str_unavailability_repeat == "month":
        repeat = "Repete a cada mês"
    elif str_unavailability_repeat == None:
        repeat = None
    
    return repeat