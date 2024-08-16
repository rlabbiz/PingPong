import math
import uuid

Rooms = {}
RightPlayer = {}
LeftPlayer = {}
Ball = {}

canvasWidth = 0
canvasHeight = 0

SPEED = 0.1
BALL_START_SPEED = 1


changeSpeed = False

def GetRoomName(roomsNames):
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

def definePlayers(message, roomName):
    global Rooms, canvasWidth, canvasHeight
    Rooms[roomName] = {
        'LeftPlayer': message['LeftPlayer'],
        'RightPlayer': message['RightPlayer'],
        'Ball': message['Ball'],
    }
    canvasWidth = message['canvasWidth']
    canvasHeight = message['canvasHeight']

def handlePlayerMove(message, roomName):
    global Rooms
    if message['dir'] == 'right':
        Rooms[roomName]['RightPlayer']['y'] = message['y']
    else:
        Rooms[roomName]['LeftPlayer']['y'] = message['y']


def collision(ball, player):
    # Ball bounding box
    ball_top = ball['y'] - ball['radius']
    ball_bottom = ball['y'] + ball['radius']
    ball_left = ball['x'] - ball['radius']
    ball_right = ball['x'] + ball['radius']

    # Player bounding box
    player_top = player['y']
    player_bottom = player['y'] + player['height']
    player_left = player['x']
    player_right = player['x'] + player['width']

    # Check for overlap
    return (ball_right > player_left and 
            ball_left < player_right and 
            ball_bottom > player_top and 
            ball_top < player_bottom)

def lerp(a, b, n):
    return (1 - n) * a + n * b

def resetBall(roomName):
    global Rooms
    Rooms[roomName]['Ball']['x'] = canvasWidth / 2
    Rooms[roomName]['Ball']['y'] = canvasHeight / 2
    Rooms[roomName]['Ball']['speed'] = BALL_START_SPEED
    Rooms[roomName]['Ball']['velocityX'] = -Rooms[roomName]['Ball']['velocityX']
    Rooms[roomName]['Ball']['velocityY'] = -Rooms[roomName]['Ball']['velocityY']

def update(roomName):
    global Rooms, changeSpeed
    # Update ball position
    Rooms[roomName]['Ball']['x'] += Rooms[roomName]['Ball']['velocityX'] * Rooms[roomName]['Ball']['speed']
    Rooms[roomName]['Ball']['y'] += Rooms[roomName]['Ball']['velocityY'] * Rooms[roomName]['Ball']['speed']

    # Check for collision with top and bottom walls
    if Rooms[roomName]['Ball']['y'] + Rooms[roomName]['Ball']['radius'] > canvasHeight or Rooms[roomName]['Ball']['y'] - Rooms[roomName]['Ball']['radius'] < 0:
        Rooms[roomName]['Ball']['velocityY'] = -Rooms[roomName]['Ball']['velocityY']

    # Determine which player to check for collision
    player = Rooms[roomName]['RightPlayer'] if Rooms[roomName]['Ball']['x'] < canvasWidth / 2 else Rooms[roomName]['LeftPlayer']

    # Check for collision between ball and player
    if collision(Rooms[roomName]['Ball'], player):
        collide_point = Rooms[roomName]['Ball']['y'] - (player['y'] + player['height'] / 2)
        collide_point /= (player['height'] / 2)

        angle_rad = collide_point * math.pi / 4

        direction = 1 if Rooms[roomName]['Ball']['x'] < canvasWidth / 2 else -1

        Rooms[roomName]['Ball']['velocityX'] = direction * Rooms[roomName]['Ball']['speed'] * math.cos(angle_rad) * 5
        Rooms[roomName]['Ball']['velocityY'] = Rooms[roomName]['Ball']['speed'] * math.sin(angle_rad) * 5

        if Rooms[roomName]['Ball']['speed'] < 1.7 and changeSpeed == True:
            if changeSpeed:
                changeSpeed = False
            Rooms[roomName]['Ball']['speed'] += SPEED
        elif changeSpeed == False:
            changeSpeed = True
            

    # Check if the ball is out of bounds
    if Rooms[roomName]['Ball']['x'] - Rooms[roomName]['Ball']['radius'] < 0:
        Rooms[roomName]['LeftPlayer']['score'] += 1
        resetBall(roomName)
    elif Rooms[roomName]['Ball']['x'] + Rooms[roomName]['Ball']['radius'] > canvasWidth:
        Rooms[roomName]['RightPlayer']['score'] += 1
        resetBall(roomName)

    # Update left player position for AI
    # target_position = Rooms[roomName]['Ball']['y'] - RightPlayer['height'] / 2
    # LeftPlayer['y'] = lerp(LeftPlayer['y'], target_position, .2)
