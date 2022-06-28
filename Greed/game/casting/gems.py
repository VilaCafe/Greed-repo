from game.casting.actor import Actor
from game.shared.point import Point
import random

class Gem(Actor):
    """
    An item of value and interest. 
    
    The responsibility of a Gem is to provide the movement for itself.

    Attributes:
        none
    """
    def __init__(self):
        super().__init__()
        
    def fall(self, max_y):
        """Moves the actor to its next position according to its velocity. Will wrap the position 
        from one side of the screen to the other when it reaches the given maximum x and y values.
        
        Args:
            max_x (int): The maximum x value.
            max_y (int): The maximum y value.
        """
        x = self._position.get_x()
        y = (self._position.get_y() + 5) % max_y
        self._position = Point(x, y)

    def change_x(self):
        x = random.randint(1, 59) * 15
        self._position = Point(x,self._position.get_y())
        