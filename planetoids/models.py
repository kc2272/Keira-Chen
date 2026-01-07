"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that
you interact with on the screen is model: the ship, the bullets, and the
planetoids.

We need models for these objects because they contain information beyond the
simple shapes like GImage and GEllipse. In particular, ALL of these classes
need a velocity representing their movement direction and speed (and hence they
all need an additional attribute representing this fact). But for the most part,
that is all they need. You will only need more complex models if you are adding
advanced features like scoring.

You are free to add even more models to this module. You may wish to do this
when you add new features to your game, such as power-ups. If you are unsure
about whether to make a new class or not, please ask on Ed Discussions.

# Keira Chen (kc2272) and Henry Yoon (hjy22)
# December 9, 2024
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a
# parameter in your method, and Wave should pass it as a argument when it calls
# the method.


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship

    Bullets are typically just white circles (ellipses). The size of the bullet
    is determined by constants in consts.py. However, we MUST subclass GEllipse,
    because we need to add an extra attribute for the velocity of the bullet.

    The class Wave will need to look at this velocity, so you will need getters
    for the velocity components. However, it is possible to write this assignment
    with no setters for the velocities. That is because the velocity is fixed
    and cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set the
    starting velocity. This __init__ method will need to call the __init__ from
    GEllipse as a helper. This init will need a parameter to set the direction
    of the velocity.

    You also want to create a method to update the bolt. You update the bolt by
    adding the velocity to the position. While it is okay to add a method to
    detect collisions in this class, you may find it easier to process
    collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: The velocity of the bullet
    # Invariant: _velocity is a Vector2 object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns a Bullet object's velocity
        """
        return self._velocity

    def getX(self):
        """
        Returns a Bullet object's x component of position
        """
        return self.x

    def getY(self):
        """
        Returns a Bullet object's y component of position
        """
        return self.y

    def getWidth(self):
        """
        Returns a Bullet object's width
        """
        return self.width

    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self, x, y, velocity):
        """
        Initializes a Bullet with given values for position and velocity

        Precondition: x is an int or float
        Precondition: y is an int or float
        Precondition: velocity is a Vector2 object
        """
        super().__init__(x=x,y=y,width=2*BULLET_RADIUS,height=2*BULLET_RADIUS,
                        fillcolor=BULLET_COLOR)
        self._velocity = Vector2(velocity.x, velocity.y)

    #bullet position is updated in wave.py _shootBullets method


class Ship(GImage):
    """
    A class to represent the game ship.

    This ship is represented by an image. The size of the ship is determined by
    constants in consts.py. However, we MUST subclass GEllipse, because we need
    to add an extra attribute for the velocity of the ship, as well as the facing
    vector (not the same) thing.

    The class Wave will need to access these two values, so you will need getters
    for them. But per the instructions,these values are changed indirectly by
    applying thrust or turning the ship. That means you won't want setters for
    these attributes, but you will want methods to apply thrust or turn the ship.

    This class needs an __init__ method to set the position and initial facing
    angle. This information is provided by the wave JSON file. Ships should
    start with a shield enabled.

    Finally, you want a method to update the ship. When you update the ship, you
    apply the velocity to the position. While it is okay to add a method to
    detect collisions in this class, you may find it easier to process collisions
    in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _facing: The facing angle of the ship
    # Invariant: _facing is a Vector2 object
    #
    # Attribute _velocity: The velocity of the ship
    # Invariant: _velocity is a Vector2 object


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getFacing(self):
        """
        Returns the direction the ship is facing (facing vector)
        """
        return self._facing

    def getX(self):
        """
        Returns a Ship object's x component of position
        """
        return self.x

    def setX(self, x):
        """
        Sets the x position of the ship to the given value

        Precondition: x must be an int or float
        """
        self.x = x

    def getY(self):
        """
        Returns a Ship object's y component of position
        """
        return self.y

    def setY(self, y):
        """
        Sets the y position of the ship to the given value

        Precondition: y must be an int or float
        """
        self.y = y

    def getWidth(self):
        """
        Returns a Ship object's width
        """
        return self.width

    def getVelocity(self):
        """
        Returns a Ship object's velocity
        """
        return self._velocity

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, json):
        """
        Initializes Ship with attributes stored in provided JSON file

        Parameter json: contains the ship's position and angle
        Precondition: json is a JSON file
        """
        xpos = json['ship']['position'][0]
        ypos = json['ship']['position'][1]
        ang = json['ship']['angle']
        w = 2 * SHIP_RADIUS
        h = 2 * SHIP_RADIUS
        src = SHIP_IMAGE
        super().__init__(x = xpos, y = ypos, angle = ang, width = w,
            height = h, source = src)
        self._velocity = Vector2(0, 0)

        #conversion
        radTheta = ang * (1/360) * 2 * math.pi
        self._facing = Vector2(math.cos(radTheta), math.sin(radTheta))

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def turn(self, ang):
        """
        Changes the direction the ship is facing

        Parameter ang: the angle to change the facing vector by
        Precondition: ang is an int or float
        """
        self.angle = self.angle + ang
        radTheta = self.angle * (1/360) * 2 * math.pi
        self._facing = Vector2(math.cos(radTheta), math.sin(radTheta))

    def impulse(self):
        """
        Alters the magnitude of the ship's velocity (capped at SHIP_MAX_SPEED)
        """
        imp = self._facing.__mul__(SHIP_IMPULSE)
        vel = self._velocity.__add__(imp)
        if (vel.length() >= SHIP_MAX_SPEED):
            self._velocity = vel.normalize().__mul__(SHIP_MAX_SPEED)
        else:
            self._velocity = vel

    #ship position is updated in wave.py _move method


