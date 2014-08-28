#!/usr/bin/env python3

# Copyright (c) 2014 Ludger Sandig
# This file is part of apollon.

# Apollon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Apollon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Apollon.  If not, see <http://www.gnu.org/licenses/>.

import cgi
import cgitb

from apollon import ApollonianGasket
from coloring import ColorScheme, ColorMap
from ag import ag_to_svg, impossible_combination



# Container for sanitized settings
class Settings(object):
    def __init__(self, form):
        self.color = form.getvalue("color", "Blues")
        self.resolution = int(form.getvalue("res", 8))
        self.c1 = float(form.getvalue("c1", 1))
        self.c2 = float(form.getvalue("c2", 2))
        self.c3 = float(form.getvalue("c3", 2))
        self.rad_or_curv = form.getvalue("roc", "curvature")
        self.depth = int(form.getvalue("depth", 3))
        
        # Sanity check
        
        if (self.resolution > 8) or (self.resolution < 3):
            self.resolution = 8
            
        if self.c1 <= 0: self.c1 = 1
        if self.c2 <= 0: self.c2 = 1
        if self.c3 <= 0: self.c3 = 1

        if not (self.rad_or_curv == "curvature" or self.rad_or_curv == "radius"):
            self.rad_or_curvature = "curvature"

        if (self.depth < 0) or (self.depth > 5):
            self.depth = 3

        # For a more usable form
        if self.rad_or_curv == "curvature":
            self.rad_checked = ""
            self.curv_checked = "checked"
        else:
            self.rad_checked = "checked"
            self.curv_checked = ""

        # Curvature or Radius?
        if self.rad_or_curv == "radius":
            self.c1 = 1/self.c1
            self.c2 = 1/self.c2
            self.c3 = 1/self.c3

        # AG possible in the first place?
        self.impossible = impossible_combination(self.c1, self.c2, self.c3)

        # What to print: With form or only svg
        action = form.getvalue("submit","Update")
        self.onlysvg = False
        if action == "Save":
            self.onlysvg = True


def print_with_form(svg, settings, schemes):
    # Print first chunk of html
    print("Content-type: text/html")

    print("""
<html>
    
<head>
<title>Apollonian Gasket Generator</title>

<style>

body {
    font-family: sans-serif;
    width: 800px;
    margin: auto;
}

h1 {
    padding: 10px;
    border: 2px solid #ccc;
    border-radius: 25px;
    text-align: center;
    width: 780px;
}

#gasket {
    width: 500px;
    float: left;
    padding: 10px;
    border: 2px solid #ccc;
    border-radius: 25px;
}

#settings {
    width: 250px;
    float: right;
    border: 2px solid #ccc;
    border-radius: 25px;
    padding: 10px;
}

#about {
    width: 780px;
    border: 2px solid #ccc;
    border-radius: 25px;
    padding: 10px;
    clear: both;
}

div.wrapper {
    padding-top: 2px;
    clear: both;
}

input[type=number] {
    width: 75px;

}

input, label, select {
    display: table-cell;
}

form { 
    display: table;
    width: inherit;
}

#settings p { display: table-row; }

</style>

</head>

<body>

<h1>Apollonian Gasket Generator</h1>
""")

    print('<div id="gasket">\n%s\n</div>' % svg)

    # Print form
    print("""
<div id="settings">
<form method="post" action="index.cgi" id="params">

<p><label for="c1">First circle</label><input type="number" name="c1" id="c1" step="any" min="0" value="%.2f"/></p>
<p><label for="c2">Second circle</label> <input type="number" name="c2" id="c2" step="any" min="0" value="%.2f"/></p>
<p><label for="c3">Third circle</label><input type="number" name="c3" id="c3" step="any" min="0" value="%.2f"/></p>
<p><label for="curv">Curvature</label><input type="radio" name="roc" id="curv" value="curvature" %s/></p>
<p><label for="rad">Radius</label><input type="radio" name="roc" id="rad" value="radius" %s/></p>
<p><label for="depth">Recursion depth</label> <input type="number" name="depth" value="%d" min="0" max="5"/></p>
<p><label for="num">No. of colors</label><input type="number" name="res" value="%d" min="3" max="8"/> </p>
<p><label>Color scheme</label><select name="color">
""" % (settings.c1, settings.c2, settings.c3, settings.curv_checked, settings.rad_checked, settings.depth, settings.resolution))

    # Sort color scheme names
    info = schemes.info()
    info.sort(key=lambda d: d["name"])
    info.insert(0, {"name" : "none"})
    for s in info:
        if s["name"] == settings.color:
            selected = "selected"
        else:
            selected = ""
        print('<option value="%s" %s>%s</value>' % (s["name"], selected, s["name"]))

    # Print last chunk of form and help text
    print("""
</select></p>
<p><input type="submit" name="submit" value="Update"> <input type="submit" name="submit" value="Save"></p>
</form>
</div>
<div class="wrapper">
<div id="about">
<h2>About</h2>

<p> Apollonian Gaskets are groups of circles in which three are
mutally tangent to each other. You can think of it as tightly filling
a big circle with lots of smaller cicles. These sets of circles can be
computed recusively with relative ease. If you are interested in the
mathematical part, see <a
href="https://en.wikipedia.org/wiki/Apollonian_gasket">Wikipedia on
this subject</a>. </p>

<p>This site showcases a small command line program I wrote to
generate svg images of those circles. It can be found on <a
href="https://github.com/lsandig/apollon">github</a>.</p>

<p>Please note that the online version has a recursion limit of depth
5 to reduce the time and memory consumption on the server. With the
command line version only your RAM is the limit.</p>

<p>This is free software published under the GPLv3.</p>

</div>
</div>
</body>
</html>
""")


def print_only_image(svg):
    print('Content-type: image/svg+xml\nContent-Disposition: attachment; filename="apollonian_gasket.svg"\n\n')
    print(svg)


if __name__ == "__main__":
    # Debugging
    #cgitb.enable()

    # Get settings from form
    form = cgi.FieldStorage()
    param = Settings(form)

    # Construct color map 
    schemes = ColorScheme("colorbrewer.json")

    if not param.impossible:
        # Magic
        ag = ApollonianGasket(param.c1, param.c2, param.c3)
        
        ag.generate(param.depth)
        
        # Get smallest and biggest radius
        smallest = abs(min(ag.genCircles, key=lambda c: abs(c.r.real)).r.real)
        biggest = abs(max(ag.genCircles, key=lambda c: abs(c.r.real)).r.real)


        if param.color == 'none':
            mp = ColorMap('none')
        else:
            mp = schemes.makeMap(smallest, biggest, param.color, param.resolution)
            
        # Convert to svg
        svg = ag_to_svg(ag.genCircles, mp, tresh=0.005)

        # Output
        if param.onlysvg:
            print_only_image(svg)
        else:
            print_with_form(svg, param, schemes)
    else:
        errortext = "<h2>No Apollonian gasket possible for these curvatures :(</2>"
        print_with_form(errortext, param, schemes)




