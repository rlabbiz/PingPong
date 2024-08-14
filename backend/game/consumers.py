import json
from channels.generic.websocket import AsyncWebsocketConsumer

roomsNames = {}

def GetRoomName():
    for id, room in roomsNames.items():
        if room['isFree']:
            room['isFree'] = False
            return room['name']
    new_room_id = len(roomsNames) + 1
    roomsNames[new_room_id] = {
        'name': "room" + str(new_room_id),
        'isFree': True
    }
    return roomsNames[new_room_id]['name']

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = GetRoomName()
        self.room_group_name = 'game_' + self.room_name
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': {
                    'type': 'playerDIr',
                    'dir': 'left',
                }
            }
        )
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )
    
    async def game_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
