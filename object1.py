import algeol_common as al
import algeol_primitive as prim

# size: (2, 1, 1)
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

def step(dx=1/4, dz=1/16, ox=0):
    cube = al.Node(prim.cube())
    af = al.dotall((
        al.translate((ox, 0, 0)),
        al.scale((dx, 1, dz)),
        al.translate((0.5, 0, -0.5)),
    ))
    edge = al.Edge(cube, af)
    return al.Node(edges=[edge])

def steps(n=4, dz=1/16, offset=0, xlen=2, height=1):
    nStep = step(dx=1/n, dz=dz) 
    afs = [al.translate(( i/n, 0, (i+offset)*height/(n*xlen) )) for i in range(n*xlen)]
    edges = [al.Edge(nStep, af) for af in afs]
    return al.Node(edges=edges)

def spiralsteps(r=1, dx=1/4, dz=1/16, quarters=4, qn=6, height=4):
    nStep = step(dx=dx, dz=dz, ox=-dx/2)
    edges = []
    kmax = quarters * qn
    af = lambda k: al.dotall((
        al.translate((0, r, 0)),
        al.rotate_z(al.PI05 * k / qn),
        al.translate((0, -r, k*height/kmax)),
    ))
    for i in range(quarters):
        for j in range(qn):
            edges.append(al.Edge(nStep, af(i * qn + j)))
    edges.append(al.Edge(nStep, af(kmax)))
    return al.Node(edges=edges)

def floorCube(sx=1, sy=1, sz=1, oz=0):
    cube = al.Node(prim.cube())
    floorAffine = al.dotall([
        al.translate((0, 0, oz)),
        al.scale((sx, sy, sz)),
        al.translate((0, 0, -0.5)),
    ])
    return al.Node(edges=[ al.Edge(cube, floorAffine) ])
