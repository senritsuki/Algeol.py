from algeol_common import *

# 座標系は以下のように考える：
# - 右方向 = x軸正方向
# - 奥方向 = y軸正方向
# - 頭方向 = z軸正方向

# 平面
def plane4():
    return plane4_verts(), plane4_faces()

def plane4_verts():
    return np.array((
        ( 0.5,  0.5, 0, 1),  # 右奥
        (-0.5,  0.5, 0, 1),  # 左奥
        (-0.5, -0.5, 0, 1),  # 左前
        ( 0.5, -0.5, 0, 1),  # 右前
    ))

def plane4_faces():
    return np.array((
        (0, 1, 2, 3),  # 上
    ))

def quarter_arc_points(n):
    c = lambda i: np.cos(i / n * PI05)
    s = lambda i: np.sin(i / n * PI05)
    return np.array([(c(i), s(i), 0, 1) for i in range(n+1)])

# 1/4パイ
# n: 円弧を近似する辺の数
def quarter_pie(n):
    return quarter_pie_verts(n), quarter_pie_faces(n)

def quarter_pie_verts(n):
    verts = np.array([(0, 0, 0, 1)] + list(quarter_arc_points(n)))
    verts = transform(translate((-0.5, -0.5, 0)), verts)
    return verts

def quarter_pie_faces(n):
    return np.array([(0, i+1, i+2) for i in range(n)])


def quarter_pie2(n):
    return quarter_pie2_verts(n), quarter_pie2_faces(n)

def quarter_pie2_verts(n):
    verts = np.array([(1, 1, 0, 1)] + list(quarter_arc_points(n)))
    verts = transform(translate((-0.5, -0.5, 0)), verts)
    return verts

def quarter_pie2_faces(n):
    return np.array([(0, i+1, i+2) for i in range(n)])


# Regular Tetrahedron - 正4面体
def tetrahedron():
    return tetrahedron_verts(), tetrahedron_faces()

def tetrahedron_verts():
    deg120_c = np.cos(120 * np.pi / 180)
    deg120_s = np.sin(120 * np.pi / 180)
    deg240_c = np.cos(240 * np.pi / 180)
    deg240_s = np.sin(240 * np.pi / 180)
    r = 0.5
    trad = np.arccos(-1 / 3)  # 正4面体の半径:高さ = 3:4
    tc = np.cos(trad)
    ts = np.sin(trad)
    return np.array((
        (0, 0, r, 1),  # 上
        (r * ts, 0, r * tc, 1),  # 下 右
        (r * ts * deg120_c, r * ts * deg120_s, r * tc, 1),  # 下 左奥
        (r * ts * deg240_c, r * ts * deg240_s, r * tc, 1),  # 下 左前
    ))

def tetrahedron_faces():
    return np.array((
        (0, 1, 2),  # 上 右奥
        (0, 2, 3),  # 上 左
        (0, 3, 1),  # 上 右前
        (3, 2, 1),  # 下
    ))

# Regular Hexahedron, Cube - 正6面体・立方体
def cube():
    return cube_verts(), cube_faces()

def cube_verts():
    return np.array((
        ( 0.5,  0.5,  0.5, 1),  # 上 右奥
        (-0.5,  0.5,  0.5, 1),  # 上 左奥
        (-0.5, -0.5,  0.5, 1),  # 上 左前
        ( 0.5, -0.5,  0.5, 1),  # 上 右前
        ( 0.5,  0.5, -0.5, 1),  # 下 右奥
        (-0.5,  0.5, -0.5, 1),  # 下 左奥
        (-0.5, -0.5, -0.5, 1),  # 下 左前
        ( 0.5, -0.5, -0.5, 1),  # 下 右前
    ))

def cube_faces():
    return np.array((
        (0, 1, 2, 3),  # 上
        (7, 6, 5, 4),  # 下
        (4, 5, 1, 0),  # 奥
        (5, 6, 2, 1),  # 左
        (6, 7, 3, 2),  # 前
        (7, 4, 0, 3),  # 右
    ))

# Regular Octahedron - 正8面体
def octahedron():
    return octahedron_verts(), octahedron_faces()

def octahedron_verts():
    return np.array((
        ( 0. ,  0. ,  0.5, 1),  # 上
        ( 0.5,  0. ,  0. , 1),  # 中 右
        ( 0. ,  0.5,  0. , 1),  # 中 奥
        (-0.5,  0. ,  0. , 1),  # 中 左
        ( 0. , -0.5,  0. , 1),  # 中 前
        ( 0. ,  0. , -0.5, 1),  # 下
    ))

def octahedron_faces():
    return np.array((
        (1, 2, 0),  # 上 右奥
        (2, 3, 0),  # 上 左奥
        (3, 4, 0),  # 上 左前
        (4, 1, 0),  # 上 右前
        (1, 4, 5),  # 下 右前
        (4, 3, 5),  # 下 左前
        (3, 2, 5),  # 下 左奥
        (2, 1, 5),  # 下 右奥
    ))

