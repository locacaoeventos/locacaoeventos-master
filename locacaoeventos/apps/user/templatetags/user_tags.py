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
