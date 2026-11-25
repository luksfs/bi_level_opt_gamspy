# Appendix A: Mathematical Formulation of the Reactive Distillation (MESHR) Superstructure Model

This appendix documents the continuous nonlinear programming (NLP) subproblem solved for each discrete column topology $(N_s, N_{FE}, N_{FB}, \mathcal{R})$ in the ETBE reactive distillation superstructure. The model follows a stage-by-stage MESHR formulation coupled with non-ideal vapor–liquid equilibrium (SRK + NRTL), LHHW reaction kinetics over Amberlyst 15, continuous-spacing Fair hydraulics, catalyst packing volume constraints, and explicit Douglas equipment costing on a 1994 economic basis.

---

## 1. Sets, Indices, and Structural Parameters

### Sets and Indices
| Symbol | Definition | Elements / Range |
| :--- | :--- | :--- |
| $i, k, h, m \in \mathcal{I}$ | Chemical components | $\{1: \text{1-butene},\; 2: \text{ethanol},\; 3: \text{isobutene},\; 4: \text{ETBE}\}$ |
| $j \in \mathcal{J}$ | Superstructure stages (top to bottom) | $\{1, 2, \dots, N_{\max}\}$, with $N_{\max} = 22$ |
| $\mathcal{J}_{\text{act}}$ | Active column stages | $\{j \in \mathcal{J} : j \le N_s\}$ |
| $\mathcal{J}_{\text{int}}$ | Active interior stages | $\{j \in \mathcal{J} : 2 \le j \le N_s - 1\}$ |
| $\mathcal{J}_{\text{inact}}$ | Inactive ("ghost") stages | $\{j \in \mathcal{J} : j > N_s\}$ |
| $c \in \mathcal{C}$ | Extended Antoine coefficient index | $\{1, \dots, 7\}$ |
| $cc \in \mathcal{CC}$ | Heat-capacity polynomial index | $\{1, \dots, 5\}$ |

Stage $j = 1$ represents a total condenser ($V_1 = 0$) and stage $j = N_s$ represents a partial reboiler.

### Outer Discrete Configuration Parameters
For any candidate discrete design $(N_s, N_{FE}, N_{FB}, \mathcal{R})$ passed to the NLP subproblem:
* $N_s \in \{5, \dots, N_{\max}\}$: total number of active stages ($N_{\text{int}} = N_s - 2$ internal stages).
* $\delta^{FE}_j \in \{0, 1\}$: equals $1$ if $j = N_{FE}$ (ethanol feed stage), $0$ otherwise.
* $\delta^{FB}_j \in \{0, 1\}$: equals $1$ if $j = N_{FB}$ (C4/butenes feed stage), $0$ otherwise.
* $\delta^{\text{rxn}}_j \in \{0, 1\}$: equals $1$ if $j \in \mathcal{R}$ (reactive stage), $0$ otherwise.

Discrete boundary feasibility requires $1 < N_{FE} < N_s$, $1 < N_{FB} < N_s$, and $1 < r < N_s$ for all $r \in \mathcal{R}$.

---

## 2. Scaling Conventions

To improve numerical conditioning of the NLP, molar flowrates, heat duties, and molar enthalpies are scaled using fixed feed-based factors:

$$
F_{\text{scale}} = 1.7118 + 5.7740 = 7.4858\ \text{mol/min}
$$

$$
FH_{\text{scale}} = 1.7118\,|h_{FE}^\circ| + 5.7740\,|h_{FB}^\circ| = 591{,}769.27\ \text{J/min}
$$

$$
H_{\text{scale}} = \frac{F_{\text{scale}}}{FH_{\text{scale}}} = 1.264986 \times 10^{-5}\ \text{mol/J}
$$

where $h_{FE}^\circ = -273{,}241.23\ \text{J/mol}$ and $h_{FB}^\circ = -21{,}481.63\ \text{J/mol}$ are the molar feed enthalpies. Throughout the model:
* Scaled molar flows $(L_j, V_j, D, B_{\text{reb}}, F_E, F_B)$ convert to physical units via $\text{mol/min} = (\text{scaled}) \times F_{\text{scale}}$.
* Scaled heat duties $(Q_c, Q_r)$ convert to physical units via $\text{J/min} = (\text{scaled}) \times FH_{\text{scale}}$.
* Scaled stream enthalpies $(H^V_j, H^L_j, H_{FE}, H_{FB})$ convert to physical units via $\text{J/mol} = (\text{scaled}) / H_{\text{scale}}$.

