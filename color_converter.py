
import numpy as np


### constant

# D65 linear sRGB から D50 XYZ への線形変換
mx_lrgb_to_xyz = np.array([
    [0.436041, 0.385113, 0.143046],
    [0.222485, 0.716905, 0.060610],
    [0.013920, 0.097067, 0.713913]])

# D50 XYZ から D65 linear sRGB への線形変換
mx_xyz_to_lrgb = np.array([
    [ 3.134187, -1.617209, -0.490694],
    [-0.978749,  1.916130,  0.033433],
    [ 0.071964, -0.228994,  1.405754]])

# 白色点
XYZn = np.array([0.9642, 1.0000, 0.8249])

# 関数合成
composite_2f = lambda f, g: lambda t: g(f(t))
composite_3f = lambda f, g, h: lambda t: h(g(f(t)))


# RGB array (0, 0, 0) .. (255, 255, 255)
#   ->
# RGB string '#000000' .. '#ffffff'
def rgb255_to_rgbhex(rgb: np.array) -> str:
    f = lambda n: 0 if n < 0 else 255 if n > 255 else int(n)
    return '#%02x%02x%02x' % (f(rgb[0]), f(rgb[1]), f(rgb[2]))

# RGB string '#000000' .. '#ffffff'
#   ->
# RGB array (0, 0, 0) .. (255, 255, 255)
def rgbhex_to_rgb255(rgbhex: str) -> np.array:
    if rgbhex[0] == '#':
        rgbhex = rgbhex[1:]
    r = int(rgbhex[0:2], 16)
    g = int(rgbhex[2:4], 16)
    b = int(rgbhex[4:6], 16)
    return np.array((r, g, b))


# RGB array (0, 0, 0) .. (255, 255, 255)
#   ->
# RGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
def rgb255_to_rgb01(rgb: np.array) -> np.array:
    return rgb / 255

# RGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
#   ->
# RGB array (0, 0, 0) .. (255, 255, 255)
def rgb01_to_rgb255(rgb: np.array) -> np.array:
    return rgb * 255


# D65 non linear sRGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
#   ->
# D65 linear sRGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
def srgb_to_lrgb(rgb: np.array) -> np.array:
    f0 = lambda n: np.power((n + 0.055) / 1.055, 2.4)
    f1 = lambda n: n / 12.92
    f = lambda n: f0(n) if n > 0.040450 else f1(0)
    return np.array([f(n) for n in rgb])

# D65 linear sRGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
#   ->
# D65 non linear sRGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
def lrgb_to_srgb(rgb: np.array) -> np.array:
    f0 = lambda n: 1.055 * np.power(n, 1 / 2.4) - 0.055
    f1 = lambda n: 12.92 * n
    f = lambda n: f0(n) if n > 0.0031308 else f1(n)
    return np.array([f(n) for n in rgb])


# D65 linear sRGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
#   ->
# D50 CIE XYZ array (*.*, *.*, *.*) .. (*.*, *.*, *.*)
def lrgb_to_xyz(rgb: np.array) -> np.array:
    return np.dot(mx_lrgb_to_xyz, rgb)

# D50 CIE XYZ array (*.*, *.*, *.*) .. (*.*, *.*, *.*)
#   ->
# D65 linear sRGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
def xyz_to_lrgb(xyz: np.array) -> np.array:
    return np.dot(mx_xyz_to_lrgb, xyz)


# D50 CIE XYZ array (*.*, *.*, *.*) .. (*.*, *.*, *.*)
#   ->
# D50 CIE L*a*b* array (0.0, *.*, *.*) .. (100.0, *.*, *.*)
def xyz_to_lab(xyz: np.array) -> np.array:
    f0 = lambda t: np.power(29 / 3, 3) * t
    f1 = lambda t: 116 * np.power(t, 1 / 3) - 16
    f = lambda t: f0(t) if t <= np.power(6 / 29, 3) else f1(t)
    fx = f(xyz[0] / XYZn[0])
    fy = f(xyz[1] / XYZn[1])
    fz = f(xyz[2] / XYZn[2])
    l = fy
    a = (500 / 116) * (fx - fy)
    b = (200 / 116) * (fy - fz)
    lab = np.array([l, a, b])
    return lab

# D50 CIE L*a*b* array (0.0, *.*, *.*) .. (100.0, *.*, *.*)
#   ->
# D50 CIE XYZ array (*.*, *.*, *.*) .. (*.*, *.*, *.*)
def lab_to_xyz(lab: np.array) -> np.array:
    fy = (lab[0] + 16) / 116
    fx = fy + (lab[1] / 500)
    fz = fy - (lab[2] / 200)
    fxyz = [fx, fy, fz]
    f0 = lambda t, n: np.power(t, 3) * n
    f1 = lambda t, n: np.power(3 / 29, 3) * (116 * t - 16) * n
    f = lambda t, n: f0(t, n) if t > 6 / 29 else f1(t, n)
    xyz = np.array([f(fxyz[i], XYZn[i]) for i in range(3)])
    return xyz


