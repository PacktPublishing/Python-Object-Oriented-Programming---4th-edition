# Python 3 Object-Oriented Programming Case Study

Chapter 4, Expecting the Unexpected

## Raising exceptions

### Raising an exception

```python
>>> print "hello world"
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/CaseStudy39/lib/python3.9/doctest.py", line 1336, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest examples.md[0]>", line 1
    print "hello world"
          ^
SyntaxError: Missing parentheses in call to 'print'. Did you mean print("hello world")?

```

```python
>>> x = 5 / 0
Traceback (most recent call last):
...
ZeroDivisionError: division by zero

>>> lst = [1,2,3]
>>> print(lst[3])
Traceback (most recent call last):
...
IndexError: list index out of range

>>> lst + 2
Traceback (most recent call last):
...
TypeError: can only concatenate list (not "int") to list

>>> lst.add
Traceback (most recent call last):
...
AttributeError: 'list' object has no attribute 'add'

>>> d = {'a': 'hello'}
>>> d['b']
Traceback (most recent call last):
...
KeyError: 'b'

>>> print(this_is_not_a_var)
Traceback (most recent call last):
...
NameError: name 'this_is_not_a_var' is not defined

```
### The effects of an exception

### Handling exceptions

```python
>>> try: 
...     raise ValueError("This is an argument") 
... except ValueError as e: 
...     print(f"The exception arguments were {e.args}") 
...
The exception arguments were ('This is an argument',)

```
### The Exception hierarchy

### Defining our own exceptions

```python
>>> class InvalidWithdrawal(ValueError): 
...     pass 
 
>>> raise InvalidWithdrawal("You don't have $50 in your account")
Traceback (most recent call last):
...
InvalidWithdrawal: You don't have $50 in your account


```

```python

>>> from decimal import Decimal

>>> class InvalidWithdrawal(ValueError): 
...     def __init__(self, balance: Decimal, amount: Decimal) -> None: 
...         super().__init__(f"account doesn't have ${amount}") 
...         self.amount = amount 
...         self.balance = balance 
...     def overage(self) -> Decimal: 
...         return self.amount - self.balance 

>>> raise InvalidWithdrawal(Decimal('25.00'), Decimal('50.00'))
Traceback (most recent call last):
...
InvalidWithdrawal: account doesn't have $50.00

>>> try: 
...     balance = Decimal('25.00')
...     raise InvalidWithdrawal(balance, Decimal('50.00')) 
... except InvalidWithdrawal as e: 
...     print("I'm sorry, but your withdrawal is " 
...             "more than your balance by " 
...             f"${e.overage()}") 
...
I'm sorry, but your withdrawal is more than your balance by $25.00


```


