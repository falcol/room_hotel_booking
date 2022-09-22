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