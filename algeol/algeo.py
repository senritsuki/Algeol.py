# Algeol - Algorithmic Geometry Generating Library

import math
from . import lia
from . import unit

V2 = lia.Vector2
V3 = lia.Vector3
V3z = lia.Vector3C.Zero
V3o = lia.Vector3C.One
V3l = lia.Vector3C.EmptyList
M4u = lia.Matrix4C.Unit
Rad = unit.Rad
Deg = unit.Deg
Deg0 = unit.RadC.Deg0
CD = unit.CD



# Linear Algebra   
class Lia:
    def __init__(self, m=M4u):
        self.m4 = m

    def move3(self, x=0.0, y=0.0, z=0.0):
        return self.move(V3(x, y, z))

    def move(self, v=V3z):
        return Lia(v.m4move().mul(self.m4))

    def turnX(self, rad=Deg0):
        return Lia(rad.turnX().m4().mul(self.m4))

    def turnY(self, rad=Deg0):
        return Lia(rad.turnY().m4().mul(self.m4))

    def turnZ(self, rad=Deg0):
        return Lia(rad.turnZ().m4().mul(self.m4))

    def scale3(self, x=1.0, y=1.0, z=1.0):
        return self.scale(V3(x, y, z))

    def scale2(self, r=1.0, z=1.0):
        return self.scale(V3(r, r, z))

    def scale1(self, r=1.0):
        return self.scale(V3(r, r, r))

    def scale(self, v=V3o):
        return Lia(v.m4scale().mul(self.m4))

    def skew(self, xy=0.0, xz=0.0, yz=0.0, yx=0.0, zx=0.0, zy=0.0):
        return Lia(lia.Matrix3.Cols((1, xy, xz), (yx, 1, yz), (zx, zy, 1)).m4().mul(self.m4))

    def basis(self, x=V3z, y=V3z, z=V3z):
        return Lia(lia.Matrix3.Cols(x, y, z).m4().mul(self.m4))

    def projection(self, v):
        return v.v4(1).projection(self.m4).v3()

    def projections(self, verts=()):
        return [self.projection(v) for v in verts]



class LtBase:
    def __repr__(self):
        return '<%s: %s>' % ('Projectable', '')

    # not immutable!
    def apply(self, lia):
        return self

    def clone(self):
        return LtBase()

    def duplicate(self, lia):
        return self.clone().apply(lia)

    def duplicates(self, lias=[]):
        return LtList([self.duplicate(lia) for lia in lias])
    

class LtList(list, LtBase):
    def __init__(self, iterable=()):
        list.__init__(self, iterable)
        LtBase.__init__(self)

    def __repr__(self):
        return '<%s: %s>' % ('Projectable', '')

    # override LtBase
    def clone(self):
        li = [lt.clone() for lt in self]
        return LtList(li)

    # not immutable!
    def apply(self, lia):
        for lt in self:
            lt.apply(lia)
        return self


class LtDict(dict, LtBase):
    def __init__(self, iterable=()):
        dict.__init__(self, iterable)
        LtBase.__init__(self)

    def __repr__(self):
        return '<%s: %s>' % ('LtDict', '')
    
    # override LtBase
    def clone(self):
        dic = {}
        for key, value in self.items():
            dic[key] = value.clone()
        return LtDict(dic)

    # not immutable!
    # override LtBase
    def apply(self, lia):
        assert isinstance(lia, Lia)
        for key, value in self.items():
            value.apply(lia)
        return self

    @classmethod
    def Merge(cls, lt):
        dic = LtDict()
        cls._Merge(lt, dic)
        return dic

    @classmethod
    def _Merge(cls, dist, dic):
        if isinstance(dist, dict):
            for key, geos in dist.items():
                if key not in dic:
                    dic[key] = LtList()
                if isinstance(geos, (tuple, list)):
                    dic[key].extend(geos)
                else:
                    dic[key].append(geos)
        elif isinstance(dist, (tuple, list)):
            for dist2 in dist:
                cls._Merge(dist2, dic)
        else:
            key = 'null'
            if key not in dic:
                dic[key] = LtList()
            dic[key].append(dist)
        return None




