"""Copia y renombra las secuencias de _source/ a frames/<vehiculo>/<desktop|mobile>/NNN.webp
Uso: python3 tools/normalize_frames.py
Detecta el vehículo por el nombre de la carpeta (PESADOS/DISTRIBU/LIGEROS) y la variante por
'mobile' en la ruta. Solo toma .webp; ignora PNG y archivos sueltos."""
import os, re, shutil, struct, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(ROOT, '_source'), os.path.join(ROOT, 'frames')
def vehicle(path):
    p = path.upper()
    if 'PESAD' in p or 'CAMION' in p: return 'pesados'
    if 'DISTRIBU' in p or 'CAJA' in p: return 'distribucion'
    if 'LIGER' in p or 'SEDAN' in p: return 'ligeros'
def webp_info(fp):
    with open(fp, 'rb') as f: b = f.read(64)
    if b[:4] != b'RIFF' or b[8:12] != b'WEBP': return None
    if b[12:16] == b'VP8X':
        w = int.from_bytes(b[24:27], 'little') + 1; h = int.from_bytes(b[27:30], 'little') + 1
        return w, h, bool(b[20] & 0x10)
    return None, None, False
report = {}
for dirpath, _, files in os.walk(SRC):
    for fn in files:
        m = re.search(r'(\d{3})\.webp$', fn, re.I)
        if not m: continue
        v = vehicle(dirpath + '/' + fn); var = 'mobile' if 'MOBILE' in dirpath.upper() else 'desktop'
        if not v: print('?? sin vehículo:', dirpath, fn); continue
        out = os.path.join(DST, v, var); os.makedirs(out, exist_ok=True)
        src = os.path.join(dirpath, fn); dst = os.path.join(out, m.group(1) + '.webp')
        shutil.copy2(src, dst)
        w, h, a = webp_info(dst) or (None, None, False)
        r = report.setdefault(f'{v}/{var}', {'count': 0, 'bytes': 0, 'sizes': set(), 'alpha': set()})
        r['count'] += 1; r['bytes'] += os.path.getsize(dst); r['sizes'].add(f'{w}x{h}'); r['alpha'].add(a)
for k, r in sorted(report.items()):
    idx = sorted(int(f[:3]) for f in os.listdir(os.path.join(DST, *k.split('/'))))
    missing = sorted(set(range(90)) - set(idx))
    print(f"{k:24} {r['count']:3} frames  {r['bytes']/1e6:5.2f} MB  {sorted(r['sizes'])}  alpha={sorted(r['alpha'])}  faltan={missing or 'ninguno'}")
