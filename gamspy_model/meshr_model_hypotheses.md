# Scientific Hypotheses and Modeling Assumptions of the MESHR Reactive Distillation Model

This document summarizes the physical, thermodynamic, kinetic, hydraulic, and economic hypotheses underlying the continuous MESHR (Mass, Equilibrium, Summation, Heat, and Reaction) superstructure model for ethyl *tert*-butyl ether (ETBE) synthesis, together with the scientific justification for each assumption.

---

## 1. Summary of Core Modeling Hypotheses

| Category | Hypothesis | Mathematical Implementation | Scientific Justification & Literature Basis |
| :--- | :--- | :--- | :--- |
| **Operating regime** | Steady-state, adiabatic column | Zero accumulation terms in all MESH balances; heat exchange occurs exclusively at the condenser ($Q_c$) and reboiler ($Q_r$). | Standard for conceptual design and superstructure optimization of distillation columns; ambient heat losses are negligible relative to latent heat duties (Bernal et al., 2018; Liñán et al., 2020). |
| **Phase equilibrium** | Ideal equilibrium stages ($100\%$ stage efficiency) | $y_{i,j} = K_{i,j} x_{i,j}$ on all active stages ($j \le N_s$), with a total condenser ($V_1 = 0$) and a partial reboiler ($j = N_s$). | Captures vapor–liquid separation thermodynamics without introducing mass-transfer rate correlations, keeping the nonlinear programming (NLP) subproblem tractable for deterministic global optimization (BARON) across exhaustive discrete sweeps (Taylor & Krishna, 2000; Liñán et al., 2020). |P
| **Thermodynamic model** | Non-ideal liquid (NRTL) + non-ideal vapor (SRK EoS), $\gamma\text{--}\phi$ formulation | $K_{i,j}\,\phi_{i,j}\,P_j = \gamma_{i,j}\,P_{i,j}^{\text{sat}}$; $\gamma_{i,j}$ from NRTL; $\phi_{i,j}$, $Z_j$, $v_j$, and $H_j^R$ from Soave–Redlich–Kwong (SRK); $P_{i,j}^{\text{sat}}$ from extended Antoine. | Required for the polar/non-polar C4–ethanol–ETBE mixture at $9.5\ \text{bar}$, which exhibits strong liquid-phase non-ideality (minimum-boiling C4–ethanol azeotropes) and non-negligible vapor-phase fugacity deviations at elevated pressure (Jensen & Datta, 1995; Bernal et al., 2018). |
| **Pressure profile** | Isobaric column (negligible pressure drop) | Uniform stage pressure $P_j = 9.5\ \text{bar}$ ($9.5 \times 10^5\ \text{Pa}$) across all active stages. | At $9.5\ \text{bar}$ ($950\ \text{kPa}$) in a laboratory/pilot column ($N_s \le 18$), total hydraulic pressure drop is typically $\sim 5\text{–}15\ \text{kPa}$ ($\sim 0.5\text{–}1.5\%$ of operating pressure), producing a minor effect on boiling points and relative volatilities while significantly reducing NLP non-convexity for global solvers. |
| **Reaction kinetics** | Pseudo-homogeneous, liquid-phase, activity-based LHHW kinetics | Reversible etherification $\text{EtOH} + \text{IB} \rightleftharpoons \text{ETBE}$ over Amberlyst 15, written in liquid activities $a_{i,j} = x_{i,j}\gamma_{i,j}$ and scaled by fixed catalyst mass $m_{\text{cat}} = 0.4\ \text{kg/stage}$. | Established experimentally by Jensen & Datta (1995): the reaction occurs exclusively in the liquid phase; activity-based rates account for strong liquid non-ideality; and for small macroporous resin beads at $335\text{–}350\ \text{K}$, internal/external transport resistances are small enough to lump into a pseudo-homogeneous rate law. |
| **Side reactions & inerts** | Single main reaction; 1-butene inert; side reactions neglected | Stoichiometry $\nu = [0, -1, -1, +1]$; neither isobutene hydration (TBA) nor isobutene dimerization (DIB) is included. | Anhydrous feeds eliminate isobutene hydration (Liñán et al., 2020). Isobutene dimerization is suppressed when ethanol covers the resin active sites (typically $\ge 4\%$ molar ethanol excess; Sneesby et al., 1997). In benchmarking studies where the ethanol feed bound $F_E^{\min}$ is relaxed to keep the discrete search space connected, compliance with the ethanol-excess guideline is evaluated *a posteriori*. |
| **Heat of reaction** | Implicitly captured via standard enthalpies of formation | No separate $\Delta H_{\text{rxn}}$ source term in the energy balance; $H_{i,j}^V$ and $H_{i,j}^L$ incorporate $\Delta H_{f,i}^\circ$. | Thermodynamically exact: referencing component enthalpies to the elements automatically accounts for the exothermic enthalpy of ETBE formation inside the stage energy balances without double-counting. |
| **Reactive stage representation** | Equilibrium catalytic-packing / tray hybrid | Reactive stages obey equilibrium MESH balances (simultaneous reaction and VLE, analogous to $y_{\text{liq/vap}} = 1$) and unified Fair hydraulics, subject to a geometric catalyst-volume constraint ($h_{\text{pack}} = 0.5\,h_t$, $\phi_c = 0.30$). | Represents structured catalytic packing (e.g., Sulzer Katapak-SP 12 envelopes with $30\%$ catalyst volume fraction and $\rho_{\text{cat}} = 770\ \text{kg/m}^3$), where half of the stage height ($h_{\text{pack}} = 0.5\,h_t$) houses the catalytic packing and the remaining height accommodates liquid distributors and vapor–liquid disengagement (Götze et al., 2001; Taylor & Krishna, 2000; Liñán et al., 2020). |
| **Hydraulics & geometry** | Uniform column diameter $D_{\text{col}}$ and stage height $h_t$; continuous-spacing Fair hydraulics | Single $D_{\text{col}}$ and $h_t$ across all interior stages; active bubbling area $= 88\%$; continuous Fair capacity factor $C_{F,j}$ via Lygeros & Magoulas (1986); operating window $0.20\,u_{fl,j} \le u_{f,j} \le 0.80\,u_{fl,j}$; aspect ratio $(1+SF)\,h_t\,(N_s - 2) \le 20\,D_{\text{col}}$. | Uniform shell geometry avoids swaged-column fabrication complexity; $80\%$ flooding and $20\%$ weeping bounds prevent entrainment flooding and tray dumping; the Lygeros & Magoulas (1986) correlation provides smooth derivatives in continuous $h_t$ for BARON; $L/D \le 20$ prevents mechanically unstable slender towers (Barker, 2017; Liñán et al., 2020). |
| **Hydraulic fluid properties** | Constant liquid density and surface tension; rigorous SRK vapor density | $\rho_L = 580\ \text{kg/m}^3$ and $\sigma = 7.2\ \text{dyn/cm}$ held constant; vapor density $\rho_{V,j} = M_j^V / v_j$ updated rigorously on every stage from SRK. | Captures the dominant stage-to-stage hydraulic variation (vapor density and flowrate) while avoiding additional liquid-property correlations that weaken convex relaxations in global optimization. |
| **Economic basis** | Explicit Douglas bare-module CAPEX + 1994 OPEX | Shell, tray, condenser, and reboiler installed costs computed explicitly via Douglas (1988) correlations ($M\&S = 1050$, $5\ \text{yr}$ at $5\%$, $AF = 0.231\ \text{yr}^{-1}$, $8000\ \text{h/yr}$); objective minimizes net TAC ($\text{CAPEX} + \text{OPEX} - \text{ETBE Revenue}$). | Directly couples column geometry ($D_{\text{col}}, h_t, N_s$) and heat-transfer driving forces ($\Delta T_{\text{lm},c}$, $T_{\text{steam}} - T_{\text{reb}}$) to capital expenditure, creating genuine non-trivial trade-offs between CAPEX, utility duties, and conversion. |