# Geometry
class Geo(LtBase):
    def __init__(self, verts=V3l, faces=lia.const.EmptyTupleList):
        self.verts = verts
        self.faces = faces

    def __repr__(self):
        return '<%s: %s>' % ('Geo', self.toString())
    
    # override LtBase
    def clone(self):
        return Geo(self.verts, self.faces)

    # override LtBase
    # not immutable!
    def apply(self, lia):
        self.verts = self._projection(lia)
        return self

    def _projection(self, lia):
        assert isinstance(lia, Lia)
        return lia.projections(self.verts)
    
    def lines(self):
        lines = []
        for face in self.faces:
            for i1, i2 in self._face2lineIndexes(face):
                line = Line(self.verts[i1], self.verts[i2])
                lines.append(line)
        return lines

    def toObjStr(self, offset=0, scale=1.0):
        s = 'g\n'
        for v in self.verts:
            s += 'v {0}\n'.format(' '.join([str(i) for i in (v.x * scale, v.z * scale, -v.y * scale)]))
        for f in self.faces:
            s += 'f {0}\n'.format(' '.join([str(i+1+offset) for i in f]))
        return s

    def _shiftFaces(self, shift=0):
        return [tuple([i + shift for i in face]) for face in self.faces]

    @classmethod
    def _sortIndex(cls, i1, i2):
        if i1 <= i2:
            return (i1, i2)
        else:
            return (i2, i1)

    @classmethod
    def _face2lineIndexes(cls, face=()): 
        return [cls._sortIndex(face[i], face[i+1]) for i in range(len(face) - 1)]

    @classmethod
    def Merge(self, geos=[]):
        verts = []
        faces = []
        offset = 0
        for geo in geos:
            assert isinstance(geo, Geo)
            verts.extend(geo.verts)
            faces.extend([tuple([i + offset for i in face]) for face in geo.faces])
            offset += len(geo.verts)
        return Geo(verts, faces)

    @classmethod
    def Export(cls, dist, file='', _scale=1.0):
        fileName = file + '.obj'
        offset = 0  
        if isinstance(dist, dict):
            for key, geos in dist.items():
                file2 = '%s_%s' % (file, key)
                cls.Export(geos, file2, _scale)
        elif isinstance(dist, (list, tuple, Geo)):
            with open(fileName, 'w') as ost:
                cls._Export(ost, dist, offset, _scale)
            print('export %s' % (fileName))
        else:
            print('Geo.exports(): missing format.')
        return None

    @classmethod
    def _Export(cls, ost, dist, offset=0, _scale=1.0):
        if isinstance(dist, (list, tuple)):
            for o in dist:
                offset = cls._Export(ost, o, offset, _scale)
        elif isinstance(dist, Geo):
            ost.write(dist.toObjStr(offset, _scale))
            offset += len(dist.verts)
        return offset
    


class Obj(LtBase):
    def __init__(self, verts=V3l):
        LtBase.__init__(self)
        self._verts = verts

    def __repr__(self):
        return '<%s: %s>' % ('Projectables', '')
    
    # override LtBase
    def clone(self):
        return Obj(self._verts)

    # override LtBase
    # not immutable!
    def apply(self, lia):
        self._verts = self._projection(lia)
        return self

    def _projection(self, lia):
        assert isinstance(lia, Lia)
        return lia.projections(self._verts)
    
    def toTuple(self):
        return tuple(self._verts)

    def toString(self):
        return str(self.toTuple())

    # not immutable!
    def update(self, verts=V3l):
        self._verts = verts
        return self

    # virtual!
    def coord(self, i=0.0, delta=0.001):
        return V3z

    # virtual!
    def dir(self, i=0.0, delta=0.001):
        return V3z

    def cd(self, i=0.0, delta=0.001):
        return CD(self.coord(i), self.dir(i, delta))

    # virtual!
    def vertexSize(self):
        return len(self._verts)

    # virtual!
    def vertex(self, i=0):
        return self._verts[i]

    def vertices(self):
        return [self.vertex(i) for i in range(self.vertexSize())]

    def splitIndex(self, i=0.0):
        i0 = math.floor(i)
        i1 = i - i0
        if i0 == len(self._verts) and i1 == 0:
            i0 -= 1
            i1 += 1.0
        return (i0, i1)

    
