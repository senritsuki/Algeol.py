import sys
import numpy as np
import algeol as al
import test_common as tc

DIR = 'obj/affine/'

def translation1():
    verts, faces = al.cube()
    name = DIR + 'translation1'
    affines = []
    def zf(y):
        if y <= -4:
            return -2
        elif y <= 4:
            return y / 2
        else:
            return 2
    for x in range(-1, 1+1):
        for y in range(-10, 10+1):
            s = 0.96
            z = zf(y)
            af = al.dotall([
                al.rotate_x90d[-1],
                al.translate((x, y, z)),
                al.scale((s, s, s/2)),
            ])
            affines.append(af)
    f = al.save_obj_affines(verts, faces, name, affines)
    print('save: ' + f)

def translation2():
    verts, faces = al.square_pyramid()
    name = DIR + 'translation2'
    affines = []
    def zf(x, y):
        dx = x / 5
        dy = y / 5
        d = 1 - np.sqrt(dx*dx + dy*dy)
        dz = 1 - np.sin(np.arccos(d))
        return dz * 10 + 1
    for x in range(-5, 5+1):
        for y in range(-5, 5+1):
            if abs(x) + abs(y) > 5+1:
                continue
            s = 0.96
            z = zf(x, y)
            af = al.dotall([
                al.rotate_x90d[-1],
                al.translate((x, y, 0)),
                al.scale((s, s, z)),
                al.translate((0, 0, -0.5)),
                al.rotate_x90d[2],
            ])
            affines.append(af)
    f = al.save_obj_affines(verts, faces, name, affines)
    print('save: ' + f)

def rotation():
    verts, faces = al.prism3()
    name = DIR + 'rotation'
    affines = []
    rotates = al.rotate_x90d + al.rotate_y90d + al.rotate_z90d
    scale = al.scale((0.5, 0.5, 0.5))
    x = len(rotates) * -0.5 + 0.5
    for rotate in rotates:
        affine = al.dotall((
            al.translate((x, 0, 0)),
            rotate,
            scale,
        ))
        affines.append(affine)
        x += 1
    f = al.save_obj_affines(verts, faces, name, affines)
    print('save: ' + f)

if __name__ == "__main__":
    d = {
        'rotation': rotation,
        'translation1': translation1,
        'translation2': translation2,
    }
    tc.main(sys.argv, d)
