"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
import re
from dice import Dice

class Pattern:
    regex : str
    reroll : int
    def condition(self, dice: Dice) -> bool:
        text = "".join(str(d) for d in dice.dice)
        return bool(re.match(self.regex, text))

class Three(Pattern):
    regex = r".*[1-6]{3}.*"
    reroll = 3
    pass

class Four(Pattern):
    regex = r".*[1-6]{4}.*"
    reroll = 2
    pass

class Five(Pattern):
    regex = r".*[1-6]{5}.*"
    reroll = 1
    pass

class SmallStraight(Pattern):
    regex = r"1.?2.?3.?4.?5.?|2.?3.?4.?5.?6.?"
    reroll = 1
    pass

class LargeStraight(Pattern):
    regex = r"123456"
    pass

class Ace(Pattern):
    regex = r".*1.*"
    reroll = 5
    pass

class Quint(Pattern):
    regex = r".*5.*"
    reroll = 5
    pass