# Line
class Line(Obj):
    def __init__(self, v1=V3z, v2=V3z):
        verts = (v1, v2)
        Obj.__init__(self, verts)

    def __repr__(self):
        return '<%s: %s>' % ('Line', self.toString())

    # virtual!
    def clone(self):
        v1, v2 = [self._verts[i] for i in (0, 1)]
        return Line(self._verts)
    
    # virtual!
    def coord(self, i=0.0):
        return self.start().add(self.end()).scalar(i)
    
    # virtual!
    def dir(self, i=0.0, delta=0.001):
        return self.end().sub(self.start())

    def start(self):
        return self.vertex(0)

    def end(self):
        return self.vertex(1)

    def len(self):
        return self.dir().length()

    # Horizontal Length
    def lenH(self):
        return self.dir().v2().length()

    # Vertical Length
    def lenV(self):
        return abs(self.dir().z)

    # Horizontal Radian
    def radH(self):
        d = self.dir()
        return Rad.XY(d.x, d.y)

    # Vertical Radian
    def radV(self):
        d = self.dir()
        return Rad.XY(d.v2().length(), d.z)
    
# 3次ベジェ曲線
class Bezier(Obj):
    def __init__(self, verts=V3l):
        assert len(verts) == 4
        Obj.__init__(self, verts)

    def __repr__(self):
        return '<%s: %s>' % ('Bezier', self.toString())
    
    # override
    def clone(self):
        return Bezier(self._verts)
    
    # override
    def coord(self, i=0.0):
        r1 = 1.0 - i
        r2 = i
        v1 = self.vertex(0).scalar(r1**3)
        v2 = self.vertex(1).scalar(3 * r1**2 * r2)
        v3 = self.vertex(2).scalar(3 * r1 * r2**2)
        v4 = self.vertex(3).scalar(r2**3)
        return v1.add(v2).add(v3).add(v4)
    
    # override
    def dir(self, i=0.0, delta=0.001):
        v1 = self.coord(i - delta)
        v2 = self.coord(i + delta)
        return v2.sub(v1)
    
    def start(self):
        return self.vertex(0)

    def end(self):
        return self.vertex(3)

    def startDir(self):
        return self.vertex(1).sub(self.vertex(0))

    def endDir(self):
        return self.vertex(2).sub(self.vertex(3))

# Path
class Path(Obj):
    def __init__(self, verts=V3l):
        Obj.__init__(self, verts)

    def __repr__(self):
        return '<%s: %s>' % ('Path', self.toString())
    
    # override
    def clone(self):
        return Path(self._verts)
    
    # override
    def coord(self, i=0.0):
        i0, i1 = self.splitIndex(i)
        return self.line(i0).coord(i1)
    
    # override
    def dir(self, i=0.0, delta=0.001):
        i0, i1 = self.splitIndex(i)
        return self.line(i0).dir(i1)

    def line(self, i=0):
        return Line(self.vertex(i), self.vertex(i+1))

    def lines(self):
        return [self.line(i) for i in range(self.vertexSize()-1)]

    def linesClose(self):
        return self.lines() + [self.line(-1)]

class Beziers(Obj):
    def __init__(self, verts=V3l):
        Obj.__init__(self, verts)

    def __repr__(self):
        return '<%s: %s>' % ('Beziers', self.toString())
    
    # override
    def clone(self):
        return Beziers(self._verts)
    
    # override
    def coord(self, i=0.0):
        i0, i1 = self.splitIndex(i)
        return self.bezier(i0).coord(i1)
    
    # override
    def dir(self, i=0.0, delta=0.001):
        i0, i1 = self.splitIndex(i)
        return self.bezier(i0).dir(i1)

    def bezier(self, i):
        return Bezier(self.vertex(i*3), self.vertex(i*3+1), self.vertex(i*3+2), self.vertex(i*3+3))

    def beziers(self):
        assert self.vertexSize() % 3 == 1
        return [self.bezier(i*3) for i in range((self.vertexSize() - 1) / 3)]

    def beziersClose(self):
        assert self.vertexSize() % 3 == 0
        return self.beziers() + [self.bezier(-3)]