# D50 CIE L*a*b* array (0.0, *.*, *.*) .. (100.0, *.*, *.*)
#   ->
# D50 CIE L*C*h array (0.0, 0.0, 0.0) .. (100.0, *.*, 360.0)
def lab_to_lch(lab: np.array) -> np.array:
    l, a, b = lab
    c = np.sqrt(a*a + b*b)
    h = np.arctan2(b, a) * 180 / np.pi
    lch = np.array((l, c, h))
    return lch

# D50 CIE L*C*h array (0.0, 0.0, 0.0) .. (100.0, *.*, 360.0)
#   ->
# D50 CIE L*a*b* array (0.0, *.*, *.*) .. (100.0, *.*, *.*)
def lch_to_lab(lch: np.array) -> np.array:
    l, c, h = lch
    rad = h / 180 * np.pi
    a = c * np.cos(rad)
    b = c * np.sin(rad)
    lab = np.array((l, a, b))
    return lab


# RGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
#   ->
# HSL array (0.0, 0.0, 0.0) .. (360.0, 1.0, 1.0)
def rgb01_to_hsl(rgb: np.array) -> np.array:
    r, g, b = rgb
    lmin = min(r, g, b)
    lmax = max(r, g, b)
    if lmax == lmin:
        h = 0
    elif lmin == b:
        h = 60 + 60 * (g - r) / (lmax - lmin)
    elif lmin == r:
        h = 180 + 60 * (b - g) / (lmax - lmin)
    elif lmin == g:
        h = 300 + 60 * (r - b) / (lmax - lmin)
    else:
        h = 0
    s = lmax - lmin
    l = (lmax + lmin) / 2
    hsl = np.array((h, s, l))
    return hsl

# HSL array (0.0, 0.0, 0.0) .. (360.0, 1.0, 1.0)
#   ->
# RGB array (0.0, 0.0, 0.0) .. (1.0, 1.0, 1.0)
def hsl_to_rgb01(hsl: np.array) -> np.array:
    h, s, l = hsl
    lmin = l - s / 2
    lmax = l + s / 2
    ldif = lmax - lmin
    if h < 60:
        r, g, b = lmax, lmin + ldif * (0 + h) / 60, lmin
    elif h < 120:
        r, g, b = lmin + ldif * (120 - h) / 60, lmax, lmin
    elif h < 180:
        r, g, b = lmin, lmax, lmin + ldif * (h - 120) / 60
    elif h < 240:
        r, g, b = lmin, lmin + ldif * (240 - h) / 60, lmax
    elif h < 300:
        r, g, b = lmin + ldif * (h - 240) / 60, lmin, lmax
    else:
        r, g, b = lmax, lmin, lmin + ldif * (360 - h) / 60
    rgb = np.array((r, g, b))
    return rgb



rgb255_to_hsl = composite_2f(rgb255_to_rgb01, rgb01_to_hsl)
hsl_to_rgb255 = composite_2f(hsl_to_rgb01, rgb01_to_rgb255)

rgbhex_to_hsl = composite_2f(rgbhex_to_rgb255, rgb255_to_hsl)
hsl_to_rgbhex = composite_2f(hsl_to_rgb255, rgb255_to_rgbhex)

rgb01_to_lab = composite_3f(srgb_to_lrgb, lrgb_to_xyz, xyz_to_lab)
lab_to_rgb01 = composite_3f(lab_to_xyz, xyz_to_lrgb, lrgb_to_srgb)

rgbhex_to_rgb01 = composite_2f(rgbhex_to_rgb255, rgb255_to_rgb01)
rgb01_to_rgbhex = composite_2f(rgb01_to_rgb255, rgb255_to_rgbhex)

rgbhex_to_lab = composite_2f(rgbhex_to_rgb01, rgb01_to_lab)
lab_to_rgbhex = composite_2f(lab_to_rgb01, rgb01_to_rgbhex)

rgbhex_to_lch = composite_2f(rgbhex_to_lab, lab_to_lch)
lch_to_rgbhex = composite_2f(lch_to_lab, lab_to_rgbhex)

rgb255_to_lab = composite_2f(rgb255_to_rgb01, rgb01_to_lab)
lab_to_rgb255 = composite_2f(lab_to_rgb01, rgb01_to_rgb255)

rgb255_to_lch = composite_2f(rgb255_to_lab, lab_to_lch)
lch_to_rgb255 = composite_2f(lch_to_lab, lab_to_rgb255)

rgb01_to_lch = composite_2f(rgb01_to_lab, lab_to_lch)
lch_to_rgb01 = composite_2f(lch_to_lab, lab_to_rgb01)

