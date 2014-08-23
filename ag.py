#! /usr/bin/python3

# Command line program to create svg apollonian circles

import argparse
import sys

from apollon import ApollonianGasket
from coloring import ColorMap, ColorScheme

def parseArguments(argv, colors):
    description = "Generate Apollonian Gaskets and save as svg"
    name = argv[0]

    colors.append('none')

    parser = argparse.ArgumentParser(description=description, prog=name)

    parser.add_argument("-d", "--depth", metavar="D", type=int, default=3, help="Recursion depth, generates 2*3^{D+1} circles.")
    parser.add_argument("-o", "--output", metavar="", type=str, default="", help="Output file name. If left blank, default is created from circle curvatures.")
    parser.add_argument("-r", "--radii", action="store_true", default=False, help="Interpret c1, c2, c3 as radii and not as curvatures")
    parser.add_argument("--color", choices=colors, metavar='', default='none', help="Color Scheme. Choose from "+", ".join(colors))

    parser.add_argument("c1", type=float, help="Curvature of first circle")
    parser.add_argument("c2", type=float, help="Curvature of second circle")
    parser.add_argument("c3", type=float, help="Curvature of third circle")

    return parser.parse_args()

def colorMsg(color):
    print("Available color schemes (name: resmin -- resmax)")
    for i in color.info():
        print("%s: %d -- %d" % (i["name"], i["low"], i["high"]))

def ag_to_svg(circles, colors, tresh=0.005):
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



def main():
    color = ColorScheme("colorbrewer.json")
    available = [d['name'] for d in color.info()]

    args = parseArguments(sys.argv, available)

    for c in [args.c1, args.c2, args.c3]:
        if c == 0:
            print("Error: curvature or radius can't be 0")
            exit(1)

    # Given curvatures were in fact radii, so take the inverse
    if args.radii:
        print('gotcha')
        args.c1 = 1/args.c1
        args.c2 = 1/args.c2
        args.c3 = 1/args.c3

    ag = ApollonianGasket(args.c1, args.c2, args.c3)

    ag.generate(args.depth)

    # Get smallest and biggest radius
    smallest = abs(min(ag.genCircles, key=lambda c: abs(c.r.real)).r.real)
    biggest = abs(max(ag.genCircles, key=lambda c: abs(c.r.real)).r.real)

    # Construct color map 
    # TODO: resolution of 8 is hardcoded, some color schemes have
    # resolutions up to 11. Make this configurable.
    mp = color.makeMap(smallest, biggest, args.color, 8)

    svg = ag_to_svg(ag.genCircles, mp)
    
    # User supplied filename? If not, we need to construct something.
    if len(args.output) == 0:
        args.output = 'ag_%.4f_%.4f_%.4f.svg' % (args.c1, args.c2, args.c3)

    with open(args.output, 'w') as f:
        f.write(svg)
        f.close()

if( __name__ == "__main__" ):
    main()
