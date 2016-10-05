# Arithmatic Sequence

import math

from . import lia
from . import unit
from . import algeo as al

v3 = lia.Vector3
v3z = lia.Vector3C.Zero
v3l = lia.Vector3C.EmptyList
m4u = lia.Matrix4C.Unit
Rad = unit.Rad
Deg = unit.Deg
cd = unit.CD



class xyz:
    @classmethod
    def check(cls, o=v3z, d=v3z):
        if isinstance(o, (tuple, list)):
            o = v3.Tuple(o)
        if isinstance(d, (tuple, list)):
            d = v3.Tuple(d)
        return (o, d)

    @classmethod
    def seq(cls, o=v3z, d=v3z, c=3):
        o, d = cls.check(o, d)
        return [d.scalar(i).add(o) for i in range(c)]

    @classmethod
    def seqCD(cls, o=v3z, d=v3z, c=3):
        o, d = cls.check(o, d)
        return [cd(v, d) for v in cls.seq(o, d, c)]

    @classmethod
    def seqLia(cls, o=v3z, d=v3z, c=3):
        o, d = cls.check(o, d)
        return [al.Lia().move(v) for v in cls.seq(o, d, c)]

class ccs:
    @classmethod
    def check(cls, o=unit.empty.ccs, d=unit.empty.ccs):
        if isinstance(o, (tuple, list)):
            o = unit.CCS.Tuple(o)
        if isinstance(d, (tuple, list)):
            d = unit.CCS.Tuple(d)
        return (o, d)

    @classmethod
    def seq(cls, o=unit.empty.ccs, d=unit.empty.ccs, c=3):
        o, d = cls.check(o, d)
        return [d.scalar(i).add(o) for i in range(c)]

    @classmethod
    def seqCD(cls, o=unit.empty.ccs, d=unit.empty.ccs, c=3):
        o, d = cls.check(o, d)
        return [ccs.cd() for ccs in cls.seq(o, d, c)]

    @classmethod
    def seqLia(cls, o=unit.empty.ccs, d=unit.empty.ccs, c=3):
        o, d = cls.check(o, d)
        return [al.Lia().turnZ(ccs.rad()).move(ccs.v3()) for ccs in cls.seq(o, d, c)]

class scs:
    @classmethod
    def seq(cls, o=unit.empty.scs, d=unit.empty.scs, c=3):
        return [d.scalar(i).add(o).cd() for i in range(c)]


class xyzccs:
    @classmethod
    def check(cls, o=v3z, d1=v3z, d2=unit.empty.ccs):
        if isinstance(o, (tuple, list)):
            o = v3.Tuple(o)
        if isinstance(d1, (tuple, list)):
            d1 = v3.Tuple(d1)
        if isinstance(d2, (tuple, list)):
            d2 = unit.CCS.Tuple(d2)
        return (o, d1, d2)

    @classmethod
    def seq(cls, o=v3z, d1=v3z, c1=3, d2=unit.empty.ccs, c2=3):
        o, d1, d2 = cls.check(o, d1, d2)
        return [(unit.CCS.V3(o.add(d1.scalar(i))).add(d2.scalar(j)), d2.scalar(j).rad()) for i in range(c1) for j in range(c2)]
    
    @classmethod
    def seqCD(cls, o=v3z, d1=v3z, c1=3, d2=unit.empty.ccs, c2=3):
        return [ccs.cd() for ccs, rad in cls.seq(o, d1, c1, d2, c2)]

    @classmethod
    def seqLia(cls, o=v3z, d1=v3z, c1=3, d2=unit.empty.ccs, c2=3):
        o, d1, d2 = cls.check(o, d1, d2)
        return [al.Lia().turnZ(rad).move(ccs.v3()) for ccs, rad in cls.seq(o, d1, c1, d2, c2)]




if __name__ == '__main__':
    print('arith.py __main__ start')
    print('arith.py __main__ end')
