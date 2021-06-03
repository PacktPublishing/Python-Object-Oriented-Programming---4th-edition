
# Case Study for Chapter 13, Testing object-oriented programs

## Unit testing distance

```python
>>> from sympy import *
>>> ED, k_sl, k_pl, k_sw, k_pw, u_sl, u_pl, u_sw, u_pw = symbols("ED, k_sl, k_pl, k_sw, k_pw, u_sl, u_pl, u_sw, u_pw")
>>> ED = sqrt( (k_sl-u_sl)**2 + (k_pl-u_pl)**2 + (k_sw-u_sw)**2 + (k_pw-u_pw)**2 )
>>> ED
sqrt((k_pl - u_pl)**2 + (k_pw - u_pw)**2 + (k_sl - u_sl)**2 + (k_sw - u_sw)**2)
>>> print(pretty(ED, use_unicode=True))
   _______________________________________________________________
  ╱            2                2              2                2 
╲╱  (kₚₗ - uₚₗ)  + (k_pw - u_pw)  + (kₛₗ - uₛₗ)  + (k_sw - u_sw)  

>>> print(pretty(ED, use_unicode=False))
   ___________________________________________________________________
  /              2                2                2                2 
\/  (k_pl - u_pl)  + (k_pw - u_pw)  + (k_sl - u_sl)  + (k_sw - u_sw)  

>>> e = ED.subs(dict(
...     k_sl=5.1, k_sw=3.5, k_pl=1.4, k_pw=0.2,
...     u_sl=7.9, u_sw=3.2, u_pl=4.7, u_pw=1.4,
... ))
>>> e.evalf(9)
4.50111097

```

```python
>>> SD = sum(
...     [abs(k_sl - u_sl), abs(k_sw - u_sw), abs(k_pl - u_pl), abs(k_pw - u_pw)]
...  ) / sum( 
...     [k_sl + u_sl, k_sw + u_sw, k_pl + u_pl, k_pw + u_pw])
>>> print(pretty(SD, use_unicode=False))
|k_pl - u_pl| + |k_pw - u_pw| + |k_sl - u_sl| + |k_sw - u_sw|
-------------------------------------------------------------
    k_pl + k_pw + k_sl + k_sw + u_pl + u_pw + u_sl + u_sw    

>>> e = SD.subs(dict(
...     k_sl=5.1, k_sw=3.5, k_pl=1.4, k_pw=0.2,
...     u_sl=7.9, u_sw=3.2, u_pl=4.7, u_pw=1.4,
... ))
>>> e.evalf(9)
0.277372263

```

## Unit Testing Hyperparameter

