import numpy as np

# 座標系は以下のように考える：
# - 右方向 = x軸正方向
# - 奥方向 = y軸正方向
# - 頭方向 = z軸正方向

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

def deg2cs(deg):
    rad = deg * np.pi / 180
    c = np.cos(rad)
    s = np.sin(rad)
    return c, s

def rot_x(deg):
    c, s = deg2cs(deg)
    return np.array((
        ( 1,  0,  0,  0),
        ( 0,  c, -s,  0),
        ( 0,  s,  c,  0),
        ( 0,  0,  0,  1),
    ))

def rot_y(deg):
    c, s = deg2cs(deg)
    return np.array((
        ( c,  0,  s,  0),
        ( 0,  1,  0,  0),
        (-s,  0,  c,  0),
        ( 0,  0,  0,  1),
    ))

def rot_z(deg):
    c, s = deg2cs(deg)
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


FORMAT_V = 'v %.6f %.6f %.6f'

def verts2lines(verts):
    return [FORMAT_V % (v[0], v[1], v[2]) for v in verts]

def faces2lines(faces, offset=1):
    return ['f ' + ' '.join(str(n+offset) for n in f) for f in faces]

def save_obj_1(verts, faces, name):
    file = name if name[-4:] == '.obj' else name + '.obj'
    with open(file, 'w') as f:
        for line in verts2lines(verts):
            f.write(line + '\n')
        f.write('g %s\n' % name)
        for line in faces2lines(faces, 1):
            f.write(line + '\n')
    print('save: ' + file)

def save_obj_affines(verts, faces, name, affines):
    file = name if name[-4:] == '.obj' else name + '.obj'
    with open(file, 'w') as f:
        i = 1
        for affine in affines:
            j = 0
            verts2 = transform(affine, verts)
            for line in verts2lines(verts2):
                f.write(line + '\n')
                j += 1
            f.write('g %s\n' % name)
            for line in faces2lines(faces, i):
                f.write(line + '\n')
            i += j
    print('save: ' + file)
