#!/usr/bin/python3

from cmath import *
import random

from mycolors import *

class Circle(object):
    """
    A circle represented by center point as complex number and radius.
    """
    def __init__ ( self, mx, my, r ):
        """
        @param mx: x center coordinate
        @type mx: int or float
        @param my: y center coordinate
        @type my: int or float
        @param r: radius
        @type r: int or float
        """
        self.r = r
        self.m = (mx +my*1j)

    def __repr__ ( self ):
        """
        Pretty printing
        """
        return "Circle( self, %s, %s, %s )" % (self.m.real, self.m.imag, self.r)

    def __str__ ( self ):
        """
        Pretty printing
        """
        return "Circle x:%.3f y:%.3f r:%.3f [cur:%.3f]" % (self.m.real, self.m.imag, self.r.real, self.curvature().real)

    def curvature (self):
        """
        Get circle's curvature.
        @rtype: float
        @return: Curvature of the circle.
        """
        return 1/self.r

def outerTangentCircle( circle1, circle2, circle3 ):
    """
    Takes three externally tangent circles and calculates the fourth one enclosing them.
    @param circle1: first circle
    @param circle2: second circle
    @param circle3: third circle
    @type circle1: L{Circle}
    @type circle2: L{Circle}
    @type circle3: L{Circle}
    @return: The enclosing circle
    @rtype: L{Circle}
    """
    cur1 = circle1.curvature()
    cur2 = circle2.curvature()
    cur3 = circle3.curvature()
    m1 = circle1.m
    m2 = circle2.m
    m3 = circle3.m
    cur4 = -2 * sqrt( cur1*cur2 + cur2*cur3 + cur1 * cur3 ) + cur1 + cur2 + cur3
    m4 = ( -2 * sqrt( cur1*m1*cur2*m2 + cur2*m2*cur3*m3 + cur1*m1*cur3*m3 ) + cur1*m1 + cur2*m2 + cur3*m3 ) /  cur4
    circle4 = Circle( m4.real, m4.imag, 1/cur4 )
    
    return circle4
    

def tangentCirclesFromRadii( r2, r3, r4 ):
    """
    Takes three radii and calculates the corresponding externally
    tangent circles as well as a fourth one enclosing them. The enclosing
    circle is the first one.

    @param r2, r3, r4: Radii of the circles to calculate
    @type r2: int or float
    @type r3: int or float
    @type r4: int or float
    @return: The four circles, where the first one is the enclosing one.
    @rtype: (L{Circle}, L{Circle}, L{Circle}, L{Circle})
    """
    circle2 = Circle( 0, 0, r2 )
    circle3 = Circle( r2 + r3, 0, r3 )
    m4x = (r2*r2 + r2*r4 + r2*r3 - r3*r4) / (r2 + r3)
    m4y = sqrt( (r2 + r4) * (r2 + r4) - m4x*m4x )
    circle4 = Circle( m4x, m4y, r4 )
    circle1 = outerTangentCircle( circle2, circle3, circle4 )
    return ( circle1, circle2, circle3, circle4 )

def secondSolution( fixed, c1, c2, c3 ):
    """
    If given four tangent circles, calculate the other one that is tangent
    to the last three.
    
    @param fixed: The fixed circle touches the other three, but not
    the one to be calculated.
    
    @param c1, c2, c3: Three circles to which the other tangent circle
    is to be calculated.

    @type fixed: L{Circle}
    @type c1: L{Circle}
    @type c2: L{Circle}
    @type c3: L{Circle}
    @return: The circle.
    @rtype: L{Circle}
    """
    
    curf = fixed.curvature()
    cur1 = c1.curvature()
    cur2 = c2.curvature()
    cur3 = c3.curvature()

    curn = 2 * (cur1 + cur2 + cur3) - curf
    mn = (2 * (cur1*c1.m + cur2*c2.m + cur3*c3.m) - curf*fixed.m ) / curn
    return Circle( mn.real, mn.imag, 1/curn )

