import sys
import algeol as al

def test_common(fn, name):
    verts, faces = fn()
    verts = al.transform(al.rot_x4[-1], verts)
    name = 'obj/' + name
    f = al.save_obj(verts, faces, name)
    print('save: ' + f)

def plane4():
    test_common(al.plane4, 'plane4')

def quarter_pie():
    test_common(lambda: al.quarter_pie(12), 'quarter_pie')

def quarter_pie2():
    test_common(lambda: al.quarter_pie2(12), 'quarter_pie2')

def tetrahedron():
    test_common(al.tetrahedron, 'tetrahedron')

def cube():
    test_common(al.cube, 'cube')

def octahedron():
    test_common(al.octahedron, 'octahedron')

def dodecahedron():
    test_common(al.dodecahedron, 'dodecahedron')

def icosahedron():
    test_common(al.icosahedron, 'icosahedron')

def prism3():
    test_common(al.prism3, 'prism3')

def quarter_cylinder():
    test_common(lambda: al.quarter_cylinder(12), 'quarter_cylinder')

def quarter_cylinder2():
    test_common(lambda: al.quarter_cylinder2(12), 'quarter_cylinder2')

def pyramid4():
    test_common(al.pyramid4, 'pyramid4')

def concaved_cube():
    test_common(lambda: al.concaved_cube(1/16), 'concaved_cube')

def main(argv):
    dic = {
        'plane4': plane4,
        'quarter_pie': quarter_pie,
        'quarter_pie2': quarter_pie2,
        'tetrahedron': tetrahedron,
        'cube': cube,
        'octahedron': octahedron,
        'dodecahedron': dodecahedron,
        'icosahedron': icosahedron,
        'prism3': prism3,
        'quarter_cylinder': quarter_cylinder,
        'quarter_cylinder2': quarter_cylinder2,
        'pyramid4': pyramid4,
        'concaved_cube': concaved_cube,
    }
    if len(argv) < 2:
        print('コマンド引数がありません')
        print('対抗コマンド：')
        for key in dic.keys():
            print(' - ' + key)
        return
    s0 = argv[1]
    if s0 == 'all':
        print('全コマンドを実行します')
        for fn in dic.values():
            fn()
    elif s0 not in dic:
        print('%s は未対応のコマンドです' % s0)
        print('対抗コマンド：')
        for key in dic.keys():
            print(' - ' + key)
    else:
        dic[s0]()

if __name__ == "__main__":
    main(sys.argv)
