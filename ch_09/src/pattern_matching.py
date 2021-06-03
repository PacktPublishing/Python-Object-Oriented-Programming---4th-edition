"""
Python 3 Object-Oriented Programming

Chapter 9. Strings and Serialization
"""
import re
from typing import Pattern, Match


def matchy(pattern: Pattern[str], text: str) -> None:
    if match := re.match(pattern, text):
        print(f"{pattern=!r} matches at {match=!r}")
    else:
        print(f"{pattern=!r} not found in {text=!r}")


# Relatively simple tests can be done as multiline docstrings.
# To properly handle the escapes, raw multiline docstrings are required.

test_matchy_incomplete = """
>>> matchy(pattern=r"hello wo", text="hello world")
pattern='hello wo' matches at match=<re.Match object; span=(0, 8), match='hello wo'>
>>> matchy(pattern=r"ello world", text="hello world")
pattern='ello world' not found in text='hello world'
"""

test_matchy_start_end = r"""
>>> matchy(pattern=r"^hello world$", text="hello world")
pattern='^hello world$' matches at match=<re.Match object; span=(0, 11), match='hello world'>
>>> matchy(pattern=r"^hello world$", text="hello worl")
pattern='^hello world$' not found in text='hello worl'

>>> matchy(pattern=r"\^hello world\$", text="hello worl")
pattern='\\^hello world\\$' not found in text='hello worl'
>>> matchy(pattern=r"\^hello world\$", text="^hello world$")
pattern='\\^hello world\\$' matches at match=<re.Match object; span=(0, 13), match='^hello world$'>

"""

test_matchy_dot = """
>>> matchy(r'hel.o world', "hello world")
pattern='hel.o world' matches at match=<re.Match object; span=(0, 11), match='hello world'>
>>> matchy(r'hel.o world', "helpo world")
pattern='hel.o world' matches at match=<re.Match object; span=(0, 11), match='helpo world'>
>>> matchy(r'hel.o world', "hel o world")
pattern='hel.o world' matches at match=<re.Match object; span=(0, 11), match='hel o world'>
>>> matchy(r'hel.o world', "helo world")
pattern='hel.o world' not found in text='helo world'
"""

test_matchy_set = """
>>> matchy(r'hel[lp]o world', "hello world")
pattern='hel[lp]o world' matches at match=<re.Match object; span=(0, 11), match='hello world'>
>>> matchy(r'hel[lp]o world', "helpo world")
pattern='hel[lp]o world' matches at match=<re.Match object; span=(0, 11), match='helpo world'>
>>> matchy(r'hel[lp]o world', "helPo world")
pattern='hel[lp]o world' not found in text='helPo world'

>>> matchy(r'hello [a-z] world', "hello   world")
pattern='hello [a-z] world' not found in text='hello   world'
>>> matchy(r'hello [a-z] world', "hello b world")
pattern='hello [a-z] world' matches at match=<re.Match object; span=(0, 13), match='hello b world'>
>>> matchy(r'hello [a-zA-Z] world', "hello B world")
pattern='hello [a-zA-Z] world' matches at match=<re.Match object; span=(0, 13), match='hello B world'>
>>> matchy(r'hello [a-zA-Z0-9] world', "hello 2 world")
pattern='hello [a-zA-Z0-9] world' matches at match=<re.Match object; span=(0, 13), match='hello 2 world'>
"""

test_matchy_simpler_set = r"""
>>> matchy(r'\d\d\s\w\w\w\s\d\d\d\d', '26 Oct 2019')
pattern='\\d\\d\\s\\w\\w\\w\\s\\d\\d\\d\\d' matches at match=<re.Match object; span=(0, 11), match='26 Oct 2019'>
>>> matchy(r'[0-9][0-9][ \t\n\r\f\v][A-Za-z0-9_][A-Za-z0-9_][A-Za-z0-9_][ \t\n\r\f\v][0-9][0-9][0-9][0-9]', '26 Oct 2019')
pattern='[0-9][0-9][ \\t\\n\\r\\f\\v][A-Za-z0-9_][A-Za-z0-9_][A-Za-z0-9_][ \\t\\n\\r\\f\\v][0-9][0-9][0-9][0-9]' matches at match=<re.Match object; span=(0, 11), match='26 Oct 2019'>

"""

