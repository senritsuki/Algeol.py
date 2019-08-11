import numpy as np

R2 = np.sqrt(2)
R3 = np.sqrt(3)
R5 = np.sqrt(5)
PI = np.pi
PI05 = PI * 0.5
PI2 = PI * 2
PHI = (1 + R5) / 2

deg2rad = lambda deg: deg * np.pi / 180
rad2deg = lambda rad: rad / np.pi * 180

cosd = lambda deg: np.cos(deg2rad(deg))
sind = lambda deg: np.sin(deg2rad(deg))

rad2cs = lambda rad: (np.cos(rad), np.sin(rad))
deg2cs = lambda deg: rad2cs(deg2rad(deg))

class Node:
    # vf: (verts, faces)
    # edges: Edge[]
    def __init__(self, vf=None, edges=[]):
        self.vf = vf
        self.edges = edges

class Edge:
    def __init__(self, dstNode, affine=None, material=None):
        self.dstNode = dstNode
        self.affine = affine
        self.material = material

class Material:
    def __init__(self, name: str, rgb: list):
        self.name = name
        self.rgb = rgb

# x軸回転行列
def rotate_x(rad):
    c, s = rad2cs(rad)
    return np.array((
        ( 1,  0,  0,  0),
        ( 0,  c, -s,  0),
        ( 0,  s,  c,  0),
        ( 0,  0,  0,  1),
    ))

# y軸回転行列
def rotate_y(rad):
    c, s = rad2cs(rad)
    return np.array((
        ( c,  0,  s,  0),
        ( 0,  1,  0,  0),
        (-s,  0,  c,  0),
        ( 0,  0,  0,  1),
    ))

# z軸回転行列
def rotate_z(rad):
    c, s = rad2cs(rad)
    return np.array((
        ( c, -s,  0,  0),
        ( s,  c,  0,  0),
        ( 0,  0,  1,  0),
        ( 0,  0,  0,  1),
    ))

# 併進行列
def translate(v):
    return np.array((
        (1, 0, 0, v[0]),
        (0, 1, 0, v[1]),
        (0, 0, 1, v[2]),
        (0, 0, 0,    1),
    ))

# 拡大縮小行列
def scale(v):
    return np.array((
        (v[0],    0,    0, 0),
        (   0, v[1],    0, 0),
        (   0,    0, v[2], 0),
        (   0,    0,    0, 1),
    ))

def refrection_xz_plane():
    return np.array((
        ( 1, 0, 0, 0),
        ( 0,-1, 0, 0),
        ( 0, 0, 1, 0),
        ( 0, 0, 0, 1),
    ))

def refrection_yz_plane():
    return np.array((
        (-1, 0, 0, 0),
        ( 0, 1, 0, 0),
        ( 0, 0, 1, 0),
        ( 0, 0, 0, 1),
    ))

def refrection_x_eq_y_plane():
    return np.array((
        ( 0, 1, 0, 0),
        ( 1, 0, 0, 0),
        ( 0, 0, 1, 0),
        ( 0, 0, 0, 1),
    ))

def refrection_z_axis():
    return np.array((
        (-1, 0, 0, 0),
        ( 0,-1, 0, 0),
        ( 0, 0, 1, 0),
        ( 0, 0, 0, 1),
    ))

unit = np.array((
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
))
rotate_x90d = [
    np.array((
        ( 1,  0,  0,  0),
        ( 0,  1,  0,  0),
        ( 0,  0,  1,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        ( 1,  0,  0,  0),
        ( 0,  0, -1,  0),
        ( 0,  1,  0,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        ( 1,  0,  0,  0),
        ( 0, -1,  0,  0),
        ( 0,  0, -1,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        ( 1,  0,  0,  0),
        ( 0,  0,  1,  0),
        ( 0, -1,  0,  0),
        ( 0,  0,  0,  1),
    )),
]
rotate_y90d = [
    np.array((
        ( 1,  0,  0,  0),
        ( 0,  1,  0,  0),
        ( 0,  0,  1,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        ( 0,  0,  1,  0),
        ( 0,  1,  0,  0),
        (-1,  0,  0,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        (-1,  0,  0,  0),
        ( 0,  1,  0,  0),
        ( 0,  0, -1,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        ( 0,  0, -1,  0),
        ( 0,  1,  0,  0),
        ( 1,  0,  0,  0),
        ( 0,  0,  0,  1),
    )),
]
rotate_z90d = [
    np.array((
        ( 1,  0,  0,  0),
        ( 0,  1,  0,  0),
        ( 0,  0,  1,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        ( 0, -1,  0,  0),
        ( 1,  0,  0,  0),
        ( 0,  0,  1,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        (-1,  0,  0,  0),
        ( 0, -1,  0,  0),
        ( 0,  0,  1,  0),
        ( 0,  0,  0,  1),
    )),
    np.array((
        ( 0,  1,  0,  0),
        (-1,  0,  0,  0),
        ( 0,  0,  1,  0),
        ( 0,  0,  0,  1),
    )),
]

def transform(affine, verts):
    return np.dot(affine, verts.transpose()).transpose()

def dotall(affines):
    d = affines[0]
    for a in affines[1:]:
        d = np.dot(d, a)
    return d

def faces_to_edges(faces):
    edges = []
    s = set()
    for f in faces:
        fl = len(faces)
        for i1 in range(fl):
            i2 = f[(i1+1) % fl]
            i12 = (i1, i2) if i1 <= i2 else (i2, i1)
            key = '%d %d' % i12
            if key not in s:
                s.add(key)
                edges.append(i12)
    return edges

def calc_rotate_z(v):
    x = v[0]
    y = v[1]
    if x > 0 and y == 0:
        return rotate_z90d[0]
    if x == 0 and y > 0:
        return rotate_z90d[1]
    if x < 0 and y == 0:
        return rotate_z90d[2]
    if x == 0 and y < 0:
        return rotate_z90d[3]
    rad = np.arctan2(y, x)
    return rotate_z(rad)