class Plane(Obj):
    def __init__(self, o=V3z, x=V3z, y=V3z):
        Obj.__init__(self, (o, x, y))
        
    def __repr__(self):
        return '<%s: %s>' % ('Rect', self.toString())

    def o(self):
        return self._verts[0]

    def oxy(self):
        return [self._verts[i] for i in (0, 1, 2)]

    def dx(self):
        return self._verts[1] - self._verts[0]

    def dy(self):
        return self._verts[2] - self._verts[0]

    def odxy(self):
        o, x, y = self.oxy()
        return o, x-o, y-o
    
    # override
    def clone(self):
        o, x, y = self.oxy()
        return Plane(o, x, y, self.c)
    
    # override
    def coord(self, i=0.0):
        i0, i1 = self.splitIndex(i)
        return self.line(i0).coord(i1)
    
    # override
    def dir(self, i=0.0, delta=0.001):
        i0, i1 = self.splitIndex(i)
        return self.line(i0).dir(i1)
    
    # override
    def vertexSize(self):
        return 4
    
    # override
    def vertex(self, i=0):
        o = self.o()
        i2 = i % self.vertexSize()
        if i2 == 0:
            return o + self.dx()
        if i2 == 1:
            return o + self.dy()
        if i2 == 2:
            return o - self.dx()
        if i2 == 3:
            return o - self.dy()

    def line(self, i=0):
        return Line(self.vertex(i), self.vertex(i+1))

    def geoPlane(self, _do=V3z):
        c = self.vertexSize()
        o = self.o().add(_do)
        verts = [o] + [self.vertex(i) for i in range(c)]
        faces = [(0, 1+i, 1+(i+1)%c) for i in range(c)]
        return Geo(verts, faces)

    def geoCone(self, dir=V3z):
        c = self.vertexSize()
        o0 = self.o()
        o1 = o0.add(dir)
        verts = [o0, o1] + [self.vertex(i) for i in range(c)]
        faces1 = [(0, i+2, (i+1)%c+2) for i in range(c)]
        faces2 = [(1, i+2, (i+1)%c+2) for i in range(c)]
        faces = faces1 + faces2
        return Geo(verts, faces)

    def geoPrism(self, dir=V3z, r=1.0, _do1=V3z, _do2=V3z):
        do = self.o().add(dir)
        dist = self.duplicate(Lia().move(-do).scale1(r).move(do + dir))
        return self.geoArray((self, dist), _do1, _do2)

    def geoPrism2(self, dir=V3z, r1=1.0, r2=1.0, _do1=V3z, _do2=V3z):
        do = self.o().add(dir)
        dist1 = self.duplicate(Lia().move(-do).scale1(r1).move(do - dir))
        dist2 = self.duplicate(Lia().move(-do).scale1(r2).move(do + dir))
        return self.geoArray((dist1, dist2), _do1, _do2)
    
    @classmethod
    def geoArray(cls, planes=(), _do1=V3z, _do2=V3z):
        c = planes[0].vertexSize()
        verts = []
        for plane in planes:
            verts.extend([plane.vertex(i) for i in range(c)])
        faces = []
        for i in range(len(planes)-1):
            faces.extend([(c*i+j, c*i+(j+1)%c, c*(i+1)+(j+1)%c, c*(i+1)+j) for j in range(c)])
        cls.geoArrayTB(verts, faces, planes, _do1, _do2)
        return Geo(verts, faces)
    
    @classmethod
    def geoArrayTB(cls, verts=[], faces=[], planes=(), _do1=V3z, _do2=V3z):
        p1 = planes[0]
        p2 = planes[-1]
        verts.append(p1.o().add(_do1))
        verts.append(p2.o().add(_do2))
        c = p1.vertexSize()
        c2 = len(planes)
        for i, io in ((0, c*c2), (c2-1, c*c2+1)):
            faces.extend([(io, c*i+j, c*i+(j+1)%c) for j in range(c)])

    @classmethod
    def geoVArray(cls, plane, rzs=(), _do1=V3z, _do2=V3z):
        assert isinstance(plane, Plane)
        oz = plane.o().z
        lias = [Lia().move3(0, 0, -oz).scale2(r, 1).move3(0, 0, oz+z) for r, z in rzs]
        planes = [plane] + plane.duplicates(lias)
        return cls.geoArray(planes, _do1, _do2)

    @classmethod
    def geoVSynmetricalArray(cls, plane, rzs=(), _do1=V3z, _do2=V3z):
        assert isinstance(plane, Plane)
        oz = plane.o().z
        oz2 = rzs[-1].z
        rzs2 = list(rzs) + [(r, oz2 * 2 - z) for r, z in rzs[:-1][::-1]]
        lias = [Lia().move3(0, 0, -oz).scale2(r, 1).move3(0, 0, oz+rzs2[i].z) for i in range(len(rzs)*2-1)]
        planes = [plane] + plane.duplicates(lias)
        return cls.geoArray(planes, _do1, _do2)

    @classmethod
    def geoRingArray(cls, plane, hoge=()):
        hoge

    @classmethod
    def rzSymmetry(cls, rzs=(), sz=1.0):
        return [(r, sz*2-z) for r, z in rzs[::-1]]


