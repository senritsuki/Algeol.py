import algeol_common as al
import algeol_primitive as prim
import color_converter as cc

def waterBlock(z_block=1/8, z_water=6/8):
    cube = al.Node(prim.cube())
    af_b = al.dotall([
        al.translate((0, 0, -1/2)),
        al.scale((1, 1, z_block)),
        al.translate((0, 0, 1/2)),
    ])
    af_w = al.dotall([
        al.translate((0, 0, -1/2+z_block)),
        al.scale((1, 1, z_water)),
        al.translate((0, 0, 1/2)),
    ])
    mtl_b = al.Material('block', cc.lch_to_rgb01((90, 0, 0)))
    mtl_w = al.Material('water', cc.lch_to_rgb01((70, 40, 225)))
    edge_b = al.Edge(cube, af_b, mtl_b)
    edge_w = al.Edge(cube, af_w, mtl_w)
    node = al.Node(edges=[edge_b, edge_w])
    mtld = {m.name: m for m in (mtl_b, mtl_w)}
    return node, mtld