test_matchy_sets = r"""
>>> matchy(r'0\.[0-9][0-9]', "0.05")
pattern='0\\.[0-9][0-9]' matches at match=<re.Match object; span=(0, 4), match='0.05'>

>>> matchy(r'0\.[0-9][0-9]', "005")
pattern='0\\.[0-9][0-9]' not found in text='005'

>>> matchy(r'0\.[0-9][0-9]', "0,05")
pattern='0\\.[0-9][0-9]' not found in text='0,05'

>>> matchy(r'\(abc\]', "(abc]")
pattern='\\(abc\\]' matches at match=<re.Match object; span=(0, 5), match='(abc]'>

>>> matchy(r'\s\d\w', " 1a")
pattern='\\s\\d\\w' matches at match=<re.Match object; span=(0, 3), match=' 1a'>

>>> matchy(r'\s\d\w', "\t5n")
pattern='\\s\\d\\w' matches at match=<re.Match object; span=(0, 3), match='\t5n'>

>>> matchy(r'\s\d\w', " 5n")
pattern='\\s\\d\\w' matches at match=<re.Match object; span=(0, 3), match=' 5n'>

"""

test_matchy_star = r"""
>>> matchy(r'hel*o', 'hello')
pattern='hel*o' matches at match=<re.Match object; span=(0, 5), match='hello'>

>>> matchy(r'hel*o', 'heo')
pattern='hel*o' matches at match=<re.Match object; span=(0, 3), match='heo'>

>>> matchy(r'hel*o', 'helllllo')
pattern='hel*o' matches at match=<re.Match object; span=(0, 8), match='helllllo'>

"""

test_matchy_identifiers = r"""
>>> matchy(r'[A-Z][a-z]* [a-z]*\.', "A string.")
pattern='[A-Z][a-z]* [a-z]*\\.' matches at match=<re.Match object; span=(0, 9), match='A string.'>
>>> matchy(r'[A-Z][a-z]* [a-z]*\.', "No .")
pattern='[A-Z][a-z]* [a-z]*\\.' matches at match=<re.Match object; span=(0, 4), match='No .'>
>>> matchy(r'[a-z]*.*', "")
pattern='[a-z]*.*' matches at match=<re.Match object; span=(0, 0), match=''>

"""

test_matchy_digits = r"""
>>> matchy(r'\d+\.\d+', "0.4")
pattern='\\d+\\.\\d+' matches at match=<re.Match object; span=(0, 3), match='0.4'>
>>> matchy(r'\d+\.\d+', "1.002")
pattern='\\d+\\.\\d+' matches at match=<re.Match object; span=(0, 5), match='1.002'>
>>> matchy(r'\d+\.\d+', "1.")
pattern='\\d+\\.\\d+' not found in text='1.'

>>> matchy(r'\d?\d%', "1%")
pattern='\\d?\\d%' matches at match=<re.Match object; span=(0, 2), match='1%'>
>>> matchy(r'\d?\d%', "99%")
pattern='\\d?\\d%' matches at match=<re.Match object; span=(0, 3), match='99%'>
>>> matchy(r'\d?\d%', "100%")
pattern='\\d?\\d%' not found in text='100%'

"""

test_matchy_explicit_count = r"""
>>> matchy(r'abc{3}', "abccc")
pattern='abc{3}' matches at match=<re.Match object; span=(0, 5), match='abccc'>
>>> matchy(r'(abc){3}', "abccc")
pattern='(abc){3}' not found in text='abccc'
>>> matchy(r'(abc){3}', "abcabcabc")
pattern='(abc){3}' matches at match=<re.Match object; span=(0, 9), match='abcabcabc'>

"""

test_matchy_escape_dot = r"""
>>> matchy(r'[A-Z][a-z]*( [a-z]+)*\.$', "Eat.")
pattern='[A-Z][a-z]*( [a-z]+)*\\.$' matches at match=<re.Match object; span=(0, 4), match='Eat.'>
>>> matchy(r'[A-Z][a-z]*( [a-z]+)*\.$', "Eat more good food.")
pattern='[A-Z][a-z]*( [a-z]+)*\\.$' matches at match=<re.Match object; span=(0, 19), match='Eat more good food.'>
>>> matchy(r'[A-Z][a-z]*( [a-z]+)*\.$', "A good meal.")
pattern='[A-Z][a-z]*( [a-z]+)*\\.$' matches at match=<re.Match object; span=(0, 12), match='A good meal.'>

"""

from typing import Optional


def email_domain(text: str) -> Optional[str]:
    email_pattern = r"[a-z0-9._%+-]+@([a-z0-9.-]+\.[a-z]{2,})"
    if match := re.match(email_pattern, text, re.IGNORECASE):
        return match.group(1)
    else:
        return None


test_email_domain = """
>>> email_domain("dusty@ccphillips.net")
'ccphillips.net'

"""


def email_domain_2(text: str) -> Optional[str]:
    email_pattern = r"(?P<name>[a-z0-9._%+-]+)@(?P<domain>[a-z0-9.-]+\.[a-z]{2,})"
    if match := re.match(email_pattern, text, re.IGNORECASE):
        return match.groupdict()["domain"]
    else:
        return None


test_email_domain_2 = """
>>> email_domain_2("dusty@ccphillips.net")
'ccphillips.net'

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