class ClosePlane(Plane):
    def __init__(self, o=V3z, x=V3z, y=V3z):
        Plane.__init__(self, o, x, y)
        
    def __repr__(self):
        return '<%s: %s>' % ('ClosePlane', self.toString())
    
    # override
    def clone(self):
        o, x, y = self.oxy()
        return ClosePlane(o, x, y)

class OpenPlane(Plane):
    def __init__(self, o=V3z, x=V3z, y=V3z):
        Plane.__init__(self, o, x, y)
        
    def __repr__(self):
        return '<%s: %s>' % ('OpenPlane', self.toString())
    
    # override
    def clone(self):
        o, x, y = self.oxy()
        return ClosePlane(o, x, y)
    
    # override
    def vertexSize(self):
        return 3
    
    # override
    def vertex(self, i=0):
        o = self.o()
        i2 = i % self.vertexSize()
        if i2 == 0:
            return o
        if i2 == 1:
            return o + self.dx()
        if i2 == 2:
            return o + self.dy()
        
    # override
    def geoPlane(self):
        c = self.vertexSize()
        verts = [self.vertex(i) for i in range(c)]
        faces = [(0, i+1, i+2) for i in range(c-2)]
        return Geo(verts, faces)
    
    # override
    def geoCone(self, dir=V3z):
        c = self.vertexSize()
        o1 = self.o().add(dir)
        verts = [o1] + [self.vertex(i) for i in range(c)]
        faces1 = [(1, i+2, i+3) for i in range(c-2)]
        faces2 = [(0, i+2, i+3) for i in range(c-2)]
        faces3 = [(0, 1, 2), (0, 1, c)]
        faces = faces1 + faces2 + faces3
        return Geo(verts, faces)
    
    # override
    def geoPrism(self, dir=V3z, r=1.0):
        do = self.o().add(dir)
        dist = self.duplicate(Lia().move(-do).scale1(r).move(do + dir))
        return self.geoArray((self, dist))
    
    # override
    def geoPrism2(self, dir=V3z, r1=1.0, r2=1.0):
        do = self.o().add(dir)
        dist1 = self.duplicate(Lia().move(-do).scale1(r1).move(do - dir))
        dist2 = self.duplicate(Lia().move(-do).scale1(r2).move(do + dir))
        return self.geoArray((dist1, dist2))

    def duplicatesMirrorX(self):
        o, x, y = self.oxy()
        dx, dy = (x - o) * 2, (y - o) * 2
        odx, ydx = o + dx, y + dx
        return (self, self.clone().update((odx, x, ydx)))

    def duplicatesMirrorY(self):
        o, x, y = self.oxy()
        dx, dy = (x - o) * 2, (y - o) * 2
        ody, xdy = o + dy, x + dy
        return (self, self.clone().update((ody, xdy, y)))

    def duplicatesMirrorXY(self):
        o, x, y = self.oxy()
        dx, dy = (x - o) * 2, (y - o) * 2
        odx, ydx = o + dx, y + dx
        ody, xdy = o + dy, x + dy
        odxy = o + dx + dy
        return (
            self,  
            self.clone().update((ody, y, xdy)),
            self.clone().update((odxy, xdy, ydx)), 
            self.clone().update((odx, ydx, x)),
            )
    
    @classmethod
    def geoArrayTB(cls, verts=[], faces=[], planes=(), _do1=V3z, _do2=V3z):
        p1 = planes[0]
        p2 = planes[-1]
        c = p1.vertexSize()
        c2 = len(planes)
        for i in (0, c2-1):
            faces.extend([(c*i, c*i+j+1, c*i+j+2) for j in range(c-2)])


