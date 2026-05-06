"""Gera uma textura de areia deserto 512x512 sem dependências externas."""
import zlib, struct, random

SIZE = 512
OUT  = "models/tex/desert_sand.png"

random.seed(42)

# --- noise helpers ---------------------------------------------------------

def smooth(t):
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

_grid = [[random.random() for _ in range(SIZE + 1)] for _ in range(SIZE + 1)]

def value_noise(x, y, scale):
    fx = (x / scale) % (SIZE)
    fy = (y / scale) % (SIZE)
    ix, iy = int(fx), int(fy)
    tx, ty = fx - ix, fy - iy
    v00 = _grid[iy    % SIZE][ix    % SIZE]
    v10 = _grid[iy    % SIZE][(ix+1) % SIZE]
    v01 = _grid[(iy+1) % SIZE][ix    % SIZE]
    v11 = _grid[(iy+1) % SIZE][(ix+1) % SIZE]
    return lerp(lerp(v00, v10, smooth(tx)),
                lerp(v01, v11, smooth(tx)), smooth(ty))

# --- pixel generation ------------------------------------------------------

def get_pixel(x, y):
    # fractional brownian motion: 3 oitavas de noise
    n  = value_noise(x, y, 120) * 0.55
    n += value_noise(x, y,  60) * 0.30
    n += value_noise(x, y,  30) * 0.15

    # cor base areia quente: (210, 185, 130)
    r = int(min(255, 190 + n * 60))
    g = int(min(255, 165 + n * 48))
    b = int(min(255, 100 + n * 42))

    # marcas escuras ocasionais (pedrinhas)
    rock = value_noise(x * 3, y * 3, 40)
    if rock > 0.80:
        r = int(r * 0.72)
        g = int(g * 0.70)
        b = int(b * 0.65)

    return r, g, b

# --- PNG writer ------------------------------------------------------------

def write_png(path, w, h):
    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc)

    sig  = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))

    raw = bytearray()
    for y in range(h):
        raw.append(0)          # filter: None
        for x in range(w):
            r, g, b = get_pixel(x, y)
            raw += bytes([r, g, b])

    idat = chunk(b'IDAT', zlib.compress(bytes(raw), 6))
    iend = chunk(b'IEND', b'')

    with open(path, 'wb') as f:
        f.write(sig + ihdr + idat + iend)

# ---------------------------------------------------------------------------

print(f"Gerando {OUT} ({SIZE}x{SIZE})...")
write_png(OUT, SIZE, SIZE)
print("Pronto!")
