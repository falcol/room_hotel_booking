import json

import aioredis
from channels.generic.websocket import AsyncWebsocketConsumer
from decouple import config


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        try:
            self.redis = await aioredis.create_redis_pool(config("REDIS_URI"))
            self.response = await self.redis.subscribe(channel=f"notify_{self.room_name}")
            channel = self.response[0]
            print("Connect to redis")
            while await channel.wait_message():
                print("Vao 3")
                raw_event = await channel.get(encoding="utf8")
                try:
                    event = json.loads(raw_event)
                except json.JSONDecodeError as e:
                    print(f"[{self.room_name}]Event '{raw_event}' was ignored. Decode failed")
                    await self.send(text_data=raw_event)
                    continue
                else:
                    await self.send(text_data=raw_event)
        except Exception as e:
            print(f"User {self.room_name} Disconnected")
            print(e)
        finally:
            self.redis.close()
            await self.redis.wait_closed()
            print("Redis closed successfully")

        print("Joined chat room %s" % self.room_name)
        print("Joined chat group: %s" % self.room_group_name)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "data": text_data_json})

    # Receive message from room group
    async def chat_message(self, event):
        message = event["data"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