class ApollonianGasket(object):
    """
    Container for an Apollonian Gasket.
    """
    def __init__(self, r1, r2, r3):
        """
        Creates a basic apollonian Gasket with four circles.  

        @param r1, r2, r3: The radii of the three inner circles of the
        starting set (i.e. depth 0 of the recursion). The fourth,
        enclosing circle will be calculated from them.
        @type r1: int or float
        @type r2: int or float
        @type r3: int or float
        """
        self.start = tangentCirclesFromRadii( r1, r2, r3 )
        self.genCircles = list(self.start)

    def recurse(self, circles, depth, maxDepth):
        """Recursively calculate the smaller circles of the AG up to the
        given depth. Note that for depth n we get 2*3^{n+1} circles.

        @param maxDepth: Maximal depth of the recursion.
        @type maxDepth: int

        @param circles: 4-Tuple of circles for which the second
        solutions are calculated
        @type circles: (L{Circle}, L{Circle}, L{Circle}, L{Circle})

        @param depth: Current depth
        @type depth: int
        """
        if( depth == maxDepth ):
            return
        (c1, c2, c3, c4) = circles
        if( depth == 0 ):
            # First recursive step, this is the only time we need to
            # calculate 4 new circles.
            del self.genCircles[4:]
            cspecial = secondSolution( c1, c2, c3, c4 )
            self.genCircles.append( cspecial )
            self.recurse( (cspecial, c2, c3, c4), 1, maxDepth )

        cn2 = secondSolution( c2, c1, c3, c4 )
        self.genCircles.append( cn2 )
        cn3 = secondSolution( c3, c1, c2, c4 )
        self.genCircles.append( cn3 )
        cn4 = secondSolution( c4, c1, c2, c3 )
        self.genCircles.append( cn4 )               

        self.recurse( (cn2, c1, c3, c4), depth+1, maxDepth )
        self.recurse( (cn3, c1, c2, c4), depth+1, maxDepth )
        self.recurse( (cn4, c1, c2, c3), depth+1, maxDepth )

    def toSVG( self, filename, colorMode = "none", colorScheme = "Blues", colorNum = 7 ):
        """
        Save AG to file.
        @param filename: The name of the file. Will be overwritten if exists.
        @type filename: string
        """
        # Biggest circle (the enclosing one, hopefully) which has negative radius
        big = min( self.genCircles, key=lambda c: c.r.real )
        self.genCircles.remove(big)
        self.genCircles.insert(0, big)

        if big.r.real >= 0:
            print( "Warning: No enclosing circle present. Not saving anything. First curvatures: %d %d %d" % (self.start[1].curvature(), self.start[1].curvature(), self.start[1].curvature()) )

        corner = big.m - ( abs(big.r) + abs(big.r) * 1j )
        vbwidth = abs(big.r)*2
        width = 500

        # Open file
        outFile = open(filename, "w")
        
        # Set up viewBox
        outFile.write( '<svg xmlns="http://www.w3.org/2000/svg" width="%f" height="%f" viewBox="%f %f %f %f">\n' % (width, width, corner.real, corner.imag, vbwidth, vbwidth))

        outFile.write( '<g stroke-width="%f">\n' % (vbwidth/width) )

        # Iterate through circle list, circles with radius<treshold
        # will not be saved because they are too small for printing.
        tres = 0.005 * abs(big.r)

        for c in self.genCircles:
            if abs(c.r) > tres:
                if( colorMode == "none" ):
                    fill = "none"
                elif( colorMode == "radius" ):
                    fill = mapToColor( abs(c.r), tres, abs(big.r), colorScheme, colorNum )
                elif( colorMode == "plan"):
                    fill = "none"
                    scale = 1.5/abs(big.r)
                    outFile.write('<text x="%f" y="%f" font-size="2" text-anchor="middle">%.2f</text>\n' % ( c.m.real, c.m.imag, abs(c.r)*scale ))
                else:
                    fill = "none"
                    print( "Warning: Unknown colorMode: %s" % colorMode )
                outFile.write( '<circle cx="%f" cy="%f" r="%f" fill="%s" stroke="black"/>\n' % (c.m.real, c.m.imag, abs(c.r), fill) )

        outFile.write( '</g>\n' )
        
        # Dump footer and close
        outFile.write( '</svg>\n' )
        outFile.close( )

def mapToColor( num, nmin, nmax, scheme, schemenum ):
    d = nmax - nmin
    idx = int( abs((log(100*(num - nmin) + 1)) / (log(100*d + 1))) * (schemenum-1) )
    #print( "nmin: %f nmax: %f" % (nmin, nmax) )
    #print( "d: %f idx: %d num: %f" % (d, idx, num) )

    if idx >= schemenum:
        print( "Warning: Index %d out of range!" % idx )
        idx = schemenum - 1

    return mycolordict[scheme][str(schemenum)][idx]
    
        
if  __name__ == "__main__":
    ag = ApollonianGasket( 1, 1, 1 )
    ag.recurse( ag.start, 0, 3 )

    # Hack: scale up so that text has reasonable size
    #ag.genCircles = list(map( lambda foo: Circle( foo.m.real*20, foo.m.imag*20, foo.r*20 ), ag.genCircles ))
    #
    #ag.toSVG("test.svg", "plan")

    ag.toSVG("ag-ludger-briefkopf.svg", "none" )



    exit( )

    random.seed( )

    for key in mycolordict:
        print( "Calculating for Scheme: %s" % key )
        n = len(mycolordict[key])
        c1 = random.randrange( 1, 20, 1 ) 
        c2 = random.randrange( 1, 20, 1 ) 
        c3 = random.randrange( 1, 20, 1 ) 
        ag = ApollonianGasket( 1/c1, 1/c2, 1/c3 )
        ag.recurse( ag.start, 0, 5 )
        ag.toSVG( "ColorTest/ag_%s-%d_%d_%d_%d.svg" % (key, n, c1, c2, c3), "radius", key, n )