---

## 3. Objective Function and Economic Model

The objective minimizes the net Total Annual Cost (TAC), scaled by $10^{-6}$ (in $\text{M\$}/\text{yr}$):

$$
\min \; \text{Obj} = \text{Profit}, \qquad \text{Profit} \times 10^6 = C_{\text{CAP}} + C_{\text{OP}}
$$

### 3.1 Annualized Capital Cost (Explicit Douglas Correlations, 1994 M&S Basis)
Let $D_{\text{ft}} = 3.28084\,D_{\text{col}}$ and $H_{\text{shell,ft}} = 3.28084\,(1 + SF)\,h_t\,(N_s - 2)$, with $M\&S = 1050.0$, shell height allowance $SF = 0.15$, and annualization factor $AF = \frac{i_r (1+i_r)^n}{(1+i_r)^n - 1} = 0.230975\ \text{yr}^{-1}$ ($i_r = 5\%$, $n = 5\ \text{yr}$).

1. **Column shell** (carbon steel vessel at $9.5\ \text{bar}$, $F_{BM,\text{shell}} = 3.33$):
$$
C_{\text{shell}} = \left(\frac{M\&S}{280}\right) 101.9 \, D_{\text{ft}}^{1.066} \, H_{\text{shell,ft}}^{0.802} \, F_{BM,\text{shell}}
$$

2. **Column internals / trays** (stainless steel sieve trays at $2\ \text{ft}$ reference spacing factor, $F_{BM,\text{tray}} = 2.70$):
$$
C_{\text{tray}} = \left(\frac{M\&S}{280}\right) 4.7 \, D_{\text{ft}}^{1.55} \, \bigl[2.0\,(N_s - 2)\bigr] \, F_{BM,\text{tray}}
$$

3. **Condenser** (CS/SS floating-head exchanger, $F_{BM,\text{cond}} = 4.04$, $U_c = 150 / 0.17611 = 851.74\ \text{W/(m}^2\text{K)}$, cooling water $303.15 \to 313.15\ \text{K}$):
$$
\Delta T_{\text{lm},c} = \frac{10.0}{\ln\!\left(\dfrac{T_{\text{cond}} - 303.15}{T_{\text{cond}} - 313.15}\right)}
$$
$$
C_{\text{cond}} = \left(\frac{M\&S}{280}\right) 101.3 \, F_{BM,\text{cond}} \left(\frac{Q_c \, FH_{\text{scale}} / 60}{U_c \, \Delta T_{\text{lm},c}} \times 10.7639\right)^{0.65}
$$

4. **Reboiler** (CS/SS kettle reboiler, $F_{BM,\text{reb}} = 4.65$, $U_r = 170 / 0.17611 = 965.31\ \text{W/(m}^2\text{K)}$, steam at $T_{\text{steam}} = 433.15\ \text{K}$):
$$
C_{\text{reb}} = \left(\frac{M\&S}{280}\right) 101.3 \, F_{BM,\text{reb}} \left(\frac{Q_r \, FH_{\text{scale}} / 60}{U_r \, (433.15 - T_{\text{reb}})} \times 10.7639\right)^{0.65}
$$

5. **Total annualized CAPEX** (including Amberlyst 15 catalyst at $C_{\text{cat}} = 7.7\ \text{\$/kg}$ and $m_{\text{cat}} = 0.4\ \text{kg/stage}$):
$$
C_{\text{CAP}} = AF \left(C_{\text{shell}} + C_{\text{tray}} + C_{\text{cond}} + C_{\text{reb}} + C_{\text{cat}} \, m_{\text{cat}} \sum_{j \in \mathcal{J}} \delta^{\text{rxn}}_j\right)
$$

