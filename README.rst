Apollon
#######

About
=====

These are some python classes and functions for calculating Apollonian
Gaskets and saving them as svg. For an overview about this
mathematical object, see wikipedia_.

The code is split into the following files:

- `apollon.py` contains all the pure math stuff
- `coloring.py` contains helpers for color mapping
- `ag.py` is a command-line tool for generating Apollonian Gaskets
- `index.cgi` is an interactive online cgi version
- `colorbrewer.json` contains the color schemes, copied from
  https://gist.github.com/jsundram/6004447#file-colorbrewer-json


Usage
=====

CLI
---

Run `./ag.py c1 c2 c3` where c1, c2, c3 are the (positive) curvatures
of the starting circles. Please also see the `--help` option.

Note: The method used to calculate the circles is recursive. For depth
d, 2*3^{d+1} circles are created. It is usually save to do this up to
d=10, but with higher values you can reach the limit of your
RAM. Because of this, and to prevent typos potentially crashing your
machine, the recursion depth is capped at d=10. If you know what you
are doing, you can use the `--force` option for higher values.

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

For the cli-program see `ag.py --help`.

For a somewhat complete documentation of the source files run
`epydoc --html apollon.py ag.py coloring.py`

BUGS
====

For some combinations of curvatures no enclosing circles can be
found. This occurs when the circle would be a straight line (0
curvature, infinite radius). Expect a crash of the program.

TODO
====
- More logical structure of the source files
- Better error handling
- Better documentation
- A time- and RAM-saving algorithm that excludes Circles from
  recursion which are too small to be seen.
- fastcgi version of index.cgi?


Author & License
================

Author: Ludger Sandig
Contact: contact@lsandig.org
Homepage: http://lsandig.org/

This software can be found on github:
https://github.com/lsandig/apollon

This software is published under the GPL, see LICENSE

.. Links
.. _wikipedia: https://en.wikipedia.org/wiki/Apollonian_gasket
