# Select a color from colorbrewer schemes

import json

class ColorMap(object):
    def __init__(self, default):
        self.pairs = []
        self.default = default

    def add_interval(self, left, right, color):
        self.pairs.append((left, right, color))

    def color_for(self, number):
        # Map number to color. If not found, return default value.
        ret = self.default
        for p in self.pairs:
            if (number >= p[0]) and (number <= p[1]):
                ret = p[2]
                break
        return ret

class ColorScheme(object):
    def __init__(self, filename):
        json_data = open(filename)

        self.schemes=json.load(json_data)
        json_data.close()

    def info(self):
        infos = []
        for name in self.schemes:
            smallest = min(self.schemes[name], key=lambda k: len(self.schemes[name][k]))
            biggest = max(self.schemes[name], key=lambda k: len(self.schemes[name][k]))
            infos.append({"name" : name, "low" : int(smallest), "high" : int(biggest)})
        return infos

    def makeMap(self, frm, to, name, res):
        delta = to-frm
        step = delta/res
        colors = self.schemes[name][str(res)]
        mp = ColorMap("none")
        # Items are (lower_bound, color)
        for n in range(res):
            mp.add_interval(frm + n*step, frm + (n+1)*step, colors[n])
        return mp
