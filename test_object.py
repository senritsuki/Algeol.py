import sys
import test_common as tc
import algeol as al

import object1 as o1
import object3 as o3

DIR = 'obj/object/'

if __name__ == "__main__":
    d = {}
    def add1(name, fn):
        def fn2():
            node = fn()
            affine = al.rotate_x90d[-1]
            fo = al.save_node(DIR + name, node, affine)
            print('save: ' + fo)
        d[name] = fn2
    def add3(name, fn):
        def fn2():
            node, mtld = fn()
            mtls = [v for k, v in mtld.items()]
            affine = al.rotate_x90d[-1]
            fo, fm = al.save_node_mtl(DIR + name, node, mtls, affine)
            print('save: ' + fo)
            print('save: ' + fm)
        d[name] = fn2
    add1('arch', o1.arch)
    add3('waterBlock', o3.waterBlock)
    tc.main(sys.argv, d)
