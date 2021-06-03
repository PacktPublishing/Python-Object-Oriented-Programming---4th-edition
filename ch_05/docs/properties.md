
## Attributes and Properties

A Python class exposes several different kinds of attributes. 
In other parts of this case study, we've used the following:

-   Instance variables. 
    These are created in the methods of a class.
    They're qualified by the `self.` variable. We often create them in the `__init__()` method.

-   Class variables. 
    These are variables created within the `class` statement,
    but outside any method definition. They belong to the class as a whole, and are shared by 
    all instances. 
    
-   Instance methods. 
    Methods defined in the `class` statement without any decoration
    apply to the instances of a class. 
    These methods receive the instance object bound to the `self` variable; the first positional parameter value.

=   Static and class methods. 
    Methods decorated with `@classmethod` or `@staticmethod apply to the class
    as a whole. These methods belong to the class and don't apply to an instance.
    A `@staticmethod` has no special parameter.
    A `@classmethod` has the class object as the first positional parameter.
    
It turns out, there are a more attribute-like features inside a class. The internal mechanism 
these are based on, the descriptor,
lets us bind an instance method to a simple name. A method with only a single `self` variable
as a parameter can be evaluated without the syntax of `()` after the name.

We can use the expression `sample.classifier` to lead to evaluaion of a `classifier()` method
on an object named `sample`.
We can also make sure that `sample.classifier = x` will lead to evaluation of a `classifier(x)`
method, allowing us to validated (or prevent) the assignment.
