import algeol as al
import object1 as o1
import object2 as o2
import object3 as o3

DIR = './obj/'

def save(name, node, mtld):
    mtls = [v for k, v in mtld.items()]
    affine = al.dotall((
        al.scale((10, 10, 10)), # for Vue
        al.rotate_x90d[-1], # for wavefront
    ))
    fo, fm = al.save_node_mtl(DIR + name, node, mtls, affine)
    print('save: ' + fo)
    print('save: ' + fm)

def towers1(mtld):
    nTowers = []
    eTowers = []
    for i in range(4):
        n, m = o3.waterArchTower1(towerN=i+1)
        nTowers.append(n)
        mtld.update(m)
    for i in range(5):
        for j in range(5):
            dx = i - 2
            dy = j - 2
            d = abs(dx) + abs(dy)
            if d == 0:
                pass
            elif d <= len(nTowers):
                af = al.translate((d*-2 + dx*20, d*-2 + dy*20, 0))
                edge = al.Edge(nTowers[d-1], af)
                eTowers.append(edge)
    return al.Node(edges=eTowers)

def _isinCircle(x, y, r):
    return x*x + y*y < r*r
def _isinRect(x, y, r):
    return abs(x) + abs(y) < r

def cubes1(mtld):
    nCube = o1.floorCube(sx=0.9, sy=0.9)
    eCubes = []
    for i in range(-50, 51):
        for j in range(-50, 51):
            b = False
            if _isinRect(i, j, 24):
                b ^= True
            if _isinRect(i, j, 32):
                b ^= True
            if _isinRect(i+26, j, 12):
                b ^= True
            if _isinRect(i+26, j, 16):
                b ^= True
            if _isinRect(i-26, j, 12):
                b ^= True
            if _isinRect(i-26, j, 16):
                b ^= True
            if _isinRect(i, j+26, 12):
                b ^= True
            if _isinRect(i, j+26, 16):
                b ^= True
            if _isinRect(i, j-26, 12):
                b ^= True
            if _isinRect(i, j-26, 16):
                b ^= True
            if _isinCircle(i, j, 44.5):
                b ^= True
            if _isinCircle(i, j, 49.5):
                b ^= True
            if b:
                edge = al.Edge(nCube, al.translate((i, j, 0)))
                eCubes.append(edge)
    return al.Node(edges=eCubes)

def cross(mtld):
    nLine, m = o3.waterArchTower0(towerHoffset=-1, xlen=15, towerN=2)
    mtld.update(m)
    nCenter, m = o3.waterArchTower1(towerHoffset=-1, towerN=3, towerWD=2)
    mtld.update(m)
    eCenter = al.Edge(nCenter, al.translate((-2*3*2+2, -2*3*2+2, 0)))
    afLines = []
    for i in range(2):
        af = al.dotall((
            al.rotate_z90d[i],
            al.translate((-30, -2, 0)),
        ))
        afLines.append(af)
    eLines = [al.Edge(nLine, af) for af in afLines]
    return al.Node(edges=[eCenter] + eLines)

def cross2(mtld):
    linelen = 30
    nLine, m = o3.waterArchTower0(towerHoffset=0, xlen=linelen, towerN=3)
    mtld.update(m)
    nCenter, m = o3.waterArchTower1(towerHoffset=0, towerN=5, towerWD=2)
    mtld.update(m)
    eCenter = al.Edge(nCenter, al.translate((-2*5*2+2, -2*5*2+2, 0)))
    afLines = []
    for i in range(2):
        af = al.dotall((
            al.rotate_z90d[i],
            al.translate((linelen*-2, -2, 0)),
        ))
        afLines.append(af)
    eLines = [al.Edge(nLine, af) for af in afLines]
    return al.Node(edges=[eCenter] + eLines)

def main1():
    mtld = {}
    nTowers = towers1(mtld)
    save('world', nTowers, mtld)

def main2():
    mtld = {}
    node = cubes1(mtld)
    save('world2', node, mtld)

def main3():
    mtld = {}
    node1 = towers1(mtld)
    node2 = cubes1(mtld)
    edges = [
        al.Edge(node1),
        al.Edge(node2, material=mtld['block'])
    ]
    save('world3', al.Node(edges=edges), mtld)

def main():
    mtld = {}
    node = cross2(mtld)
    save('world5_cross2', node, mtld)

if __name__ == "__main__":
    main()
