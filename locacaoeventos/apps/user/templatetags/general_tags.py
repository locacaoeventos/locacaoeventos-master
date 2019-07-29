from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

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


@register.filter
def create_range(number):
    list_number = []
    for i in range(number):
        if i%50 == 0:
            list_number.append(i)
    return list_number


@register.filter
def my_float_format(number, decimal_places=2, decimal=','):
    result = intcomma(number)
    result += decimal if decimal not in result else ''
    while len(result.split(decimal)[1]) != decimal_places:
        result += '0'
    return result