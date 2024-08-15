import math
import uuid

RightPlayer = {}
LeftPlayer = {}
Ball = {}

canvasWidth = 0
canvasHeight = 0

SPEED = 0.1
BALL_START_SPEED = 1


def GetRoomName(roomsNames):
    # Check for an available room
    for room_id, room in roomsNames.items():
        if room['isFree']:
            room['isFree'] = False
            return room['name']
    
    # If no free room is available, create a new one
    new_room_id = str(uuid.uuid4())  # Generate a unique room ID using UUID
    roomsNames[new_room_id] = {
        'name': f"room_{new_room_id}",
        'isFree': False
    }
    
    return roomsNames[new_room_id]['name']

def definePlayers(message):
    global RightPlayer, LeftPlayer, Ball, canvasWidth, canvasHeight
    LeftPlayer = message['LeftPlayer']
    RightPlayer = message['RightPlayer']
    Ball = message['Ball']
    canvasWidth = message['canvasWidth']
    canvasHeight = message['canvasHeight']

def handlePlayerMove(message):
    global RightPlayer, LeftPlayer
    if message['dir'] == 'right':
        RightPlayer['y'] = message['y']
    else:
        LeftPlayer['y'] = message['y']


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

def resetBall():
    Ball['x'] = canvasWidth / 2
    Ball['y'] = canvasHeight / 2
    Ball['speed'] = BALL_START_SPEED
    Ball['velocityX'] = -Ball['velocityX']
    Ball['velocityY'] = -Ball['velocityY']

def update():
    global RightPlayer, LeftPlayer, Ball
    # Update ball position
    Ball['x'] += Ball['velocityX'] * Ball['speed']
    Ball['y'] += Ball['velocityY'] * Ball['speed']

    # Check for collision with top and bottom walls
    if Ball['y'] + Ball['radius'] > canvasHeight or Ball['y'] - Ball['radius'] < 0:
        Ball['velocityY'] = -Ball['velocityY']

    # Determine which player to check for collision
    player = RightPlayer if Ball['x'] < canvasWidth / 2 else LeftPlayer

    # Check for collision between ball and player
    if collision(Ball, player):
        collide_point = Ball['y'] - (player['y'] + player['height'] / 2)
        collide_point /= (player['height'] / 2)

        angle_rad = collide_point * math.pi / 4

        direction = 1 if Ball['x'] < canvasWidth / 2 else -1

        Ball['velocityX'] = direction * Ball['speed'] * math.cos(angle_rad) * 5
        Ball['velocityY'] = Ball['speed'] * math.sin(angle_rad) * 5

        # Ball.speed += 1  # Uncomment if you want to increase speed
        # Ball.velocityX = -Ball.velocityX  # Uncomment if you want to reverse X velocity
        # if Ball['speed'] < 1.8:
        Ball['speed'] += SPEED

    # Check if the ball is out of bounds
    if Ball['x'] - Ball['radius'] < 0:
        LeftPlayer['score'] += 1
        resetBall()
    elif Ball['x'] + Ball['radius'] > canvasWidth:
        RightPlayer['score'] += 1
        resetBall()

    # Update left player position for AI
    # target_position = Ball['y'] - RightPlayer['height'] / 2
    # LeftPlayer['y'] = lerp(LeftPlayer['y'], target_position, .2)
