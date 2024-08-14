import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import game


# This dictionary will store the room name as key and the number of players in the room as value
roomsNames = {}

# Constants
# Game
WINNING_SCORE = 10

# ball
BALL_START_SPEED = 1
BALL_MAX_SPEED = 10
SPEED = .1
BALL_RADIUS = 10



# this class will handle the websocket connection
class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = game.GetRoomName(roomsNames)
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
                'message': "message"
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
        if message['type'] == 'definePlayer':
            game.definePlayers(message)
        elif message['type'] == 'update':
            game.update()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_message',
                    'message': {
                        'type': 'render',
                        'RightPlayer': game.RightPlayer,
                        'LeftPlayer': game.LeftPlayer,
                        'Ball': game.Ball
                    }
                }
            )
        elif message['type'] == 'playerMove':
            game.handlePlayerMove(message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_message',
                    'message': {
                        'type': 'playerMove',
                        'RightPlayer': game.RightPlayer,
                        'LeftPlayer': game.LeftPlayer,
                    }
                }
            )

        
    async def game_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
