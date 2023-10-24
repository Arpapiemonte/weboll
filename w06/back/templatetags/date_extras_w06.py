import locale

from django import template

locale.setlocale(locale.LC_TIME, "it_IT.UTF8")
register = template.Library()
