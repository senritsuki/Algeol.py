# Unit 単位

import math
from . import lia
from . import const

V2 = lia.Vector2
V2z = lia.Vector2C.Zero
V3 = lia.Vector3
V3z = lia.Vector3C.Zero
M2 = lia.Matrix2
M3 = lia.Matrix3

# 角度（弧度法）
class Rad:
    @classmethod
    def mapDegRad(cls, degree=0.0):
        return degree * math.pi / 180

    @classmethod
    def mapRadDeg(cls, radian=0.0):
        return radian / math.pi * 180

    @classmethod
    def XY(cls, x=1.0, y=1.0):
        return Rad(math.atan2(y, x))

    @classmethod
    def V2(cls, v2=V2z):
        return Rad(math.atan2(v2.y, v2.x))

    def __init__(self, radian=0.0):
        self.n = radian

    def addDeg(self, d=0.0):
        return Deg(self.deg() + d)

    def __mul__(self, n=1.0):
        return self.scalar(n)

    def __div__(self, n=1.0):
        return self.scalar(1/n)

    def scalar(self, n=0.0):
        return Rad(self.n * n)

    def __neg__(self):
        return self.scalar(-1)

    def rev(self):
        return self.scalar(-1)

    def deg(self):
        return self.mapRadDeg(self.n)

    def clone(self):
        return Rad(self.n)

    def toString(self):
        return str(self.deg())

    def __repr__(self):
        return '<{0}: {1}>'.format('Rad(Deg)', self.toString())

    def cos(self):
        return math.cos(self.n)
        
    def sin(self):
        return math.sin(self.n)

    def tan(self):
        return math.tan(self.n)

    def xy(self):
        return self.cos(), self.sin()

    def v2(self):
        return V2(self.cos(), self.sin())

    def turn(self):
        c = self.cos()
        s = self.sin()
        return M2((
            (c, -s),
            (s, c)))

    def turnX(self):
        c = self.cos()
        s = self.sin()
        return M3((
            (1, 0, 0),
            (0, c, -s),
            (0, s, c)))
    
    def turnY(self):
        c = self.cos()
        s = self.sin()
        return M3((
            (c, 0, s),
            (0, 1, 0),
            (-s, 0, c)))
        
    def turnZ(self):
        c = self.cos()
        s = self.sin()
        return M3((
            (c, -s, 0),
            (s, c, 0),
            (0, 0, 1)))

# 角度（度数法）
def Deg(deg=0.0):
    return Rad(Rad.mapDegRad(deg))

class RadC:
    Deg0 = Deg(0)
    Deg5 = Deg(45)
    Deg90 = Deg(90)
    Deg180 = Deg(180)
    Deg270 = Deg(270)
    Deg360 = Deg(360)
    EmptyList = [Rad(0) for i in range(0)]

class Rad3:
    @classmethod
    def V3(cls, d=lia.Vector3C.Zero):
        x = Rad.V2(lia.Vector2(d.y, d.z))
        y = Rad.V2(lia.Vector2(d.z, d.x))
        z = Rad.V2(lia.Vector2(d.x, d.y))
        return Rad3(x, y, z)

    def __init__(self, x=RadC.Deg0, y=RadC.Deg0, z=RadC.Deg0):
        self.x = x
        self.y = y
        self.z = z


class Dir:
    def __init__(self, d=V3z):
        self.v = d

    def toTuple(self):
        return self.v.toTuple()
        
    def toString(self):
        return self.v.toString()

    def __repr__(self):
        return '<{0}: {1}>'.format('Dir', self.toString())

    def unit(self):
        return self.v.normalize()

    def length(self):
        return self.v.length()

    def radZ(self):
        return Rad.XY(self.v.x, self.v.y)

    def radX(self):
        return Rad.XY(self.v.y, self.v.z)

    def radY(self):
        return Rad.XY(self.v.z, self.v.x)

    def radV(self):
        return Rad.XY(self.v.v2().length(), self.v.z)

    def turnXtoDir(self):
        turnV = self.radV().rev().turnY()
        turnH = self.radZ().turnZ()
        return turnH.mul(turnV)

    def turnZtoDir(self):
        turnV = self.radV().rev().addDeg(90).turnY()
        turnH = self.radZ().turnZ()
        return turnH.mul(turnV)


