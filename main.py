# Imports
import random
from microbit import *

# todo, snake_case not camelCase

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
    
    # add Ship (bypasses checkShipConstraint)
    def addShip(self, ship):
        assert isinstance(ship, Ship), 'variable ship must be of type Ship'

        # append to layer 6
        self.field['layer6'].append(ship)

    # add random Ship x, y, rot. size is determined by type
    def addRandomShip(self, type):
        assert type == 'minesweeper' or type == 'submarine' or type == 'cruiser' or type == 'aircraft_carrier', 'value type must be "minesweeper", "submarine", "cruiser" or "aircraft_carrier"'

        # define size pre-emptively 
        size = 1 if type == 'minesweeper' else 2 if type == 'submarine' else 3 if type == 'cruiser' else 4

        # request loop (overlap will restart loop), safetyLimit = 10
        safetyLimit = 20
        while safetyLimit > 0:
            safetyLimit -= 1

            # get random position and rotation
            rot  = 'vert' if random.randint(0, 1) == 0 else 'hori'
            xPos = getRandomXYValueConstrainted(self.xFieldSize, size, rot)['x']
            yPos = getRandomXYValueConstrainted(self.yFieldSize, size, rot)['y']

            # check if ship can be placed
            ship = Ship(xPos, yPos, size, rot)
            if self.checkShipConstraint(ship) == True:
                continue

            # append to the Field
            self.addShip(ship)

            # return success
            return { 'x': xPos, 'y': yPos, 'rot': rot, 'size': size }

        raise Exception('Safety limit reached, could not place ship')

    # check if input ship overlaps with any other ship already in the field (returns True/False)
    def checkShipConstraint(self, ship): 
        assert isinstance(ship, Ship), 'variable ship must be of type Ship'

        tilesToCheck = convertShiptoTiles(ship)

        # ensure the entire ship is within bounds
        for tile in tilesToCheck:
            if tile['x'] < 1 or tile['x'] > 5 or tile['y'] < 1 or tile['y'] > 5:
                return True

        # convert Ships in layer 6 to tiles
        ships = self.field['layer6']
        otherShipTilesToCheck = []
        for ship in ships:
            otherShipTilesToCheck += convertShiptoTiles(ship)

        # check for overlap
        for tile in tilesToCheck:
            if tile in otherShipTilesToCheck:
                print('overlap')
                return True
            
        return False
   
    # add Player
    def addPlayer(self, player):
        assert isinstance(player, Player), 'variable player must be of type Player'
        if len(self.field['layer9']) > 0:
            raise AssertionError('Only one player can be added to the field')

        self.field['layer9'].append(player)

    # remove Ship
    def removeShip(self, ship, layer=6):
        assert isinstance(ship, Ship), 'variable ship must be of type Ship'
        assert layer == 6, 'value layer must be 6'
        self.field['layer' + str(layer)].remove(ship)

    # move object between layers
    def moveObject(self, object, fromLayer, toLayer):
        assert fromLayer == 0 or fromLayer == 3 or fromLayer == 6 or fromLayer == 9, 'value fromLayer must be 0, 3, 6 or 9'
        assert toLayer == 0 or toLayer == 3 or toLayer == 6 or toLayer == 9, 'value toLayer must be 0, 3, 6 or 9'

        self.field['layer' + str(toLayer)].append(object)
        self.field['layer' + str(fromLayer)].remove(object)

# Ship class, contains the position, size and rotation of a ship. Manages ship death and hit detection. Child of the Field class
class Ship:
    # init
    def __init__(self, xPos, yPos, size, rot):
        assert rot == 'hori' or rot == 'vert', 'value rot must be "hori" or "vert"'
        assert xPos < 6 and xPos > 0, 'xPos is out of bounds'
        assert yPos < 6 and yPos > 0, 'yPos is out of bounds'

        # set values
        self.xPos = xPos
        self.yPos = yPos
        self.size = size
        self.rot = rot # rotation (hori/vert)

# Player class, manages Player position, etc. Note: Needs to be added to the Field class manually
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

    # Set the player's position
    def setPosition(self, x, y):
        assert x < 6 and x > 0, 'x is out of bounds'
        assert y < 6 and y > 0, 'y is out of bounds'
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
        matrix = [[0]*5 for i in range(5)]
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


        # generate matrix for layer 3
        for ship in layer3:
            tiles = convertShiptoTiles(ship)
            for tile in tiles:
                # 2d matrix
                matrix[tile['y'] - 1][tile['x'] - 1] = 3
        
        # generate matrix for layer 6
        for ship in layer6:
            tiles = convertShiptoTiles(ship)
            for tile in tiles:
                # 2d matrix
                matrix[tile['y'] - 1][tile['x'] - 1] = 6

        # generate matrix for layer 9
        for player in layer9:
            matrix[player.yPos - 1][player.xPos - 1] = 9

        return matrix
    
    # renders the pixelMatrix returned by __generatePixelMatrix
    def renderMatrix(self, layers):
        matrix = self.__generatePixelMatrix(layers)
        microbit.display.clear()
        for row in matrix:
            for pixel in row:
                microbit.display.set_pixel(row.index(pixel), matrix.index(row), pixel)
    
    # Render any other object
    def renderOther(type, input=None):
        if type == 'x-cross':
            microbit.display.show(Image.NO)
        elif type == 'skull':
            microbit.display.show(Image.SKULL)
        elif type == 'text':
            assert input != None, 'input must be a string or integer'
            pass
        elif type == 'win':
            pass
        else:
            raise AssertionError('Invalid object to render')

# Functions
# Converts a Ship object to an absolute list of tiles (absolute being relative to the field's 1,1 coords)
def convertShiptoTiles(ship):
    tiles = []

    # get all tiles of ship
    for i in range(ship.size):
        if ship.rot == 'vert':
            tiles.append({'x': ship.xPos, 'y': ship.yPos + i})
        else:
            tiles.append({'x': ship.xPos + i, 'y': ship.yPos})
    return tiles

# Returns a random x and y value between 1 and 5 (for use on Field > addRandomShip)
def getRandomXYValue():
    return { 'x': random.randint(1, 5), 'y': random.randint(1, 5)}

# Returns a random x and y value between 1 and 5, but has a maxFieldSize and a length (length of the ship). This ensures the ship is within bounds of the player field.
def getRandomXYValueConstrainted(max, length, rot):
    possiblePos = max - length + 1
    if rot == 'vert':
        return { 'x': random.randint(1, max), 'y': random.randint(1, possiblePos)}
    else:
        return { 'x': random.randint(1, possiblePos), 'y': random.randint(1, max)}

# Init
field = Field()
field.addRandomShip('minesweeper')      # 1 long
field.addRandomShip('submarine')        # 2 long
field.addRandomShip('submarine')        # 2 long
field.addRandomShip('cruiser')          # 3 long
field.addRandomShip('aircraft_carrier') # 4 long

player = Player()
field.addPlayer(player)

renderer = Render(field)
renderer.renderMatrix([3, 6, 9])

# Indefinite loop
while True:
    # whether a new Frame, or a render call is needed.
    dispatchRender = False

    # get user movement input
    gesture = microbit