# Linear Algebra

import math
from . import const


def add(a=(0.0,), b=(0.0,), c=1):
    return [a[i] + b[i] for i in range(c)]

def sub(a=(0.0,), b=(0.0,), c=1):
    return [a[i] - b[i] for i in range(c)]

def scalar(a=(0.0,), b=1.0, c=1):
    return [a[i] * b for i in range(c)]

def hadamard(a=(0.0,), b=(0.0,), c=1):
    return [a[i] * b[i] for i in range(c)]

# Inner Product 内積
def ip(a=(0.0,), b=(0.0,), c=1):
    return sum([a[i] * b[i] for i in range(c)])

# Cross Product 外積
def cp2(a=(0.0,), b=(0.0,)):
    return a[0] * b[1] - a[1] * b[0]

def cp3(a=(0.0,), b=(0.0,)):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0])


class Vector:
    Dim = 0

    @classmethod
    def Tuple(cls, t=(0.0,)):
        return Vector()

    def clone(self):
        return Vector()

    def tuple(self):
        return ()

    def toString(self):
        return '()'

    def __repr__(self):
        return '<{0}: {1}>'.format('Vector', self.toString())

    # 加算
    def __add__(self, v):
        return self.add(v)

    def add(self, v):
        if isinstance(v, Vector):
            v = v.tuple()
        return self.Tuple(add(self.tuple(), v, self.Dim))

    # 減算
    def __sub__(self, v):
        return self.sub(v)

    def sub(self, v):
        if isinstance(v, Vector):
            v = v.tuple()
        return self.Tuple(sub(self.tuple(), v, self.Dim))

    # スカラー倍
    def __mul__(self, n=1.0):
        return self.scalar(n)

    def scalar(self, n=1.0):
        return self.Tuple(scalar(self.tuple(), n, self.Dim))

    def __neg__(self):
        return self.scalar(-1)


    # アダマール積
    def hadamard(self, v):
        if isinstance(v, Vector):
            v = v.tuple()
        return hadamard(self.tuple(), v, self.Dim)

    # Inner Product 内積
    def ip(self, v):
        if isinstance(v, Vector):
            v = v.tuple()
        return ip(self.tuple(), v, self.Dim)

    # 長さの二乗
    def length2(self):
        v = self.tuple()
        return ip(v, v, self.Dim)

    # 長さ
    def length(self):
        return math.sqrt(self.length2())

    # 単位ベクトル
    def normalize(self):
        return self.scalar(1 / self.length())

    def projection(self, m):
        return m.projection(self)

class Vector2(Vector):
    Dim = 2

    @classmethod
    def Tuple(cls, t=(0.0, 0.0)):
        return Vector2(t[0], t[1])

    def __init__(self, x=0.0, y=0.0):
        Vector.__init__(self)
        self.x = x
        self.y = y

    def clone(self):
        return Vector2(self.x, self.y)

    def tuple(self):
        return (self.x, self.y)

    def toString(self):
        return '(%.1f, %.1f)' % (self.x, self.y)

    def __repr__(self):
        return '<{0}: {1}>'.format('Vector2', self.toString())

    def cp(self, v):
        if isinstance(v, Vector):
            v = v.tuple()
        return cp2(self.tuple(), v)

    def v3(self, z=0.0):
        return Vector3(self.x, self.y, z)

class Vector2C:
    Zero = Vector2(0, 0)
    One = Vector2(1, 1)
    UnitX = Vector2(1, 0)
    UnitY = Vector2(0, 1)
    UnitXR = Vector2(-1, 0)
    UnitYR = Vector2(0, -1)
    EmptyList = [Zero for i in range(0)]

    
class Vector3(Vector):
    Dim = 3

    @classmethod
    def Tuple(cls, tuple=(0.0, 0.0, 0.0)):
        return Vector3(tuple[0], tuple[1], tuple[2])

    def __init__(self, x=0.0, y=0.0, z=0.0):
        Vector.__init__(self)
        self.x = x
        self.y = y
        self.z = z

    def clone(self):
        return Vector3(self.x, self.y, self.z)

    def tuple(self):
        return (self.x, self.y, self.z)

    def toString(self):
        return '(%.1f, %.1f, %.1f)' % (self.x, self.y, self.z)

    def __repr__(self):
        return '<{0}: {1}>'.format('Vector3', self.toString())

    def add3(self, x=0.0, y=0.0, z=0.0):
        return self.add((x, y, z))

    def sub3(self, x=0.0, y=0.0, z=0.0):
        return self.sub((x, y, z))

    def hadamard3(self, x=0.0, y=0.0, z=0.0):
        return self.hadamard((x, y, z))

    def cp(self, v):
        if isinstance(v, Vector):
            v = v.tuple()
        return self.Tuple(cp3(self.tuple(), v))

    def v2(self):
        return Vector2(self.x, self.y)

    def v4(self, w=0.0):
        return Vector4(self.x, self.y, self.z, w)

    def m4move(self):
        return Matrix4((
            (1, 0, 0, self.x),
            (0, 1, 0, self.y),
            (0, 0, 1, self.z),
            (0, 0, 0, 1)))

    def m4scale(self):
        return Matrix4((
            (self.x, 0, 0, 0),
            (0, self.y, 0, 0),
            (0, 0, self.z, 0),
            (0, 0, 0, 1)))

