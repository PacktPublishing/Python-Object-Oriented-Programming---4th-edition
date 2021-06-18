"""
Python 3 Object-Oriented Programming

Chapter 9. Strings and Serialization
"""

from math import cos, radians, hypot, pi


def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    >>> annapolis = (38.9784, 76.4922)
    >>> saint_michaels = (38.7854, 76.2233)
    >>> round(distance(*annapolis, *saint_michaels), 9)
    17.070608794
    """
    d_lat = radians(lat2) - radians(lat1)
    d_lon = min(
        (radians(lon2) - radians(lon1)) % (2 * pi),
        (radians(lon1) - radians(lon2)) % (2 * pi),
    )
    R = 60 * 180 / pi
    d = hypot(R * d_lat, R * cos(radians(lat1)) * d_lon)
    return d


test_distance = """

>>> annapolis = (38.9784, 76.4922)
>>> saint_michaels = (38.7854, 76.2233)
>>> oxford = (38.6865, 76.1716)
>>> cambridge = (38.5632, 76.0788)

>>> legs = [
...     ("to st.michaels", annapolis, saint_michaels),
...     ("to oxford", saint_michaels, oxford),
...     ("to cambridge", oxford, cambridge),
...     ("return", cambridge, annapolis),
... ]

>>> speed = 5
>>> fuel_per_hr = 2.2
>>> for name, start, end in legs:
...     d = distance(*start, *end)
...     print(name, d, d/speed, d/speed*fuel_per_hr)
to st.michaels 17.070608794397305 3.4141217588794612 7.511067869534815
to oxford 6.407736547720565 1.281547309544113 2.8194040809970486
to cambridge 8.580230239760064 1.716046047952013 3.7753013054944287
return 31.571582240989173 6.314316448197834 13.891496186035237


>>> speed = 5
>>> fuel_per_hr = 2.2
>>> print(f"{'leg':16s} {'dist':5s} {'time':4s} {'fuel':4s}")
leg              dist  time fuel
>>> for name, start, end in legs:
...     d = distance(*start, *end)
...     print(
...         f"{name:16s} {d:5.2f} {d/speed:4.1f} "
...         f"{d/speed*fuel_per_hr:4.0f}"
...     )
to st.michaels   17.07  3.4    8
to oxford         6.41  1.3    3
to cambridge      8.58  1.7    4
return           31.57  6.3   14



"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