# 原点を含みxy平面・yz平面・zx平面に平行で合同な長方形3枚
def trirect_verts(a, b):
    return np.array((
        ( a,  b,  0, 1),
        (-a,  b,  0, 1),
        (-a, -b,  0, 1),
        ( a, -b,  0, 1),
        ( 0,  a,  b, 1),
        ( 0, -a,  b, 1),
        ( 0, -a, -b, 1),
        ( 0,  a, -b, 1),
        ( b,  0,  a, 1),
        ( b,  0, -a, 1),
        (-b,  0, -a, 1),
        (-b,  0,  a, 1),
    ))

# Dodecahedron - 正12面体
def dodecahedron():
    return dodecahedron_verts(), dodecahedron_faces()

def dodecahedron_verts():
    c = 1 / R3
    b = 0.5 * c / PHI
    a = 0.5 * c * PHI
    verts1 = trirect_verts(a, b)
    verts2 = cube_verts()
    verts2 = transform(scale((c, c, c)), verts2)
    return np.array(list(verts1) + list(verts2))

def rot_dodecahedron():
    rad_rot_y_to_z = PI05 - np.arctan2(PHI * PHI, 1)
    affine = rot_y(rad_rot_y_to_z)
    return affine

def dodecahedron_faces():
    xy = [i for i in range(0, 4)]
    yz = [i for i in range(4, 8)]
    zx = [i for i in range(8, 12)]
    ct = [i for i in range(12, 16)]
    cb = [i for i in range(16, 20)]
    return np.array((
        (xy[0], ct[0], zx[0], ct[3], xy[3]),  # 上 右
        (xy[3], cb[3], zx[1], cb[0], xy[0]),  # 下 右
        (xy[2], ct[2], zx[3], ct[1], xy[1]),  # 上 左
        (xy[1], cb[1], zx[2], cb[2], xy[2]),  # 下 左
        (yz[2], cb[3], xy[3], ct[3], yz[1]),  # 中 右前
        (yz[1], ct[2], xy[2], cb[2], yz[2]),  # 中 左前
        (yz[0], ct[0], xy[0], cb[0], yz[3]),  # 中 右奥
        (yz[3], cb[1], xy[1], ct[1], yz[0]),  # 中 左奥
        (zx[3], ct[2], yz[1], ct[3], zx[0]),  # 上 前
        (zx[0], ct[0], yz[0], ct[1], zx[3]),  # 上 奥
        (zx[1], cb[3], yz[2], cb[2], zx[2]),  # 下 前
        (zx[2], cb[1], yz[3], cb[0], zx[1]),  # 下 奥
    ))

# Icosahedron - 正20面体
def icosahedron():
    return icosahedron_verts(), icosahedron_faces()

def icosahedron_verts():
    r = 0.5
    b = r / np.sqrt(2 + PHI)  # 0^2 + 1^2 + ut.phi^2
    a = b * PHI
    verts = trirect_verts(a, b)
    return verts

def rot_icosahedron():
    rad_rot_y_to_z = PI05 - np.arctan2(PHI, 1)
    affine = rot_y(rad_rot_y_to_z)
    return affine

def icosahedron_faces():
    xy = [i for i in range(0, 4)]
    yz = [i for i in range(4, 8)]
    zx = [i for i in range(8, 12)]
    return np.array((
        (xy[0], zx[0], xy[3]),  # 上 右
        (xy[3], zx[1], xy[0]),  # 下 右
        (xy[2], zx[3], xy[1]),  # 上 左
        (xy[1], zx[2], xy[2]),  # 下 左
        (yz[2], xy[3], yz[1]),  # 中 前右
        (yz[1], xy[2], yz[2]),  # 中 前左
        (yz[0], xy[0], yz[3]),  # 中 奥右
        (yz[3], xy[1], yz[0]),  # 中 奥左
        (zx[3], yz[1], zx[0]),  # 上 前
        (zx[0], yz[0], zx[3]),  # 上 奥
        (zx[1], yz[2], zx[2]),  # 下 前
        (zx[2], yz[3], zx[1]),  # 下 奥
        (zx[0], yz[1], xy[3]),  # 中上 右前
        (zx[0], xy[0], yz[0]),  # 中上 右奥
        (zx[1], xy[3], yz[2]),  # 中下 右前
        (zx[1], yz[3], xy[0]),  # 中下 右奥
        (zx[3], xy[2], yz[1]),  # 中上 左前
        (zx[3], yz[0], xy[1]),  # 中上 左奥
        (zx[2], yz[2], xy[2]),  # 中下 左前
        (zx[2], xy[1], yz[3]),  # 中下 左奥
    ))


