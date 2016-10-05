
import math
from . import lia

V3 = lia.Vector3


# 複素数
class Complex:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def add(self, c):
        assert isinstance(c, Complex)
        return Complex(self.x + c.x, self.y + c.y)

    def sub(self, c):
        assert isinstance(c, Complex)
        return Complex(self.x - c.x, self.y - c.y)

    def scalar(self, n=1.0):
        return Complex(self.x * n, self.y * n)

    def mul(self, c):
        assert isinstance(c, Complex)
        x = self.x * c.x - self.y * c.y
        y = self.x * c.y + self.y * c.x
        return Complex(x, y)

    # 共役
    def conjugate(self):
        return Complex(self.x, -self.y)

    # 逆数
    def reverse(self):
        return self.conjugate().scalar(1 / self.length())

    def length2(self):
        return self.x * self.x + self.y * self.y

    def length(self):
        return math.sqrt(self.length2())

    def normalize(self):
        return self.scalar(1 / self.length())


# クォータニオン
class Quaternion:
    def __init__(self, w=0.0, v=lia.Vector3C.Zero):
        self.w = w
        self.v = v

    def scalar(self, n=1.0):
        return Quaternion(self.v.scalar(n), self.w * n)

    def mul(self, q):
        assert isinstance(q, Quaternion)
        w = self.w * q.w - self.v.ip(q.v)
        v1 = q.v.scalar(self.w)
        v2 = self.v.scalar(q.w)
        v3 = self.v.cp(q.v)
        v = v1.add(v2).add(v3)
        return Quaternion(w, v)

    # 共役
    def conjugate(self):
        return Quaternion(self.w, self.v.scalar(-1))

    def reverse(self):
        return self.conjugate().scalar(1 / self.length())

    def length2(self):
        return self.w * self.w + self.v.length2()

    def length(self):
        return math.sqrt(self.length2())

    def normalize(self):
        return self.scalar(1 / self.length())

    def projection(self, v=lia.Vector3C.Zero):
        rev = self.reverse()
        qv1 = Quaternion(0, v)
        qv2 = self.mul(qv1).mul(rev)
        return qv2.v