class Asteroid(GImage):
    """
    A class to represent a single asteroid.

    Asteroids are typically are represented by images. Asteroids come in three
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that
    determine the choice of image and asteroid radius. We MUST subclass GImage,
    because we need extra attributes for both the size and the velocity of the
    asteroid.

    The class Wave will need to look at the size and velocity, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for either of these. That is because they are fixed and cannot
    change when the asteroid is created.

    In addition to the getters, you need to write the __init__ method to set the
    size and starting velocity. Note that the SPEED of an asteroid is defined in
    const.py, so the only thing that differs is the velocity direction.

    You also want to create a method to update the asteroid. You update the
    asteroid by adding the velocity to the position. While it is okay to add a
    method to detect collisions in this class, you may find it easier to process
    collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: The velocity of the asteroid
    # Invariant: _velocity is a Vector2 object
    #
    # Attribute _size: The size of the asteroid
    # Invariant: _size is a string "small", "medium", or "large"

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns an Asteroid object's x component of position
        """
        return self.x

    def getY(self):
        """
        Returns an Asteroid object's y component of position
        """
        return self.y

    def setX(self, x):
        """
        Sets the x position of the asteroid to the given value

        Precondition: x must be an int or float
        """
        self.x = x

    def setY(self, y):
        """
        Sets the y position of the ship to the given value

        Precondition: y must be an int or float
        """
        self.y = y

    def getWidth(self):
        """
        Returns an Asteroid object's width
        """
        return self.width

    def getSize(self):
        """
        Returns the asteroid's size (small, medium, large)
        """
        return self._size

    def getVelocity(self):
        """
        Returns the velocity of the asteroid.
        """
        return self._velocity

    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self, dict):
        """
        Initializes attributes of an asteroid with given values in dict

        Parameter dict: contains the ship's position, size, and direction
        Precondition: dict is a dictionary
        """
        self._size = dict['size']
        if self._size == 'small':
            src = SMALL_IMAGE
            w = 2 * SMALL_RADIUS
            h = 2 * SMALL_RADIUS
            sp = SMALL_SPEED
        elif self._size == 'medium':
            src = MEDIUM_IMAGE
            w = 2 * MEDIUM_RADIUS
            h = 2 * MEDIUM_RADIUS
            sp = MEDIUM_SPEED
        elif self._size == 'large':
            src = LARGE_IMAGE
            w = 2 * LARGE_RADIUS
            h = 2 * LARGE_RADIUS
            sp = LARGE_SPEED
        xpos = dict['position'][0]
        ypos = dict['position'][1]
        super().__init__(x = xpos, y = ypos, width = w, height = h, source = src)
        self._velocity = self._vel(dict['direction'], sp)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def _vel(self, dir, sp):
        """
        Returns the velocity vector of the asteroid

        Parameter dir: the direction of the asteroid's velocity
        Parameter sp: the magnitude of the asteroid's velocity
        Precondition: dir is a list
        Precondition: sp is either SMALL_SPEED, MEDIUM_SPEED, or LARGE_SPEED
        """
        if dir[0] == 0 and dir[1] == 0:
            return Vector2(0,0)
        else:
            unit = Vector2(dir[0], dir[1]).normalize()
            return unit.__mul__(sp)

    #asteroid position is updated in wave.py _move method
