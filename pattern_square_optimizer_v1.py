"""
pattern_square_optimizer_v1.py

Compute the largest square block size S for a lamination pattern,
given:
- pattern [(material, size_tag), ...]
- relative width units per tag (thin/thick)
- usable board widths per material
- surfaced thickness T_surfaced for the lamination
- saw kerf
- glue-up oversize G (added to lamination width, not thickness)
"""

from collections import defaultdict

# ---------- USER INPUT ----------

PATTERN = [
    ("Walnut", "thin"),
    ("Maple",  "thick"),
    ("Red",    "thin"),
    ("Beech",  "thick"),
    ("Walnut", "thin"),
]

WIDTH_UNITS = {
    "thin": 1.0,
    "thick": 2.0,
}

BOARD_WIDTH = {
    "Walnut": 4.75,
    "Maple":  6.00,
    "Beech":  6.00,
    "Red":    4.50,
}

# lamination square size must be <= this thickness
T_SURFACED = 2.00   # e.g. you know you can get 2.0" from your stack

KERF   = 0.052      # in inches
G      = 0.25       # lamination oversize for glue-up (inches)
SAFETY = 0.95

# ---------- COMPUTATION ----------

# units and occurrences per material
units_per_mat = defaultdict(float)
occ_per_mat   = defaultdict(int)
units_total   = 0.0

for mat, tag in PATTERN:
    u = WIDTH_UNITS[tag]
    units_per_mat[mat] += u
    units_total        += u
    occ_per_mat[mat]   += 1

# per-material limit on S from board WIDTH (with kerf & oversize)
S_limits = []

for mat, units_i in units_per_mat.items():
    f_i = units_i / units_total          # fraction of lamination width
    occ_i = occ_per_mat[mat]
    W_i = BOARD_WIDTH[mat]

    numerator   = W_i - f_i * G - (occ_i - 1) * KERF
    S_max_i     = numerator / f_i
    S_limits.append(S_max_i)

# thickness limit (square requirement)
S_limits.append(T_SURFACED)

S_raw = min(S_limits)
S     = S_raw * SAFETY

# final + cut strip widths
final_segments = []
cut_segments   = []
for mat, tag in PATTERN:
    u = WIDTH_UNITS[tag]
    frac = u / units_total
    w_final = frac * S
    w_cut   = frac * (S + G)
    final_segments.append((mat, tag, round(w_final, 3)))
    cut_segments.append((mat, tag, round(w_cut, 3)))

# ---------- OUTPUT ----------

print("=== Square Lamination Optimizer ===\n")
print(f"T_surfaced (thickness limit): {T_SURFACED:.3f} in")
print(f"Kerf: {KERF:.3f} in, Glue oversize G: {G:.3f} in")
print(f"Safety factor: {SAFETY*100:.0f}%\n")

print(f"Max theoretical square size S_raw: {S_raw:.3f} in")
print(f"Chosen S (after safety):           {S:.3f} in\n")

print("Final strip widths (planed to S overall):")
for mat, tag, w in final_segments:
    print(f"  {mat:6s} {tag:5s} -> {w:.3f} in")

print("\nInitial cut widths for glue-up (sum to S + G):")
for mat, tag, w in cut_segments:
    print(f"  {mat:6s} {tag:5s} -> {w:.3f} in")