### 3.2 Net Annual Operating Cost (1994 Prices, $t_{\text{op}} = 8000\ \text{h/yr}$)
$$
C_{\text{OP}} = 60\,t_{\text{op}}\,FH_{\text{scale}}\left(c_{\text{cw}}\,Q_c + c_{\text{steam}}\,Q_r\right) + 60\,t_{\text{op}}\,F_{\text{scale}}\left(c_{\text{Eth}}\,F_E + c_{\text{But}}\,F_B - c_{\text{ETBE}}\,B_{\text{reb}}\right)
$$
where $c_{\text{steam}} = 4.54 \times 10^{-9}\ \text{\$/J}$, $c_{\text{cw}} = 0.378 \times 10^{-9}\ \text{\$/J}$, $c_{\text{Eth}} = 0.015\ \text{\$/mol}$, $c_{\text{But}} = 0.00825\ \text{\$/mol}$, and $c_{\text{ETBE}} = 0.0253\ \text{\$/mol}$.

---

## 4. Stage-by-Stage MESHR Equations

### 4.1 Total Mole Balances
* **Condenser ($j = 1$):**
$$
V_1 + L_1 + D - V_2 = 0, \qquad V_1 = 0
$$
* **Interior stages ($j \in \mathcal{J}_{\text{int}}$):**
$$
L_j + V_j - V_{j+1} - L_{j-1} - F_E\,\delta^{FE}_j - F_B\,\delta^{FB}_j - \frac{m_{\text{cat}}\,r_j}{F_{\text{scale}}} \sum_{i \in \mathcal{I}} \nu_i = 0
$$
* **Reboiler ($j = N_s$):**
$$
V_{N_s} + L_{N_s} - L_{N_s - 1} = 0
$$

### 4.2 Component Mole Balances ($\forall i \in \mathcal{I}$)
* **Condenser ($j = 1$):**
$$
V_1 y_{i,1} + (L_1 + D) x_{i,1} - V_2 y_{i,2} = 0
$$
* **Interior stages ($j \in \mathcal{J}_{\text{int}}$):**
$$
L_j x_{i,j} + V_j y_{i,j} - V_{j+1} y_{i,j+1} - L_{j-1} x_{i,j-1} - F_E\,\delta^{FE}_j z_{E,i} - F_B\,\delta^{FB}_j z_{B,i} - \frac{m_{\text{cat}}\,\nu_i\,r_j}{F_{\text{scale}}} = 0
$$
* **Reboiler ($j = N_s$):**
$$
V_{N_s} y_{i,N_s} + L_{N_s} x_{i,N_s} - L_{N_s - 1} x_{i,N_s - 1} = 0
$$

### 4.3 Phase Equilibrium and Mole-Fraction Summation ($\forall j \in \mathcal{J}_{\text{act}}$)
$$
K_{i,j} x_{i,j} - y_{i,j} = 0 \quad \forall i \in \mathcal{I}, \qquad \sum_{i \in \mathcal{I}} (y_{i,j} - x_{i,j}) = 0
$$

### 4.4 Energy Balances
* **Condenser ($j = 1$):**
$$
V_1 H^V_1 + (L_1 + D) H^L_1 - V_2 H^V_2 + Q_c = 0
$$
* **Interior stages ($j \in \mathcal{J}_{\text{int}}$):**
$$
V_j H^V_j + L_j H^L_j - V_{j+1} H^V_{j+1} - L_{j-1} H^L_{j-1} - F_E\,\delta^{FE}_j H_{FE} - F_B\,\delta^{FB}_j H_{FB} = 0
$$
* **Reboiler ($j = N_s$):**
$$
V_{N_s} H^V_{N_s} + L_{N_s} H^L_{N_s} - L_{N_s - 1} H^L_{N_s - 1} - Q_r = 0
$$

### 4.5 Product Specification and Boundary Variable Definitions
$$
x_{4, N_s} = 0.83, \qquad T_{\text{cond}} = T_1, \qquad T_{\text{reb}} = T_{N_s}, \qquad B_{\text{reb}} = L_{N_s}
$$

---

## 5. Thermodynamic Property Model ($\forall j \in \mathcal{J}_{\text{act}}$)

Column pressure is uniform at $P_j = 9.5 \times 10^5\ \text{Pa}$ ($9.5\ \text{bar}$), with $R = 8.314463\ \text{J/(mol}\cdot\text{K)}$ and reference temperature $T_0 = 298.15\ \text{K}$.

