import sys
import algeol as al

def test_plane4():
    verts = al.plane4_verts()
    faces = al.plane4_faces()
    name = 'obj/plane4'
    al.save_obj_1(verts, faces, name)

def test_cube():
    verts = al.cube_verts()
    faces = al.cube_faces()
    name = 'obj/cube'
    al.save_obj_1(verts, faces, name)

def test_octahedron():
    verts = al.octahedron_verts()
    faces = al.octahedron_faces()
    name = 'obj/octahedron'
    al.save_obj_1(verts, faces, name)

def test_prism3():
    verts = al.prism3_verts()
    faces = al.prism3_faces()
    name = 'obj/prism3'
    al.save_obj_1(verts, faces, name)

def test_pyramid4():
    verts = al.pyramid4_verts()
    faces = al.pyramid4_faces()
    name = 'obj/pyramid4'
    al.save_obj_1(verts, faces, name)

def main(argv):
    if len(argv) < 2:
        print('コマンド引数がありません')
        return
    s0 = argv[1]
    if s0 == 'plane4':
        test_plane4()
    elif s0 == 'cube':
        test_cube()
    elif s0 == 'octahedron':
        test_octahedron()
    elif s0 == 'prism3':
        test_prism3()
    elif s0 == 'pyramid4':
        test_pyramid4()
    else:
        print('%s は未対応のコマンドです' % s0)

if __name__ == "__main__":
    main(sys.argv)
