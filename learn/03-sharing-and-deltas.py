#!/usr/bin/env python3
"""
Lesson 03 - the sharing idea, with real numbers.

The chain being tested:
    axes are arbitrary
      -> vectors can't be shared
      -> every model stores its own table
      -> we store the same knowledge N times
    IF the basis were standard
      -> vectors shareable -> tables shared, not duplicated

We simulate two models that learned the SAME reality through different random
axes. Then:
  1. show the redundancy
  2. align B onto A (Procrustes)
  3. CHECK the alignment actually helped (never trust a matrix)
  4. measure the residual, and turn it into a storage number

Run:  python3 learn/03-sharing-and-deltas.py
"""
import math
import random

random.seed(7)
WORDS = ["cat", "dog", "kitten", "horse", "car", "truck", "bus", "bicycle", "rock", "chair"]

# ground truth: where each word really sits on 3 latent factors
TRUTH = {
    #          animal  size   moves
    "cat":     ( 1.0,  -0.3,   0.6),
    "dog":     ( 1.0,   0.1,   0.6),
    "kitten":  ( 1.0,  -0.7,   0.5),
    "horse":   ( 1.0,   0.8,   0.7),
    "car":     (-1.0,   0.6,   0.9),
    "truck":   (-1.0,   0.9,   0.8),
    "bus":     (-1.0,   0.8,   0.8),
    "bicycle": (-1.0,  -0.3,   0.9),
    "rock":    (-1.0,  -0.2,  -0.9),
    "chair":   (-1.0,   0.0,  -0.9),
}
D = 4  # numbers stored per word