### 5.1 Vapor–Liquid Partition Coefficient
$$
K_{i,j}\,\phi_{i,j}\,P_j = \gamma_{i,j}\,\exp(\ln P^{\text{sat}}_{i,j}) \qquad \forall i \in \mathcal{I}
$$

### 5.2 Extended Antoine Vapor Pressure ($\forall i \in \mathcal{I}$)
$$
\ln P^{\text{sat}}_{i,j} = k_{i,1} + \frac{k_{i,2}}{k_{i,3} + T_j} + k_{i,4} T_j + k_{i,5} \ln T_j + k_{i,6} T_j^{k_{i,7}}
$$

### 5.3 Soave–Redlich–Kwong (SRK) Vapor Equation of State
Pure-component constants ($\Omega_a = 0.42747$, $\Omega_b = 0.08664$):
$$
\kappa_i = 0.480 + 1.574\,\omega_i - 0.176\,\omega_i^2, \qquad a_{c,i} = \Omega_a \frac{(R T_{c,i})^2}{P_{c,i}}, \qquad b_{ii} = \Omega_b \frac{R T_{c,i}}{P_{c,i}}
$$

Stage-dependent parameters and mixing rules:
$$
\alpha_{i,j} = \left[1 + \kappa_i\left(1 - \sqrt{\frac{T_j}{T_{c,i}}}\right)\right]^2, \qquad a_{ii,j} = \alpha_{i,j}\,a_{c,i}
$$
$$
b_j = \sum_{i \in \mathcal{I}} y_{i,j}\,b_{ii}, \qquad a_j = \sum_{i \in \mathcal{I}} \sum_{k \in \mathcal{I}} y_{i,j} y_{k,j} \sqrt{a_{ii,j}\,a_{kk,j}}
$$

Compressibility factor $Z_j$ and vapor molar volume $v_j$:
$$
-Z_j + 1 + \beta_j - q_j \beta_j \frac{Z_j - \beta_j}{Z_j (Z_j + \beta_j)} = 0, \qquad \beta_j = \frac{b_j P_j}{R T_j}, \qquad q_j = \frac{a_j}{b_j R T_j}
$$
$$
v_j = \frac{Z_j R T_j}{P_j}
$$

Vapor-phase fugacity coefficient $\phi_{i,j}$:
$$
\phi_{i,j} = \exp\!\left[\frac{b_{ii}}{b_j}(Z_j - 1) - \ln\!\left(\frac{P_j (v_j - b_j)}{R T_j}\right) + q_j \left(\frac{b_{ii}}{b_j} - \frac{2}{a_j}\sum_{k \in \mathcal{I}} y_{k,j}\sqrt{a_{ii,j} a_{kk,j}}\right) \ln\!\left(\frac{v_j + b_j}{v_j}\right)\right]
$$

Temperature derivative of $a_j$ and vapor residual enthalpy $H^R_j$:
$$
\left(\frac{da}{dT}\right)_{ii,j} = -\frac{a_{c,i}\kappa_i}{T_j}\sqrt{\alpha_{i,j}\frac{T_j}{T_{c,i}}}, \qquad \left(\frac{da}{dT}\right)_j = \sqrt{a_j}\sum_{i \in \mathcal{I}} \frac{y_{i,j}}{\sqrt{a_{ii,j}}}\left(\frac{da}{dT}\right)_{ii,j}
$$
$$
H^R_j = R T_j \left[Z_j - 1 + \frac{T_j (da/dT)_j - a_j}{b_j R T_j} \ln\!\left(\frac{v_j + b_j}{v_j}\right)\right]
$$

### 5.4 NRTL Liquid Activity Coefficient ($\forall i \in \mathcal{I}$)
With $\tau_{h,i,j} = b^{\text{NRTL}}_{h,i} / T_j$ and $G_{h,i,j} = \exp\!\left(-c^{\text{NRTL}}_{h,i}\,\tau_{h,i,j}\right)$:
$$
\gamma_{i,j} = \exp\!\left[\frac{\sum_h x_{h,j}\,\tau_{h,i,j}\,G_{h,i,j}}{\sum_k x_{k,j}\,G_{k,i,j}} + \sum_h \frac{x_{h,j}\,G_{i,h,j}}{\sum_k x_{k,j}\,G_{k,h,j}}\left(\tau_{i,h,j} - \frac{\sum_m x_{m,j}\,\tau_{m,h,j}\,G_{m,h,j}}{\sum_k x_{k,j}\,G_{k,h,j}}\right)\right]
$$

