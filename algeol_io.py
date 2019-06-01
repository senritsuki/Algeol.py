from algeol_common import *

FORMAT_V = 'v %.6f %.6f %.6f'

def verts2lines(verts):
    return [FORMAT_V % (v[0], v[1], v[2]) for v in verts]

def faces2lines(faces, offset=1):
    return ['f ' + ' '.join(str(n+offset) for n in f) for f in faces]

def rgb2line(rgb):
    return '%.3f %.3f %.3f' % (rgb[0], rgb[1], rgb[2])

# for *.obj
def write_mtllib(f, name):
    file = name if name[-4:] == '.mtl' else name + '.mtl'
    f.write('mtllib %s\n\n' % file)

def write_g(f, g):
    f.write('g %s\n' % g)

def write_usemtl(f, usemtl):
    f.write('usemtl %s\n' % usemtl)

# for *.mtl
def write_newmtl_kd(f, newmtl, kd_rgb):
    f.write('newmtl %s\n' % newmtl)
    f.write('Kd %s\n\n' % rgb2line(kd_rgb))

def write_obj(f, verts, faces, face_offset):
    i = 0
    for line in verts2lines(verts):
        f.write(line + '\n')
        i += 1
    for line in faces2lines(faces, face_offset):
        f.write(line + '\n')
    return face_offset + i

def write_obj_affine(f, verts, faces, face_offset, affines):
    i = face_offset
    for affine in affines:
        j = 0
        verts2 = transform(affine, verts)
        for line in verts2lines(verts2):
            f.write(line + '\n')
            j += 1
        for line in faces2lines(faces, i):
            f.write(line + '\n')
        i += j
    return i

# mtls: (newmtl, kd_rgb)[]
def write_mtls(f, mtls):
    for newmtl, kd_rgb in mtls:
        write_newmtl_kd(f, newmtl, kd_rgb)

def open_w_obj(name, callback):
    file = name if name[-4:] == '.obj' else name + '.obj'
    with open(file, 'w') as f:
        callback(f)
    return file

def save_obj(verts, faces, name):
    return open_w_obj(name, lambda f: write_obj(f, verts, faces, 1))

def save_obj_affines(verts, faces, name, affines):
    return open_w_obj(name, lambda f: write_obj_affine(f, verts, faces, 1, affines))

def open_w_mtl(name, callback):
    file = name if name[-4:] == '.mtl' else name + '.mtl'
    with open(file, 'w') as f:
        callback(f)
    return file

# mtls: (newmtl, kd_rgb)[]
def save_mtls(name, mtls):
    return open_w_mtl(name, lambda f: write_mtls(f, mtls))

"""
hoge.obj
    mtllib hoge.mtl

    g triangle_01
    usemtl triangle_01
    v 0 0 0
    v 1 0 0
    v 0 1 0
    f 1 2 3

hoge.mtl
    newmtl triangle_01
    Kd 0.7 0.8 0.9
"""
