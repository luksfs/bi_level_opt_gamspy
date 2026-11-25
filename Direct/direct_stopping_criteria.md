# Termination Criteria (`len_tol`) for Pure DIRECT and Hybrid DIRECT + D-SDA

This document details the mathematical derivation, software-level behavior, and exact `len_tol` settings for each problem dimension (4D–7D) and superstructure size ($N_{s,\max} \in \{10, 12, 14, 22\}$) when applying SciPy's `direct` solver (`locally_biased=True`) either as a standalone global optimizer (**Pure DIRECT**) or as Phase 1 of a hybrid global–local framework (**DIRECT + D-SDA**).

---

## 1. Technical Reference & Case-by-Case Specification

### 1.1 Discrete Grid Resolution and DIRECT Trisection Geometry
In the continuous relaxation passed to DIRECT, the search domain is normalized to the unit hypercube $[0, 1]^d$ ($d \in \{4, 5, 6, 7\}$). Along the finest discrete coordinate axes—the internal feed and reactive stage locations ($N_{FE}, N_{FB}, N_{R,m}$)—valid integer stages span from stage $2$ through stage $N_{s,\max} - 2$ (excluding the condenser, the reboiler, and the stage immediately above the reboiler). Thus, the maximum number of discrete integer points along any normalized axis is:

$$
N = (N_{s,\max} - 2) - 2 + 1 = N_{s,\max} - 3
$$

Each discrete stage therefore occupies a normalized bin width of $w = 1/N$. Meanwhile, the $N_s$ axis spans $N_{N_s} = N_{s,\max} - N_{s,\min} + 1 \le N$ integers (with $N_{s,\min} = 5$ for 4D–5D, $6$ for 6D, and $7$ for 7D), so any tolerance that resolves the $N$-point internal-stage grid automatically resolves the $N_s$ axis as well.

Because DIRECT partitions hyperrectangles exclusively via **trisection**, the normalized side length along any coordinate after $k$ splits takes discrete values:

$$
L_k = 3^{-k} \in \left\{\frac{1}{3},\; \frac{1}{9},\; \frac{1}{27},\; \frac{1}{81},\; \dots\right\}
$$

> **Implementation note (`scipy.optimize.direct`):** With the default `locally_biased=True` (DIRECT-L), SciPy's underlying C implementation terminates once the **full** normalized maximal side length of the hyperrectangle containing the incumbent satisfies $L_k \le \text{len\_tol}$ (rather than half the side length as described in the docstring). Consequently, any two `len_tol` values lying inside the same interval $(3^{-(k+1)},\; 3^{-k}]$ produce identical DIRECT trajectories.

### 1.2 Closed-Form Splitting Depth ($k$) and `len_tol` Rule
To guarantee a clean, non-overlapping separation between **Pure DIRECT** and **Hybrid DIRECT + D-SDA**:

* **Pure DIRECT (single-point resolution):** Terminate at the shallowest trisection depth $k_{\text{pure}}$ for which the hyperrectangle side spans **at most one** discrete stage ($N \cdot 3^{-k} \le 1$):
  $$
  k_{\text{pure}} = \left\lceil \log_3(N) \right\rceil, \qquad \text{len\_tol}_{\text{pure}} = 3^{-k_{\text{pure}}} + \varepsilon_{\text{num}}
  $$
* **Hybrid DIRECT + D-SDA (multi-point handoff):** Terminate one trisection earlier ($k_{\text{hybrid}}$), where the maximal side still spans **strictly more than one** discrete stage ($N \cdot 3^{-k} > 1$, allowing at least two adjacent discrete configurations along the side), and transfer the incumbent and evaluation cache to D-SDA for local discrete refinement:
  $$
  k_{\text{hybrid}} = k_{\text{pure}} - 1 = \left\lceil \log_3(N) \right\rceil - 1, \qquad \text{len\_tol}_{\text{hybrid}} = 3^{-k_{\text{hybrid}}} + \varepsilon_{\text{num}}
  $$

Here $\varepsilon_{\text{num}} = 10^{-4}$ is a small floating-point safety margin ensuring that termination occurs cleanly at depth $k$ without floating-point rounding triggering an unintended $(k+1)$-th split.

### 1.3 Case-by-Case Tolerance Table ($N_{s,\max} = 10, 12, 14, 22$)

