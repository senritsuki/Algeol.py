from algeol_common import np, transform, Node, Material, unit

FORMAT_V = 'v %.3f %.3f %.3f'

def update_format_v(format = 'v %.3f %.3f %.3f'):
    global FORMAT_V
    FORMAT_V = format

def verts2lines(verts):
    return [FORMAT_V % (v[0], v[1], v[2]) for v in verts]

def faces2lines(faces, offset=1):
    return ['f ' + ' '.join([str(n+offset) for n in f]) for f in faces]

def rgb2line(rgb):
    return '%.3f %.3f %.3f' % (rgb[0], rgb[1], rgb[2])

# for *.obj
def write_mtllib(fp, name):
    file = name if name[-4:] == '.mtl' else name + '.mtl'
    fp.write('mtllib %s\n\n' % file)

def write_g(fp, name):
    fp.write('g %s\n' % name)

def write_usemtl(fp, name):
    fp.write('usemtl %s\n' % name)

# for *.mtl
def write_newmtl_kd(fp, material: Material):
    fp.write('newmtl %s\n' % material.name)
    fp.write('Kd %s\n\n' % rgb2line(material.rgb))

def write_obj(fp, verts, faces, face_offset):
    i = 0
    for line in verts2lines(verts):
        fp.write(line + '\n')
        i += 1
    for line in faces2lines(faces, face_offset):
        fp.write(line + '\n')
    return face_offset + i

def write_obj_affine(fp, verts, faces, face_offset, affines):
    i = face_offset
    for affine in affines:
        j = 0
        verts2 = transform(affine, verts)
        for line in verts2lines(verts2):
            fp.write(line + '\n')
            j += 1
        for line in faces2lines(faces, i):
            fp.write(line + '\n')
        i += j
    return i

def write_mtls(fp, mtls: list):
    for mtl in mtls:
        write_newmtl_kd(fp, mtl)

def open_w_obj(name, callback):
    file = name if name[-4:] == '.obj' else name + '.obj'
    with open(file, 'w') as fp:
        callback(fp)
    return file

def save_obj(verts, faces, name):
    return open_w_obj(name, lambda f: write_obj(f, verts, faces, 1))

def save_obj_affines(verts, faces, name, affines):
    return open_w_obj(name, lambda f: write_obj_affine(f, verts, faces, 1, affines))

def open_w_mtl(name, callback):
    file = name if name[-4:] == '.mtl' else name + '.mtl'
    with open(file, 'w') as f:
        callback(f)
    return file

# mtls: (newmtl, kd_rgb)[]
def save_mtls(name, mtls):
    return open_w_mtl(name, lambda f: write_mtls(f, mtls))

def write_node(fp, node: Node, affine: np.ndarray, face_offset: int) -> int:
    j = face_offset
    if node.vf:
        v = transform(affine, node.vf[0])
        f = node.vf[1]
        j = write_obj(fp, v, f, j)
    for edge in node.edges:
        if edge.material is not None:
            write_g(fp, edge.material.name)
            write_usemtl(fp, edge.material.name)
        af2 = affine
        if edge.affine is not None:
            af2 = np.dot(affine, edge.affine)
        j = write_node(fp, edge.dstNode, af2, j)
    return j

def save_node(name, node, affine=unit):
    return open_w_obj(name, lambda fp: write_node(fp, node, affine, 1))

def save_node_mtl(name, node, mtls, affine=unit):
    def fn(fp):
        write_mtllib(fp, name)
        return write_node(fp, node, affine, 1)
    fo = open_w_obj(name, fn)
    fm = save_mtls(name, mtls)
    return fo, fm

"""
hoge.obj
    mtllib hoge.mtl

    g triangle_01
    usemtl triangle_01
    v 0 0 0
    v 1 0 0
    v 0 1 0
    f 1 2 3

hoge.mtl
    newmtl triangle_01
    Kd 0.7 0.8 0.9
"""
