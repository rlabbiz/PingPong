import math

RightPlayer = {}
LeftPlayer = {}
Ball = {}

canvasWidth = 0
canvasHeight = 0

SPEED = 0.1
BALL_START_SPEED = 1


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
    # Ball['y'] += Ball['velocityY'] * Ball['speed']

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

        Ball['velocityX'] = direction * Ball['speed'] * math.cos(angle_rad) * 8
        Ball['velocityY'] = Ball['speed'] * math.sin(angle_rad) * 8

        # Ball.speed += 1  # Uncomment if you want to increase speed
        # Ball.velocityX = -Ball.velocityX  # Uncomment if you want to reverse X velocity
        Ball['speed'] += SPEED

    # Check if the ball is out of bounds
    if Ball['x'] - Ball['radius'] < 0:
        LeftPlayer['score'] += 1
        resetBall()
        print(Ball['speed'])
    elif Ball['x'] + Ball['radius'] > canvasWidth:
        RightPlayer['score'] += 1
        resetBall()
        print(Ball['speed'])
    #    print("{.2f}".format(Ball['speed']))

    # Update left player position for AI
    target_position = Ball['y'] - RightPlayer['height'] / 2
    LeftPlayer['y'] = lerp(LeftPlayer['y'], target_position, .2)
