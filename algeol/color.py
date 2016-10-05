
import math

from . import lia

V3 = lia.Vector3
M3 = lia.Matrix3


class HSL:
    def __init__(self, h=0.0, s=0.0, l=0.0):
        self.h = h  # 0 .. 1.0, Hue
        self.s = s  # 0 .. 1.0, Saturation
        self.l = l  # 0 .. 1.0, Lightness

    def hue6(self):
        return math.floor(self.h * 6)

    def calcMd(self):
        h6 = self.h * 6.0
        d6 = self.hue6()
        if d6 == 0:
            return h6
        elif d6 == 1:
            return 2.0 - h6
        elif d6 == 2:
            return h6 - 2.0
        elif d6 == 3:
            return 4.0 - h6
        elif d6 == 4:
            return h6 - 4.0
        elif d6 == 5:
            return 6.0 - h6
        return 0

    def calcMnMdMx(self):
        ld = abs(2 * self.l - 1.0) # 0 .. 1.0, 0%(黒):0, 25%:0.5, 50%:1.0, 75%:0.5, 100%(白):0
        sld = self.s * ld / 2 # 0 .. 0.5
        mn = self.l - sld # 0 .. 1.0
        mx = self.l + sld # 0 .. 1.0
        md = self.calcMd()
        return (mn, md, mx)

    def rgb(self):
        mn, md, mx = self.calcMnMdMx()
        d = self.hue6()
        if d == 0:
            return RGB(mx, md, mn)
        elif d == 1:
            return RGB(md, mx, mn)
        elif d == 2:
            return RGB(mn, mx, md)
        elif d == 3:
            return RGB(mn, md, mx)
        elif d == 4:
            return RGB(md, mn, mx)
        elif d == 5:
            return RGB(mx, mn, md)
        return RGB(0, 0, 0)


class RGB:
    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.r = r  # 0 .. 1.0, Red
        self.g = g  # 0 .. 1.0, Green
        self.b = b  # 0 .. 1.0, Blue

    def toTuple(self):
        return (self.r, self.g, self.b)

    def min(self):
        return min(self.r, self.g, self.b)

    def max(self):
        return max(self.r, self.g, self.b)

    def hsl(self):
        mn = self.min()
        mx = self.max()
        e = 0.005
        l = (mn + mx) / 2
        sd = 1 - abs(mn + mx - 1) # 0..1
        s = (mx - mn) / sd if sd > e else 0
        hd = mx - mn
        if hd < e:
            h = 0.0
        elif self.b == mn:
            h = 1.0 + (self.g - self.r) / hd
        elif self.r == mn:
            h = 3.0 + (self.b - self.g) / hd
        elif self.g == mn:
            h = 5.0 + (self.r - self.b) / hd
        else:
            h = 0.0
        return HSL(h, s, l)

# D65 sRGB
class SRGB65(RGB):
    def __init__(self, r=0.0, g=0.0, b=0.0):
        RGB.__init__(self, r, g, b)

    @classmethod
    def toLinear(cls, n=0.0):
        if n > 0.040450:
            return math.pow((n + 0.055) / 1.055, 2.4)
        else:
            return n / 12.92

    # Linear RGB
    def lrgb(self):
        r, g, b = [self.toLinear(n) for n in self.toTuple()]
        return LRGB65(r, g, b)

# D65 Linear RGB
class LRGB65(RGB):
    def __init__(self, r=0.0, g=0.0, b=0.0):
        RGB.__init__(self, r, g, b)

    @classmethod
    def toNonLinear(self, n=0.0):
        if n > 0.0031308:
            return 1.055 * math.pow(n, 1 / 2.4) - 0.055
        else:
            return n * 12.92

    MxXYZ65 = M3.RowTuples(
        (0.412391, 0.357584, 0.180481),
        (0.212639, 0.715169, 0.072192),
        (0.019331, 0.119195, 0.950532))

    MxXYZ50 = M3.RowTuples(
        (0.436041, 0.385113, 0.143046),
        (0.222485, 0.716905, 0.060610),
        (0.013920, 0.097067, 0.713913))

    # sRGB
    def srgb(self):
        r, g, b = [self.toNonLinear(n) for n in self.toTuple()]
        return SRGB65(r, g, b)

    # D65 XYZ
    def xyz65(self):
        return V3.Tuple(self.toTuple()).projection(self.MxXYZ65)

    # D50 XYZ
    def xyz50(self):
        return V3.Tuple(self.toTuple()).projection(self.MxXYZ50)



# XYZ色空間
class XYZ:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def toTuple(self):
        return (self.x, self.y, self.z)


class XYZ65(XYZ):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        XYZ.__init__(self, x, y, z)

    MxLRGB65 = M3.RowTuples(
        (+3.240970, -1.537383, -0.498611),
        (-0.969244, +1.875968, +0.041555),
        (+0.055630, -0.203977, +1.056972))

    def lrgb65(self):
        return V3.Tuple(self.toTuple()).projection(self.MxLRGB65)

class XYZ50(XYZ):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        XYZ.__init__(self, x, y, z)

    Xn = 0.9642 # 白色点X
    Yn = 1.0000 # 白色点Y
    Zn = 0.8249 # 白色点Z

    MxLRGB65 = M3.RowTuples(
        (+3.134187, -1.617209, -0.490694),
        (-0.978749, +1.916130, +0.033433),
        (+0.071964, -0.228994, +1.405754))

    def lrgb65(self):
        return V3.Tuple(self.toTuple()).projection(self.MxLRGB65)

    @classmethod
    def toLab(self, n=0.0):
        if n > 0.008856:
            return math.pow(n, 1 / 3)
        else:
            return (math.pow(29 / 3, 3) * n + 16) / 116

    def lab(self):
        xn = self.toLab(self.x / self.Xn)
        yn = self.toLab(self.y / self.Yn)
        zn = self.toLab(self.z / self.Zn)
        l = 116 * yn - 16
        a = 500 * (xn - yn)
        b = 200 * (yn - zn)
        return Lab(l, a, b)

class Lab:
    def __init__(self, l=0.0, a=0.0, b=0.0):
        self.l = l
        self.a = a
        self.b = b

    def toTuple(self):
        return (self.l, self.a, self.b)

    @classmethod
    def toXyz(self, n=0.0):
        if n > 0.206896:
            return math.pow(n, 3)
        else:
            return math.pow(3 / 29, 3) * (116 * n - 16)

    def xyz50(self):
        fy = (self.l + 16) / 116
        fx = fy + (self.a / 500)
        fz = fy - (self.b / 200)
        x = self.toXyz(fx) + XYZ50.Xn
        y = self.toXyz(fy) + XYZ50.Yn
        z = self.toXyz(fz) + XYZ50.Zn
        return XYZ50(x, y, z)

