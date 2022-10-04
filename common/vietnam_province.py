import orjson
from vietnam_provinces import NESTED_DIVISIONS_JSON_PATH


def vietnam_province():
    data = orjson.loads(NESTED_DIVISIONS_JSON_PATH.read_bytes())

    result = ((i.get('code'), i.get('name')) for i in data)

    return result


data = vietnam_province()

print(data)
