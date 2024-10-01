import locale

from django import template

locale.setlocale(locale.LC_TIME, "it_IT.UTF8")
register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name="format")
def format(value, fmt):
    if value is not None:
        return fmt.format(float(value))
    else:
        return ""