# ---- tiny matrix helpers (no numpy in this environment) --------------------
def matmul(X, Y):
    n, k, m = len(X), len(Y), len(Y[0])
    return [[sum(X[i][t] * Y[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


def transpose(X):
    return [list(col) for col in zip(*X)]


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def scale_mat(X, s):
    return [[s * x for x in row] for row in X]


def sub(A, B):
    return [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def max_abs(X):
    return max(abs(x) for row in X for x in row)


def orthonormal_cols(n, k, rng):
    """k orthonormal vectors in n dimensions - Gram-Schmidt on random draws."""
    cols = []
    while len(cols) < k:
        v = [rng.gauss(0, 1) for _ in range(n)]
        for u in cols:
            dot = sum(a * b for a, b in zip(v, u))
            v = [a - dot * b for a, b in zip(v, u)]
        nv = math.sqrt(sum(x * x for x in v))
        if nv > 1e-6:
            cols.append([x / nv for x in v])
    return cols


def make_model(seed, noise, shared_axes, private_only=False):
    """A model projects the 3 true factors into D dims using axes it chose itself.

    shared_axes: list of D basis vectors in R^3 defining the SHARED meaning
                 directions. If two models use the same vectors here (in a
                 different order or sign), a perfect rotation between them
                 exists. That is the premise the experiment tests.

    private_only=True gives the model its own random axes with no relation to
    any other model - the control case, where no alignment should be possible.
    """
    rng = random.Random(seed)
    if private_only:
        # 3 orthonormal axes in the 3-dim meaning space, then lift into D dims.
        # (Asking for D orthonormal vectors in 3 dimensions is impossible and
        #  loops forever - the subspace is only 3-dimensional.)
        base = orthonormal_cols(3, 3, rng)
        axes = [base[i] + [0.0] * (D - 3) for i in range(3)] + [[0.0] * D]
    else:
        axes = shared_axes
    out = {}
    for w, t in TRUTH.items():
        v = [sum(t[j] * axes[i][j] for j in range(3)) for i in range(D)]
        out[w] = [x + rng.gauss(0, noise) for x in v]
    return out


# The shared reality: axes defined in the 3-dimensional meaning space, then
# lifted into D dims by zero-padding. Asking for D orthonormal vectors in a
# 3-dimensional space is impossible - it loops forever, which is why this is
# 3 axes padded to D rather than D axes drawn from R^3.
_base = orthonormal_cols(3, 3, random.Random(99))
TRUTH_AXES = [_base[i] + [0.0] * (D - 3) for i in range(3)] + [[0.0] * D]


def cos(u, v):
    d = sum(a * b for a, b in zip(u, v))
    nu = math.sqrt(sum(a * a for a in u))
    nv = math.sqrt(sum(b * b for b in v))
    return d / (nu * nv) if nu and nv else 0.0


# Model A uses the shared axes directly.
# Model B uses a ROTATED MIX of the same axes - so the two models describe the
# same reality, in different (arbitrary) coordinate systems.
def mix_axes(axes, seed):
    rng = random.Random(seed)
    M = [[rng.gauss(0, 1) for _ in range(D)] for _ in range(D)]
    Q = []
    for c in range(D):
        v = [M[i][c] for i in range(D)]
        for u in Q:
            d = sum(a * b for a, b in zip(v, u))
            v = [a - d * b for a, b in zip(v, u)]
        nv = math.sqrt(sum(x * x for x in v))
        Q.append([x / nv for x in v])
    # new axis i = sum_j Q[j][i] * axes[j]   (a rotation of the same span)
    return [[sum(Q[j][i] * axes[j][k] for j in range(D)) for k in range(3)] for i in range(D)]


model_A = make_model(1, 0.03, TRUTH_AXES)
model_B = make_model(2, 0.03, mix_axes(TRUTH_AXES, 5))
A = [model_A[w] for w in WORDS]
B = [model_B[w] for w in WORDS]

print("=" * 78)
print("THE SITUATION")
print("=" * 78)
print(f"""
  Two models, same {len(WORDS)} words, {D} numbers each, same underlying reality.
  Different random axes ("based off nothing"). Small training noise.
""")
print(f"  {'word':<9} {'model A':<32} {'model B'}")
print("  " + "-" * 72)
for w in WORDS[:4]:
    a = " ".join(f"{x:+.3f}" for x in model_A[w])
    b = " ".join(f"{x:+.3f}" for x in model_B[w])
    print(f"  {w:<9} {a:<32} {b}")
print("  ...")
print(f"""
  The numbers are unrelated. Yet both models know cat is an animal and a truck
  is not.

  Storage: 2 x {len(WORDS)} x {D} = {2*len(WORDS)*D} numbers stored,
  of which only {len(WORDS)*D} numbers carry shared information.
""")

def svd_one_sided(M, iters=60):
    """SVD of M (r x d) by one-sided Jacobi rotations.

    Rotates PAIRS OF COLUMNS of M until they are mutually orthogonal; at that
    point the column norms are the singular values and the accumulated
    rotations are the right singular vectors V. U is then recovered directly.

    One-sided Jacobi is used because it is self-verifying: after convergence we
    can check that the columns of U*S are orthogonal. The two-sided
    eigendecomposition tried earlier produced V that was not orthonormal
    (V^T V off by 1.98), which silently corrupted every result downstream.

    Returns U (r x k), S (length k), V (d x k) with M = U diag(S) V^T.
    """
    r, d = len(M), len(M[0])
    U = [row[:] for row in M]
    V = identity(d)
    for _ in range(iters):
        off = 0.0
        for p in range(d):
            for q in range(p + 1, d):
                alpha = sum(U[i][p] * U[i][p] for i in range(r))
                beta  = sum(U[i][q] * U[i][q] for i in range(r))
                gamma = sum(U[i][p] * U[i][q] for i in range(r))
                if abs(gamma) < 1e-15 * math.sqrt(alpha * beta + 1e-300):
                    continue
                off = max(off, abs(gamma) / math.sqrt(alpha * beta + 1e-300))
                zeta = (beta - alpha) / (2.0 * gamma)
                t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                sn = c * t
                for i in range(r):
                    up, uq = U[i][p], U[i][q]
                    U[i][p] = c * up - sn * uq
                    U[i][q] = sn * up + c * uq
                for i in range(d):
                    vp, vq = V[i][p], V[i][q]
                    V[i][p] = c * vp - sn * vq
                    V[i][q] = sn * vp + c * vq
        if off < 1e-14:
            break
    # singular values = column norms; drop negligible ones
    norms = [math.sqrt(sum(U[i][j] ** 2 for i in range(r))) for j in range(d)]
    keep = [j for j in range(d) if norms[j] > 1e-12]
    S = [norms[j] for j in keep]
    Uc = [[U[i][j] / norms[j] for j in keep] for i in range(r)]
    Vc = [[V[i][j] for j in keep] for i in range(d)]
    return Uc, S, Vc


def orthogonal_procrustes(A, B):
    """Orthogonal W minimising ||A W - B||.

    Kabsch: with the cross-covariance C = A^T B = U S V^T, the optimum is

        W = U V^T

    Verified numerically on a rotation whose answer is known by hand:
        U V^T = [[+0.764842, -0.644218], [+0.644218, +0.764842]]  = the truth
        V U^T = the transpose of it                                = wrong
    (V U^T was tried and is wrong. The two differ only by a transpose, which
    is easy to mistake for a working answer when the true rotation happens to
    be near-symmetric.)
    """
    C = matmul(transpose(A), B)
    U, S, V = svd_one_sided(C)
    W = matmul(U, transpose(V))
    # reflection guard: a rotation has det = +1; if the SVD handed us a mirror,
    # flip the last singular direction of U and rebuild.
    if det(W) < 0:
        k = len(S)
        U = [[U[i][j] * (-1.0 if j == k - 1 else 1.0) for j in range(k)] for i in range(len(U))]
        W = matmul(U, transpose(V))
    return W


def det(X):
    n = len(X)
    if n == 1:
        return X[0][0]
    if n == 2:
        return X[0][0] * X[1][1] - X[0][1] * X[1][0]
    total = 0.0
    for j in range(n):
        minor = [[X[i][k] for k in range(n) if k != j] for i in range(1, n)]
        total += ((-1) ** j) * X[0][j] * det(minor)
    return total


# ---- self-test: does the machinery work on a case whose answer we know? ----
def _selftest():
    """A known rotation must be recovered exactly."""
    ang = 0.7
    Rtrue = [[math.cos(ang), -math.sin(ang)],
             [math.sin(ang), math.cos(ang)]]
    P = [[1.0, 2.0], [3.0, -1.0], [0.5, 4.0]]     # arbitrary points
    Q = matmul(P, Rtrue)                          # P rotated by Rtrue
    # verify the SVD first, independently of Procrustes
    C = matmul(transpose(P), Q)
    Uc, Sv, Vc = svd_one_sided(C)
    recon = matmul([[Uc[i][j] * Sv[j] for j in range(len(Sv))] for i in range(len(Uc))],
                   transpose(Vc))
    svd_err = max_abs(sub(recon, C))
    W = orthogonal_procrustes(P, Q)
    err = max_abs(sub(W, Rtrue))
    print(f"\n  Self-test part 1: SVD reconstruction error {svd_err:.2e}")
    print(f"  ({'PASS' if svd_err < 1e-9 else 'FAIL'} - M = U diag(S) V^T)")
    return err


err = _selftest()
print(f"\n  Self-test: recovering a known 2D rotation -> max error {err:.2e}")
print(f"  ({'PASS - the alignment machinery is correct' if err < 1e-8 else 'FAIL - machinery is broken'})")
if err >= 1e-8:
    raise SystemExit("refusing to report numbers from broken machinery")

# ---------------------------------------------------------------------------
print("=" * 78)
print("ALIGNING B ONTO A  (Procrustes)")
print("=" * 78)

W = orthogonal_procrustes(A, B)

# check W really is a rotation: W^T W should be the identity, det should be +1
WtW = matmul(transpose(W), W)
off = max(abs(WtW[i][j] - (1.0 if i == j else 0.0)) for i in range(D) for j in range(D))
dW = det(W)
print(f"\n  Orthogonality check: max deviation of W^T W from identity = {off:.2e}")
print(f"  Determinant of W = {dW:+.6f}  (a rotation has det = +1)")
ok = off < 1e-8 and abs(dW - 1.0) < 1e-6
print(f"  ({'PASS - W is a valid rotation' if ok else 'FAIL - W is not a valid rotation'})")

aligned = matmul(B, W)

print(f"""
  Now verify it helped - compare how well B matches A, before vs after.
  A real rotation must make matching words MORE similar than random pairs.
""")
before = [cos(A[r], B[r]) for r in range(len(WORDS))]
after = [cos(A[r], aligned[r]) for r in range(len(WORDS))]
random_pairs = [cos(A[i], B[(i + 3) % len(WORDS)]) for i in range(len(WORDS))]

mb, ma, mr = sum(before) / len(before), sum(after) / len(after), sum(random_pairs) / len(random_pairs)
print(f"    matching words, BEFORE alignment : {mb:+.4f}")
print(f"    matching words, AFTER  alignment : {ma:+.4f}")
print(f"    mismatched words (control)       : {mr:+.4f}")
verdict = "PASS - alignment worked" if (ma > mb and ma > mr) else "FAIL - alignment did not help"
print(f"    -> {verdict}")

# residual
def dist(u, v):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))

res = [dist(A[r], aligned[r]) for r in range(len(WORDS))]
avg_res = sum(res) / len(res)
avg_len = sum(math.sqrt(sum(x * x for x in A[r])) for r in range(len(WORDS))) / len(WORDS)

print(f"""
  Residual after alignment - how far each word still misses:
""")
print(f"  {'word':<9} {'residual':>10} {'length':>10} {'as %':>8}")
print("  " + "-" * 40)
for w, r in zip(WORDS, res):
    L = math.sqrt(sum(x * x for x in model_A[w]))
    print(f"  {w:<9} {r:>10.4f} {L:>10.4f} {100*r/L:>7.1f}%")
print(f"""
  average residual {avg_res:.4f} against average length {avg_len:.4f}
  -> {100*avg_res/avg_len:.1f}% disagreement remaining after alignment
""")

# ---------------------------------------------------------------------------
print("=" * 78)
print("TURNING THE RESIDUAL INTO A STORAGE NUMBER")
print("=" * 78)

span_B = max(x for w in WORDS for x in model_B[w]) - min(x for w in WORDS for x in model_B[w])
deltas = [A[r][j] - aligned[r][j] for r in range(len(WORDS)) for j in range(D)]
span_D = max(deltas) - min(deltas)

# How many bits to store a number to a fixed absolute precision?
PREC = 1e-3
bits_B = math.log2(max(span_B / PREC, 2))
bits_D = math.log2(max(span_D / PREC, 2))
saving = 100 * (1 - bits_D / bits_B)

print(f"""
  B's coordinates span {span_B:.3f}. The residual spans {span_D:.3f}.
  That is {span_B/span_D:.0f}x narrower.

  Storage per number, at {PREC:g} absolute precision:
      store B's own value      : ~{bits_B:.1f} bits
      store only the delta     : ~{bits_D:.1f} bits
      saving per number        : ~{saving:.0f}%

  Plus: the anchor table is now stored ONCE ({len(WORDS)*D} numbers) and shared,
  instead of duplicated per model.
""")

print("=" * 78)
print("WHAT THIS SHOWS")
print("=" * 78)
print(f"""
  1. ALIGNMENT WORKS ({verdict.split(' - ')[0]}). A rotation exists that lines B up with A.
     You never need the axes to match. You need a map between them.

  2. HERE, THE RESIDUAL IS SMALL ({100*avg_res/avg_len:.0f}%) because these two models learned the
     SAME reality. That is the premise - and the risk.

  3. THE RESIDUAL IS THE WHOLE ANSWER.
        small residual -> deltas are cheap -> sharing saves storage -> idea works
        large residual -> deltas as big as the original -> no saving at all

  4. So the real research question is not "can we standardise the basis"
     (nobody can) but:

        "HOW MUCH DO INDEPENDENTLY TRAINED MODELS ACTUALLY DISAGREE,
         ONCE ALIGNED?"

     That is measurable today, on real embeddings, in an afternoon.
""")
