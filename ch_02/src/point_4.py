"""
Python 3 Object-Oriented Programming 4th ed.

Chapter 2, Objects in Python.
"""

import math


class Point:
    """
    Represents a point in two-dimensional geometric coordinates

    >>> p_0 = Point()
    >>> p_1 = Point(3, 4)
    >>> p_0.calculate_distance(p_1)
    5.0
    """

    def __init__(self, x: float = 0, y: float = 0) -> None:
        """
        Initialize the position of a new point. The x and y
        coordinates can be specified. If they are not, the
        point defaults to the origin.

        :param x: float x-coordinate
        :param y: float x-coordinate
        """
        self.move(x, y)

    def move(self, x: float, y: float) -> None:
        """
        Move the point to a new location in 2D space.

        :param x: float x-coordinate
        :param y: float x-coordinate
        """
        self.x = x
        self.y = y

    def reset(self) -> None:
        """
        Reset the point back to the geometric origin: 0, 0
        """
        self.move(0, 0)

    def calculate_distance(self, other: "Point") -> float:
        """
        Calculate the Euclidean distance from this point
        to a second point passed as a parameter.

        :param other: Point instance
        :return: float distance
        """
        return math.hypot(self.x - other.x, self.y - other.y)


test_point_help = """
>>> help(Point)
Help on class Point in module point_4:
<BLANKLINE>
class Point(builtins.object)
 |  Point(x: float = 0, y: float = 0) -> None
 |  
 |  Represents a point in two-dimensional geometric coordinates
 |  
 |  >>> p_0 = Point()
 |  >>> p_1 = Point(3, 4)
 |  >>> p_0.calculate_distance(p_1)
 |  5.0
 |  
 |  Methods defined here:
 |  
 |  __init__(self, x: float = 0, y: float = 0) -> None
 |      Initialize the position of a new point. The x and y
 |      coordinates can be specified. If they are not, the
 |      point defaults to the origin.
 |      
 |      :param x: float x-coordinate
 |      :param y: float x-coordinate
 |  
 |  calculate_distance(self, other: 'Point') -> float
 |      Calculate the Euclidean distance from this point
 |      to a second point passed as a parameter.
 |      
 |      :param other: Point instance
 |      :return: float distance
 |  
 |  move(self, x: float, y: float) -> None
 |      Move the point to a new location in 2D space.
 |      
 |      :param x: float x-coordinate
 |      :param y: float x-coordinate
 |  
 |  reset(self) -> None
 |      Reset the point back to the geometric origin: 0, 0
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
<BLANKLINE>

"""

test_main = """
>>> main()
p1.calculate_distance(p2)=5.0
"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}


def main() -> None:
    """
    Does the useful work.

    >>> main()
    p1.calculate_distance(p2)=5.0
    """
    p1 = Point()
    p2 = Point(3, 4)
    print(f"{p1.calculate_distance(p2)=}")


if __name__ == "__main__":
    main()
