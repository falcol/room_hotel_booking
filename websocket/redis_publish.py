import json

import redis
from decouple import config


def publish_event(channel, event):
    r = redis.Redis.from_url(config("REDIS_URI"))
    pub = r.publish(channel=channel, message=json.dumps(event))
    return pub
