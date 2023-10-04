from django import template
from time import strftime, localtime

register = template.Library()

# Format value as USD
@register.filter(name='usd')
def usd(value):
    return f"${value:,.0f}"

# Convert server time to local time
@register.filter(name="local_time")
def time(value):
    return strftime('%d.%m.%Y %H:%M', localtime(value.timestamp()))

# Reverse list
@register.filter(name="reverse")
def reverse(value):
    return value[::-1]

# Return 1 if listing in watchlist or 0 if not
@register.filter(name="watch")
def watch(watchlist, user_id):
    try:
        for x in list(watchlist):
            if x["user_id_id"] == user_id:
                return 1
        return 0
    except IndexError:
        return 0