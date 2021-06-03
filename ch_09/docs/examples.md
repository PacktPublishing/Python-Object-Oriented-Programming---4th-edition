# Python 3 Object-Oriented Programming

Chapter 9. Strings and Serialization

## Strings

### String Manipulation

```python

>>> a = "hello" 
>>> b = 'world' 
>>> c = '''a multiple 
... line string''' 
>>> d = """More 
... multiple""" 
>>> e = ("Three " "Strings " 
...        "Together") 


```

```python
>>> help(str.isalpha)
Help on method_descriptor:
<BLANKLINE>
isalpha(self, /)
    Return True if the string is an alphabetic string, False otherwise.
<BLANKLINE>    
    A string is alphabetic if all characters in the string are alphabetic and there
    is at least one character in the string.
<BLANKLINE>


```

```python
>>> t = "The Cremation of Sam McGee"
>>> t.istitle()
False

```

```python
>>> float('45\u06602')
4502.0

```

```python
>>> s = "hello world"
>>> s.count('l')
3
>>> s.find('l')
2
>>> s.rindex('m')
Traceback (most recent call last):
  ...
  File "<doctest examples.md[11]>", line 1, in <module>
    s.rindex('m')
ValueError: substring not found

```

```python
>>> s = "hello world, how are you"
>>> s2 = s.split(' ')
>>> s2
['hello', 'world,', 'how', 'are', 'you']
>>> '#'.join(s2)
'hello#world,#how#are#you'
>>> s.replace(' ', '**')
'hello**world,**how**are**you'
>>> s.partition(' ')
('hello', ' ', 'world, how are you')

```

### String formatting

```python
>>> name = "Dusty"
>>> activity = "reviewing"
>>> message = f"Hello {name}, you are currently {activity}."
>>> print(message)
Hello Dusty, you are currently reviewing.

```

### Escaping braces

```python

>>> classname = "MyClass"
>>> python_code = "print('hello world')"
>>> template = f"""
... public class {classname} {{
...     public static void main(String[] args) {{
...         System.out.println("{python_code}");
...     }}
... }}
... """

>>> print(template)
<BLANKLINE>
public class MyClass {
    public static void main(String[] args) {
        System.out.println("print('hello world')");
    }
}
<BLANKLINE>

```

### f-strings can contain Python code

```python
>>> emails = ("steve@example.com", "dusty@example.com")
>>> message = {
...     "subject": "Next Chapter",
...     "message": "Here's the next chapter to review!",
... }

>>> formatted = f"""
... From: <{emails[0]}>
... To: <{emails[1]}>
... Subject: {message['subject']}
... 
... {message['message']}
... """
>>> print(formatted)
<BLANKLINE>
From: <steve@example.com>
To: <dusty@example.com>
Subject: Next Chapter
<BLANKLINE>
Here's the next chapter to review!
<BLANKLINE>


```

```python
>>> class Notification:
...     def __init__(
...             self, 
...             from_addr: str, 
...             to_addr: str, 
...             subject: str, 
...             message: str
...     ) -> None:
...         self.from_addr = from_addr
...         self.to_addr = to_addr
...         self.subject = subject
...         self._message = message
...     def message(self):
...         return self._message

>>> email = Notification(
...     "dusty@example.com",
...     "steve@example.com",
...     "Comments on the Chapter",
...     "Can we emphasize Python 3.9 type hints?",
... )

>>> formatted = f"""
... From: <{email.from_addr}>
... To: <{email.to_addr}>
... Subject: {email.subject}
... 
... {email.message()}
... """
>>> print(formatted)
<BLANKLINE>
From: <dusty@example.com>
To: <steve@example.com>
Subject: Comments on the Chapter
<BLANKLINE>
Can we emphasize Python 3.9 type hints?
<BLANKLINE>


```

```python
>>> f"{[2*a+1 for a in range(5)]}"
'[1, 3, 5, 7, 9]'
>>> for n in range(1, 5):
...     print(f"{'fizz' if n % 3 == 0 else n}")
1
2
fizz
4

```

```python
>>> a = 5
>>> b = 7
>>> f"{a=}, {b=}, {31*a//42*b + b=}"
'a=5, b=7, 31*a//42*b + b=28'

```

```python
>>> from math import cos, radians, hypot, pi
>>> def distance(lat1, lon1, lat2, lon2):
...     d_lat = radians(lat2) - radians(lat1)
...     d_lon = min(
...         (radians(lon2)-radians(lon1)) % (2*pi),
...         (radians(lon1)-radians(lon2)) % (2*pi))
...     R = 60*180/pi
...     d = hypot(R*d_lat, R*cos(radians(lat1))*d_lon)
...     return d

>>> annapolis = (38.9784, 76.4922)
>>> saint_michaels = (38.7854, 76.2233)
>>> round(distance(*annapolis, *saint_michaels), 9)
17.070608794

>>> oxford = (38.6865, 76.1716)
>>> round(distance(*saint_michaels, *oxford), 9)
6.407736548

>>> cambridge = (38.5632, 76.0788)
>>> round(distance(*oxford, *cambridge), 9)
8.58023024

Boat is 0.007 nm in length. Too much precision here.

```

### Custom formatters

```python
>>> import datetime 
>>> important = datetime.datetime(2019, 10, 26, 13, 14)
>>> f"{important:%Y-%m-%d %I:%M%p}"
'2019-10-26 01:14PM'

```

