# env
targetClickDelay = 20 # how many frames to wait before registering a new button press
fieldSizeX = 5 
fieldSizeY = 5

# Imports
import random
import microbit
import time

# was gonna do snake_case as per pep8, but as per the coteach guidelines, I'm doing camelCase

# Classes
# Field class, contains all ships, users and their positions
class Field:
    xFieldSize = 5
    yFieldSize = 5

    # init
    def __init__(self):
        self.field = {}
        self.field['layer0'] = [] # layer 0
        self.field['layer3'] = [] 
        self.field['layer6'] = [] # { Ship }
        self.field['layer9'] = []

    # add Player
    def addPlayer(self, player):
        assert isinstance(player, Player), 'variable player must be of type Player'
        if len(self.field['layer9']) > 0:
            raise AssertionError('Only one player can be added to the field')

        self.field['layer9'].append(player)

# Player class, manages Player position, etc. Needs to be added to the Field class manually, functions as a child of the Field class
class Player:
    # init
    def __init__(self):
        self.xPos = 1
        self.yPos = 1

    # Move the player in a direction
    def move(self, direction):
        assert direction == 'up' or direction == 'down' or direction == 'left' or direction == 'right', 'value direction must be "up", "down", "left" or "right"'

        if direction == 'up':
            self.yPos -= 1
        elif direction == 'down':
            self.yPos += 1
        elif direction == 'left':
            self.xPos -= 1
        elif direction == 'right':
            self.xPos += 1

        # ensure player is within bounds
        if self.xPos < 1:
            self.xPos = 1
        elif self.xPos > fieldSizeX:
            self.xPos = fieldSizeX
        if self.yPos < 1:
            self.yPos = 1
        elif self.yPos > fieldSizeY:
            self.yPos = fieldSizeX

    # Set the player's position
    def setPosition(self, x, y):
        assert x < (fieldSizeX + 1) and x > 0, 'x is out of bounds'
        assert y < (fieldSizeY + 1) and y > 0, 'y is out of bounds'
        self.xPos = x
        self.yPos = y

    # Get the player's position
    def getPosition(self):
        return { 'x': self.xPos, 'y': self.yPos }

# Rendering class, renders everything to the screen.
class Render:
    # init
    def __init__(self, field):
        assert isinstance(field, Field), 'variable field must be of type Field'
        self.field = field

    # generate a 5x5 matrix of pixels, each pixel represents a ship or player. 2d array.
    def __generatePixelMatrix(self, layers):
        matrix = [[0]*fieldSizeX for i in range(fieldSizeY)]
        field = self.field.field
        layer3 = field['layer3']
        layer6 = field['layer6']
        layer9 = field['layer9']

        # skip over layers the function caller doesn't want
        if not 3 in layers:
            layer3 = []
        if not 6 in layers:
            layer6 = []
        if not 9 in layers:
            layer9 = []

        # todo: ships

        # generate matrix for layer 9
        for player in layer9:
            matrix[player.yPos - 1][player.xPos - 1] = 9

        return matrix
    
    # renders the pixelMatrix returned by __generatePixelMatrix
    def renderMatrix(self, layers):
        matrix = self.__generatePixelMatrix(layers)
        print(matrix)
        for y, row in enumerate(matrix):
            for x, pixel in enumerate(row):
                microbit.display.set_pixel(x, y, pixel)

# Functions
# Todo

# Init
# Create new field with ships
field = Field()

# Add player
player = Player()
field.addPlayer(player)

# Instantiate renderer
renderer = Render(field)

# Variables
clickDelay = 0 # button/movement debounce
callRenderDispatchInNextFrame = True # first frame render must always render

# Game Loop
while True:
    # whether a new Frame, or a render call is needed.
    dispatchRender = False # Render a new Frame?

    # sometimes the next frame needs to be rendered too. the previous iteration will set this to True if needed.
    if callRenderDispatchInNextFrame == True: 
        dispatchRender = True
        callRenderDispatchInNextFrame = False

    # decrease clickDelay (button debounce)
    if clickDelay > 0:
        clickDelay -= 1

    # get user movement input
    gesture = microbit.accelerometer.current_gesture()
    if gesture == 'up':
        if not clickDelay > 0:
            player.move('up')
            dispatchRender = True
            clickDelay = targetClickDelay # 20
    elif gesture == 'down':
        if not clickDelay > 0:
            player.move('down')
            dispatchRender = True
            clickDelay = targetClickDelay
    elif gesture == 'left':
        if not clickDelay > 0:
            player.move('left')
            dispatchRender = True
            clickDelay = targetClickDelay
    elif gesture == 'right':
        if not clickDelay > 0:
            player.move('right')
            dispatchRender = True
            clickDelay = targetClickDelay

    # render the frame
    if dispatchRender:
        renderer.renderMatrix([9])

    # sleep for 50ms (20fps)
    time.sleep(0.05)
