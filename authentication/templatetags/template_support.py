from datetime import datetime

from dateutil.parser import parse
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def to_str(data):
    return str(data)


@register.filter
def check_date(date_1, date_2):
    if date_1 is None or date_1 == "":
        return date_2
    return date_1


@register.filter
def check_value_none(data):
    if data:
        return data
    return ""


@register.filter
def check_number_none(data):
    if data:
        return data
    return 0


@register.filter
def get_full_room_status(data):
    ROOM_STATUS = {'E': 'Trống', 'C': 'Đang dọn', 'L': 'Cho thuê', 'B': 'Đã đặt'}
    return ROOM_STATUS.get(data, "")


@register.filter
def format_datetime_local(date):
    if date:
        date = parse(str(date))
        result = datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
        return result
    return ""