### The format method

```python
>>> from decimal import Decimal
>>> subtotal = Decimal('2.95') * Decimal('1.0625')
>>> template = "{label}: {number:*^{size}.2f}" 
>>> template.format(label="Amount", size=10, number=subtotal)
'Amount: ***3.13***'

>>> grand_total = subtotal + Decimal('12.34')
>>> template.format(label="Total", size=12, number=grand_total)
'Total: ***15.47****'

>>> "Hello {0}!".format("world")
'Hello world!'

>>> "{} {}!".format("Hello", "world")
'Hello world!'

```

## Strings are Unicode

```python
>>> list(map(hex, b'abc'))
['0x61', '0x62', '0x63']
>>> list(map(bin, b'abc'))
['0b1100001', '0b1100010', '0b1100011']

>>> bytes([137, 80, 78, 71, 13, 10, 26, 10])
b'\x89PNG\r\n\x1a\n'

>>> bytes([27, 91, 57, 55, 59, 52, 49, 109])
b'\x1b[97;41m'

```


### Converting bytes to text

```python
>>> characters = b'\x63\x6c\x69\x63\x68\xc3\xa9' 
>>> characters 
b'clich\xc3\xa9'

>>> characters.decode("utf-8") 
'cliché'

>>> characters.decode("latin-1")
'clichÃ©'

>>> characters.decode("cp1252")
'clichÃ©'

>>> characters.decode("iso8859-5")
'clichУЉ'

>>> characters.decode("cp037")
'Ä%ÑÄÇCz'


```

### Converting text to bytes

```python

>>> characters = "cliché" 
>>> characters.encode("UTF-8")
b'clich\xc3\xa9'

>>> characters.encode("latin-1")
b'clich\xe9'

>>> characters.encode("cp1252")
b'clich\xe9'

>>> characters.encode("CP437")
b'clich\x82'

>>> characters.encode("ascii") 
Traceback (most recent call last):
  ...
  File "<doctest examples.md[73]>", line 1, in <module>
    characters.encode("ascii")
UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 5: ordinal not in range(128)

```

```python

>>> characters = "cliché" 
>>> characters.encode("ascii", "replace")
b'clich?'

>>> characters.encode("ascii", "ignore")
b'clich'

>>> characters.encode("ascii", "xmlcharrefreplace")
b'clich&#233;'

```

### Mutable byte strings

```python

>>> ba = bytearray(b"abcdefgh") 
>>> ba[4:6] = b"\x15\xa3"
>>> ba
bytearray(b'abcd\x15\xa3gh')


>>> ba = bytearray(b"abcdefgh") 
>>> ba[3] = ord(b'g')
>>> ba[4] = 68
>>> ba
bytearray(b'abcgDfgh')

```

## Regular expressions

### Matching patterns

```python

>>> import re 
 
>>> search_string = "hello world" 
>>> pattern = r"hello world" 
 
>>> if match := re.match(pattern, search_string): 
...     print("regex matches") 
...     print(match)
regex matches
<re.Match object; span=(0, 11), match='hello world'>


```


### Matching a selection of characters

### Escaping characters

### Matching multiple characters

### Grouping patterns together

### Parsing information with regular expressions



```python

>>> import re
>>> re.findall(r"\d+[hms]", "3h 2m   45s")
['3h', '2m', '45s']
>>> re.findall(r"(\d+)[hms]", "3h:2m:45s")
['3', '2', '45']
>>> re.findall(r"(\d+)([hms])", "3h, 2m, 45s")
[('3', 'h'), ('2', 'm'), ('45', 's')]
>>> re.findall(r"((\d+)([hms]))", "3h - 2m - 45s")
[('3h', '3', 'h'), ('2m', '2', 'm'), ('45s', '45', 's')]

>>> duration_pattern = re.compile(r"\d+[hms]")
>>> duration_pattern.findall("3h 2m   45s")
['3h', '2m', '45s']
>>> duration_pattern.findall("3h:2m:45s")
['3h', '2m', '45s']

```

## Filesystem paths

NOTE Windows and mac OS X provide
dramatically different results.

```python
>>> import os.path
>>> path = os.path.abspath(
...     os.sep.join(
...         ["", "Users", "dusty", "subdir", "subsubdir", "file.ext"]))
>>> import sys
>>> assert (
... path == "C:\\Users\\dusty\\subdir\\subsubdir\\file.ext"
... if sys.platform == "win32"
... else path == "/Users/dusty/subdir/subsubdir/file.ext"
... ), f"{path!r} invalid for {sys.platform!r}"



```

```python
>>> from pathlib import Path
>>> path = Path("/Users") / "dusty" / "subdir" / "subsubdir" / "file.ext"
>>> import sys
>>> assert path == Path("/Users/dusty/subdir/subsubdir/file.ext")


```

## Serializing objects

```python
>>> import pickle
>>> some_data = [
... "a list", "containing", 5, "items",
... {"including": ["str", "int", "dict"]}
... ]

>>> with open("pickled_list", 'wb') as file: 
...     pickle.dump(some_data, file) 
 
>>> with open("pickled_list", 'rb') as file: 
...     loaded_data = pickle.load(file) 

>>> print(loaded_data)
['a list', 'containing', 5, 'items', {'including': ['str', 'int', 'dict']}]

>>> assert loaded_data == some_data
>>> assert id(loaded_data) != id(some_data)


```
