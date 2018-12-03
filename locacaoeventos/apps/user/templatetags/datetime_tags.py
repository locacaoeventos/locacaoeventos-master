from django import template

import datetime

register = template.Library()



@register.filter
def create_monthday_set(number):
    list_number = []
    count = 1
    for i in range(number):
        count_str = str(count)
        if len(count_str) == 1:
            count_str = "0" + count_str
        list_number.append(count_str)
        count += 1
    return list_number













@register.filter
def create_year_set(number):
    list_number = []
    count = datetime.date.today().year - number + 1
    while count <= datetime.date.today().year:
        list_number.append(count)
        count += 1
    list_number.sort(reverse=True)
    return list_number







@register.filter
def create_year_set_later(number):
    list_number = []
    count = datetime.date.today().year 
    while count <= datetime.date.today().year + number + 1:
        list_number.append(count)
        count += 1
    list_number.sort()
    return list_number




@register.filter
def create_minutehour_set(number):
    list_number = []
    count = 0
    for i in range(number):
        count_str = str(count)
        if len(count_str) == 1:
            count_str = "0" + count_str
        list_number.append(count_str)
        count += 1
    return list_number





@register.filter
def create_minutehour(number):
    list_time = []
    for i in range(24):
        hour = ""
        if i < 10:
            hour = "0" + str(i)
        else:
            hour = str(i)

        for j in range(6):
            minute = ""
            j = j*10
            if j == 0:
                minute = "0" + str(j)
            else:
                minute = str(j)
            list_time.append(hour + "h" + minute)
    return list_time









# ==============================================
# Int-Str Day, Month Year
# ==============================================
@register.filter
def create_monthday_set_int_str(number):
    list_number = []
    count = 1
    for i in range(number):
        dic = {}
        dic["int"] = count
        count_str = str(count)
        if len(count_str) == 1:
            count_str = "0" + count_str
        dic["str"] = count_str
        list_number.append(dic)
        count += 1
    return list_number

@register.filter
def create_year_set_int_str(number):
    list_number = []
    count = datetime.date.today().year - number + 1
    while count <= datetime.date.today().year:
        list_number.append({
            "int":count,
            "str":str(count),
        })
        count += 1
    list_number = sorted(list_number, key=lambda k: k['int'], reverse=True) 
    return list_number
