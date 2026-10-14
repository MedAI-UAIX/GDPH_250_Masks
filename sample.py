#!/usr/bin/env python3
"""One-pass pipeline: original-name images -> rename -> sample.

Steps:
1. Rename images in E:\\BUSEye\\label\\GDPH
      benign(N).png     -> GDPH_0N00_B.png
      malignant(N).png  -> GDPH_0N00_M.png
   and copy them to renamed_pool.
2. Sample with the same logic as sample_images.py (seed=42, draw 125 primary
   images per class; candidates with pHash similarity >= 0.75 to an accepted
   image, or serial number within 1 of an accepted one, are rejected and
   replaced from the remaining pool), and copy the result to
   sampled_from_original.
"""
import random
import re
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

SRC_DIR = Path(r'E:/BUSEye/label/GDPH')
WORK_DIR = Path(r'E:/BUSEye/label/GDPH_250_mask/GDPH_250_mask/renamed_pool')
DST_DIR = Path(r'E:/BUSEye/label/GDPH_250_mask/GDPH_250_mask/sampled_from_original')

SEED = 42
PER_CLASS = 125          # 250 total, 125 benign + 125 malignant
SIM_THRESHOLD = 0.75     # reject candidates with similarity >= 0.75 to an accepted image
SERIAL_GAP = 1           # reject serial numbers within 1 of an accepted one

HASH_SIZE = 8            # pHash: 8x8 low-frequency DCT = 64 bits


# ---------- Step 1: rename ----------

def rename_rule(name):
    """benign(446).png -> GDPH_0446_B.png; malignant(1332).png -> GDPH_1332_M.png"""
    m = re.match(r'(benign|malignant)\((\d+)\)\.png', name)
    if not m:
        return None
    cls = 'B' if m.group(1) == 'benign' else 'M'
    return f'GDPH_{int(m.group(2)):04d}_{cls}.png'


def step_rename():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in sorted(SRC_DIR.glob('*.png')):
        new_name = rename_rule(p.name)
        if new_name:
            shutil.copy2(p, WORK_DIR / new_name)
            n += 1
    print(f'[rename] {n} images -> {WORK_DIR}')


# ---------- Step 2: sample ----------

def phash(img_path):
    """64-bit perceptual hash (DCT low frequencies)"""
    size = HASH_SIZE * 4
    with Image.open(img_path) as im:
        im = im.convert('L').resize((size, size), Image.LANCZOS)
        pixels = np.asarray(im, dtype=np.float32)
    import cv2
    dct = cv2.dct(pixels)[:HASH_SIZE, :HASH_SIZE].flatten()
    med = np.median(dct[1:])
    v = 0
    for bit in dct > med:
        v = (v << 1) | int(bit)
    return v


def sim(a, b):
    return 1.0 - bin(a ^ b).count('1') / (HASH_SIZE ** 2)


def serial(path):
    m = re.search(r'GDPH_(\d+)_', path.name)
    return int(m.group(1)) if m else None


def sample_class(pool, primary):
    """Accept in primary order; rejected slots are filled from the remaining pool."""
    rest = [p for p in pool if p not in set(primary)]
    order = list(primary) + random.sample(rest, len(rest))
    accepted, acc_hash, acc_serial = [], [], []
    for img in order:
        if len(accepted) >= PER_CLASS:
            break
        num = serial(img)
        if num is not None and any(abs(num - s) <= SERIAL_GAP for s in acc_serial):
            continue
        h = phash(img)
        if any(sim(h, ah) >= SIM_THRESHOLD for ah in acc_hash):
            continue
        accepted.append(img)
        acc_hash.append(h)
        if num is not None:
            acc_serial.append(num)
    return accepted


def step_sample():
    benign = sorted(p for p in WORK_DIR.iterdir() if p.stem.endswith('_B'))
    malignant = sorted(p for p in WORK_DIR.iterdir() if p.stem.endswith('_M'))
    random.seed(SEED)
    primary_b = random.sample(benign, PER_CLASS)
    primary_m = random.sample(malignant, PER_CLASS)
    sampled = sample_class(benign, primary_b) + sample_class(malignant, primary_m)

    DST_DIR.mkdir(parents=True, exist_ok=True)
    for img in sampled:
        shutil.copy2(img, DST_DIR / img.name)
    print(f'[sample] {len(sampled)} images -> {DST_DIR}')


if __name__ == '__main__':
    step_rename()
    step_sample()