# Coordinate 'c' & Direction 'd'
# 座標c(3次元ベクトル)と方向d(3次元ベクトル)
# - 直線cd(点cを通る方向dの直線)を表す
# - dは単位ベクトルとは限らない
class CD:
    def __init__(self, c=V3z, d=V3z):
        if isinstance(d, V3):
            d = Dir(d)
        assert isinstance(d, Dir)
        self.c = c
        self.d = d
        
    def toTuple(self):
        return (self.c, self.d)
        
    def toString(self):
        return '(%.1f, %.1f)' % self.toTuple()

    def __repr__(self):
        return '<{0}: {1}>'.format('CD', self.toString())

    # 点vを直線cdに投影
    # - return: 投影点と投影方向を表す直線
    def projection(self, v=V3z):
        d1 = v.sub(self.c)
        d2u = self.d.unit()
        d2 = d2u.scalar(d2u.ip(d1))
        d3 = d2.sub(d1)
        return CD(v.add(d3), d3)

    def dirToLine(self, dist):
        assert isinstance(dist, CD)
        d1 = self.d.normalize()
        d2 = dist.d.normalize()
        dircp = d1.cp(d2)
        dircplen = dircp.length()
        if dircplen == 0:
            return self.projection(dist.c).d
        dir = dist.c.sub(self.c)
        dircp2 = dircp.scalar(dircp.ip(dir) / dircplen)
        return Dir(dircp2)


# Cylindrical Coordinate System 円柱座標系
class CCS:
    Dim = 3

    @classmethod
    def Tuple(cls, t):
        return CCS(*t)

    @classmethod
    def V3(cls, v3):
        assert isinstance(v3, V3)
        r = v3.v2().length()
        d = Rad.mapRadDeg(math.atan2(v3.y, v3.x))
        z = v3.z
        return CCS(r, d, z)

    def __init__(self, r=1.0, d=0.0, z=0.0):
        self.r = r
        self.d = d
        self.z = z
        
    def tuple(self):
        return (self.r, self.d, self.z)
        
    def toString(self):
        return '(%.1f, %.1f, %.1f)' % self.tuple()

    def __repr__(self):
        return '<{0}: {1}>'.format('CCS', self.toString())

    def v3(self):
        v2 = Deg(self.d).v2().scalar(self.r)
        return lia.Vector3(v2.x, v2.y, self.z)

    def rad(self):
        return Deg(self.d)

    def add3(self, r=0.0, d=0.0, z=0.0):
        return self.add((r, d, z))
    
    def __add__(self, ccs):
        return self.add(ccs)

    def add(self, ccs):
        if isinstance(ccs, CCS):
            ccs = ccs.tuple()
        return self.Tuple(lia.add(self.tuple(), ccs, self.Dim))
    
    def __sub__(self, ccs):
        return self.sub(ccs)

    def sub(self, ccs):
        if isinstance(ccs, CCS):
            ccs = ccs.tuple()
        return self.Tuple(lia.sub(self.tuple(), ccs, self.Dim))

    def scale3(self, r=1.0, d=1.0, z=1.0):
        return CCS(self.r * r, self.d * d, self.z * z)
    
    def __mul__(self, n):
        return self.scalar(n)
    
    def __div__(self, n):
        return self.scalar(1/n)
    
    def __neg__(self):
        return self.scalar(-1)

    def scalar(self, n=1.0):
        return self.scale3(n, n, n)

    def cd(self, ccs, delta=0.001):
        assert isinstance(ccs, CCS)
        d1 = self.sub(ccs.scalar(delta))
        d2 = self.add(ccs.scalar(delta))
        return CD(self.v3(), d2.sub(d1))


# Spherical Coordinate System
class SCS:
    @classmethod
    def V3(cls, v3):
        assert isinstance(v3, lia.Vector3)
        r = v3.length()
        dh = Rad.mapRadDeg(math.atan2(v3.y, v3.x))
        dv = Rad.mapRadDeg(math.atan2(v3.z, v3.v2().length()))
        return SCS(r, dh, dv)

    def __init__(self, r=1.0, dh=0.0, dv=0.0):
        self.r = r
        self.dh = dh
        self.dv = dv
        
    def toTuple(self):
        return (self.r, self.dh, self.dv)
        
    def toString(self):
        return '(%.1f, %.1f, %.1f)' % self.toTuple()

    def __repr__(self):
        return '<{0}: {1}>'.format('SCS', self.toString())

    def v3(self):
        turnY = Deg(self.dv).rev().turnY()
        turnZ = Deg(self.dh).turnZ()
        return lia.Vector3(self.r, 0, 0).projection(turnZ.mul(turnY))

    def add3(self, r=1.0, dh=0.0, dv=0.0):
        return SCS(self.r + r, self.dh + dh, self.dv + dv)

    def add(self, scs):
        assert isinstance(scs, SCS)
        return SCS(self.r + scs.r, self.dh + scs.dh, self.dv + scs.dv)

    def sub(self, scs):
        assert isinstance(scs, SCS)
        return SCS(self.r - scs.r, self.dh - scs.dh, self.dv - scs.dv)

    def scale3(self, r=1.0, dh=1.0, dv=1.0):
        return SCS(self.r * r, self.dh * dh, self.dv * dv)

    def scalar(self, n=1.0):
        return self.scale3(n, n, n)

    def cd(self, scs, delta=0.001):
        assert isinstance(scs, SCS)
        d1 = self.sub(scs.scalar(delta))
        d2 = self.add(scs.scalar(delta))
        return CD(self.v3(), d2.sub(d1))