# 三角柱
def prism3():
    return prism3_verts(), prism3_faces()

def prism3_verts():
    return np.array((
        (-0.5,  0.5, -0.5, 1),  # 上 左奥
        (-0.5, -0.5, -0.5, 1),  # 上 左前
        ( 0.5, -0.5, -0.5, 1),  # 上 右前
        (-0.5,  0.5,  0.5, 1),  # 下 左奥
        (-0.5, -0.5,  0.5, 1),  # 下 左前
        ( 0.5, -0.5,  0.5, 1),  # 下 右前
    ))

def prism3_faces():
    return np.array((
        (0, 1, 2),  # 上
        (5, 4, 3),  # 下
        (0, 1, 4, 3),  # 左
        (1, 2, 5, 4),  # 前
        (2, 0, 3, 5),  # 右奥
    ))

# 1/4円柱
# n: 円弧を近似する辺の数
def quarter_cylinder(n):
    return quarter_cylinder_verts(n), quarter_cylinder_faces(n)

def quarter_cylinder_verts(n):
    pie = quarter_pie_verts(n)
    pie1 = transform(translate((0, 0, -0.5)), pie)
    pie2 = transform(np.dot(translate((0, 0, 0.5)), reverse_xy()), pie)
    return np.array(list(pie1) + list(pie2))

def quarter_cylinder_faces(n):
    N = n + 2
    faces_pie = quarter_pie_faces(n)
    faces_pie1 = list(faces_pie)
    faces_pie2 = list(faces_pie + N)
    faces_side = [(0, 1, 2*N-1, N), (N, N+1, N-1, 0)]
    faces_side_arc = [(i+2, i+1, 2*N-(i+1), 2*N-(i+2)) for i in range(n)]
    return np.array(faces_pie1 + faces_pie2 + faces_side + faces_side_arc)

def quarter_cylinder2(n):
    return quarter_cylinder2_verts(n), quarter_cylinder2_faces(n)

def quarter_cylinder2_verts(n):
    pie = quarter_pie2_verts(n)
    pie1 = transform(translate((0, 0, 0.5)), pie)
    pie2 = transform(np.dot(translate((0, 0, -0.5)), reverse_xy()), pie)
    return np.array(list(pie1) + list(pie2))

def quarter_cylinder2_faces(n):
    return quarter_cylinder_faces(n)

# 四角錐
def pyramid4():
    return pyramid4_verts(), pyramid4_faces()

def pyramid4_verts():
    return np.array((
        ( 0.5,  0.5, -0.5, 1),  # 下 右奥
        (-0.5,  0.5, -0.5, 1),  # 下 左奥
        (-0.5, -0.5, -0.5, 1),  # 下 左前
        ( 0.5, -0.5, -0.5, 1),  # 下 右前
        ( 0. ,  0. ,  0.5, 1),  # 上
    ))

def pyramid4_faces():
    return np.array((
        (3, 2, 1, 0),  # 下
        (0, 1, 4),  # 奥
        (1, 2, 4),  # 左
        (2, 3, 4),  # 前
        (3, 0, 4),  # 右
    ))

def concaved_cube(d):
    return concaved_cube_verts(d), concaved_cube_faces()

def concaved_cube_verts(d):
    return np.array([
        ( 0.5,  0.5, -0.5, 1),  # 下 右奥
        (-0.5,  0.5, -0.5, 1),  # 下 左奥
        (-0.5, -0.5, -0.5, 1),  # 下 左前
        ( 0.5, -0.5, -0.5, 1),  # 下 右前
        ( 0.5,  0.5,  0.5, 1),  # 上 右奥
        (-0.5,  0.5,  0.5, 1),  # 上 左奥
        (-0.5, -0.5,  0.5, 1),  # 上 左前
        ( 0.5, -0.5,  0.5, 1),  # 上 右前
        ( 0    ,  0.5-d,  0    , 1),  # 奥
        (-0.5+d,  0    ,  0    , 1),  # 左
        ( 0    , -0.5+d,  0    , 1),  # 前
        ( 0.5-d,  0    ,  0    , 1),  # 右
        ( 0    ,  0    , -0.5+d, 1),  # 下
        ( 0    ,  0    ,  0.5-d, 1),  # 上
    ])

def concaved_cube_faces():
    faces = []
    for i in range(4):
        j = (i+1) % 4
        faces += [
            (i  , j  , 8+i),
            (j  , j+4, 8+i),
            (j+4, i+4, 8+i),
            (i+4, i  , 8+i),
        ]
    faces += [
        (0, 3, 12),
        (3, 2, 12),
        (2, 1, 12),
        (1, 0, 12),
    ]
    faces += [
        (4, 5, 13),
        (5, 6, 13),
        (6, 7, 13),
        (7, 4, 13),
    ]
    return np.array(faces)