---

## 2. Clarification on Reactive Trays and Catalyst Fill (`Cat_fill_pct`)

A frequent point of clarification in this formulation is how a **fixed catalyst mass per stage** interacts with a **variable column geometry**:

1. **Fixed required catalyst volume ($V_{\text{cat,req}}$):**
   Because both the catalyst mass per reactive stage ($m_{\text{cat}} = 0.4\ \text{kg}$) and the apparent resin density ($\rho_{\text{cat}} = 770\ \text{kg/m}^3$) are fixed parameters, the physical catalyst volume required on each reactive stage is constant:
   $$V_{\text{cat,req}} = \frac{m_{\text{cat}}}{\rho_{\text{cat}}} = \frac{0.4}{770} = 5.1948 \times 10^{-4}\ \text{m}^3 = 0.5195\ \text{L}$$

2. **Variable available catalyst volume ($V_{\text{cat,avail}}$):**
   The available volume inside the catalytic packing pockets depends continuously on both column diameter $D_{\text{col}}$ and stage height $h_t$ (with $h_{\text{pack}} = 0.5\,h_t$ and $\phi_c = 0.30$):
   $$V_{\text{cat,avail}}(D_{\text{col}}, h_t) = \phi_c \frac{\pi}{4} D_{\text{col}}^2 h_{\text{pack}} = 0.30 \cdot \frac{\pi}{4} D_{\text{col}}^2 (0.5\,h_t)$$

