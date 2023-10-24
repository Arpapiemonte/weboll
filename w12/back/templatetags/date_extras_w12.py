import datetime
import locale

from django import template

locale.setlocale(locale.LC_TIME, "it_IT.UTF8")
register = template.Library()


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
def my_date(value):
    return value.strftime("%A, %d %B %Y").title().lower()


@register.filter
def my_date_JtD(value):
    return value.strftime("%A, %d %B %Y").lower().title()


@register.filter
def my_date_JtD_ita(value):
    return value.strftime("%d/%m/%Y ore %H:%M").lower()


@register.filter
def year(value):
    return value.strftime("%Y")
