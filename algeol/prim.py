# Geometry - Primitive

import math
from . import const
from . import lia
from . import unit
from . import algeo as al

V3 = lia.Vector3

# Inscribed Circle 内接円
# Circumscribed Circle 外接円

# 多角形 Polygon
def Polygon(vc=3, cr=0.5):
    verts = []
    for i in range(vc):
        rad = unit.Deg(360 * i / vc)
        vert = V3(cr * rad.cos(), cr * rad.sin(), 0)
        verts.append(vert)
    faces = [[i for i in range(vc)]]
    return al.Geo(verts, faces)


# 正四面体 4 vertices, 4 faces
def Tetrahedron(cr=0.5):
    r0 = unit.Rad(math.acos(-1.0 / 3.0)) # 半径 : 高さ = 3 : 4
    r1 = unit.Deg(360 / 3)
    m0 = r0.turnY()
    m1 = r1.turnZ()
    v0 = V3(0, 0, cr)
    v1 = v0.projection(m0)
    v2 = v1.projection(m1)
    v3 = v2.projection(m1)
    verts = [v0, v1, v2, v3]
    faces = [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 3)]
    return al.Geo(verts, faces)

# 正八面体 6 vertices, 8 faces
def Octahedron(cr=0.5):
    r0 = unit.Deg(90)
    r1 = unit.Deg(360 / 4)
    m0 = r0.turnY()
    m1 = r1.turnZ()
    v0 = V3(0, 0, cr)
    v1 = v0.projection(m0)
    v2 = v1.projection(m1)
    v3 = v2.projection(m1)
    v4 = v3.projection(m1)
    v5 = v1.projection(m0)
    verts = [v0, v1, v2, v3, v4, v5]
    faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), 
             (5, 1, 4), (5, 4, 3), (5, 3, 2), (5, 2, 1)]
    return al.Geo(verts, faces)

# 立方体 8 vertices, 6 faces
def Cube(cr=0.5):
    r0 = unit.Deg(90)
    m0 = r0.turnZ()
    v0 = V3(cr, cr, cr)
    v1 = V3(cr, cr, -cr)
    v2 = v0.projection(m0)
    v3 = v1.projection(m0)
    v4 = v2.projection(m0)
    v5 = v3.projection(m0)
    v6 = v4.projection(m0)
    v7 = v5.projection(m0)
    verts = [v0, v1, v2, v3, v4, v5, v6, v7]
    faces = [(0,1,3,2), (2,3,5,4), (4,5,7,6), (6,7,1,0),
             (0,2,4,6), (7,5,3,1)]
    return al.Geo(verts, faces)
    
# 正十二面体 20 vertices, 12 faces
def Dodecahedron(cr=0.5):
    a = cr / (const.r3 * const.phi)
    b = cr / const.r3
    c = cr * const.phi / const.r3
    ct1, ct2, ct3, ct4 = [i+0 for i in range(4)] # cube top 上から見た正方形
    cb1, cb2, cb3, cb4 = [i+4 for i in range(4)] # cube bottom 上から見た正方形
    xy1, xy2, xy3, xy4 = [i+8 for i in range(4)] # x-y rect 上から見た横長長方形
    yz1, yz2, yz3, yz4 = [i+12 for i in range(4)] # y-z rect 右から見た横長長方形
    zx1, zx2, zx3, zx4 = [i+16 for i in range(4)] # z-x rect 正面から見た縦長長方形
    verts = [
        # cube top 上から見た正方形
        V3(b, b, b),
        V3(-b, b, b),
        V3(-b, -b, b),
        V3(b, -b, b),
        # cube bottom 上から見た正方形
        V3(b, b, -b),
        V3(-b, b, -b),
        V3(-b, -b, -b),
        V3(b, -b, -b),
        # x-y rect 上から見た横長長方形
        V3(c, a, 0),
        V3(-c, a, 0),
        V3(-c, -a, 0),
        V3(c, -a, 0),
        # y-z rect 右から見た横長長方形
        V3(0, c, a),
        V3(0, -c, a),
        V3(0, -c, -a),
        V3(0, c, -a),
        # z-x rect 正面から見た縦長長方形
        V3(a, 0, c),
        V3(-a, 0, c),
        V3(-a, 0, -c),
        V3(a, 0, -c),
        ]
    faces = [
        (xy1,ct1,zx1,ct4,xy4), # 右上
        (xy4,cb4,zx4,cb1,xy1), # 右下
        (xy3,ct3,zx2,ct2,xy2), # 左上
        (xy2,cb2,zx3,cb3,xy3), # 左下
        (yz3,cb4,xy4,ct4,yz2), # 手前右
        (yz2,ct3,xy3,cb3,yz3), # 手前左
        (yz1,ct1,xy1,cb1,yz4), # 奥右
        (yz4,cb2,xy2,ct2,yz1), # 奥左
        (zx2,ct3,yz2,ct4,zx1), # 上手前
        (zx1,ct1,yz1,ct2,zx2), # 上奥
        (zx4,cb4,yz3,cb3,zx3), # 下手前
        (zx3,cb1,yz4,cb2,zx4), # 下奥
        ]
    return al.Geo(verts, faces)

