import sys
import numpy as np
import algeol as al
import color_converter as cc
import test_common as tc

DIR = 'obj/material/'

def write_affines_mtls(f, name, verts, faces, affines, mtls):
    al.write_mtllib(f, name)
    i = 1
    for affine, (mtl, kd) in zip(affines, mtls):
        verts2 = al.transform(affine, verts)
        al.write_g(f, mtl)
        al.write_usemtl(f, mtl)
        i = al.write_obj(f, verts2, faces, i)

def colors1():
    name = 'colors1'
    verts, faces = al.octahedron()
    colornum = 72
    colordeg = 5
    fn_mtl = lambda deg: ('lch_70_40_%d' % deg, cc.lch_to_rgb01((70, 40, deg)))
    r = 10 * np.pi / colornum
    fn_affine = lambda deg: al.dotall([
        al.rotate_x90d[-1],
        al.rotate_z(al.PI2 * -deg / 360),
        al.translate((0, 5, 0)),
        al.scale((r, r, r)),
    ])
    mtls = [fn_mtl(i * colordeg) for i in range(colornum)]
    affines = [fn_affine(i * colordeg) for i in range(colornum)]
    f = al.open_w_obj(DIR + name, 
        lambda f: write_affines_mtls(f, name, verts, faces, affines, mtls))
    print('save: ' + f)
    f = al.save_mtls(DIR + name, mtls)
    print('save: ' + f)

def colors2():
    name = 'colors2'
    d = 4
    scalen = 0.96
    scale = (scalen, scalen, scalen)
    verts, faces = al.cube()
    mtls = []
    affines = []
    for a in range(-40, 40+1, d):
        for b in range(-40, 40+1, d):
            if a*a + b*b >= (40+d/2) * (40+d/2):
                continue
            mtl = 'lab_70_%d_%d' % (a, b), cc.lab_to_rgb01((70, a, b))
            affine = al.dotall([
                al.rotate_x90d[-1],
                al.translate((b / d, a / d, 0)),
                al.scale(scale),
            ])
            mtls.append(mtl)
            affines.append(affine)
    f = al.open_w_obj(DIR + name, 
        lambda f: write_affines_mtls(f, name, verts, faces, affines, mtls))
    print('save: ' + f)
    f = al.save_mtls(DIR + name, mtls)
    print('save: ' + f)

if __name__ == "__main__":
    tc.main(sys.argv, {
        'colors1': colors1,
        'colors2': colors2,
    })
