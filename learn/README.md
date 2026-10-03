# learn/ — teaching scripts

Small, self-contained programs that demonstrate why the embedding-standardisation
problem behaves the way it does. Pure Python standard library; no numpy needed.

Run them in order:

| Script | Demonstrates |
| --- | --- |
| `01-why-not-coordinates.py` | Rotating a whole space changes every coordinate and no similarity. Flipping the sign of a decomposition gives equally valid, totally different coordinates. |
| `02-what-are-axes-based-off.py` | Axes are a lens, not a property of the space. Directions the data puts there survive any change of axes. |
| `03-sharing-and-deltas.py` | Aligning two models that learned the same reality (Procrustes), and turning the leftover residual into a storage estimate. |

## A note on how these were built

`03` contains real linear algebra written from scratch (SVD by one-sided Jacobi
rotations). It shipped several bugs, each caught by a self-test rather than by
reading the code:

1. The Jacobi rotation angle had a sign error, so the eigenvectors were neither
   orthogonal nor unit length (`V^T V` came out at 1.98).
2. The Kabsch formula was used as `V U^T`; the correct one is `U V^T`. The two
   differ by a transpose, which is easy to mistake for a working answer.
3. A model was asked for 4 orthonormal vectors in 3 dimensions — impossible, and
   it looped forever.

The lesson generalises: **an alignment result that looks plausible is not
evidence that the alignment code is correct.** Keep a case whose answer you know
by hand, and refuse to report numbers when it fails. `03` now refuses to print
its results unless the self-test passes.
