#! /usr/bin/python3

# Command line program to create svg apollonian circles

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


import argparse
import sys
import math

from apollon import ApollonianGasket
from coloring import ColorMap, ColorScheme

def parseArguments(argv, colors):
    description = "Generate Apollonian Gaskets and save as svg"
    name = argv[0]

    colors.append('none')
    colors.sort()

    parser = argparse.ArgumentParser(description=description, prog=name)

    parser.add_argument("-d", "--depth", metavar="D", type=int, default=3, help="Recursion depth, generates 2*3^{D+1} circles. Usually safe for D<=10. For higher D use --force if you know what you are doing.")
    parser.add_argument("-o", "--output", metavar="", type=str, default="", help="Output file name. If left blank, default is created from circle curvatures.")
    parser.add_argument("-r", "--radii", action="store_true", default=False, help="Interpret c1, c2, c3 as radii and not as curvatures")
    parser.add_argument("--color", choices=colors, metavar='SCHEME', default='none', help="Color Scheme. Choose from "+", ".join(colors))
    parser.add_argument("--treshold", metavar='T', default=0.005, type=float, help="Don't save circles that are too small. Useful for higher depths to reduce filesize.")
    parser.add_argument("--force", action="store_true", default=False, help="Use if you want a higher recursion depth than 10.")

    parser.add_argument("c1", type=float, help="Curvature of first circle")
    parser.add_argument("c2", type=float, help="Curvature of second circle")
    parser.add_argument("c3", type=float, help="Curvature of third circle")

    return parser.parse_args()

def colorMsg(color):
    print("Available color schemes (name: resmin -- resmax)")
    for i in color.info():
        print("%s: %d -- %d" % (i["name"], i["low"], i["high"]))

def ag_to_svg(circles, colors, tresh=0.005):
    """
    Convert a list of circles to svg, optionally color them.
    @param circles: A list of L{Circle}s
    @param colors: A L{ColorMap} object
    @param tresh: Only circles with a radius greater than the product of tresh and maximal radius are saved
    """
    svg = []
    
    # Find the biggest circle, which hopefully is the enclosing one
    # and has a negative radius because of this. Note that this does
    # not have to be the case if we picked an unlucky set of radii at
    # the start. If that was the case, we're screwed now.
    
    big = min(circles, key=lambda c: c.r.real)

    # Move biggest circle to front so it gets drawn first
    circles.remove(big)
    circles.insert(0, big)

    if big.r.real < 0:
        # Bounding box from biggest circle, lower left corner and two
        # times the radius as width
        corner = big.m - ( abs(big.r) + abs(big.r) * 1j )
        vbwidth = abs(big.r)*2
        width = 500 # Hardcoded!

        # Line width independent of circle size
        lw = (vbwidth/width)

        svg.append('<svg xmlns="http://www.w3.org/2000/svg" width="%f" height="%f" viewBox="%f %f %f %f">\n' % (width, width, corner.real, corner.imag, vbwidth, vbwidth))

        # Keep stroke width relative
        svg.append('<g stroke-width="%f">\n' % lw)

        # Iterate through circle list, circles with radius<radmin
        # will not be saved because they are too small for printing.
        radmin = tresh * abs(big.r)

        for c in circles:
            if abs(c.r) > radmin:
                fill = colors.color_for(abs(c.r))
                svg.append(( '<circle cx="%f" cy="%f" r="%f" fill="%s" stroke="black"/>\n' % (c.m.real, c.m.imag, abs(c.r), fill)))

        svg.append('</g>\n')
        svg.append('</svg>\n')

    return ''.join(svg)

def impossible_combination(c1, c2, c3):
    # If any curvatures x, y, z satisfy the equation
    # x = 2*sqrt(y*z) + y + z
    # then no fourth enclosing circle can be genereated, because it
    # would be a line.
    # We need to see for c1, c2, c3 if they could be "x".
    
    impossible = False
    
    sets = [(c1,c2,c3), (c2,c3,c1), (c3,c1,c2)]
    
    for (x, y, z) in sets:
        if x == 2*math.sqrt(y*z) + y + z:
            impossible = True
    
    return impossible

def main():
    color = ColorScheme("colorbrewer.json")
    available = [d['name'] for d in color.info()]

    args = parseArguments(sys.argv, available)

    # Sanity checks
    for c in [args.c1, args.c2, args.c3]:
        if c == 0:
            print("Error: curvature or radius can't be 0")
            exit(1)
    if impossible_combination(args.c1, args.c2, args.c3):
        print("Error: no apollonian gasket possible for these curvatures")
        exit(1)

    # Given curvatures were in fact radii, so take the reciprocal
    if args.radii:
        args.c1 = 1/args.c1
        args.c2 = 1/args.c2
        args.c3 = 1/args.c3

    ag = ApollonianGasket(args.c1, args.c2, args.c3)

    # At a recursion depth > 10 things start to get serious.
    if args.depth > 10:
        if not args.force:
            print("Note: Number of cicles increases exponentially with 2*3^{D+1} at depth D.\nIf you want to use D>10, specify the --force option.")
            args.depth = 10

    ag.generate(args.depth)

    # Get smallest and biggest radius
    smallest = abs(min(ag.genCircles, key=lambda c: abs(c.r.real)).r.real)
    biggest = abs(max(ag.genCircles, key=lambda c: abs(c.r.real)).r.real)

    # Construct color map 
    if args.color == 'none':
        mp = ColorMap('none')
    else:
        # TODO: resolution of 8 is hardcoded, some color schemes have
        # resolutions up to 11. Make this configurable.
        mp = color.makeMap(smallest, biggest, args.color, 8)

    svg = ag_to_svg(ag.genCircles, mp, tresh=args.treshold)
    
    # User supplied filename? If not, we need to construct something.
    if len(args.output) == 0:
        args.output = 'ag_%.4f_%.4f_%.4f.svg' % (args.c1, args.c2, args.c3)

    with open(args.output, 'w') as f:
        f.write(svg)
        f.close()

if( __name__ == "__main__" ):
    main()