3. **Interpretation of the catalyst fill metric:**
   The packing volume constraint $V_{\text{cat,req}} \le V_{\text{cat,avail}}$ enforces:
   $$\text{Cat\_fill\_pct} = 100 \times \frac{V_{\text{cat,req}}}{V_{\text{cat,avail}}} \le 100\%$$
   * When **`Cat_fill_pct = 100%`** (active constraint), the stage cross-section and height are sized tightly around the $0.5195\ \text{L}$ of Amberlyst 15 resin ($V_{\text{pack}} = 1.732\ \text{L}$), directly coupling $D_{\text{col}}^2 h_t = \text{const}$.
   * When **`Cat_fill_pct < 100%`** (slack constraint), hydraulics or boilup require a larger diameter/height than the catalyst alone demands, leaving spare packing volume (physically filled with inert packing or open channels) while total catalyst mass remains fixed at $0.4\ \text{kg/stage}$.

---

## References

* Barker, G. B. (2017). *The Engineer's Guide to Plant Layout and Piping Design for the Oil and Gas Industries*. Gulf Professional Publishing.
* Bernal, D. E., Carrillo-Díaz, C., Gómez, J. M., & Ricardez-Sandoval, L. A. (2018). Simultaneous design and control of catalytic distillation columns using comprehensive rigorous dynamic models. *Ind. Eng. Chem. Res.*, 57, 2587–2608.
* Douglas, J. M. (1988). *Conceptual Design of Chemical Processes*. McGraw-Hill.
* Götze, L., Bailer, O., Moritz, P., & von Scala, C. (2001). Reactive distillation with KATAPAK®. *Catalysis Today*, 69, 201–208.
* Jensen, K. L., & Datta, R. (1995). Ethers from ethanol. 1. Equilibrium thermodynamic analysis of the liquid-phase ethyl *tert*-butyl ether reaction (ETBE). *Ind. Eng. Chem. Res.*, 34, 392–399.
* Liñán, D. A., Bernal, D. E., Ricardez-Sandoval, L. A., & Gómez, J. M. (2020). Optimal design of superstructures for placing units and streams with multiple and ordered available locations. Part II: Rigorous design of catalytic distillation columns. *Computers & Chemical Engineering*, 139, 106845.
* Lygeros, A. I., & Magoulas, K. G. (1986). Column flooding and entrainment. *Hydrocarbon Processing*, 65(12), 43–44.
* Sneesby, M. G., Tadé, M. O., Datta, R., & Smith, T. N. (1997). ETBE synthesis via reactive distillation. 1. Steady-state simulation and design aspects. *Ind. Eng. Chem. Res.*, 36, 1855–1869.
* Taylor, R., & Krishna, R. (2000). Modelling reactive distillation. *Chemical Engineering Science*, 55, 5183–5229.