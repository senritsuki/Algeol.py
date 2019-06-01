import sys
import numpy as np
import algeol as al
import color_converter as cc

def test_colors1():
    verts = al.octahedron_verts()
    faces = al.octahedron_faces()
    mtls = [('lch_70_40_%d' % (i*15), cc.lch_to_rgb01((70, 40, i*15))) for i in range(24)]
    affines = [al.translate((4 * al.sind(i*15), 4 * al.cosd(i*15), 0)) for i in range(24)]
    def obj_writer(f):
        al.write_mtllib(f, 'colors1')
        i = 1
        for affine, (mtl, kd_rgb) in zip(affines, mtls):
            verts2 = al.transform(affine, verts)
            al.write_g(f, mtl)
            al.write_usemtl(f, mtl)
            i = al.write_obj(f, verts2, faces, i)
    f = al.open_w_obj('obj/colors1', obj_writer)
    print('save: ' + f)
    f = al.save_mtls('obj/colors1', mtls)
    print('save: ' + f)

def main(argv):
    if len(argv) < 2:
        print('コマンド引数がありません')
        return
    s0 = argv[1]
    if s0 == 'colors1':
        test_colors1()
    else:
        print('%s は未対応のコマンドです' % s0)

if __name__ == "__main__":
    main(sys.argv)