class Rect(ClosePlane):
    def __init__(self, o=V3z, x=V3z, y=V3z):
        ClosePlane.__init__(self, o, x, y)
        
    def __repr__(self):
        return '<%s: %s>' % ('Rect', self.toString())
    
    # override
    def clone(self):
        o, x, y = self.oxy()
        return Rect(o, x, y)
    
    # override
    def vertexSize(self):
        return 4
    
    # override
    def vertex(self, i=0):
        o, dx, dy = self.o(), self.dx(), self.dy()
        i2 = i % self.vertexSize()
        if i2 == 0:
            return o + dx + dy
        if i2 == 1:
            return o - dx + dy
        if i2 == 2:
            return o - dx - dy
        if i2 == 3:
            return o + dx - dy

    def divide(self, xc=2, yc=2):
        o, dx, dy = self.odxy()
        sdx = dx.scalar(1 / xc)
        sdy = dy.scalar(1 / yc)
        sdx2 = sdx.scalar(2)
        sdy2 = sdy.scalar(2)
        so = o - dx - dy + sdx + sdy
        rects = []
        for i in range(xc):
            sdx3 = sdx2.scalar(i)
            for j in range(yc):
                sdy3 = sdy2.scalar(j)
                so2 = so + sdx3 + sdy3
                rects.append(Rect(so2, so2 + sdx, so2 + sdy))
        return rects


class CloseTriangle(ClosePlane):
    def __init__(self, o=V3z, x=V3z, y=V3z):
        ClosePlane.__init__(self, o, x, y)
        
    def __repr__(self):
        return '<%s: %s>' % ('CloseTriangle', self.toString())
    
    # override
    def clone(self):
        o, x, y = self.oxy()
        return CloseTriangle(o, x, y)
    
    # override
    def vertexSize(self):
        return 3
    
    # override
    def vertex(self, i=0):
        o, dx, dy = self.o(), self.dx(), self.dy()
        i2 = i % self.vertexSize()
        if i2 == 0:
            return o + dx - dy
        if i2 == 1:
            return o + dx + dy
        if i2 == 2:
            return o - dx + dy
        
    def divideRT(self, c=2):
        o, dx, dy = self.odxy()
        sdx = dx.scalar(1 / c)
        sdy = dy.scalar(1 / c)
        sdx2 = sdx.scalar(2)
        sdy2 = sdy.scalar(2)

        triangles = []
        so = o - dx + dy + sdx - sdy
        for i in range(c):
            so2 = so + sdx2.scalar(i) - sdy2.scalar(i)
            triangles.append(CloseTriangle(so2, so2 + sdx, so2 + sdy))

        rects = []
        so = o + dx + dy - sdx - sdy
        for i in range(c-1):
            sdx3 = sdx2.scalar(i)
            for j in range(c-1-i):
                sdy3 = sdy2.scalar(j)
                so2 = so - sdx3 - sdy3
                rects.append(Rect(so2, so2 + sdx, so2 + sdy))
        return (rects, triangles)


