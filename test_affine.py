import sys
import numpy as np
import algeol as al

def test_translate1():
    verts = al.octahedron_verts()
    faces = al.octahedron_faces()
    name = 'obj/affine_translate1'
    affines = [al.translate((x, 0, 0)) for x in range(5)]
    f = al.save_obj_affines(verts, faces, name, affines)
    print('save: ' + f)

def test_translate2():
    verts = al.octahedron_verts()
    faces = al.octahedron_faces()
    name = 'obj/affine_translate2'
    affines = [[al.translate((x, y, 0)) for y in range(6)] for x in range(5)]
    affines = np.array(affines).reshape((-1, 4, 4))
    f = al.save_obj_affines(verts, faces, name, affines)
    print('save: ' + f)

def test_affines():
    verts = al.prism3_verts()
    faces = al.prism3_faces()
    name = 'obj/affine_affines'
    affines = []
    rotates = al.rot_x4 + al.rot_y4 + al.rot_z4
    scale = al.scale((0.5, 0.5, 0.5))
    x = len(rotates) * -0.5 + 0.5
    for rotate in rotates:
        translate = al.translate((x, 0, 0))
        mx = np.dot(rotate, scale)
        mx = np.dot(translate, mx)
        affines.append(mx)
        x += 1
    f = al.save_obj_affines(verts, faces, name, affines)
    print('save: ' + f)


def main(argv):
    if len(argv) < 2:
        print('コマンド引数がありません')
        return
    s0 = argv[1]
    if s0 == 'translate1':
        test_translate1()
    elif s0 == 'translate2':
        test_translate2()
    elif s0 == 'affines':
        test_affines()
    else:
        print('%s は未対応のコマンドです' % s0)

if __name__ == "__main__":
    main(sys.argv)