### 5.5 Vapor and Liquid Enthalpies
* **Vapor enthalpy:**
$$
\Delta H^{\text{ig}}_{i,j} = \sum_{n=1}^{5} \frac{C^{\text{ig}}_{i,n}}{n}\left(T_j^n - T_0^n\right), \qquad H^{V}_{i,j} = \Delta H^{\text{ig}}_{i,j} + \Delta H_{f,i}^\circ
$$
$$
\frac{H^V_j}{H_{\text{scale}}} = \sum_{i \in \mathcal{I}} y_{i,j} H^V_{i,j} + H^R_j
$$

* **Pure-component SRK residual enthalpy at $T_{b,i}$** (with $\beta^p_{i,j} = \frac{b_{ii} P_j}{R T_{b,i}}$ and $q^p_i = \frac{a_{i}(T_{b,i})}{b_{ii} R T_{b,i}}$):
$$
-Z^V_{i,j} + 1 + \beta^p_{i,j} - q^p_i \beta^p_{i,j}\frac{Z^V_{i,j} - \beta^p_{i,j}}{Z^V_{i,j}(Z^V_{i,j} + \beta^p_{i,j})} = 0, \qquad v_{i,j} = \frac{Z^V_{i,j} R T_{b,i}}{P_j}
$$
$$
H^{R,\text{pure}}_{i,j} = R T_{b,i}\left[Z^V_{i,j} - 1 + \frac{T_{b,i}(da/dT)_{i,T_b} - a_i(T_{b,i})}{b_{ii} R T_{b,i}} \ln\!\left(\frac{v_{i,j} + b_{ii}}{v_{i,j}}\right)\right]
$$

* **Liquid enthalpy** (using heat of vaporization $\Delta H_{\text{vap},i} = C^{\text{vap}}_{i,1}(1 - T_{br,i})^{C^{\text{vap}}_{i,2} + C^{\text{vap}}_{i,3} T_{br,i} + C^{\text{vap}}_{i,4} T_{br,i}^2 + C^{\text{vap}}_{i,5} T_{br,i}^3}$, $T_{br,i} = T_{b,i}/T_{c,i}$):
$$
\Delta H^{\text{liq}}_{i,j} = \sum_{n=1}^{5} \frac{C^{\text{liq}}_{i,n}}{n}\left(T_j^n - T_{b,i}^n\right), \qquad H^V_{T_{b,i},P,j} = \Delta H^{\text{ig}}_{i,T_b} + \Delta H_{f,i}^\circ + H^{R,\text{pure}}_{i,j}
$$
$$
H^L_{i,j} = \Delta H^{\text{liq}}_{i,j} + H^V_{T_{b,i},P,j} - \Delta H_{\text{vap},i}, \qquad \frac{H^L_j}{H_{\text{scale}}} = \sum_{i \in \mathcal{I}} x_{i,j} H^L_{i,j}
$$

---

## 6. Reaction Kinetics (ETBE Synthesis over Amberlyst 15)

The reversible liquid-phase etherification $\text{EtOH}\ (2) + \text{IB}\ (3) \rightleftharpoons \text{ETBE}\ (4)$ is modeled via LHHW kinetics in activity form ($a_{i,j} = x_{i,j}\gamma_{i,j}$) for all $j \in \mathcal{J}_{\text{act}}$:

$$
K_{\text{eq},j} = \exp\!\left(10.387 + \frac{4060.59}{T_j} - 2.89055\ln T_j - 0.01915144\,T_j + 5.28586\times 10^{-5}\,T_j^2 - 5.32977\times 10^{-8}\,T_j^3\right)
$$

$$
k_{\text{rate},j} = \frac{7.41816 \times 10^{15}}{60}\exp\!\left(-\frac{60{,}400}{R T_j}\right) \quad \left[\frac{\text{mol}}{\text{kg}_{\text{cat}}\cdot\text{min}}\right]
$$

