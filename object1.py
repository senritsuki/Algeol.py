import algeol_common as al
import algeol_primitive as prim

def arch(n=12, x=1):
    leaf = al.Node(prim.quarter_cylinder_complement(n))
    af1 = al.dotall([
        al.rotate_x90d[1],
        al.rotate_z90d[1],
    ])
    af2 = al.dotall([
        al.translate((x, 0, 0)),
        al.rotate_x90d[1],
    ])
    edges = [al.Edge(leaf, af) for af in (af1, af2)]
    return al.Node(edges=edges)

def prism_outside(n=12):
    leaf = al.Node(prim.regular_prism(n))
    edge = al.Edge(leaf, al.scale((al.R2, al.R2, 1)))
    return al.Node(edges=[edge])
