Apollon
#######

About
=====

These are some python classes and functions for calculating Apollonian
Gaskets and saving them as svg. For an overview about this
mathematical object, see wikipedia_.

The code is split into the following files:

- `apollon.py`:code: contains all the pure math stuff
- `coloring.py`:code: contains helpers for color mapping
- `ag.py`:code: is a command-line tool for generating Apollonian Gaskets
- `index.cgi`:code: is an interactive online cgi version
- `colorbrewer.json`:code: contains the color schemes, copied from
  https://gist.github.com/jsundram/6004447#file-colorbrewer-json


Usage
=====

CLI
---

Run `./ag.py c1 c2 c3`:code: where c1, c2, c3 are the (positive) curvatures
of the starting circles. Please also see the `--help`:code: option.

Note: The method used to calculate the circles is recursive. For depth
d, 2*3^{d+1} circles are created. It is usually safe to do this up to
d=10, but with higher values you can reach the limit of your
RAM. Because of this, and to prevent typos potentially crashing your
machine, the recursion depth is capped at d=10. If you know what you
are doing, you can use the `--force`:code: option for higher values.

CGI
---

Online interactive version. You can try it at
http://lsandig.org/cgi-bin/apollon/index.cgi

Recursion depth is limited to 5 to reduce server load and RAM
usage. This implementation might not be very fast, it is just intended
as a showcase of what you can expect from the CLI-version.

Needs python3 and the other three files to work.

Documentation
=============

For the cli-program see `ag.py --help`:code:.

For a somewhat complete documentation of the source files run
`epydoc --html apollon.py ag.py coloring.py`:code:

For a writeup on how the math behind this program works see my
blogpost here: http://lsandig.org/blog/2014/08/apollon-python/en/

TODO
====
- More logical structure of the source files
- Better documentation
- A time- and RAM-saving algorithm that excludes Circles from
  recursion which are too small to be seen.
- fastcgi version of index.cgi?

Credits
=======

Colors from www.ColorBrewer.org by Cynthia A. Brewer, Geography,
Pennsylvania State University.

Thanks to Dorothee Henke for helping me figuring out the math.

Author & License
================

| Author: Ludger Sandig
| Contact: contact@lsandig.org
| Homepage: http://lsandig.org/

This software can be found on github:
https://github.com/lsandig/apollon

This software is published under the GPL, see LICENSE

.. Links
.. _wikipedia: https://en.wikipedia.org/wiki/Apollonian_gasket
