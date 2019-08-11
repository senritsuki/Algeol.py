import algeol_common as al
import algeol_primitive as prim
import object1 as o1
import numpy as np

# inner, side, corner は None でもよい
# inner, side, corner のsizeは 1*1*n を想定している
def rectBorder(inner, side, corner, dx, dy, ox=0, oy=0):
    x0 = ox - dx / 2
    y0 = oy - dy / 2
    x1 = x0 + dx
    y1 = y0 + dy
    edges = []
    if inner:
        edges.append(al.Edge(inner, al.dotall([ al.translate((ox, oy, 0)), al.scale((dx, dy, 1)), ])))
    if side:
        edges += [
            al.Edge(side, al.dotall([ al.translate((ox, y0, 0)), al.scale((dx,  1, 1)), ])),
            al.Edge(side, al.dotall([ al.translate((ox, y1, 0)), al.scale((dx,  1, 1)), ])),
            al.Edge(side, al.dotall([ al.translate((x0, oy, 0)), al.scale(( 1, dy, 1)), ])),
            al.Edge(side, al.dotall([ al.translate((x1, oy, 0)), al.scale(( 1, dy, 1)), ])),
        ]
    if corner:
        edges += [
            al.Edge(corner, al.translate((x0, y0, 0))),
            al.Edge(corner, al.translate((x0, y1, 0))),
            al.Edge(corner, al.translate((x1, y0, 0))),
            al.Edge(corner, al.translate((x1, y1, 0))),
        ]
    return al.Node(edges=edges)

# 原点ではなくx=1からスタート
def roadArch(arcN=12, archLen=2, floorNode=None, floorHeight=1, ox=1):
    arch = o1.arch(arcN)
    archScale = archLen / 2
    archE = al.Edge(arch, al.dotall([
        al.translate((-0.5+ox, 0, -floorHeight)),
        al.scale((archScale, 1, archScale)),
        al.translate((0.5, 0, -0.5)),
    ]))
    if not floorNode:
        floorNodeAf = al.dotall([
            al.scale((1, 1, floorHeight)),
            al.translate((0, 0, -0.5)),
        ])
        floorNode = al.Node(edges=[al.Edge(al.Node(prim.cube()), floorNodeAf)])
    floorE = al.Edge(floorNode, al.dotall([
        al.translate((-0.5+ox, 0, 0)),
        al.scale((archLen, 1, 1)),
        al.translate((0.5, 0, 0)),
    ]))
    return al.Node(edges=[ archE, floorE ])

def underColumn(columnH=4, floor=None, floorH=1):
    column = al.Node(prim.cube())
    columnEdge = al.Edge(column, al.dotall([
        al.translate((0, 0, -floorH)),
        al.scale((1, 1, columnH)),
        al.translate((0, 0, -0.5)),
    ]))
    if not floor:
        floor = o1.floorCube()
    floorEdge = al.Edge(floor)
    return al.Node(edges=[ columnEdge, floorEdge ])

def squareColumns(column, xylist=[]):
    edges = [al.Edge(column, al.translate((x, y, 0))) for x, y in xylist]
    return al.Node(edges=edges)

def archBridgeN(
    arcN=12, 
    archN=2, 
    archLen=2, 
    columnH=4, 
    floorNodeA=None, 
    floorNodeC=None, 
    floorH=1,
    ):
    bridge = roadArch(arcN, archLen, floorNodeA, floorH)
    column = underColumn(columnH, floorNodeC, floorH)
    eBridges = [al.Edge(bridge, al.translate((i * (archLen+1), 0, 0))) for i in range(archN)]
    eColumns = [al.Edge(column, al.translate((i * (archLen+1), 0, 0))) for i in range(archN+1)]
    return al.Node(edges=eBridges+eColumns)

def archBridgeNN(
    arcN=12, 
    archNX=2, 
    archNY=2, 
    archLenX=2, 
    archLenY=2, 
    columnH=4, 
    floorNodeA=None, 
    floorNodeC=None, 
    floorH=1,
    grid=False,
    ):
    bridgeX = roadArch(arcN, archLenX, floorNodeA, floorH)
    bridgeY = roadArch(arcN, archLenY, floorNodeA, floorH)
    column = underColumn(columnH, floorNodeC, floorH)
    eBridgesX = []
    eBridgesY = []
    eColumns = []
    ij2xy = lambda i, j: (i * (archLenX + 1), j * (archLenY + 1))
    for i in range(archNX):
        for j in range(archNY+1):
            if grid == False:
                if 1 <= j and j < archNY:
                    continue
            x, y = ij2xy(i, j)
            af = al.translate((x, y, 0))
            eBridgesX.append(al.Edge(bridgeX, af))
    for i in range(archNX+1):
        for j in range(archNY):
            if grid == False:
                if 1 <= i and i < archNX:
                    continue
            x, y = ij2xy(i, j)
            af = np.dot( al.translate((x, y, 0)), al.rotate_z90d[1] )
            eBridgesY.append(al.Edge(bridgeY, af))
    for i in range(archNX+1):
        for j in range(archNY+1):
            if grid == False:
                if 1 <= i and i < archNX and 1 <= j and j < archNY:
                    continue
            af = al.translate((i * (archLenX+1), j * (archLenY+1), 0))
            eColumns.append(al.Edge(column, af))
    return al.Node(edges=eBridgesX+eBridgesY+eColumns)

def steps(src=(0, 0, 5), dst=(8, 0, -1), width=3):
    d = np.array(dst) - np.array(src)
    xlen = int(np.linalg.norm((d[0], d[1], 0)) - 1)
    nSteps = o1.steps(xlen=xlen, height=d[2])
    af = al.dotall((
        al.translate(src),
        al.calc_rotate_z(d),
        al.scale((1, width, 1)),
    ))
    edge = al.Edge(nSteps, af)
    return al.Node(edges=[edge])