| Superstructure Size ($N_{s,\max}$) | Max Discrete Span $N = N_{s,\max} - 3$ | Mode | Depth $k$ | Normalized Side $L_k = 3^{-k}$ | Recommended `len_tol` ($3^{-k} + 10^{-4}$) | Internal Stage Width ($N \cdot L_k$) | $N_s$-Axis Width ($N_{N_s} \cdot L_k$, 4D–7D) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **10** | 7 | **Hybrid (DIRECT + D-SDA)** | $k = 1$ | $1/3$ (`0.33333`) | `0.33343` (`1/3 + 1e-4`) | `2.33` pts/side | `1.33 – 2.00` pts/side |
| **10** | 7 | **Pure DIRECT** | $k = 2$ | $1/9$ (`0.11111`) | `0.11121` (`1/9 + 1e-4`) | `0.78` pts/side | `0.44 – 0.67` pts/side |
| **12** | 9 | **Hybrid (DIRECT + D-SDA)** | $k = 1$ | $1/3$ (`0.33333`) | `0.33343` (`1/3 + 1e-4`) | `3.00` pts/side | `2.00 – 2.67` pts/side |
| **12** | 9 | **Pure DIRECT** *(exact boundary)* | $k = 2$ | $1/9$ (`0.11111`) | `0.11121` (`1/9 + 1e-4`) | `1.00` pt/side | `0.67 – 0.89` pts/side |
| **12** | 9 | **Pure DIRECT** *(strict $< 1$)* | $k = 3$ | $1/27$ (`0.03704`) | `0.03714` (`1/27 + 1e-4`) | `0.33` pts/side | `0.22 – 0.30` pts/side |
| **14** | 11 | **Hybrid (DIRECT + D-SDA)** | $k = 2$ | $1/9$ (`0.11111`) | `0.11121` (`1/9 + 1e-4`) | `1.22` pts/side | `0.89 – 1.11` pts/side |
| **14** | 11 | **Pure DIRECT** | $k = 3$ | $1/27$ (`0.03704`) | `0.03714` (`1/27 + 1e-4`) | `0.41` pts/side | `0.30 – 0.37` pts/side |
| **22** | 19 | **Hybrid (DIRECT + D-SDA)** | $k = 2$ | $1/9$ (`0.11111`) | `0.11121` (`1/9 + 1e-4`) | `2.11` pts/side | `1.78 – 2.00` pts/side |
| **22** | 19 | **Pure DIRECT** | $k = 3$ | $1/27$ (`0.03704`) | `0.03714` (`1/27 + 1e-4`) | `0.70` pts/side | `0.59 – 0.67` pts/side |

**Notes by Dimension (4D–7D):**
* Because `N = Ns_max - 3` is governed by the internal feed and reactive-tray axes—which exist identically in 4D ($N_{\text{rxn}}=1$), 5D ($N_{\text{rxn}}=2$), 6D ($N_{\text{rxn}}=3$), and 7D ($N_{\text{rxn}}=4$)—**the same `len_tol` applies across 4D–7D for a given $N_{s,\max}$**.
* **Special boundary at $N_{s,\max} = 12$ ($N = 9 = 3^2$):** At $k = 2$, $N \cdot L_2 = 9/9 = 1.00$ exactly (one discrete stage per side). Use $k = 2$ (`1/9 + 1e-4`) for Pure DIRECT if $N \cdot L_k \le 1$ is your criterion, or $k = 3$ (`1/27 + 1e-4`) if strict sub-grid resolution ($N \cdot L_k < 1$) is preferred.

---

## 2. Draft Text for Scientific Paper Methodology

> *The subsection below is written in journal-ready style and can be inserted directly into the Optimization Methodology section of your manuscript (adjusting section numbers and citation keys as needed).*

### X.X Termination Criteria for Continuous-to-Discrete DIRECT Partitioning

In the proposed bi-level optimization framework, the discrete column topology variables $\mathbf{y} = [N_s, N_{FE}, N_{FB}, N_{R,1}, \dots, N_{R,K}]$ are mapped onto a continuous box domain and explored via the locally biased Dividing Rectangles algorithm (DIRECT-L; Gablonsky & Kelley, 2001) as implemented in SciPy (`scipy.optimize.direct`, `locally_biased=True`). Internally, DIRECT normalizes the search domain to the unit hypercube $[0,1]^d$ and recursively partitions potentially optimal hyperrectangles by trisecting their longest coordinate directions. Consequently, after $k$ trisections along a given coordinate, the normalized side length of a hyperrectangle takes discrete values of the form

$$
L_k = 3^{-k}, \qquad k \in \mathbb{Z}_{\ge 0}.
$$

In the SciPy DIRECT-L implementation, the side-length stopping criterion terminates the search once the normalized maximal side length of the hyperrectangle containing the incumbent solution satisfies $L_k \le \text{len\_tol}$. Because the underlying decision space is discrete rather than continuous, selecting an arbitrary small tolerance (e.g., $\text{len\_tol} = 10^{-6}$) wastes function evaluations by repeatedly subdividing sub-regions that map to the exact same integer column configuration.

