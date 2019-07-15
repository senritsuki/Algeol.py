import sys
import algeol as al
import test_common as tc

DIR = 'obj/primitive/'

if __name__ == "__main__":
    d = {}

    def add(fn, name):
        def fn2():
            verts, faces = fn()
            verts = al.transform(al.rotate_x90d[-1], verts)
            f = al.save_obj(verts, faces, DIR + name)
            print('save: ' + f)
        d[name] = fn2

    add(al.square, 'square'),
    add(lambda: al.regular_polygon(4), 'regular_polygon4'),
    add(lambda: al.regular_polygon(6), 'regular_polygon6'),
    add(lambda: al.quarter_pie(12), 'quarter_pie'),
    add(lambda: al.quarter_pie_complement(12), 'quarter_pie_complement'),
    add(al.isosceles_right_triangle, 'isosceles_right_triangle'),
    add(al.tetrahedron, 'tetrahedron'),
    add(al.cube, 'cube'),
    add(al.octahedron, 'octahedron'),
    add(al.dodecahedron, 'dodecahedron'),
    add(al.icosahedron, 'icosahedron'),
    add(lambda: al.regular_prism(4), 'regular_prism4')
    add(lambda: al.regular_prism(6), 'regular_prism6')
    add(al.isosceles_right_triangular_prism, 'isosceles_right_triangular_prism'),
    add(lambda: al.quarter_cylinder(12), 'quarter_cylinder'),
    add(lambda: al.quarter_cylinder_complement(12), 'quarter_cylinder_complement'),
    add(al.square_pyramid, 'square_pyramid'),
    add(lambda: al.icosphere(0), 'icosphere0'),
    add(lambda: al.icosphere(1), 'icosphere1'),
    add(lambda: al.icosphere(2), 'icosphere2'),
    add(lambda: al.torus(0.75, 4, 4), 'torus_4_4'),
    add(lambda: al.torus(0.75, 4, 8), 'torus_4_8'),
    add(lambda: al.torus(0.75, 4, 12), 'torus_4_12'),
    add(lambda: al.torus(0.75, 4, 48), 'torus_4_48'),
    add(lambda: al.torus(0.75, 6, 24), 'torus_6_24'),
    add(lambda: al.concaved_cube(1/16), 'concaved_cube'),

    tc.main(sys.argv, d)
