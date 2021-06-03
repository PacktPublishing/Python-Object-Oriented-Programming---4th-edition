######
Images
######

For the antigravity image, run

::

    import antigravity

The image link is https://imgs.xkcd.com/comics/python.png

Other images that seem relevant to this chapter:

https://imgs.xkcd.com/comics/exploits_of_a_mom.png

https://imgs.xkcd.com/comics/compiling.png

https://imgs.xkcd.com/comics/sandwich.png

The ``row`` and ``bricks`` images were produced
by functions in the ``make_images.py`` application

The ``bricks_1`` and ``bricks_2`` images can
be reproduced with PlantUML and Graphviz. This is
a bit more complex to set up.

The ``make_images.py`` application will download or
create all the images in this directory.

If you want to experiment with images
created by PlantUML and the Graphviz ``dot`` language,
the following setup is required:

1.  Download Java Runtime (JRE) for your platform.
    https://www.java.com/en/download/manual.jsp

2.  Download the ``plantuml.jar`` and put into your conda environment ``share`` directory.
    https://plantuml.com/download

3.  Use ``conda install graphiz`` to create the ``dot`` application in your conda environment.

4.  If necessary, update the ``make_images.py`` script with environment name and locations