# 正二十面体 12 vertices, 20 faces
def Icosahedron(cr=0.5):
    a = cr / (const.r3 * const.phi)
    b = cr / const.r3
    c = cr * const.phi / const.r3
    xy1, xy2, xy3, xy4 = [i+0 for i in range(4)] # x-y rect 上から見た横長長方形
    yz1, yz2, yz3, yz4 = [i+4 for i in range(4)] # y-z rect 右から見た横長長方形
    zx1, zx2, zx3, zx4 = [i+8 for i in range(4)] # z-x rect 正面から見た縦長長方形
    verts = [
        # x-y rect 上から見た横長長方形
        V3(c, a, 0),
        V3(-c, a, 0),
        V3(-c, -a, 0),
        V3(c, -a, 0),
        # y-z rect 右から見た横長長方形
        V3(0, c, a),
        V3(0, -c, a),
        V3(0, -c, -a),
        V3(0, c, -a),
        # z-x rect 正面から見た縦長長方形
        V3(a, 0, c),
        V3(-a, 0, c),
        V3(-a, 0, -c),
        V3(a, 0, -c),
        ]
    faces = [
        (xy1,zx1,xy4), # 右上
        (xy4,zx4,xy1), # 右下
        (xy3,zx2,xy2), # 左上
        (xy2,zx3,xy3), # 左下
        (yz3,xy4,yz2), # 手前右
        (yz2,xy3,yz3), # 手前左
        (yz1,xy1,yz4), # 奥右
        (yz4,xy2,yz1), # 奥左
        (zx2,yz2,zx1), # 上手前
        (zx1,yz1,zx2), # 上奥
        (zx4,yz3,zx3), # 下手前
        (zx3,yz4,zx4), # 下奥
        (zx1,yz2,xy4), # 右上手前
        (zx1,xy1,yz1), # 右上奥
        (zx4,xy4,yz3), # 右下手前
        (zx4,yz4,xy1), # 右下奥
        (zx2,xy3,yz2), # 左上手前
        (zx2,yz1,xy2), # 左上奥
        (zx3,yz3,xy3), # 左下手前
        (zx3,xy2,yz4), # 左下奥
        ]
    return al.Geo(verts, faces)

# x + 2 vertices, x * 2 faces
def Crystal(vertex=6, cr=0.5, hc=0.0):
    verts = []
    for i in range(vertex):
        rad = unit.Deg(360 * i / vertex)
        v = V3(cr * rad.cos(), cr * rad.sin(), hc)
        verts.append(v)
    verts.append(V3(0, 0, cr))
    verts.append(V3(0, 0, -cr))
    iT = vertex
    iD = vertex + 1
    faces = []
    for i in range(vertex):
        i1 = i % vertex
        i2 = (i + 1) % vertex
        f1 = (iT, i1, i2)
        f2 = (iD, i2, i1)
        faces.append(f1)
        faces.append(f2)
    return al.Geo(verts, faces)

# 角柱 x * 2 vertices, x + 2 faces
def Prism(vertex=6, cr=0.5, h=1.0):
    zT = h * 0.5
    zB = h * -0.5
    verts = []
    for i in range(vertex):
        rad = unit.Deg(360 * i / vertex)
        x = cr * rad.cos()
        y = cr * rad.sin()
        v1 = V3(x, y, zB)
        v2 = V3(x, y, zT)
        verts.append(v1)
        verts.append(v2)
    faces = [
        tuple([i * 2 for i in range(vertex)]),
        tuple([i * 2 + 1 for i in range(vertex)]),
        ]
    for i in range(vertex):
        i1 = 2 * (i % vertex)
        i2 = 2 * ((i + 1) % vertex)
        f1 = (i1 + 1, i1, i2, i2 + 1)
        faces.append(f1)
    return al.Geo(verts, faces)
    
# x * 2 vertices, x + 2 faces
def TrapezoidPrism(vertex=6, crB=0.5, crT=0.5, h=1.0):
    zT = h * 0.5
    zB = h * -0.5
    verts = []
    for i in range(vertex):
        rad = unit.Deg(360 * i / vertex)
        x = rad.cos()
        y = rad.sin()
        v1 = V3(x * crB, y * crB, zB)
        v2 = V3(x * crT, y * crT, zT)
        verts.append(v1)
        verts.append(v2)
    faces = [
        tuple([i * 2 for i in range(vertex)]),
        tuple([i * 2 + 1 for i in range(vertex)]),
        ]
    for i in range(vertex):
        i1 = 2 * (i % vertex)
        i2 = 2 * ((i + 1) % vertex)
        f1 = (i1 + 1, i1, i2, i2 + 1)
        faces.append(f1)
    return al.Geo(verts, faces)
    
