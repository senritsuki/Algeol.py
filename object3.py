import algeol_common as al
import algeol_primitive as prim
import color_converter as cc
import object2 as o2

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

# width: 5, 9, 13, ...
def waterArchBridge(
    arcN=12, 
    xlen=2, 
    ylen=2, 
    columnH=4,
    archLen=3,
    ):
    archBridge = o2.archBridgeNN(
        arcN=arcN, 
        archNX=xlen, 
        archNY=ylen, 
        archLenX=archLen, 
        archLenY=archLen, 
        columnH=columnH, 
        floorH=1,
        grid=False,
        )
    water, mtld = waterBlock()
    eArchBridge = al.Edge(archBridge, material=mtld['block'])
    eWaterBlock = al.Edge(water, al.dotall((
        al.scale(((archLen+1) * xlen, (archLen+1) * ylen, 1)),
        al.translate((0.5, 0.5, -0.5)),
    )))
    node = al.Node(edges=[eArchBridge, eWaterBlock])
    return node, mtld

def waterArchTower0(
    arcN=12, 
    xlen=1,
    ylen=1,
    towerH=5,
    towerHoffset=0,
    underH=5,
    towerN=3,
    ):
    edges = []
    mtld = {}
    for i in range(towerN):
        dz = (i+1) * towerH + towerHoffset
        node, mtld2 = waterArchBridge(
            arcN=arcN,
            xlen=xlen, 
            ylen=ylen, 
            columnH=dz+underH, 
        )
        edge = al.Edge(node, al.translate((0, 0, dz)))
        edges.append(edge)
        mtld.update(mtld2)
    return al.Node(edges=edges), mtld

# size: 5, 9, 13, ...
def waterArchTower1(
    arcN=12, 
    towerH=5,
    towerHoffset=0,
    underH=5,
    towerN=3,
    towerW0=1,
    towerWD=1,
    ):
    edges = []
    mtld = {}
    for i in range(towerN):
        dlen = towerW0 + (towerN - i - 1) * towerWD
        dxy = i * 2 * towerWD
        dz = (i+1) * towerH + towerHoffset
        node, mtld2 = waterArchBridge(
            arcN=arcN,
            xlen=dlen, 
            ylen=dlen, 
            columnH=dz+underH, 
        )
        edge = al.Edge(node, al.translate((dxy, dxy, dz)))
        edges.append(edge)
        mtld.update(mtld2)
    return al.Node(edges=edges), mtld

def waterArchTower2(
    arcN=12, 
    xlen=3,
    towerH=5,
    towerHoffset=0,
    underH=5,
    towerN=3,
    ):
    edges = []
    mtld = {}
    for i in range(towerN):
        dz = (towerN-i) * towerH + towerHoffset
        node, mtld2 = waterArchBridge(
            arcN=arcN,
            xlen=xlen, 
            ylen=i+1, 
            columnH=dz+underH, 
        )
        edge = al.Edge(node, al.translate((0, 0, dz)))
        edges.append(edge)
        mtld.update(mtld2)
    return al.Node(edges=edges), mtld
