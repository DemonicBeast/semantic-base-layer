#!/usr/bin/env python3
"""
Demonstrate WHY embedding spaces cannot be standardised by picking coordinates.

Two experiments, both pure standard library:

  A. Rotation invariance - rotating a whole space changes every coordinate
     while changing nothing about the meaning encoded in it.
  B. Basis ambiguity  - building an embedding from the SAME data can legitimately
     produce different coordinates for the same word.

Run:  python3 learn/01-why-not-coordinates.py
"""
import math

# ----------------------------------------------------------------------------
# A tiny "embedding": 5 words, 2 dimensions. In 2D so it can be printed.
# Pretend a model was trained and produced these.
# ----------------------------------------------------------------------------
WORDS = ["cat", "dog", "kitten", "car", "truck"]
VECTORS = {
    "cat":    (2.0,  0.0),
    "dog":    (1.8,  0.9),
    "kitten": (1.2,  1.4),
    "car":    (-1.5, 1.6),
    "truck":  (-2.0, 0.7),
}


def rotate(v, degrees):
    """Rotate a 2D vector counter-clockwise."""
    t = math.radians(degrees)
    c, s = math.cos(t), math.sin(t)
    x, y = v
    return (x * c - y * s, x * s + y * c)


def cosine(a, b):
    dot = sum(p * q for p, q in zip(a, b))
    na = math.sqrt(sum(p * p for p in a))
    nb = math.sqrt(sum(q * q for q in b))
    return dot / (na * nb)


def show_space(label, space):
    print(f"\n  {label}")
    for w in WORDS:
        x, y = space[w]
        print(f"    {w:<7} [{x:+.3f}, {y:+.3f}]")


print("=" * 74)
print("A.  ROTATION INVARIANCE")
print("=" * 74)
print("""
  Take a trained embedding space and rotate the ENTIRE space by 90 degrees.
  Every coordinate changes. Now compare what the space actually encodes.
""")

original = VECTORS
rotated = {w: rotate(v, 90) for w, v in VECTORS.items()}

show_space("ORIGINAL  (model as trained)", original)
show_space("ROTATED 90 degrees  (a different set of numbers)", rotated)

print("\n  Similarity between words - the thing the space is FOR:\n")
print(f"    {'pair':<16} {'original':>10} {'rotated':>10}   {'same?':>6}")
print("    " + "-" * 46)
for i, a in enumerate(WORDS):
    for b in WORDS[i + 1:]:
        co = cosine(original[a], original[b])
        cr = cosine(rotated[a], rotated[b])
        same = "yes" if abs(co - cr) < 1e-12 else "NO"
        print(f"    {a + ' / ' + b:<16} {co:>10.6f} {cr:>10.6f}   {same:>6}")

print("""
  Every similarity is IDENTICAL. The rotated space means exactly the same
  thing. It is just written in different numbers.

  So: which one is "the correct coordinates" for the word cat?
  Neither. Both. The question has no answer.
""")

# ----------------------------------------------------------------------------
print("=" * 74)
print("B.  BASIS AMBIGUITY - different runs, same data, different coordinates")
print("=" * 74)
print("""
  Now build an embedding from scratch, twice, from the SAME word counts.
  A standard way to build one: count which words appear near each other,
  then factor that table to get dense vectors.

  The factoring step involves choosing directions, and those choices can
  legitimately come out sign-flipped. Let's see what that does.
""")

# --- build a co-occurrence style table from toy sentences -------------------
SENTENCES = [
    "the cat sat on the mat".split(),
    "the dog sat on the log".split(),
    "the cat chased the dog".split(),
    "a kitten is a small cat".split(),
    "the truck carried the car".split(),
    "a car is not a truck".split(),
]
vocab = sorted({w for s in SENTENCES for w in s})
idx = {w: i for i, w in enumerate(vocab)}
n = len(vocab)

# counts[i][j] = how often word j appears within 2 positions of word i
counts = [[0.0] * n for _ in range(n)]
for s in SENTENCES:
    for i, wi in enumerate(s):
        for j, wj in enumerate(s):
            if i != j and abs(i - j) <= 2:
                counts[idx[wi]][idx[wj]] += 1.0


def power_iteration(mat, iters=200):
    """Largest eigenvector of a symmetric matrix -> one principal direction."""
    v = [1.0] * len(mat)
    for _ in range(iters):
        w = [sum(mat[i][j] * v[j] for j in range(len(mat))) for i in range(len(mat))]
        norm = math.sqrt(sum(x * x for x in w))
        if norm == 0:
            return [0.0] * len(mat)
        v = [x / norm for x in w]
    return v


def deflate(mat, v, lam):
    return [[mat[i][j] - lam * v[i] * v[j] for j in range(len(mat))]
            for i in range(len(mat))]


# two principal directions of the co-occurrence matrix
m = [row[:] for row in counts]
v1 = power_iteration(m)
lam1 = sum(v1[i] * sum(m[i][j] * v1[j] for j in range(n)) for i in range(n))
m2 = deflate(m, v1, lam1)
v2 = power_iteration(m2)

# SIGN FLIP: a perfectly valid alternative answer. -v is as good as +v.
v1b = [-x for x in v1]
v2b = [-x for x in v2]

emb_a = {w: (v1[idx[w]], v2[idx[w]]) for w in vocab}
emb_b = {w: (v1b[idx[w]], v2b[idx[w]]) for w in vocab}

print(f"  {'word':<9} {'run 1  [d1, d2]':>24} {'run 2  [d1, d2]':>24}")
print("  " + "-" * 60)
for w in vocab:
    a1, a2 = emb_a[w]
    b1, b2 = emb_b[w]
    print(f"  {w:<9} {a1:>+11.4f} {a2:>+11.4f} {b1:>+11.4f} {b2:>+11.4f}")

print("\n  Now compare what each run says about which words are similar:\n")
pairs = [("cat", "kitten"), ("cat", "dog"), ("cat", "truck"),
         ("car", "truck"), ("dog", "truck")]
print(f"    {'pair':<18} {'run 1':>10} {'run 2':>10}   {'same?':>6}")
print("    " + "-" * 48)
for a, b in pairs:
    ca = cosine(emb_a[a], emb_a[b])
    cb = cosine(emb_b[a], emb_b[b])
    same = "yes" if abs(ca - cb) < 1e-12 else "NO"
    print(f"    {a + ' / ' + b:<18} {ca:>10.6f} {cb:>10.6f}   {same:>6}")

print("""
  Same data. Same method. Same conclusions about meaning.
  Completely different coordinate values.

  Note run 2 is just run 1 flipped - and you cannot tell which is "right",
  because both are. This is the ambiguity. It is not a bug and no amount of
  engineering removes it.
""")

print("=" * 74)
print("WHAT THIS MEANS")
print("=" * 74)
print("""
  1. Embedding coordinates are not transferable facts. They are a choice of
     axes - like deciding which way is "north" on a blank sheet of paper.

  2. What IS stable is the geometry: how words sit relative to each other.
     That is what alignment methods actually try to match.

  3. So "standardise the coordinates" has no solution. "Make two spaces
     agree on their geometry" does - that is the alignment problem, and it
     is what the next script demonstrates.
""")
