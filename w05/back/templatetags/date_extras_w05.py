#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import pytz
from django import template

cet = pytz.timezone("CET")
register = template.Library()


@register.filter
def iso_date(value):
    return value.astimezone(cet).isoformat()


@register.filter
def year(value):
    return value.strftime("%Y")


@register.filter
def trend(id_trend):
    mapping = {1: "Aumento", 0: "Stazionario", 2: "Diminuzione"}
    return mapping.get(id_trend, "Invalid code")


@register.filter
def tendenza(id_trend):
    mapping = {1: 1, 0: 0, 2: -1}
    return mapping.get(id_trend, "")


@register.filter
def codifica_per_regione(id_sky_condition):
    mapping = {
        "2.00": 3,
        "3.00": 1,
        "4.00": 4,
        "5.00": 4,
        "6.00": 6,
        "7.00": 7,
        "8.00": 5,
        "9.00": 7,
        "11.00": 2,
        "16.00": 2,
        "17.00": 6,
        "18.00": 7,
        "20.00": 8,
        "21.00": 7,
        "22.00": 1,
        "23.00": 9,
        "24.00": 8,
        "25.00": 6,
        "26.00": 7,
        "29.00": 10,
        "30.00": 10,
        "31.00": 10,
        "32.00": 1,
        "33.00": 2,
        "34.00": 10,
        "35.00": 10,
    }
    return mapping.get(
        id_sky_condition, "Invalid id_sky_condition: %s" % id_sky_condition
    )
