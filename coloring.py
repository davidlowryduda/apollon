# Select a color from colorbrewer schemes

import json

class ColorMap(object):
    """
    Map numbers to colors.
    """
    def __init__(self, default):
        """
        @param default: Is returned when a number can't be mapped.
        """
        self.pairs = []
        self.default = default

    def add_interval(self, left, right, color):
        """
        A number in interval [left,right] gets mapped to color.
        """
        self.pairs.append((left, right, color))

    def color_for(self, number):
        """
        Map number to color. If not found, return default value.
        """
        ret = self.default
        for p in self.pairs:
            if (number >= p[0]) and (number <= p[1]):
                ret = p[2]
                break
        return ret

class ColorScheme(object):
    """
    Color Scheme helper class.
    """
    def __init__(self, filename):
        """
        Load color scheme definitions from json file.
        """
        json_data = open(filename)

        self.schemes=json.load(json_data)
        json_data.close()

    def info(self):
        """
        Get information on available color schemes
        """
        infos = []
        for name in self.schemes:
            smallest = min(self.schemes[name], key=lambda k: len(self.schemes[name][k]))
            biggest = max(self.schemes[name], key=lambda k: len(self.schemes[name][k]))
            infos.append({"name" : name, "low" : int(smallest), "high" : int(biggest)})
        return infos

    def makeMap(self, frm, to, name, res):
        """
        Construct a L{ColorMap} that maps numbers between frm and to to color scheme name with resolution res.
        """
        # TODO: Proper error handling when name or res are not available
        delta = to-frm
        step = delta/res
        colors = self.schemes[name][str(res)]
        mp = ColorMap("none")
        # Items are (lower_bound, color)
        for n in range(res):
            mp.add_interval(frm + n*step, frm + (n+1)*step, colors[n])
        return mp
