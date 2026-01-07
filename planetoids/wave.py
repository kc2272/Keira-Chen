"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in
the Planetoids game. Instances of Wave represent a single level, and should
correspond to a JSON file in the Data directory. Whenever you move to a new
level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on
screen. These are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue. If you do not know, ask on Ed Discussions and we will answer.

# Keira Chen (kc2272) and Henry Yoon (hjy22)
# December 9, 2024
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.

    This subcontroller has a reference to the ship, asteroids, and any bullets
    on screen. It animates all of these by adding the velocity to the position
    at each step. It checks for collisions between bullets and asteroids or
    asteroids and the ship (asteroids can safely pass through each other). A
    bullet collision either breaks up or removes a asteroid. A ship collision
    kills the player.

    The player wins once all asteroids are destroyed. The player loses if they
    run out of lives. When the wave is complete, you should create a NEW instance
    of Wave (in Planetoids) if you want to make a new wave of asteroids.

    If you want to pause the game, tell this controller to draw, but do not
    update. See subcontrollers.py from Lecture 25 for an example. This class
    will be similar to than one in many ways.

    All attributes of this class are to be hidden. No attribute should be
    accessed without going through a getter/setter first. However, just because
    you have an attribute does not mean that you have to have a getter for it.
    For example, the Planetoids app probably never needs to access the attribute
    for the bullets, so there is no need for a getter there. But at a minimum,
    you need getters indicating whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _bullet_frame_count: # of frames since the player has fired
    # Invariant: _bullet_frame_count is an int >= 0
    #
    # Attribute _win: Whether or not the player won the game
    # Invariant: _win is a boolean; True if the player won, False if the player
    #            lost, None if the game is still in progress

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWin(self):
        """
        Returns whether or not the player won the game (True if yes, False if no)
        """
        return self._win

    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self, json):
        """
        Initializes the initial wave state: ship, asteroids, and bullets

        Parameter json: contains data for the wave's Ship and Asteroid objects.
        Precondition: json is a JSON file
        """
        self._data = json
        self._ship = Ship(self._data)
        self._asteroids = []

        self._bullets = []
        self._bullet_frame_count = 0

        self._win = None

        for x in self._data['asteroids']:
            self._asteroids += [Asteroid(x)]

    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self, input):
        """
        Changes the wave during each game through user inputs

        Logs user input to change the ship's x position, y position,
        direction, and to shoot bullets. In the absence of input, objects
        will continue to move around the screen or wrap to the other side
        if they go off screen. This function also deletes two objects on
        the game screen if they collide. If an asteroid has a collision,
        it will break.

        Parameter input: the keyboard input passed from Planetoids
        Precondition: input is the GInput object
        """
        if not self._ship is None and len(self._asteroids) != 0:
            if input.is_key_down('left'):
                self._ship.turn(SHIP_TURN_RATE)
            elif input.is_key_down('right'):
                self._ship.turn(-SHIP_TURN_RATE)
            elif input.is_key_down('up'):
                self._ship.impulse()
            self._move(self._ship)
            self._shootBullets(input)
            for ast in self._asteroids:
                self._move(ast)
                for bul in self._bullets:
                    if self._collision(ast, bul):
                        self._asteroids.remove(ast)
                        self._bullets.remove(bul)
                        self._asteroids += self._breakAsteroid(ast, bul)
            i = 0
            remaining = len(self._asteroids)
            while self._ship != None and i < remaining:
                ast = self._asteroids[i]
                if self._collision(self._ship, ast):
                    self._asteroids.remove(ast)
                    remaining -= 1
                    self._ship = None
                else:
                    i += 1
        else:
            self._win = False if self._ship == None else True

    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self, view, app):
        """
        Draws the current game state.

        The game state includes the ship, asteroids, and bullets. It will also
        display "Game Over" or "You Win" when the game completes.

        Parameter view: the game view passed from Planetoids
        Parameter app: the controller for the game (in this case, Planetoids)
        Precondition: view must be a GView object
        Precondition: app must be a GameApp object
        """
        if self._ship != None and self._asteroids != []:
            self._ship.draw(view)
            for ast in self._asteroids:
                ast.draw(view)
            for bul in self._bullets:
                bul.draw(view)
        else:
            if self._win == False:
                message = "GAME OVER"
            else:
                message = "YOU WIN!"
            end = GLabel(text = message, font_size = TITLE_SIZE,
                font_name = TITLE_FONT, x = app.width/2, y = app.height/2 + 50)
            end.draw(view)

    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def _move(self, object):
        """
        Moves objects around on screen and wraps objects if they go off screen.

        Objects move at a constant velocity. If the object's center exits the
        dead zone, it "wraps" to the other side and reappears on screen.

        Parameter object: the object (Ship or Asteroid) to be moved
        Precondition: object is a Ship or Asteroid object
        """
        #move normally
        object.setX(object.getX() + object.getVelocity().x)
        object.setY(object.getY() + object.getVelocity().y)

        #horizontal wrap
        if object.getX() >= GAME_WIDTH + 2*DEAD_ZONE:
            object.setX(-DEAD_ZONE)
        elif object.getX() < -DEAD_ZONE:
            object.setX(GAME_WIDTH + 2*DEAD_ZONE)

        #vertical wrap
        if object.getY() >= GAME_WIDTH + 2*DEAD_ZONE:
            object.setY(-DEAD_ZONE)
        elif object.getY() < -DEAD_ZONE:
            object.setY(GAME_WIDTH + 2*DEAD_ZONE)

    def _rotate(self, vect, ang):
        """
        Returns a new vector as the result of rotating a vector by a given angle

        Parameter vect: the vector to be rotated
        Parameter ang: the angle that vect is to be rotated by
        Precondition: vect is a Vector2 object
        Precondition: ang is an int or float
        """
        x = vect.x*math.cos(ang) - vect.y*math.sin(ang)
        y = vect.x*math.sin(ang) + vect.y*math.cos(ang)
        return Vector2(x, y)

    def _collision(self, object, other):
        """
        Returns True or False based on if two objects' positions overlap

        Parameter object: an object that can collide
        Parameter other: another object that can collide
        Precondition: object is an Asteroid, Ship, or Bullet object
        Precondition: other is an Asteroid, Ship, or Bullet object
        """
        d = math.sqrt((object.getX() - other.getX())**2
                    + (object.getY() - other.getY())**2)
        if d <= object.getWidth() / 2 + other.getWidth() / 2 :
            return True
        else:
            return False

    def _breakAsteroid(self, ast, bul):
        """
        Returns list of new Asteroid objects resulting from asteroid collision

        This method calculates the resultant vectors for each of the smaller
        asteroids that result from the collision, then initializes them and
        returns them in a list.

        Parameter ast: an asteroid that was hit by a bullet
        Parameter bul: the bullet that hit the asteroid
        Precondition: ast is an Asteroid object
        Precondition: bul is a Bullet object
        """
        colVector = bul.getVelocity().normalize()
        result1 = colVector
        result2 = self._rotate(colVector, (2/3)*math.pi)
        result3 = self._rotate(colVector, -(2/3)*math.pi)

        if ast.getSize() == 'large':
            s = 'medium'
            radius = MEDIUM_RADIUS
        elif ast.getSize() == 'medium':
            s = 'small'
            radius = SMALL_RADIUS
        elif ast.getSize() == 'small':
            return []

        x1 = result1.__mul__(radius).x + ast.getX()
        y1 = result1.__mul__(radius).y + ast.getY()
        x2 = result2.__mul__(radius).x + ast.getX()
        y2 = result2.__mul__(radius).y + ast.getY()
        x3 = result3.__mul__(radius).x + ast.getX()
        y3 = result3.__mul__(radius).y + ast.getY()

        dict1 = {"size":s,"position":[x1,y1],"direction":[result1.x,result1.y]}
        dict2 = {"size":s,"position":[x2,y2],"direction":[result2.x,result2.y]}
        dict3 = {"size":s,"position":[x3,y3],"direction":[result3.x,result3.y]}

        return [Asteroid(dict1), Asteroid(dict2), Asteroid(dict3)]

    def _shootBullets(self, input):
        """
        Initializes and updates bullets, and removes bullets out of frame.

        This method initializes bullets when the space bar is pressed, keeping
        track of the firing rate by incrementing _bullet_frame_count and comparing
        it to BULLET_RATE, and adds the bullets to _bullets. When the bullets
        go off screen and exit the dead zone, they are removed from _bullets.

        Parameter input: the keyboard input passed from Planetoids
        Precondition: input must be a GInput object
        """
        self._bullet_frame_count += 1
        if input.is_key_down('spacebar'):
            if self._bullet_frame_count >= BULLET_RATE:
                self._bullet_frame_count = 0

                xpos = self._ship.getX() + self._ship.getFacing().x *SHIP_RADIUS
                ypos = self._ship.getY() + self._ship.getFacing().y *SHIP_RADIUS
                vx = self._ship.getFacing().x * BULLET_SPEED
                vy = self._ship.getFacing().y * BULLET_SPEED

                bullet = Bullet(x = xpos, y = ypos, velocity = Vector2(vx, vy))
                self._bullets.append(bullet)

        present_bullets = []
        for bul in self._bullets:
            bul.x += bul.getVelocity().x
            bul.y += bul.getVelocity().y
            if ((-DEAD_ZONE <= bul.x <= GAME_WIDTH + DEAD_ZONE) and
            (-DEAD_ZONE <= bul.y <= GAME_HEIGHT + DEAD_ZONE)):
                present_bullets.append(bul)
        self._bullets = present_bullets