To match the partitioning resolution directly to the discrete lattice of the catalytic distillation superstructure, the stopping tolerance is tied to the finest discrete coordinate span. For a superstructure with maximum stage count $N_{s,\max}$, internal feed and reactive trays may occupy stages $\{2, \dots, N_{s,\max} - 2\}$, giving a maximum of

$$
N = N_{s,\max} - 3
$$

distinct integer positions along a normalized unit axis (corresponding to an average discrete bin width of $w = N^{-1}$). The number of discrete stages spanned by the longest edge of the incumbent hyperrectangle at trisection depth $k$ is therefore $N \cdot L_k = N \cdot 3^{-k}$. Based on this relationship, two distinct termination depths are defined for comparative benchmarking:

1. **Standalone DIRECT (single-point resolution):** When DIRECT is executed without local discrete refinement, partitioning continues until the incumbent hyperrectangle spans at most one discrete stage along every coordinate direction ($N \cdot 3^{-k} \le 1$):
   $$
   k_{\text{pure}} = \left\lceil \log_3(N) \right\rceil, \qquad \text{len\_tol}_{\text{pure}} = 3^{-k_{\text{pure}}} + \varepsilon_{\text{num}},
   $$
   where $\varepsilon_{\text{num}} = 10^{-4}$ prevents floating-point rounding from triggering an unnecessary additional trisection level.

2. **Hybrid DIRECT + D-SDA (multi-point handoff):** When DIRECT serves as a global warm-starter for the Discrete-Steepest Descent Algorithm (D-SDA; Liñán et al., 2020), partitioning is terminated one trisection level earlier:
   $$
   k_{\text{hybrid}} = k_{\text{pure}} - 1 = \left\lceil \log_3(N) \right\rceil - 1, \qquad \text{len\_tol}_{\text{hybrid}} = 3^{-k_{\text{hybrid}}} + \varepsilon_{\text{num}}.
   $$
   At depth $k_{\text{hybrid}}$, the incumbent hyperrectangle still satisfies $N \cdot 3^{-k_{\text{hybrid}}} > 1$, meaning its longest side spans more than one discrete stage (encompassing at least two adjacent integer configurations). Terminating DIRECT at this coarser resolution avoids redundant sub-integer subdivisions in the continuous space and transfers the best incumbent—along with the complete cache of previously evaluated discrete topologies—to D-SDA, which exploits exact discrete neighborhood search and steepest-descent line search to converge efficiently to a local discrete optimum.

**Table X.** Summary of DIRECT-L trisection depths ($k$) and side-length tolerances (`len_tol`) used across superstructure sizes ($N_{s,\max}$) for standalone DIRECT and hybrid DIRECT + D-SDA runs (applicable across 4D–7D).

| $N_{s,\max}$ | Finest Discrete Span $N$ | Hybrid DIRECT + D-SDA ($k_{\text{hybrid}}$, `len_tol`, $N \cdot 3^{-k}$) | Standalone DIRECT ($k_{\text{pure}}$, `len_tol`, $N \cdot 3^{-k}$) |
| :---: | :---: | :--- | :--- |
| 10 | 7 | $k = 1$, `len_tol` $= 3^{-1} + 10^{-4}$ ($2.33$ stages/side) | $k = 2$, `len_tol` $= 3^{-2} + 10^{-4}$ ($0.78$ stages/side) |
| 12 | 9 | $k = 1$, `len_tol` $= 3^{-1} + 10^{-4}$ ($3.00$ stages/side) | $k = 2$, `len_tol` $= 3^{-2} + 10^{-4}$ ($1.00$ stage/side)$^*$ |
| 14 | 11 | $k = 2$, `len_tol` $= 3^{-2} + 10^{-4}$ ($1.22$ stages/side) | $k = 3$, `len_tol` $= 3^{-3} + 10^{-4}$ ($0.41$ stages/side) |
| 22 | 19 | $k = 2$, `len_tol` $= 3^{-2} + 10^{-4}$ ($2.11$ stages/side) | $k = 3$, `len_tol` $= 3^{-3} + 10^{-4}$ ($0.70$ stages/side) |

$^*$For $N_{s,\max} = 12$ ($N = 9 = 3^2$), $k = 2$ sits exactly on the $N \cdot 3^{-k} = 1.00$ threshold; if strict sub-unit resolution ($N \cdot 3^{-k} < 1$) is required, $k_{\text{pure}} = 3$ (`len_tol` $= 3^{-3} + 10^{-4}$, $0.33$ stages/side) is used.