import locale
from datetime import timedelta

from django import template

locale.setlocale(locale.LC_TIME, "it_IT.UTF8")
register = template.Library()


@register.filter
def my_date(value):
    return value.strftime("%A, %d %B %Y").title().lower()


@register.filter
def my_pericolo(value):
    mapping = {"-": "A", "1": "I", "2": "P", "3": "D"}
    return mapping.get(value, "np")


@register.filter
def date_tomorrow(value):
    value = value + timedelta(1)
    return value.strftime("%d/%m/%Y").title().lower()


@register.filter
def my_date_JtD(value):
    return value.strftime("%A, %d %B %Y").lower().title()


@register.filter
def my_date_JtD_ita(value):
    return value.strftime("%d/%m/%Y ore %H:%M").lower()


@register.filter
def my_date_dmY(value):
    return value.strftime("%d/%m/%Y").title().lower()


@register.filter
def year(value):
    return value.strftime("%Y")


@register.filter
def mul(value):
    return (value * 22.65) + 162


@register.filter
def get_numeric_value(dictionary, key):
    return float(dictionary.get(key).get("numeric_value"))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