class Ellipse(ClosePlane):
    def __init__(self, o=V3z, x=V3z, y=V3z, c=6):
        ClosePlane.__init__(self, o, x, y)
        self.c = c
        
    def __repr__(self):
        return '<%s: %s>' % ('Ellipse', self.toString())
    
    # override
    def clone(self):
        o, x, y = self.oxy()
        return Ellipse(o, x, y, self.c)
    
    # override
    def vertexSize(self):
        return self.c
    
    # override
    def vertex(self, i=0):
        o, x, y = self.oxy()
        dx, dy = x.sub(o), y.sub(o)
        rad = self.rad(i)
        rx, ry = rad.cos(), rad.sin()
        return o.add(dx.scalar(rx)).add(dy.scalar(ry))

    def rad(self, i=0):
        return unit.Deg(360 * i / self.vertexSize())


class RevArc4(OpenPlane):
    def __init__(self, o=V3z, x=V3z, y=V3z, c=6):
        OpenPlane.__init__(self, o, x, y)
        self.c = c
        
    def __repr__(self):
        return '<%s: %s>' % ('RevArc4', self.toString())
    
    # override
    def clone(self):
        o, x, y = self.oxy()
        return RevArc4(o, x, y, self.c)
    
    # override
    def vertexSize(self):
        return self.c + 2 # 辺が6なら原点含め8
    
    # override
    def vertex(self, i=0):
        o, x, y = self.oxy()
        if i == 0:
            return o
        dx, dy = x - o, y - o
        co = o + dx + dy
        cdx, cdy = x - co, y - co
        rx, ry = self.rad(i).xy()
        return co + cdx.scalar(rx) + cdy.scalar(ry)

    def rad(self, i=0):
        return unit.Deg(90 * (i-1) / self.c)

class RevArc4r(OpenPlane):
    def __init__(self, o=V3z, x=V3z, y=V3z, c=6, cx=1.0, cy=1.0, rx=1.0, ry=1.0):
        OpenPlane.__init__(self, o, x, y)
        self.c = c + 1
        self.cx = cx
        self.cy = cy
        self.rx = rx
        self.ry = ry
        
    def __repr__(self):
        return '<%s: %s>' % ('RevArc4r', self.toString())
    
    # override
    def clone(self):
        o, x, y = self.oxy()
        return RevArc4r(o, x, y, self.c, self.cx, self.cy, self.rx, self.ry)

    def numOptX(self):
        c = 0
        if self.cx < 1.0:
            c += 1
            if self.rx < 1.0:
                c += 1
        return c

    def numOptY(self):
        c = 0
        if self.cy < 1.0:
            c += 1
            if self.ry < 1.0:
                c += 1
        return c
    
    # override
    def vertexSize(self):
        c = self.c + 2 # 辺6なら点7 + 原点1
        c += self.numOptX()
        c += self.numOptY()
        return c
    
    # override
    def vertex(self, i=0):
        o, x, y = self.oxy()
        if i == 0:
            return o
        dx, dy = x - o, y - o
        rdx, rdy = dx.scalar(self.rx), dy.scalar(self.ry)
        nx = self.numOptX()
        if i == 1 and nx >= 1:
            return x
        if i == 2 and nx >= 2:
            return x + rdy.scalar(1 - self.cx)
        co = o + rdx + rdy
        if i - 1 - nx <= self.c:
            cdx = rdy.scalar(-self.cx)
            cdy = rdx.scalar(-self.cy)
            rx, ry = self.rad(i).xy()
            return co + cdx.scalar(rx) + cdy.scalar(ry)
        vsize = self.vertexSize()
        ny = self.numOptY()
        if ny >= 2 and i == vsize - 2:
            return y + rdx.scalar(1 - self.cy)
        if ny >= 1 and i == vsize - 1:
            return y
        return o

    def rad(self, i=0):
        return unit.Deg(90 * (i-1-self.numOptX()) / self.c)





class empty:
    geo = Geo()
    lia = Lia()
    
if __name__ == '__main__':
    print('algeol.py __main__ start')
    print('algeol.py __main__ end')
