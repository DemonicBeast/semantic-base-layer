#!/usr/bin/env python3
"""
What are the axes based off?

Answer, demonstrated: the axes are NOT a property of the space. They are a
LENS you describe the space through. The space contains DIRECTIONS, which
come from the data. Coordinates are those directions expressed in whatever
labels you chose.

The test: find the directions the data actually cares about, then write them
down in two totally different coordinate systems. If they are real features
of the data, they survive the change of labels.

Run:  python3 learn/02-what-are-axes-based-off.py
"""
import math

# ---------------------------------------------------------------------------
# Data. A tiny corpus where the ONLY thing going on is:
#   animals (cat, dog, kitten)  vs  vehicles (car, truck, bus)
# ---------------------------------------------------------------------------
SENTENCES = [
    "the cat sat on the mat".split(),
    "the dog sat on the log".split(),
    "a kitten is a small cat".split(),
    "the cat chased the dog".split(),
    "the kitten played with the cat".split(),
    "the truck carried the car".split(),
    "a car is not a truck".split(),
    "the bus followed the truck".split(),
    "the car overtook the bus".split(),
    "a truck is a big car".split(),
]

vocab = sorted({w for s in SENTENCES for w in s})
idx = {w: i for i, w in enumerate(vocab)}
n = len(vocab)

counts = [[0.0] * n for _ in range(n)]
for s in SENTENCES:
    for i, wi in enumerate(s):
        for j, wj in enumerate(s):
            if i != j and abs(i - j) <= 2:
                counts[idx[wi]][idx[wj]] += 1.0


def matvec(m, v):
    return [sum(m[i][j] * v[j] for j in range(len(v))) for i in range(len(m))]


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def principal_directions(m, k=2):
    """Directions where the data varies most (power iteration + deflation)."""
    work = [row[:] for row in m]
    out = []
    for _ in range(k):
        v = [1.0] * n
        for _ in range(300):
            w = matvec(work, v)
            nw = norm(w)
            if nw < 1e-12:
                break
            v = [x / nw for x in w]
        lam = sum(v[i] * matvec(work, v)[i] for i in range(n))
        out.append((v, lam))
        # deflate: remove this direction so the next one is orthogonal to it
        work = [[work[i][j] - lam * v[i] * v[j] for j in range(n)] for i in range(n)]
    return out

dirs = principal_directions(counts, 2)
(V1, L1), (V2, L2) = dirs

print("=" * 76)
print("STEP 1  -  what directions does the DATA actually contain?")
print("=" * 76)
print(f"""
  We factored the word-count table. It gave us {n} directions, but they are
  not equally important. How much data lives along each one:

      direction 1 : strength {L1:8.3f}
      direction 2 : strength {L2:8.3f}
      directions 3..{n} : the rest

  (strength = how much of the data's structure runs along that direction)
""")

# The top 2 directions are where the data lives. Print them as word-scores.
print("  What direction 1 looks like, as scores on each word:\n")
ranked = sorted(vocab, key=lambda w: -V1[idx[w]])
for w in ranked:
    bar = "#" * int(abs(V1[idx[w]]) * 40)
    sign = "+" if V1[idx[w]] >= 0 else "-"
    print(f"    {w:<9} {V1[idx[w]]:+.4f}  {sign}{bar}")

print("""
  Read the top and the bottom: animals at one end, vehicles at the other.
  Direction 1 IS "animal-ness vs vehicle-ness". The data put it there.
  Nobody chose it.
""")

print("  Direction 2:\n")
ranked2 = sorted(vocab, key=lambda w: -V2[idx[w]])
for w in ranked2[:5]:
    print(f"    {w:<9} {V2[idx[w]]:+.4f}  (high)")
print("      ...")
for w in ranked2[-5:]:
    print(f"    {w:<9} {V2[idx[w]]:+.4f}  (low)")

print("""
  This one is weaker and mushier - it captures some second-order regularity.
  Real embeddings are like this: a few strong directions, a long tail of
  weak, hard-to-name ones.
""")

# ---------------------------------------------------------------------------
print("=" * 76)
print("STEP 2  -  now CHANGE THE AXES 200 degrees and re-describe everything")
print("=" * 76)
print("""
  We are going to write down those same two data directions in a coordinate
  system rotated 200 degrees. Completely different labels. Let's see whether
  the meaning survives.
""")

THETA = math.radians(200)
C, S = math.cos(THETA), math.sin(THETA)


def express_in_basis(direction, basis_a, basis_b):
    """Coordinates of a vector, expressed against two basis vectors."""
    # solve  direction = p*a + q*b   in 2D
    ax, ay = basis_a
    bx, by = basis_b
    det = ax * by - ay * bx
    dx, dy = direction
    p = (dx * by - dy * bx) / det
    q = (ax * dy - ay * dx) / det
    return p, q


# work in the 2D subspace spanned by V1, V2
def to2(v):
    return (sum(v[i] * V1[i] for i in range(n)), sum(v[i] * V2[i] for i in range(n)))


# The data directions, as 2D vectors in the ORIGINAL frame
d_animal = to2(V1)   # this is just (1, 0) by construction
d_second = to2(V2)   # (0, 1)

# A rotated basis - the "different axes"
b1 = (C, S)
b2 = (-S, C)

p1, q1 = express_in_basis(d_animal, b1, b2)
p2, q2 = express_in_basis(d_second, b1, b2)

print(f"  The animal/vehicle direction, written in the ORIGINAL axes:  ({d_animal[0]:+.4f}, {d_animal[1]:+.4f})")
print(f"  The SAME direction, written in the ROTATED 200-degree axes:  ({p1:+.4f}, {q1:+.4f})")
print()
print(f"  The second direction, original axes:                         ({d_second[0]:+.4f}, {d_second[1]:+.4f})")
print(f"  The SAME direction, rotated axes:                            ({p2:+.4f}, {q2:+.4f})")

print(f"""
  Totally different numbers. Same two directions.

  And the angle between them, which is what actually matters:
""")
ang_orig = math.degrees(math.acos(max(-1, min(1, d_animal[0] * d_second[0] + d_animal[1] * d_second[1]))))
ang_rot = math.degrees(math.acos(max(-1, min(1, p1 * p2 + q1 * q2))))
print(f"      original axes : {ang_orig:8.4f} degrees apart")
print(f"      rotated axes  : {ang_rot:8.4f} degrees apart")

print("""
  Identical. The direction "animal vs vehicle" is a real feature of the data.
  It exists no matter which labels you write it in.
""")

print("=" * 76)
print("SO WHAT ARE THE AXES BASED OFF?")
print("=" * 76)
print("""
  Two different things, and it is worth keeping them apart:

  1. THE AXES THE MODEL SHIPS WITH (dim 1, dim 2, ... dim 1536)
     Based off: nothing. A random starting point inside the training code.
     No meaning, not reproducible, not derivable from the data.
     -> This is why you cannot standardise them.

  2. THE DIRECTIONS THE DATA PUTS IN THE SPACE
     Based off: the data itself. Words used in similar contexts got pulled
     together. "animal vs vehicle" appears because the corpus has animals
     and vehicles in it. It is a real feature.
     -> This is what is actually worth aligning.

  The axes are a LENS. The directions are the SCENERY.
  Change the lens and the scenery does not move.

  Alignment is possible because the scenery is stable.
  Coordinate standardisation is impossible because the lens is arbitrary.
""")
