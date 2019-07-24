import algeol_common as al
import algeol_primitive as prim

# inner, side, corner は None でもよい
# inner, side, corner のsizeは 1*1*n を想定している
def rectBorder(inner, side, corner, dx, dy, ox=0, oy=0):
    x0 = ox - dx / 2
    y0 = oy - dy / 2
    x1 = x0 + dx
    y1 = y0 + dy
    edges = []
    if inner:
        edges.append(al.Edge(inner, al.dotall([al.translate(ox, oy, 0), al.scale((dx, dy, 1))])))
    if side:
        edges += [
            al.Edge(side, al.dotall([al.translate((ox, y0, 0)), al.scale((dx,  1, 1))])),
            al.Edge(side, al.dotall([al.translate((ox, y1, 0)), al.scale((dx,  1, 1))])),
            al.Edge(side, al.dotall([al.translate((x0, oy, 0)), al.scale(( 1, dy, 1))])),
            al.Edge(side, al.dotall([al.translate((x1, oy, 0)), al.scale(( 1, dy, 1))])),
        ]
    if corner:
        edges += [
            al.Edge(corner, al.translate((x0, y0, 0))),
            al.Edge(corner, al.translate((x0, y1, 0))),
            al.Edge(corner, al.translate((x1, y0, 0))),
            al.Edge(corner, al.translate((x1, y1, 0))),
        ]
    return al.Node(edges=edges)

