from algeol_common import *

# 座標系は以下のように考える：
# - 右方向 = x軸正方向
# - 奥方向 = y軸正方向
# - 頭方向 = z軸正方向

# 平面
def square():
    return square_verts(), square_faces()

def square_verts():
    return np.array((
        ( 0.5,  0.5, 0, 1),  # 右奥
        (-0.5,  0.5, 0, 1),  # 左奥
        (-0.5, -0.5, 0, 1),  # 左前
        ( 0.5, -0.5, 0, 1),  # 右前
    ))

def square_faces():
    return [
        (0, 1, 2, 3),  # 上
    ]

# n角の正多角形
def regular_polygon(n):
    return regular_polygon_verts(n), regular_polygon_faces(n)

def regular_polygon_verts(n):
    c = lambda i: np.cos(i / n * PI2) * 0.5
    s = lambda i: np.sin(i / n * PI2) * 0.5
    return np.array([(c(i), s(i), 0, 1) for i in range(n)])

def regular_polygon_faces(n):
    return [[i for i in range(n)]]


def quarter_arc_points(n):
    c = lambda i: np.cos(i / n * PI05)
    s = lambda i: np.sin(i / n * PI05)
    return np.array([(c(i), s(i), 0, 1) for i in range(n+1)])

# 1/4パイ
# n: 円弧を近似する辺の数
def quarter_pie(n):
    return quarter_pie_verts(n), quarter_pie_faces(n)

def quarter_pie_verts(n):
    arc = list(quarter_arc_points(n))
    verts = np.array([(0, 0, 0, 1)] + arc)
    verts = transform(translate((-0.5, -0.5, 0)), verts)
    return verts

def quarter_pie_faces(n):
    return [(0, i+1, i+2) for i in range(n)]

# Isosceles Right Triangle - 直角二等辺三角形
def isosceles_right_triangle():
    return quarter_pie(1)

# 正方形 と 1/4パイ の差集合
# n: 円弧を近似する辺の数
def quarter_pie_complement(n):
    return quarter_pie_complement_verts(n), quarter_pie_faces(n)

def quarter_pie_complement_verts(n):
    arc = list(quarter_arc_points(n))
    arc.reverse()
    verts = np.array([(1, 1, 0, 1)] + arc)
    verts = transform(translate((-0.5, -0.5, 0)), verts)
    return verts

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
    return [
        (0, 1, 2),  # 上 右奥
        (0, 2, 3),  # 上 左
        (0, 3, 1),  # 上 右前
        (3, 2, 1),  # 下
    ]

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
    return [
        (0, 1, 2, 3),  # 上
        (7, 6, 5, 4),  # 下
        (4, 5, 1, 0),  # 奥
        (5, 6, 2, 1),  # 左
        (6, 7, 3, 2),  # 前
        (7, 4, 0, 3),  # 右
    ]

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
    return [
        (1, 2, 0),  # 上 右奥
        (2, 3, 0),  # 上 左奥
        (3, 4, 0),  # 上 左前
        (4, 1, 0),  # 上 右前
        (1, 4, 5),  # 下 右前
        (4, 3, 5),  # 下 左前
        (3, 2, 5),  # 下 左奥
        (2, 1, 5),  # 下 右奥
    ]

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
    affine = rotate_y(rad_rot_y_to_z)
    return affine

def dodecahedron_faces():
    xy = [i for i in range(0, 4)]
    yz = [i for i in range(4, 8)]
    zx = [i for i in range(8, 12)]
    ct = [i for i in range(12, 16)]
    cb = [i for i in range(16, 20)]
    return [
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
    ]

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
    affine = rotate_y(rad_rot_y_to_z)
    return affine

def icosahedron_faces():
    xy = [i for i in range(0, 4)]
    yz = [i for i in range(4, 8)]
    zx = [i for i in range(8, 12)]
    return [
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
    ]

def icosphere(recurse):
    verts, faces = icosahedron()
    return _icosphere_recurse(verts, faces, recurse)

def _icosphere_recurse(verts, faces, recurse):
    if recurse <= 0:
        return np.array(verts), np.array(faces)
    keymap = dict()
    verts = list(verts)
    subverts = []
    subfaces = []
    loop = ((0, 1), (1, 2), (2, 0))
    for face in faces:
        vvi = [(verts[i], i) for i in face]
        mvi = [_icosphere_mid(keymap, face[ii[0]], face[ii[1]], verts, subverts) for ii in loop]
        ff = [[vvi[ii[1]], mvi[ii[1]], mvi[ii[0]]] for ii in loop]
        ff.append([mvi[0], mvi[1], mvi[2]])
        ff = [[vi[1] for vi in f] for f in ff]
        subfaces.extend(ff)
    return _icosphere_recurse(verts + subverts, subfaces, recurse - 1)

def _icosphere_key(i1, i2):
    return '%d %d' % (i1, i2) if i1 <= i2 else '%d %d' % (i2, i1)

def _icosphere_mid(keymap, i1, i2, verts, subverts):
    key = _icosphere_key(i1, i2)
    if key in keymap:
        return keymap[key]
    i = len(verts) + len(subverts)
    v = (verts[i1] + verts[i2]) * 0.5
    v3 = v[:3] * 0.5 * (1 / np.linalg.norm(v[:3]))
    v = np.array(list(v3) + [1])
    keymap[key] = (v, i)
    subverts.append(v)
    return (v, i)

