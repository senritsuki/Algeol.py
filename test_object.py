import sys
import test_common as tc
import algeol as al
import object1 as o1
import object2 as o2
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
    add2 = add1
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
    add1('steps', o1.steps)
    add1('steps2', o2.steps)
    add1('spiralsteps', o1.spiralsteps)
    add1('spiralsteps_q1', lambda: o1.spiralsteps(quarters=1, height=1))
    add1('spiralsteps_q2', lambda: o1.spiralsteps(quarters=2, height=2))
    add2('archBridgeN', o2.archBridgeN)
    add2('archBridgeNN', o2.archBridgeNN)
    add2('archBridgeNNG', lambda: o2.archBridgeNN(archLenX=5, archNY=4, grid=True))
    add3('waterBlock', o3.waterBlock)
    add3('waterArchBridge', o3.waterArchBridge)
    add3('waterArchTower0', o3.waterArchTower0)
    add3('waterArchTower1', o3.waterArchTower1)
    add3('waterArchTower2', o3.waterArchTower2)
    tc.main(sys.argv, d)
