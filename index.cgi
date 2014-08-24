#!/usr/bin/env python3

import cgi
import cgitb

from apollon import ApollonianGasket
from coloring import ColorScheme, ColorMap
from ag import ag_to_svg

cgitb.enable()

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

<p><label for="c1">First circle</label><input type="number" name="c1" id="c1" value="%.2f"/></p>
<p><label for="c2">Second circle</label> <input type="number" name="c2" id="c2" value="%.2f"/></p>
<p><label for="c3">Third circle</label><input type="number" name="c3" id="c3" value="%.2f"/></p>
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

    # Print last chunk of html
    print("""
</select></p>
<p><input type="submit" name="submit" value="Update"> <input type="submit" name="submit" value="Save"></p>
</form>
</div>
</body>
</html>
""")


def print_only_image(svg):
    print('Content-type: image/svg+xml\nContent-Disposition: attachment; filename="apollonian_gasket.svg"\n\n')
    print(svg)


if __name__ == "__main__":
    # Get settings from form
    form = cgi.FieldStorage()
    param = Settings(form)


    # Magic
    ag = ApollonianGasket(param.c1, param.c2, param.c3)
    
    ag.generate(param.depth)

    # Get smallest and biggest radius
    smallest = abs(min(ag.genCircles, key=lambda c: abs(c.r.real)).r.real)
    biggest = abs(max(ag.genCircles, key=lambda c: abs(c.r.real)).r.real)

    # Construct color map 
    schemes = ColorScheme("colorbrewer.json")

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





