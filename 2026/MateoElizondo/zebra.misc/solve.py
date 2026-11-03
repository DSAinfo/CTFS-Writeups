import base64
import subprocess, json, re
from PIL import Image, ImageOps
import cv2, numpy as np

# Este script requiere tener el directorio "output_pixels" que se consigue
# al descomprimir el zip en recursos "buncharandoms.zip"

# también tener la utility de exiftool instalada

dir = "output_pixels"
meta = json.loads(subprocess.check_output(
    ["exiftool", "-j", "-UserComment", "-Comment", dir]))

items = []
for m in meta:
    c = m.get("UserComment") or m.get("Comment") or ""
    digits = re.sub(r"\D", "", c)
    items.append((int(digits), m["SourceFile"], c))

idxs = [i for i, _, _ in items]

items.sort()
N = 29
bits = []
for _, f, _ in items:
    v = Image.open(f).convert("L").getpixel((5, 5))
    bits.append(1 if v < 128 else 0)   # negro = 1

grid = np.array(bits, dtype=np.uint8).reshape(N, N)
img = np.where(grid == 1, 0, 255).astype(np.uint8)
img = np.pad(img, 4, constant_values=255)
img = cv2.resize(img, None, fx=10, fy=10, interpolation=cv2.INTER_NEAREST)
cv2.imwrite(f"qr.png", img)

print(base64.b64decode(cv2.QRCodeDetector().detectAndDecode(img)[0]).decode('utf-8'))
