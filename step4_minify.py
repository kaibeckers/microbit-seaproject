targetClickDelay = 20
fieldSizeX = 5 
fieldSizeY = 5
import random
import time
import microbit
class Field:
    xFieldSize = 5
    yFieldSize = 5
    def __init__(self):
        self.field = {}
        self.field['layer0'] = []
        self.field['layer3'] = [] 
        self.field['layer6'] = []
        self.field['layer9'] = []
    def addShip(self, ship):
        assert isinstance(ship, Ship), 'variable ship must be of type Ship'
        self.field['layer6'].append(ship)
    def addRandomShip(self, type):
        assert type == 'minesweeper' or type == 'submarine' or type == 'cruiser' or type == 'aircraft_carrier', 'value type must be "minesweeper", "submarine", "cruiser" or "aircraft_carrier"'
        size = 1 if type == 'minesweeper' else 2 if type == 'submarine' else 3 if type == 'cruiser' else 4
        safetyLimit = 20
        while safetyLimit > 0:
            safetyLimit -= 1
            rot  = 'vert' if random.randint(0, 1) == 0 else 'hori'
            xPos = getRandomXYValueConstrainted(self.xFieldSize, size, rot)['x']
            yPos = getRandomXYValueConstrainted(self.yFieldSize, size, rot)['y']
            ship = Ship(xPos, yPos, size, rot)
            if self.checkShipConstraint(ship) == True:
                continue
            self.addShip(ship)
            return { 'x': xPos, 'y': yPos, 'rot': rot, 'size': size }
        raise Exception('Safety limit reached, could not place ship')
    def checkShipConstraint(self, ship): 
        assert isinstance(ship, Ship), 'variable ship must be of type Ship'
        tilesToCheck = convertShiptoTiles(ship)
        for tile in tilesToCheck:
            if tile['x'] < 1 or tile['x'] > fieldSizeX or tile['y'] < 1 or tile['y'] > fieldSizeY:
                return True
        ships = self.field['layer6']
        otherShipTilesToCheck = []
        for ship in ships:
            otherShipTilesToCheck += convertShiptoTiles(ship)
        for tile in tilesToCheck:
            if tile in otherShipTilesToCheck:
                print('overlap')
                return True
        return False
    def addPlayer(self, player):
        assert isinstance(player, Player), 'variable player must be of type Player'
        if len(self.field['layer9']) > 0:
            raise AssertionError('Only one player can be added to the field')
        self.field['layer9'].append(player)
    def removeShip(self, ship, layer=6):
        assert isinstance(ship, Ship), 'variable ship must be of type Ship'
        assert layer == 6, 'value layer must be 6'
        self.field['layer' + str(layer)].remove(ship)
    def changeObjectLayer(self, object, fromLayer, toLayer):
        assert fromLayer == 0 or fromLayer == 3 or fromLayer == 6 or fromLayer == 9, 'value fromLayer must be 0, 3, 6 or 9'
        assert toLayer == 0 or toLayer == 3 or toLayer == 6 or toLayer == 9, 'value toLayer must be 0, 3, 6 or 9'

        self.field['layer' + str(toLayer)].append(object)
        self.field['layer' + str(fromLayer)].remove(object)
class Ship:
    def __init__(self, xPos, yPos, size, rot):
        assert rot == 'hori' or rot == 'vert', 'value rot must be "hori" or "vert"'
        assert xPos < (fieldSizeX + 1) and xPos > 0, 'xPos is out of bounds'
        assert yPos < (fieldSizeY + 1) and yPos > 0, 'yPos is out of bounds'
        self.xPos = xPos
        self.yPos = yPos
        self.size = size
        self.rot = rot
class Player:
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
        print(matrix)
        for y, row in enumerate(matrix):
            for x, pixel in enumerate(row):
                # skip over pixels that are already rendered
                previousPixel = microbit.display.get_pixel(x, y)
                if pixel == previousPixel:
                    continue

                # render pixel
                microbit.display.set_pixel(x, y, pixel)
    
    # Render any other object
    def renderOther(self, type, input=None):
        if type == 'x-cross':
            microbit.display.show(microbit.Image.NO, delay=500, clear=True, wait=True)
        elif type == 'skull':
            microbit.display.show(microbit.Image.SKULL, delay=500, clear=True, wait=True)
        elif type == 'win':
            microbit.display.show(microbit.Image.HAPPY, delay=500, clear=True, wait=True)
        elif type == 'text':
            assert input != None, 'input must be a string or integer'
            microbit.display.scroll(str(input), delay=100, wait=True)
        else:
            raise AssertionError('Invalid object to render')

