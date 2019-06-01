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


def rot_x(rad):
    c, s = rad2cs(rad)
    return np.array((
        ( 1,  0,  0,  0),
        ( 0,  c, -s,  0),
        ( 0,  s,  c,  0),
        ( 0,  0,  0,  1),
    ))

def rot_y(rad):
    c, s = rad2cs(rad)
    return np.array((
        ( c,  0,  s,  0),
        ( 0,  1,  0,  0),
        (-s,  0,  c,  0),
        ( 0,  0,  0,  1),
    ))

def rot_z(rad):
    c, s = rad2cs(rad)
    return np.array((
        ( c, -s,  0,  0),
        ( s,  c,  0,  0),
        ( 0,  0,  1,  0),
        ( 0,  0,  0,  1),
    ))

def translate(v):
    return np.array((
        (1, 0, 0, v[0]),
        (0, 1, 0, v[1]),
        (0, 0, 1, v[2]),
        (0, 0, 0,    1),
    ))

def scale(v):
    return np.array((
        (v[0],    0,    0, 0),
        (   0, v[1],    0, 0),
        (   0,    0, v[2], 0),
        (   0,    0,    0, 1),
    ))

def reverse_xy():
    return np.array((
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    ))


rot_x4 = [
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
rot_y4 = [
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
rot_z4 = [
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