$$
k_{A,j} = \exp\!\left(-1.0707 + \frac{1323.1}{T_j}\right)
$$

$$
r_j = \delta^{\text{rxn}}_j \, \frac{k_{\text{rate},j}\,a_{2,j}\left(a_{2,j}\,a_{3,j} - a_{4,j}/K_{\text{eq},j}\right)}{\left(1 + k_{A,j}\,a_{2,j}\right)^3} \quad \left[\frac{\text{mol}}{\text{kg}_{\text{cat}}\cdot\text{min}}\right]
$$

---

## 7. Column Sizing, Continuous-Spacing Hydraulics, and Mechanical Constraints

For all active interior stages $j \in \mathcal{J}_{\text{int}}$ (with liquid density $\rho_L = 5.80 \times 10^5\ \text{g/m}^3$ and surface tension $\sigma = 7.2\ \text{dyn/cm}$):

### 7.1 Mixture Molecular Weights and Flow Parameter
$$
M^V_j = \sum_{i \in \mathcal{I}} y_{i,j} M_{w,i}, \qquad M^L_j = \sum_{i \in \mathcal{I}} x_{i,j} M_{w,i}
$$
$$
F_{lv,j} = \frac{L_j M^L_j}{V_j M^V_j}\sqrt{\frac{M^V_j / v_j}{\rho_L}}
$$

### 7.2 Fair Flooding Velocity (Continuous Stage Spacing via Lygeros & Magoulas, 1986)
With stage height $h_t$ as a continuous variable (in $\text{m}$), the capacity factor $C_{F,j}$ (in $\text{m/s}$) and flooding velocity $u_{fl,j}$ (in $\text{m/min}$) are:
$$
C_{F,j} = 0.0105 + 0.1496\,h_t^{0.755}\,\exp\!\left(-1.463\,F_{lv,j}^{0.842}\right)
$$
$$
u_{fl,j} = 60.0 \left(\frac{\sigma}{20.0}\right)^{0.2} \sqrt{\frac{\rho_L - M^V_j/v_j}{M^V_j/v_j}}\,C_{F,j}
$$

### 7.3 Superficial Vapor Velocity and Operating Window
Assuming an active bubbling area fraction of $0.88$:
$$
u_{f,j} = \frac{4\,(V_j F_{\text{scale}})\,v_j}{0.88\,\pi\,D_{\text{col}}^2}, \qquad 0.20\,u_{fl,j} \le u_{f,j} \le 0.80\,u_{fl,j}
$$

### 7.4 Catalyst Packing Volume and Mechanical Aspect Ratio
Each reactive stage holds $m_{\text{cat}} = 0.4\ \text{kg}$ of Amberlyst 15 ($\rho_{\text{cat}} = 770\ \text{kg/m}^3$, catalytic packing volume fraction $\phi_c = 0.30$, packing bed height $h_{\text{pack}} = 0.5\,h_t$):
$$
h_{\text{pack}} = 0.5\,h_t, \qquad \frac{m_{\text{cat}}}{\rho_{\text{cat}}} \le \phi_c \frac{\pi}{4} D_{\text{col}}^2 h_{\text{pack}}
$$
Mechanical column height-to-diameter limit:
$$
(1 + SF)\,h_t\,(N_s - 2) \le 20.0\,D_{\text{col}}
$$

### 7.5 Inactive ("Ghost") Stage Regularization ($\forall j \in \mathcal{J}_{\text{inact}}$)
To avoid singular derivatives on unused superstructure stages:
$$
T_j = 350\ \text{K}, \qquad L_j = 10^{-5}, \qquad V_j = 10^{-5}, \qquad x_{i,j} = 0.25 \quad \forall i \in \mathcal{I}
$$

---

## 8. Parameter Values and Variable Bounds