# x * 2 vertices, x + 2 faces
def ParallelPrism(vertex=6, cr=0.5, vTop=V3C.UnitZ):
    zB = 0
    verts = []
    for i in range(vertex):
        rad = unit.Deg(360 * i / vertex)
        x = cr * rad.cos()
        y = cr * rad.sin()
        v1 = V3(x, y, zB)
        v2 = v1.add(vTop)
        verts.append(v1)
        verts.append(v2)
    faces = [
        tuple([i * 2 for i in range(vertex)]),
        tuple([i * 2 + 1 for i in range(vertex)]),
        ]
    for i in range(vertex):
        i1 = 2 * (i % vertex)
        i2 = 2 * ((i + 1) % vertex)
        f1 = (i1 + 1, i1, i2, i2 + 1)
        faces.append(f1)
    return al.Geo(verts, faces)
    
# 角錐 x * 2 vertices, x + 1 faces
def Cone(vertex=6, cr=0.5):
    zT = cr
    zB = -cr
    vTop = V3(0, 0, zT)
    verts = []
    for i in range(vertex):
        rad = unit.Deg(360 * i / vertex)
        x = cr * rad.cos()
        y = cr * rad.sin()
        v1 = V3(x, y, zB)
        verts.append(v1)
    verts.append(vTop)
    iT = vertex
    faces = [
        tuple([i for i in range(vertex)]),
        ]
    for i in range(vertex):
        i1 = i % vertex
        i2 = (i + 1) % vertex
        f1 = (iT, i1, i2)
        faces.append(f1)
    return al.Geo(verts, faces)
    
# x * 2 vertices, x + 1 faces
def ParallelCone(vertex=6, cr=0.5, vTop=V3C.UnitZ):
    zB = 0
    verts = []
    for i in range(vertex):
        rad = unit.Deg(360 * i / vertex)
        x = cr * rad.cos()
        y = cr * rad.sin()
        v1 = V3(x, y, zB)
        verts.append(v1)
    verts.append(vTop)
    iT = vertex
    faces = [
        tuple([i for i in range(vertex)]),
        ]
    for i in range(vertex):
        i1 = i % vertex
        i2 = (i + 1) % vertex
        f1 = (iT, i1, i2)
        faces.append(f1)
    return al.Geo(verts, faces)

def SpiralPiece(ir=0.5, d=45.0, h=1.0):
    zB = 0
    v1 = V3(ir, 0, 0)
    v2 = V3(ir + 1, 0, 0)
    turn = unit.Deg(d).turnZ()
    vs = []
    vs.append(v1)
    vs.append(v2)
    vs.append(v2.projection(turn))
    vs.append(v1.projection(turn))
    verts = []
    for v in vs:
        verts.append(v)
        verts.append(v.add(0, 0, h))
    faces = [
        tuple([i * 2 for i in range(vertex)]),
        tuple([i * 2 + 1 for i in range(vertex)]),
        ]
    for i in range(vertex):
        i1 = 2 * (i % vertex)
        i2 = 2 * ((i + 1) % vertex)
        f1 = (i1 + 1, i1, i2, i2 + 1)
        faces.append(f1)
    return al.Geo(verts, faces)

def Arch(ri=0.4, v=12):
    ro = 0.5
    dp = 0.5
    verts = []
    for i in range(v+1):
        rad = unit.Deg(180 * i / v)
        for r in (ri, ro):
            x = r * rad.cos()
            z = r * rad.sin()
            verts.extend([V3(x, y, z) for y in (-dp, dp)])
    faces = []
    faces.extend([(i, i+1, i+3, i+2) for i in (0, len(verts)-4)]) # 右, 左
    for i in range(v):
        faces.extend([
            (i, i+4, i+5, i+1), # 下
            (i, i+2, i+6, i+4), # 前
            (i+3, i+7, i+6, i+2), # 上
            (i+3, i+1, i+5, i+7), # 奥
            ])
    return al.Geo(verts, faces)

def ArchWall(ri=0.4, h=0.5, v=12):
    ro = 0.5
    dp = 0.5
    verts = []
    for x, z in ((ro, 0), (ro, h)):
        verts.extend([V3(x, y, z) for y in (-dp, dp)])
    for i in range(v+1):
        rad = unit.Deg(180 * i / v)
        x = ri * rad.cos()
        z_ = ri * rad.sin()
        for z in (z_, h):
            verts.extend([V3(x, y, z) for y in (-dp, dp)])
    for x, z in ((-ro, h), (-ro, 0)):
        verts.extend([V3(x, y, z) for y in (-dp, dp)])
    vl = len(verts)
    faces = []
    faces.extend([(i, i+1, j+1, j) for i, j in ((0, 2), (2, vl-4), (vl-2, vl-4))]) # 右, 上, 左
    for i in range(v+2):
        faces.extend([
            (i, i+2, i+6, i+4), # 前
            (i, i+4, i+5, i+1), # 下
            (i+1, i+5, i+7, i+3), # 奥
            ])
    return al.Geo(verts, faces)


def TestExport():
    Polygon().export('./test/', 'Polygon')
    Tetrahedron().export('./test/', 'Tetrahedron')
    Octahedron().export('./test/', 'Octahedron')
    Cube().export('./test/', 'Cube')
    Crystal().export('./test/', 'Crystal')
    Prism().export('./test/', 'Prism')

if __name__ == '__main__':
    print('prim.py __main__ start')
    print('prim.py __main__ end')