# Functions
# Converts a Ship object to an absolute list of tiles (absolute being relative to the field's 0,0 coords)
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
    possiblePos = max - length + 1 # max field lenght minus the ship length = tiles available for the ship, +1 to fix offset
    if rot == 'vert':
        return { 'x': random.randint(1, max), 'y': random.randint(1, possiblePos)}
    else:
        return { 'x': random.randint(1, possiblePos), 'y': random.randint(1, max)}

# Similar to checkShipConstraint, but returns the ship object that is at the position x, y, otherwhise None, instead of True/False
def getShipFromCoords(field, x, y):
    ships = field.field['layer6']
    for ship in ships:
        tiles = convertShiptoTiles(ship)
        for tile in tiles:
            if tile['x'] == x and tile['y'] == y:
                return ship
    return None

# Fires a shot at a position, returns True/False if a ship was hit
def fire(field, x, y):
    target = getShipFromCoords(field, x, y)
    if target != None:
        if target in field.field['layer6']:
            return True
    return False

# Infinite loop
while True:
    # Init
    # Create new field with ships
    field = Field()
    try:
        field.addRandomShip('minesweeper')      # 1 long
        field.addRandomShip('submarine')        # 2 long
        field.addRandomShip('submarine')        # 2 long
        field.addRandomShip('cruiser')          # 3 long
        field.addRandomShip('aircraft_carrier') # 4 long
    except:
        continue # catch error 'Safety limit reached, could not place ship, skip this iteration and retry

    # Add player
    player = Player()
    field.addPlayer(player)

    # Instantiate renderer
    renderer = Render(field)

    # Variables
    attempts = 0 # how many the fire() function was called
    clickDelay = 0 # button/movement debounce
    callRenderDispatchInNextFrame = True # first frame render must always render

    # Game Loop
    while True:
        # whether a new Frame, or a render call is needed.
        dispatchRender = False # Render a new Frame?
        dispatchShipRender = False # Render the ships in that frame?

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
        elif gesture == 'shake':
            break # exit current game

        # get button input
        buttonAPresses = microbit.button_a.get_presses() # resets to 0 everytime this is called. this is more reliable than is_pressed(), although doesnt work when holding down the button
        buttonBPresses = microbit.button_b.get_presses()
        buttonBPressed = microbit.button_b.is_pressed() # fallback to get_presses when holding down the button
        if buttonAPresses > 0:
            # log attempts
            attempts += 1

            # fire at position
            hit = fire(field, player.xPos, player.yPos) # boolean
            if hit == True:
                field.changeObjectLayer(getShipFromCoords(field, player.xPos, player.yPos), 6, 3)
                renderer.renderOther('skull')
                time.sleep(0.1)
                renderer.renderOther('text', 'HIT')
                time.sleep(0.1)
                callRenderDispatchInNextFrame = True

                # check if all ships are dead, and win
                if len(field.field['layer6']) < 1:
                    renderer.renderOther('win')
                    time.sleep(0.1)
                    renderer.renderOther('text', 'WIN!')
                    time.sleep(0.1)
                    renderer.renderOther('text', 'Attempts: ' + str(attempts))
                    callRenderDispatchInNextFrame = True
                    break # exit and restart
            else:
                renderer.renderOther('x-cross')
                time.sleep(0.1)
                renderer.renderOther('text', 'MISS')
                time.sleep(0.1)
                callRenderDispatchInNextFrame = True
        if buttonBPresses > 0 or buttonBPressed == True:
            dispatchRender = True
            dispatchShipRender = True
            callRenderDispatchInNextFrame = True

        # render the frame, Matrix only. Some events have their own render call, namely the Button A press 'listener'.
        if dispatchRender:
            renderer.renderMatrix([3, 9])
        if dispatchRender and dispatchShipRender:
            renderer.renderMatrix([3, 6, 9])

        # sleep for 50ms (20fps)
        time.sleep(0.05)