# 角柱
def prism(polygon_verts, polygon_faces, fn_refrection=None):
    return prism_verts(polygon_verts), prism_faces(polygon_verts, polygon_faces)

def prism_verts(polygon_verts, fn_refrection=None):
    affine1 = translate((0, 0, -0.5))
    affine2 = translate((0, 0,  0.5))
    if fn_refrection is not None:
        affine1 = np.dot(affine1, fn_refrection())
    polygon1 = transform(affine1, polygon_verts)
    polygon2 = transform(affine2, polygon_verts)
    return np.array(list(polygon1) + list(polygon2))

def prism_faces(polygon_verts, polygon_faces, fn_refrection=None):
    N = len(polygon_verts)
    faces1 = [(f[0],   f[2],   f[1]  ) for f in polygon_faces]
    faces2 = [(f[0]+N, f[1]+N, f[2]+N) for f in polygon_faces]
    faces_side = []
    for i in range(N):
        j = (i + 1) % N
        if fn_refrection is not None:
            face = [i, i+N, j+N, j]
        else:
            face = [i, j, j+N, i+N]
        faces_side.append(face)
    return faces1 + faces2 + faces_side

#
def regular_prism(n):
    verts, faces = regular_polygon(n)
    return prism(verts, faces, refrection_xz_plane)

# 直角二等辺三角形の三角柱
def isosceles_right_triangular_prism():
    verts, faces = isosceles_right_triangle()
    return prism(verts, faces, refrection_x_eq_y_plane)

# 1/4円柱
# n: 円弧を近似する辺の数
def quarter_cylinder(n):
    verts, faces = quarter_pie(n)
    return prism(verts, faces, refrection_x_eq_y_plane)

def quarter_cylinder_complement(n):
    verts, faces = quarter_pie_complement(n)
    return prism(verts, faces, refrection_x_eq_y_plane)

# 四角錐
def square_pyramid():
    return square_pyramid_verts(), square_pyramid_faces()

def square_pyramid_verts():
    return np.array((
        ( 0.5,  0.5, -0.5, 1),  # 下 右奥
        (-0.5,  0.5, -0.5, 1),  # 下 左奥
        (-0.5, -0.5, -0.5, 1),  # 下 左前
        ( 0.5, -0.5, -0.5, 1),  # 下 右前
        ( 0. ,  0. ,  0.5, 1),  # 上
    ))

def square_pyramid_faces():
    return [
        (3, 2, 1, 0),  # 下
        (0, 1, 4),  # 奥
        (1, 2, 4),  # 左
        (2, 3, 4),  # 前
        (3, 0, 4),  # 右
    ]

# トーラス
# r: 空洞径 0.0 ～ 1.0
def torus(r, n1, n2):
    return torus_verts(r, n1, n2), torus_faces(n1, n2)

def torus_verts(r, n1, n2):
    v1 = []
    d = (1 - r) / 4     # r=0.500のとき、輪の半径は0.125
    for i in range(n1):
        rad = PI2 * i / n1
        x = d * np.cos(rad) + (r / 2) + d
        z = d * np.sin(rad)
        v1.append((x, 0, z, 1))
    v2 = []
    for i in range(n2):
        rad = PI2 * i / n2
        rot = rotate_z(rad)
        for v in v1:
            v = np.dot(rot, v)
            v2.append(v)
    return np.array(v2)

def torus_faces(n1, n2):
    f = []
    for i in range(n2):
        i2 = (i+1) % n2
        k = i * n1
        k2 = i2 * n1
        for j in range(n1):
            j2 = (j+1) % n1
            f.append((k + j, k2 + j, k2 + j2, k + j2))
    return f

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
    return faces

def rotate_z_verts(affines, z1, vv, z2):
    verts = []
    verts.append((0, 0, z1, 1))
    for v in vv:
        for affine in affines:
            verts.append(np.dot(affine, v))
    verts.append((0, 0, z2, 1))
    return np.array(verts)

def rotate_z_faces(affines, vv):
    I = len(vv)
    J = len(affines)
    faces = []
    i = 1
    for j in range(J):
        j2 = (j + 1) % J
        faces.append((0, i+j, i+j2))
    for k in range(I-1):
        i = k * J + 1
        i2 = i + J
        for j in range(J):
            j2 = (j + 1) % J
            faces.append((i+j, i+j2, i2+j2, i2+j))
    i = (I - 1) * J + 1
    i2 = i + J
    for j in range(J):
        j2 = (j + 1) % J
        faces.append((i+j, i+j2, i2))
    return faces

def refrection_xy(z1, verts, z2):
    affines = (
        unit,
        refrection_yz_plane(),
        refrection_z_axis(),
        refrection_xz_plane(),
    )
    return rotate_z_verts(affines, z1, verts, z2), rotate_z_faces(affines, verts)

def rotation_z(n, z1, verts, z2):
    affines = [rotate_z(PI2 * i / n) for i in range(n)]
    return rotate_z_verts(affines, z1, verts, z2), rotate_z_faces(affines, verts)

def roundcube(n):
    return roundcube_verts(n), roundcube_faces(n)

def roundcube_verts(n):
    pass

def roundcube_faces(n):
    pass

