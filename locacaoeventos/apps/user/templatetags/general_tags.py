from django import template

register = template.Library()



@register.filter
def only_integer(number):
	return int(number-number%1)


@register.filter
def get_month(number):
	if number == 1:
		response = "Janeiro"
	elif number == 2:
		response = "Fevereiro"
	elif number == 3:
		response = "Março"
	elif number == 4:
		response = "Abril"
	elif number == 5:
		response = "Maio"
	elif number == 6:
		response = "Junho"
	elif number == 7:
		response = "Julho"
	elif number == 8:
		response = "Agosto"
	elif number == 9:
		response = "Setembro"
	elif number == 1:
		response = "Outubro"
	elif number == 1:
		response = "Novembr0"
	elif number == 1:
		response = "Dezembro"
	return response