class Vector3C:
    Zero = Vector3(0, 0, 0)
    One = Vector3(1, 1, 1)
    UnitX = Vector3(1, 0, 0)
    UnitY = Vector3(0, 1, 0)
    UnitZ = Vector3(0, 0, 1)
    EmptyList = tuple([Vector3() for i in range(0)])

    
class Vector4(Vector):
    Dim = 4

    @classmethod
    def Tuple(cls, t=(0.0, 0.0, 0.0, 0.0)):
        return Vector4(t[0], t[1], t[2], t[3])

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def clone(self):
        return Vector4(self.x, self.y, self.z, self.w)

    def tuple(self):
        return (self.x, self.y, self.z, self.w)

    def toString(self):
        return '(%.1f, %.1f, %.1f, %.1f)' % (self.x, self.y, self.z, self.w)

    def __repr__(self):
        return '<{0}: {1}>'.format('Vector4', self.toString())

    def v3(self):
        return Vector3(self.x, self.y, self.z)
    
class Vector4C:
    Zero = Vector4(0, 0, 0, 0)
    One = Vector4(1, 1, 1, 1)
    UnitX = Vector4(1, 0, 0, 0)
    UnitY = Vector4(0, 1, 0, 0)
    UnitZ = Vector4(0, 0, 1, 0)
    UnitW = Vector4(0, 0, 0, 1)
    EmptyList = [Vector4() for i in range(0)]



class Matrix:
    Dim = 0

    @classmethod
    def Rows(cls, t=((0.0,),)):
        return Matrix(t)

    @classmethod
    def Cols(cls, t=((0.0,),)):
        return Matrix(cls.T(t))

    @classmethod
    def T(cls, t=((0.0,),)):
        dim = cls.Dim
        rows = []
        for i in range(dim):
            row = [t[i][j] for j in range(dim)]
            rows.append(row)
        return rows

    def __init__(self, t=((0.0,),)):
        self._rc = t
    
    def tuple(self):
        return self._rc

    def toString(self):
        rows = []
        for row in self._rc:
            row2 = ', '.join(['%.1f' % (c) for c in row])
            rows.append(row2)
        return '((%s))' % ('), ('.join(rows))

    def __repr__(self):
        return '<{0}: {1}>'.format('Matrix', self.toString())

    def row(self, i=0):
        return self._rc[i]

    def rows(self):
        return [self.row(i) for i in range(self.Dim)]

    def col(self, j=0):
        return [self._rc[i][j] for i in range(self.Dim)]
    
    def cols(self):
        return [self.col(i) for i in range(self.Dim)]

    def __mul__(self, dist):
        return self.mul(dist)

    def mul(self, dist):
        dim = self.Dim
        assert dim == dist.Dim
        lRows = self.rows()
        rCols = dist.cols()
        m = []
        for i in range(dim):
            row = [ip(lRows[i], rCols[j], dim) for j in range(dim)]
            m.append(row)
        return self.Rows(m)

    def projection(self, dist):
        dim = self.Dim
        assert isinstance(dist, Vector) and dim == dist.Dim
        lRows = self.rows()
        rCol = dist.tuple()
        v = [ip(lRows[i], rCol, dim) for i in range(dim)]
        return dist.Tuple(v)

class Matrix2(Matrix):
    Dim = 2

    @classmethod
    def Rows(cls, t=((0.0,),)):
        return Matrix2(t)

    @classmethod
    def Cols(cls, t=((0.0,),)):
        return Matrix2(cls.T(t))
    
    def __init__(self, t=((0.0,),)):
        Matrix.__init__(self, t)

    def __repr__(self):
        return '<{0}: {1}>'.format('Matrix2', self.toString())

class Matrix2C:
    Unit = Matrix2.Cols(((1, 0), (0, 1)))
    Turn90 = Matrix2.Cols(((0, 1), (-1, 0)))
    Turn180 = Matrix2.Cols(((-1, 0), (0, -1)))
    Turn270 = Matrix2.Cols(((0, -1), (1, 0)))


class Matrix3(Matrix):
    Dim = 3

    @classmethod
    def Rows(cls, t=((0.0,),)):
        return Matrix3(t)

    @classmethod
    def Cols(cls, t=((0.0,),)):
        return Matrix3(cls.T(t))
    
    def __init__(self, t=((0.0,),)):
        Matrix.__init__(self, t)

    def __repr__(self):
        return '<{0}: {1}>'.format('Matrix3', self.toString())

    def m4(self):
        t = (
            list(self._rc[0]) + [0],
            list(self._rc[1]) + [0],
            list(self._rc[2]) + [0],
            (0, 0, 0, 1),
            )
        return Matrix4(t)

class Matrix3C:
    Unit = Matrix3.Cols(((1,0,0), (0,1,0), (0,0,1)))

class Matrix4(Matrix):
    Dim = 4

    @classmethod
    def Rows(cls, t=((0.0,),)):
        return Matrix4(t)

    @classmethod
    def Cols(cls, t=((0.0,),)):
        return Matrix4(cls.T(t))
    
    def __init__(self, t=((0.0,),)):
        Matrix.__init__(self, t)

    def __repr__(self):
        return '<{0}: {1}>'.format('Matrix4', self.toString())
    
class Matrix4C:
    Unit = Matrix4.Cols(((1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1)))




if __name__ == '__main__':
    print('lia.py __main__ start')
    print('lia.py __main__ end')
