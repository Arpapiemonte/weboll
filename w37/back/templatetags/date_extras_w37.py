import datetime
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
    # print(value)
    if type(value) == str:
        if value != "n.d.":
            return (
                (datetime.datetime.strptime(value, "%Y-%m-%d"))
                .strftime("%d/%m/%Y")
                .title()
                .lower()
            )
        else:
            return value
    else:
        if value is None:
            return "---"
        else:
            return value.strftime("%d/%m/%Y").title().lower()


@register.filter
def year(value):
    return value.strftime("%Y")


@register.filter
def mul(value, arg):
    return str(((value * 18) - 38 - (arg * 630)))


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def page_number(value):
    return str(value + 2)


@register.filter
def ora_aggiornamento_none(value):
    if value is None:
        return ""
    else:
        return value


@register.filter
def classes(value):
    if value == 0:
        return str("VERDE")
    if value == 1:
        return str("GIALLO")
    if value == 2:
        return str("ARANCIONE")
    if value == 3:
        return str("ROSSO")
    if value == -1:
        return str("N.D.")
    if value == -99:
        return str("N.D.")
