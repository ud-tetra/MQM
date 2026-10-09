# MQM A4/S4 metric carrier audit v0.1

## A4 literal carrier — EXACT PASS

Take the regular outer tetrahedron with vertices (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1) and insert the centroid O=(0,0,0). The four tetrahedra O joined to the four outer faces are congruent and have dual graph K4. Every cell has three radial edges sqrt(3), three face edges 2 sqrt(2), volume 2/3, and Cayley-Menger determinant 128. The four cells partition the outer tetrahedron of volume 8/3. The orientation-preserving tetrahedral group A4 acts transitively on the four cells.

## S4 one-cell-per-module carrier — scoped NO-GO

A six-module octahedron adjacency graph has degree 4. If each module were one Euclidean tetrahedron and each adjacency used a distinct full triangular face, all 24 tetrahedral face incidences would be paired into 12 shared faces, leaving zero boundary faces. A nonempty finite face-to-face tetrahedral complex with disjoint interiors in R3 cannot be compact with empty topological boundary. Therefore a six-tetrahedron one-cell-per-module octahedral carrier is impossible under these assumptions.

## S4 literal repair — EXACT PASS with 24 tetrahedra

Use the cube [-1,1]^3, its center O, and the six square-face centers. Split each square face into four triangles by its face center and cone each triangle to O. This gives 24 congruent tetrahedra grouped as four tetrahedra per face module. The six face modules have the octahedron adjacency graph. Each tetrahedron has edge multiset {1, sqrt(2), sqrt(2), sqrt(3), sqrt(3), 2}, volume 1/3, and Cayley-Menger determinant 32. The 24 cells exactly fill cube volume 8. Full cube/octahedron symmetry permutes the six modules and the 24 cells.

## Typed comparison

D6 literal carrier: 6 modules / 6 tetrahedral cells. A4 literal carrier: 4 modules / 4 tetrahedral cells. S4 literal fully symmetric repair: 6 modules / 24 tetrahedral cells. Module count and tetrahedral-cell count are distinct resource objects.

Physical promotion remains 0.
