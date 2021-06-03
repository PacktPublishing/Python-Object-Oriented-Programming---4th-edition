Python class definitions leave every attribute and method as public. It's simplest
to leave everything as public, and eschew the obfuscation that comes from moore
complex rules. We often say "We're all adults here." The source code is readily 
available, and having a "private" attribute or method is so easily circumvented that
we'd rather not invest the effort in it.

There are four categories of attribute names.

-   `names`. These are the ordinary, publicly-visible names.

-   `_names`. These names are sometimes elided from lists of attributes. Some commands
    and functions will quietly skip past these names, leaving them concealed, but still usable.
    
-   `__names`. Two leading underscores (and zero or one trailing underscore) leads to "name mangling."  
    The name is adjusted to be sure that it is unique to the class. 
    (The class name becomes a prefix: `_{class}__names`.)

-   `__names__`. Two leading and two training underscores are Python special names. 
    No application should ever create new names of this form. 
    The Python run-time may use any name of this form, and could, at some 
    point in the future, break your code. 
    
For the most part, public `names` and concealed `_names` form the bulk of our naming.
Mangled names may be helpful for creating an attribute that cannot be used by a subclass;
this doesn't seem useful. 
Python's special names, however, are very widely used, 
but defined by the language, and not by our code.
