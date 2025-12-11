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
        return value.strftime("%d/%m/%Y").title().lower()


@register.filter
def my_date_dm_oggi(value):
    if type(value) == str:
        if value != "n.d.":
            return (
                (datetime.datetime.strptime(value, "%Y-%m-%d"))
                .strftime("%d/%m")
                .title()
                .lower()
            )
        else:
            return value
    else:
        return value.strftime("%d/%m").title().lower()


@register.filter
def my_date_dm_domani(value):
    if type(value) == str:
        if value != "n.d.":
            return (
                (
                    datetime.datetime.strptime(value, "%Y-%m-%d")
                    + datetime.timedelta(days=1)
                )
                .strftime("%d/%m")
                .title()
                .lower()
            )
        else:
            return value
    else:
        return (value + datetime.timedelta(days=1)).strftime("%d/%m").title().lower()


@register.filter
def my_date_dm_dopodomani(value):
    if type(value) == str:
        if value != "n.d.":
            return (
                (
                    datetime.datetime.strptime(value, "%Y-%m-%d")
                    + datetime.timedelta(days=2)
                )
                .strftime("%d/%m")
                .title()
                .lower()
            )
        else:
            return value
    else:
        return (value + datetime.timedelta(days=2)).strftime("%d/%m").title().lower()


@register.filter
def year(value):
    return value.strftime("%Y")


@register.filter
def mul(value):
    return str((value * 10) + 32)