### Table A1: Pure-Component Physical Properties and Feed Compositions
| Comp. $i$ | Name | $\nu_i$ | $M_{w,i}$ (g/mol) | $T_{c,i}$ (K) | $P_{c,i}$ (Pa) | $\omega_i$ | $T_{b,i}$ (K) | $\Delta H_{f,i}^\circ$ (J/mol) | $z_{E,i}$ | $z_{B,i}$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 1-Butene | 0 | 56.10752 | 419.5 | $4.020\times 10^6$ | 0.184495 | 342.6 | $-500$ | 0 | 0.7 |
| 2 | Ethanol | $-1$ | 46.06904 | 514.0 | $6.137\times 10^6$ | 0.643558 | 421.5 | $-234{,}950$ | 1 | 0 |
| 3 | Isobutene | $-1$ | 56.10752 | 417.9 | $4.000\times 10^6$ | 0.194840 | 341.8 | $-17{,}100$ | 0 | 0.3 |
| 4 | ETBE | $+1$ | 102.17656 | 509.4 | $2.934\times 10^6$ | 0.316231 | 441.4 | $-313{,}900$ | 0 | 0 |

*Fixed C4 feed rate:* $F_B \cdot F_{\text{scale}} = 5.774\ \text{mol/min}$ (isobutene feed $= 1.7322\ \text{mol/min}$).

### Table A2: Extended Antoine Coefficients ($P^{\text{sat}}$ in Pa, $T$ in K)
| Comp. $i$ | $k_{i,1}$ | $k_{i,2}$ | $k_{i,3}$ | $k_{i,4}$ | $k_{i,5}$ | $k_{i,6}$ | $k_{i,7}$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 51.836 | $-4019.2$ | 0 | 0 | $-4.5229$ | $4.8833\times 10^{-17}$ | 6 |
| 2 | 73.304 | $-7122.3$ | 0 | 0 | $-7.1424$ | $2.8853\times 10^{-6}$ | 2 |
| 3 | 78.010 | $-4634.1$ | 0 | 0 | $-8.9575$ | $1.3413\times 10^{-5}$ | 2 |
| 4 | 64.188 | $-5820.2$ | 0 | 0 | $-6.1343$ | $2.1405\times 10^{-17}$ | 6 |

### Table A3: NRTL Binary Interaction Parameters ($b^{\text{NRTL}}_{i,k}$ in K; $c^{\text{NRTL}}_{i,k} = 0.3$ for $i \ne k$, $0$ for $i = k$)
| $i \setminus k$ | 1 | 2 | 3 | 4 |
| :---: | :---: | :---: | :---: | :---: |
| **1** | 0 | 595.529982 | 110.239086 | 226.373398 |
| **2** | 164.572560 | 0 | 141.963213 | 187.104064 |
| **3** | $-95.4252161$ | 623.581001 | 0 | 219.734070 |
| **4** | $-177.885650$ | 344.481315 | $-172.591520$ | 0 |

### Table A4: Heat-Capacity and Heat-of-Vaporization Coefficients (J/(mol·K) and J/mol)
* **Ideal-gas heat capacity ($C^{\text{ig}}_{i,n}$):**

| $i$ | $n=1$ | $n=2$ | $n=3$ | $n=4$ | $n=5$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 111.022862 | $-0.750243683$ | $3.74664805\times 10^{-3}$ | $-6.16980174\times 10^{-6}$ | $3.65183052\times 10^{-9}$ |
| 2 | 78.1195715 | $-0.495919524$ | $2.57066991\times 10^{-3}$ | $-4.30332398\times 10^{-6}$ | $2.57806954\times 10^{-9}$ |
| 3 | 150.319619 | $-0.966221476$ | $4.04410804\times 10^{-3}$ | $-6.00376885\times 10^{-6}$ | $3.23582716\times 10^{-9}$ |
| 4 | 47.4579586 | $-0.349114826$ | $1.80207897\times 10^{-3}$ | $-3.04885369\times 10^{-6}$ | $1.83440907\times 10^{-9}$ |

* **Liquid heat capacity ($C^{\text{liq}}_{i,n}$):**

