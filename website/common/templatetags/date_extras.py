#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import locale

from django import template

locale.setlocale(locale.LC_TIME, "it_IT.UTF8")
register = template.Library()


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
def my_date_dmY(value):
    return value.strftime("%d/%m/%Y").title().lower()


@register.filter
def year(value):
    return value.strftime("%Y")