# Polar Coordinate System
class Polar:
    @classmethod
    def V2(cls, v2):
        assert isinstance(v2, lia.Vector2)
        r = v2.length()
        d = Rad.mapRadDeg(math.atan2(v2.y, v2.x))
        return Polar

    def __init__(self, r=1.0, d=0.0):
        self.r = r  # 0.0 ..
        self.d = d  # 0 .. 360

    def v2(self):
        return Deg(self.d).v2().scalar(self.r)

    def z(self, z=0.0):
        return PolarZ(self, z)

class PolarZ:
    @classmethod
    def V3(cls, v3):
        assert isinstance(v3, lia.Vector3)
        return PolarZ(lia.Vector2(v3.x, v3.y), v3.z)
    
    @classmethod
    def RDZ(cls, r=1.0, d=0.0, z=0.0):
        return PolarZ(Polar(r, d), z)

    def __init__(self, p, z=0.0):
        assert isinstance(p, Polar)
        self.p = p
        self.z = z

    def v3(self):
        v2 = self.p.v2()
        return lia.Vector3(v2.x, v2.y, self.z)


class PolarSquare:
    def __init__(self, ir=0.0, d=0):
        if d < 0:
            d = 8 - (-d % 8)
        d %= 8
        self.r = ir  # 半径
        self.d = d  # 角度 0:0*PI, 4:1*PI, 8:2*PI

    def polar(self):
        r = self.r if self.d % 2 == 0 else self.r * const.r2
        return Polar(r, self.d * 45)

    def v2(self):
        return self.polar().v2()

    def z(self, z=0.0):
        return PolarSquareZ(self, z)

class PolarSquareZ:
    def __init__(self, ps, z=0.0):
        assert isinstance(ps, PolarSquare)
        self.ps = ps
        self.z = z

    def v3(self):
        v2 = self.ps.v2()
        return lia.Vector3(v2.x, v2.y, self.z)


class empty:
    polar = Polar()
    polarZ = PolarZ.RDZ()
    ccs = CCS()
    scs = SCS()


def TestDeg():
    name = 'Deg(30)'
    deg = Deg(30)
    print('%s: %s' % (name, deg))
    print('%s.cos(): %.1f' % (name, deg.cos()))
    print('%s.sin(): %.1f' % (name, deg.sin()))
    print('%s.tan(): %.1f' % (name, deg.tan()))
    print('%s.turn(): %s' % (name, deg.turn()))
    print('%s.turnX(): %s' % (name, deg.turnX()))
    print('%s.turnY(): %s' % (name, deg.turnY()))
    print('%s.turnZ(): %s' % (name, deg.turnZ()))

def TestCCS():
    fn = lambda v: (v, CCS.V3(v), CCS.V3(v).v3())
    print('V3 -> CCS -> V3: %s -> %s -> %s' % fn((lia.Vector3(1, 0, 0))))
    print('V3 -> CCS -> V3: %s -> %s -> %s' % fn((lia.Vector3(0, 1, 0))))
    print('V3 -> CCS -> V3: %s -> %s -> %s' % fn((lia.Vector3(0, 0, 1))))
    print('V3 -> CCS -> V3: %s -> %s -> %s' % fn((lia.Vector3(1, 1, 1))))

def TestSCS():
    fn = lambda v: (v, SCS.V3(v), SCS.V3(v).v3())
    print('V3 -> SCS -> V3: %s -> %s -> %s' % fn((lia.Vector3(1, 0, 0))))
    print('V3 -> SCS -> V3: %s -> %s -> %s' % fn((lia.Vector3(0, 1, 0))))
    print('V3 -> SCS -> V3: %s -> %s -> %s' % fn((lia.Vector3(0, 0, 1))))
    print('V3 -> SCS -> V3: %s -> %s -> %s' % fn((lia.Vector3(1, 1, 1))))


if __name__ == '__main__':
    print('unit.py __main__ start')
    TestDeg()
    TestCCS()
    TestSCS()
    print('unit.py __main__ end')