| $i$ | $n=1$ | $n=2$ | $n=3$ | $n=4$ | $n=5$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | $2.42239762\times 10^5$ | $-2.74746461\times 10^3$ | $1.16801221\times 10^1$ | $-2.20506997\times 10^{-2}$ | $1.56048214\times 10^{-5}$ |
| 2 | $1.21280234\times 10^3$ | $-1.30223888\times 10^1$ | $5.71358761\times 10^{-2}$ | $-1.12370042\times 10^{-4}$ | $8.73258381\times 10^{-8}$ |
| 3 | $3.08689696\times 10^5$ | $-3.49815711\times 10^3$ | $1.48572135\times 10^1$ | $-2.80226414\times 10^{-2}$ | $1.98131733\times 10^{-5}$ |
| 4 | $1.20736602\times 10^3$ | $-1.29812644\times 10^1$ | $5.93572571\times 10^{-2}$ | $-1.16271343\times 10^{-4}$ | $8.66983296\times 10^{-8}$ |

* **Heat of vaporization ($C^{\text{vap}}_{i,n}$):**

| $i$ | $n=1$ | $n=2$ | $n=3$ | $n=4$ | $n=5$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 33774 | 0.51070 | $-0.17304$ | 0.05181 | 0 |
| 2 | 65831 | 1.19050 | $-1.76660$ | 1.00120 | 0 |
| 3 | 43172 | 1.53340 | $-1.90000$ | 0.83816 | 0 |
| 4 | 45290 | 0.27343 | 0.21645 | $-0.11756$ | 0 |

### Table A5: Key Continuous Variable Bounds
| Variable | Physical Meaning | Lower Bound | Upper Bound | Units |
| :--- | :--- | :---: | :---: | :--- |
| $T_j$ | Stage temperature | $330$ | $410$ | K |
| $T_{\text{cond}}, T_{\text{reb}}$ | Condenser / reboiler temperature | $330$ / $360$ | $380$ / $410$ | K |
| $L_j, V_j$ ($j \ge 2$) | Scaled liquid / vapor flowrate | $10^{-5}$ | $50$ | dimensionless |
| $x_{i,j}, y_{i,j}$ | Liquid / vapor mole fraction | $0$ | $1$ | mol/mol |
| $F_E \cdot F_{\text{scale}}$ | Ethanol feed rate | $0.7 \times 1.7322 = 1.2125$ | $2.5 \times 1.7322 = 4.3305$ | mol/min |
| $D, B_{\text{reb}}$ | Scaled distillate / bottoms flow | $0.01$ / $0.001$ | $1$ / $1$ | dimensionless |
| $Q_c, Q_r$ | Scaled condenser / reboiler duty | $0.01$ | $10$ | dimensionless |
| $D_{\text{col}}$ | Column diameter | $0.05$ | $2.0$ | m |
| $h_t, h_{\text{pack}}$ | Stage height / catalytic bed height | $0.10$ / $0.05$ | $0.60$ / $0.30$ | m |
| $F_{lv,j}$ | Fair flow parameter | $0.02$ | $1.0$ | dimensionless |
| $C_{F,j}$ | Fair capacity factor | $0.005$ | $0.50$ | m/s |
| $u_{f,j}, u_{fl,j}$ | Superficial / flooding velocity | $0.01$ / $0.01$ | $80$ / $100$ | m/min |
| $Z_j, Z^V_{i,j}$ | Vapor compressibility factors | $0.60$ / $0.75$ | $0.90$ / $1.00$ | dimensionless |
| $\gamma_{i,j}, \phi_{i,j}, K_{i,j}$ | Activity / fugacity / partition coeff. | $0.01$ / $0.1$ / $0.001$ | $20$ / $1.2$ / $10$ | dimensionless |
| $r_j$ | Net reaction rate | $-10$ | $10$ | mol/(kg$_{\text{cat}}$·min) |

---

## 9. Numerical Solution Strategy

Each fixed-topology NLP is solved in GAMSPy using a two-stage global verification procedure:
1. **Local warm-start (`CONOPT`):** Solved first with `time_limit = 15 s` and `enable_scaling = True` to generate a high-accuracy primal feasible point. If CONOPT fails to converge, variable levels are reset to default initial profiles.
2. **Global optimality proof (`BARON`):** Invoked with relative optimality tolerance `optcr = 1e-4`, `time_limit = 160 s`, `Threads = 1`, `NumLoc = 1`, and embedded in-process NLP subsolvers (`AllowExternal = 0`, `AllowMinos = 0`, `AllowSnopt = 0`, restricting local search to `IPOPT` and `FILTERSQP`).