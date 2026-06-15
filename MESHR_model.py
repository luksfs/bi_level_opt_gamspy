import gamspy as gp
import gamspy.math as gmath
import numpy as np
import pandas as pd
import sys

Ns  = 10
NFE = 5
NFB = 7
NR1 = 3
NR2 = 5
NR3 = 7
# 1. Initialize the GAMSPy Container
m = gp.Container()

# ============================================================================ #
# SETS
# ============================================================================ #
# Define sets as strings. j goes up to 22.
i = gp.Set(m, name="i", description="Number of components", records=[str(x) for x in range(1, 5)])
j = gp.Set(m, name="j", description="Number of stages", records=[str(x) for x in range(1, Ns+1)])

# ============================================================================ #
# DISCRETE VARIABLES / SCALARS (0-D Parameters)
# ============================================================================ #
# Ns  = gp.Parameter(m, name="Ns", description="Total stages currently active")
# NFE = gp.Parameter(m, name="NFE", description="Ethanol feed stage")
# NFB = gp.Parameter(m, name="NFB", description="Butenes feed stage")
# NR1 = gp.Parameter(m, name="NR1", description="First reactive tray")
# NR2 = gp.Parameter(m, name="NR2", description="Second reactive tray")
# NR3 = gp.Parameter(m, name="NR3", description="Third reactive tray")



# R = gp.Parameter(m, name="R", records=8.314)

# ============================================================================ #
# PARAMETERS (1-D and 2-D Arrays)
# ============================================================================ #


# Provide data using standard Python dictionaries or Pandas DataFrames

P = gp.Parameter(m, name="P", domain=[j], description="Pressure (Pa)")

# Assign the same value to all trays
P[...] = 9.5e5 # [Pa]

m_cat = 0.4 # [kg]

Tmin = gp.Parameter(m, name="Tmin", description="Minimum temperature limit")
Tmin[...] = 330

Tmax = gp.Parameter(m, name="Tmax", description="Maximum temperature limit")
Tmax[...] = 410

R = gp.Parameter(m, name="R", records=8.314463, description="Gas constant J K-1 kmol-1")

# reaction coefficient
# v_i = {"1": 0, "2": -1, "3": -1, "4": 1}
# v_i = gp.Parameter(m, name="v_i", domain=[i], records=v_i_data)
v_i = gp.Parameter(
    m, name="v_i", domain=[i], description="Reaction coefficient",
    records=[("1", 0), ("2", -1), ("3", -1), ("4", 1)]
)

Tc = gp.Parameter(
    m, name="Tc", domain=[i], description="Critical Temperature [K]",
    records=[("1", 419.5), ("2", 514), ("3", 417.9), ("4", 509.4)]
)

zE = gp.Parameter(
    m, name="zE", domain=[i], description="Molar fraction of ethanol",
    records=[("1", 0), ("2", 1), ("3", 0), ("4", 0)]
)

zB = gp.Parameter(
    m, name="zB", domain=[i], description="Molar fraction of butenes",
    records=[("1", 0.7), ("2", 0), ("3", 0.3), ("4", 0)]
)

Mw = gp.Parameter(
    m, name="Mw", domain=[i], description="Molecular weights (kg/kmol)",
    records=[("1", 56.10752), ("2", 46.06904), ("3", 56.10752), ("4", 102.17656)]
)

Pc = gp.Parameter(
    m, name="Pc", domain=[i], description="Critical pressure (Pa)",
    records=[("1", 4.02E6), ("2", 6.137E6), ("3", 4.0E6), ("4", 2.934E6)]
)

w = gp.Parameter(
    m, name="w", domain=[i], description="Acentric factor",
    records=[("1", 0.184495), ("2", 0.643558), ("3", 0.19484), ("4", 0.316231)]
)

Tb = gp.Parameter(
    m, name="Tb", domain=[i], description="Boiling temperature (K)",
    records=[("1", 342.6), ("2", 421.5), ("3", 341.8), ("4", 441.4)]
)

Hform = gp.Parameter(
    m, name="Hform", domain=[i], description="Heat of formation (J/mol)",
    records=[("1", -500), ("2", -234950), ("3", -17100), ("4", -313900)]
)

Omega_a = gp.Parameter(m, name="Omega_a", description="SRK parameter", records=0.42747)
Omega_b = gp.Parameter(m, name="Omega_b", description="SRK parameter", records=0.08664)

# Uninitialized indexed parameters (Computed later via Equations or assignments)
kappa = gp.Parameter(m, name="kappa", domain=[i], description="SRK equation parameter")
ac = gp.Parameter(m, name="ac", domain=[i], description="Component-specific parameter")
bii = gp.Parameter(m, name="bii", domain=[i], description="SRK b-parameter")

kappa[i] = 0.480 + 1.574 * w[i] - 0.176 * w[i]**2
ac[i] = Omega_a * (R * Tc[i])**2 / Pc[i]
bii[i] = Omega_b * R * Tc[i] / Pc[i]

# Feed Enthalpy [J/mol]
hfb_d_val = -21481.62933928521
hfe_d_val = -273241.2338487912

#Scaling factors
F_factor = 1.7118 + 5.774
FH_factor = 1.7118 * abs(hfe_d_val) + 5.774 * abs(hfb_d_val)
H_factor = F_factor / FH_factor
TF_factor = (342.38 + 325) / 2

# Now declare the GAMSPy Parameters using the computed python values
# F_factor = gp.Parameter(m, name="F_factor", records=f_factor_val)
# FH_factor = gp.Parameter(m, name="FH_factor", records=fh_factor_val)
# H_factor = gp.Parameter(m, name="H_factor", records=h_factor_val)
# TF_factor = gp.Parameter(m, name="TF_factor", records=tf_factor_val)

HFE = gp.Parameter(m, name="HFE", records=hfe_d_val * H_factor)
HFB = gp.Parameter(m, name="HFB", records=hfb_d_val * H_factor)
FB = gp.Parameter(m, name="FB", records=5.774 / F_factor)

# Parameters for analysis (maybe not necessary because I can calculate later in Python)
# X_etoh  = gp.Parameter(m, name="X_etoh", description="Etanol conversion")
# X_ibut  = gp.Parameter(m, name="X_ibut", description="Isobutene conversion")
# x_B_etbe = gp.Parameter(m, name="x_B_etbe", description="ETBE molar fraction on the bottom")



# ... (Load the rest of Pc, w, Tb, Hform, b_nrtl, etc., similarly) ...

# ============================================================================ #
# VARIABLES
# ============================================================================ #
L  = gp.Variable(m, name="L", domain=[j], type="Positive", description="Liquid flowrate [mol/min]")
V  = gp.Variable(m, name="V", domain=[j], type="Positive", description="Vapor flowrate [mol/min]")
x  = gp.Variable(m, name="x", domain=[i, j], type="Positive", description="Liquid fraction")
y  = gp.Variable(m, name="y", domain=[i, j], type="Positive", description="Vapor fraction")
T  = gp.Variable(m, name="T", domain=[j], type="Positive", description="Temperature [K]")
FE = gp.Variable(m, name="FE", type="Positive", description="Etanol feed molar flowrate [mol/min]")
D  = gp.Variable(m, name="D", type="Positive", description="Destillate product flowrate (mol/min)")
Qc  = gp.Variable(m, name="Qc", type="Positive", description="Condenser Duty (J/min)")
Qr  = gp.Variable(m, name="Qr", type="Positive", description="Reboiler Duty (J/min)")

#SRK model
Z        = gp.Variable(m, name="Z", domain=[j], description="Compressibility factor")
v_mol    = gp.Variable(m, name="v_mol", domain=[j], description="Molar volume")
phi      = gp.Variable(m, name="phi", domain=[i, j], description="Fugacity coefficient")
HR       = gp.Variable(m, name="HR", domain=[j], description="Residual enthalpy")
alpha_ij = gp.Variable(m, name="alpha_ij", domain=[i, j], description="Alpha parameter")
aii      = gp.Variable(m, name="aii", domain=[i, j], description="Component-wise SRK aii parameter")
a        = gp.Variable(m, name="a", domain=[j], description="Mixture parameter a")
b        = gp.Variable(m, name="b", domain=[j], description="Mixture parameter b")
dadT_ii  = gp.Variable(m, name="dadT_ii", domain=[i, j], description="Partial derivative of a to T")
dadT     = gp.Variable(m, name="dadT", domain=[j], description="Total temperature derivative of a")

# ============================================================================ *
# ================================= EQUATIONS ================================ *
# ============================================================================ *

# ---------------------------------------------------------------------------- #
# Alias
# ---------------------------------------------------------------------------- #
# Create an alias for set i
k = gp.Alias(m, name="k", alias_with=i)

# ============================================================================ #
# Antoine for sat pressure model
# ============================================================================ #


# ---------------------------------------------------------------------------- #
# Sets
# ---------------------------------------------------------------------------- #
# The GAMS code uses the universal set '*' for the Antoine parameters (1 to 7).
# In GAMSPY, we explicitly define a Set for these columns.
c = gp.Set(m, name="c", description="Antoine coefficient columns", records=[str(x) for x in range(1, 8)])

# ---------------------------------------------------------------------------- #
# Variables
# ---------------------------------------------------------------------------- #
logPsat = gp.Variable(m, name="logPsat", type="positive", domain=[i, j], description="Saturation Pressure (Pa)")

# ---------------------------------------------------------------------------- #
# Parameters & Table Initialization
# ---------------------------------------------------------------------------- #
kk = gp.Parameter(m, name="kk", domain=[i, c], description="psat antoine parameters")

# Convert the GAMS TABLE format using a Pandas DataFrame
table_data = [
    ["1", 51.836, -4019.2, 0, 0, -4.5229, 4.8833E-17, 6],
    ["2", 73.304, -7122.3, 0, 0, -7.1424, 2.8853E-06, 2],
    ["3", 78.01,  -4634.1, 0, 0, -8.9575, 1.3413E-05, 2],
    ["4", 64.188, -5820.2, 0, 0, -6.1343, 2.1405E-17, 6]
]

# Create a "wide" dataframe (similar to how it looks visually in GAMS)
df_wide = pd.DataFrame(table_data, columns=["i", "1", "2", "3", "4", "5", "6", "7"])

# GAMSPY expects 2D data in a "long" format: (Index1, Index2, Value). 
# The pd.melt() function easily converts the table to this format.
df_long = df_wide.melt(id_vars=["i"], var_name="c", value_name="value")

# Load the data into the parameter
kk.setRecords(df_long)

# ---------------------------------------------------------------------------- #
# Equations Declaration
# ---------------------------------------------------------------------------- #
psat_def = gp.Equation(m, name="psat_def", domain=[i, j])

# ---------------------------------------------------------------------------- #
# Equations Definition
# ---------------------------------------------------------------------------- #
# cond_j = j.where[gp.Ord(j) <= Ns]

# You can access specific set elements dynamically by passing the string literal 
# (e.g., "1", "2") directly into the parameter index.
psat_def[i, j] = (
    logPsat[i, j] == (
        kk[i, "1"] + kk[i, "2"] / (kk[i, "3"] + T[j]) 
        + kk[i, "4"] * T[j] + kk[i, "5"] * gmath.log(T[j]) 
        + kk[i, "6"] * (T[j] ** kk[i, "7"])
    )
)

# ============================================================================ #
# SRK model
# ============================================================================ #

# ---------------------------------------------------------------------------- #
# Macros (Implemented as Python functions returning GAMSPY expressions)
# ---------------------------------------------------------------------------- #
def Tr(i_, j_): 
    return T[j_] / Tc[i_]

def Betav(j_): 
    return (b[j_] * P[j_]) / (R * T[j_])

def qv(j_): 
    return a[j_] / (b[j_] * R * T[j_])

# ---------------------------------------------------------------------------- #
# Equations Declaration
# ---------------------------------------------------------------------------- #
cubic_eos        = gp.Equation(m, name="cubic_eos", domain=[j])
v_definition     = gp.Equation(m, name="v_definition", domain=[j])
fugacity_eq      = gp.Equation(m, name="fugacity_eq", domain=[i, j])
enthalpy_eq      = gp.Equation(m, name="enthalpy_eq", domain=[j])
alpha_definition = gp.Equation(m, name="alpha_definition", domain=[i, j])
aii_definition   = gp.Equation(m, name="aii_definition", domain=[i, j])
mixing_rule_b    = gp.Equation(m, name="mixing_rule_b", domain=[j])
mixing_rule_a    = gp.Equation(m, name="mixing_rule_a", domain=[j])
dadT_ii_eq       = gp.Equation(m, name="dadT_ii_eq", domain=[i, j])
dadT_eq          = gp.Equation(m, name="dadT_eq", domain=[j])

# ---------------------------------------------------------------------------- #
# Equations Definition
# ---------------------------------------------------------------------------- #
# Define the domain condition $(ord(j) <= Ns) for cleaner syntax below
# cond_j = j.where[gp.Ord(j) <= Ns]

cubic_eos[j] = (
    -Z[j] + 1 + Betav(j) - qv(j) * Betav(j) * (Z[j] - Betav(j)) / (Z[j] * (Z[j] + Betav(j))) == 0
)

alpha_definition[i, j] = (
    alpha_ij[i, j] == (1 + kappa[i] * (1 - gmath.sqrt(Tr(i, j))))**2
)

aii_definition[i, j] = (
    aii[i, j] == alpha_ij[i, j] * ac[i]
)

mixing_rule_b[j] = (
    b[j] == gp.Sum(i, y[i, j] * bii[i])
)

mixing_rule_a[j] = (
    a[j] == gp.Sum(i, gp.Sum(k, y[i, j] * y[k, j] * gmath.sqrt(aii[i, j] * aii[k, j])))
)

v_definition[j] = (
    v_mol[j] == Z[j] * R * T[j] / P[j]
)

fugacity_eq[i, j] = (
    phi[i, j] == gmath.exp(
        bii[i] * (Z[j] - 1) / b[j] - gmath.log(P[j] * (v_mol[j] - b[j]) / (R * T[j])) +
        (a[j] / (b[j] * R * T[j])) * (bii[i] / b[j] - 2 * gp.Sum(k, y[k, j] * gmath.sqrt(aii[i, j] * aii[k, j])) / a[j]) * gmath.log((v_mol[j] + b[j]) / v_mol[j])
    )
)

dadT_ii_eq[i, j] = (
    dadT_ii[i, j] == -(ac[i] * kappa[i]) * gmath.sqrt(alpha_ij[i, j] * Tr(i, j)) / T[j]
)

dadT_eq[j] = (
    dadT[j] == -gp.Sum(i, gp.Sum(k, y[i, j] * y[k, j] * gmath.sqrt(dadT_ii[i, j] * dadT_ii[k, j])))
)

enthalpy_eq[j] = (
    HR[j] == R * T[j] * (Z[j] - 1 + (T[j] * dadT[j] - a[j]) / (b[j] * R * T[j]) * gmath.log((v_mol[j] + b[j]) / v_mol[j]))
)

#  ============================================================================ *
#  NRTL model
#  ============================================================================ *

# ---------------------------------------------------------------------------- #
# Aliases
# ---------------------------------------------------------------------------- #
# NOTE: 'm' is usually used for the Container (m = gp.Container()). 
# To avoid overwriting the container, the GAMS alias 'm' is renamed to 'm_alias'.
k = gp.Alias(m, name="k", alias_with=i)
h = gp.Alias(m, name="h", alias_with=i)
m_alias = gp.Alias(m, name="m_alias", alias_with=i) 

# ---------------------------------------------------------------------------- #
# Parameters & Data Initialization
# ---------------------------------------------------------------------------- #
b_nrtl = gp.Parameter(m, name="b_nrtl", domain=[i, i], description="NRTL b parameter")
c_nrtl = gp.Parameter(m, name="c_nrtl", domain=[i, i], description="NRTL c parameter")

# In GAMSPY, the cleanest way to load 2D sparse data is using a Pandas DataFrame 
# created from a list of tuples (i, k, value).
b_data = [
    ("1", "2", 595.529982), ("1", "3", 110.239086), ("1", "4", 226.373398),
    ("2", "1", 164.57256),  ("2", "3", 141.963213), ("2", "4", 187.104064),
    ("3", "1", -95.4252161),("3", "2", 623.581001), ("3", "4", 219.73407),
    ("4", "1", -177.88565), ("4", "2", 344.481315), ("4", "3", -172.59152)
]
b_nrtl.setRecords(pd.DataFrame(b_data, columns=["i_1", "i_2", "value"]))

c_data = [
    ("1", "1", 0.0), ("1", "2", 0.3), ("1", "3", 0.3), ("1", "4", 0.3),
    ("2", "1", 0.3), ("2", "2", 0.0), ("2", "3", 0.3), ("2", "4", 0.3),
    ("3", "1", 0.3), ("3", "2", 0.3), ("3", "3", 0.0), ("3", "4", 0.3),
    ("4", "1", 0.3), ("4", "2", 0.3), ("4", "3", 0.3), ("4", "4", 0.0)
]
c_nrtl.setRecords(pd.DataFrame(c_data, columns=["i_1", "i_2", "value"]))

# ---------------------------------------------------------------------------- #
# Variables
# ---------------------------------------------------------------------------- #
gamma_nrtl = gp.Variable(m, name="gamma_nrtl", domain=[i, j])

# Notice the type="positive" argument here
K_part = gp.Variable(m, name="K_part", type="positive", domain=[i, j]) 

# ---------------------------------------------------------------------------- #
# Macros (Implemented as Functions)
# ---------------------------------------------------------------------------- #
def tao_nrtl(i_, k_, j_): 
    return b_nrtl[i_, k_] / T[j_]

def g_nrtl(i_, k_, j_): 
    # return gmath.exp(-c_nrtl[i_, k_] * tao_nrtl(i_, k_, j_))
    return gmath.exp(-c_nrtl[i_, k_] * ( b_nrtl[i_, k_] / T[j_] ) )

# ---------------------------------------------------------------------------- #
# Equations Declaration
# ---------------------------------------------------------------------------- #
Compute_gamma       = gp.Equation(m, name="Compute_gamma", domain=[i, j])
K_equation          = gp.Equation(m, name="K_equation", domain=[i, j])

# ---------------------------------------------------------------------------- #
# Equations Definition
# ---------------------------------------------------------------------------- #
# cond_j = j.where[gp.Ord(j) <= Ns]

Compute_gamma[i, j] = gamma_nrtl[i, j] == gmath.exp(
    gp.Sum(h, x[h, j] * tao_nrtl(h, i, j) * g_nrtl(h, i, j)) /
    gp.Sum(k, x[k, j] * g_nrtl(k, i, j))
    +
    gp.Sum(h, (x[h, j] * g_nrtl(i, h, j)) /
    gp.Sum(k, x[k, j] * g_nrtl(k, h, j)) *
    (tao_nrtl(i, h, j) -
    gp.Sum(m_alias, x[m_alias, j] * tao_nrtl(m_alias, h, j) * g_nrtl(m_alias, h, j)) /
    gp.Sum(k, x[k, j] * g_nrtl(k, h, j))))
)

# * ============================================================================ *
# * Partiion coeffient
# * ============================================================================ *
K_equation[i, j] = (
    K_part[i, j] * (phi[i, j] * P[j]) == gamma_nrtl[i, j] * gmath.exp(logPsat[i, j])
)

#  ============================================================================ *
#  Enthalpy Calculation
#  ============================================================================ *

# ---------------------------------------------------------------------------- #
# Sets
# ---------------------------------------------------------------------------- #
cc = gp.Set(m, name="cc", description="Coefficient columns", records=[str(x) for x in range(1, 6)])

# ---------------------------------------------------------------------------- #
# Scalar / Constant Parameters
# ---------------------------------------------------------------------------- #
T0 = gp.Parameter(m, name="T0", description="Reference temperature [K]")
T0[...] = 298.15

e = gp.Parameter(m, name="e")
e[...] = 0

sigma = gp.Parameter(m, name="sigma")
sigma[...] = 1

# ---------------------------------------------------------------------------- #
# Data Tables (Ideal Gas, Liquid, Vap Enthalpy)
# ---------------------------------------------------------------------------- #
C_ig = gp.Parameter(m, name="C_ig", domain=[i, cc], description="Heat capacity coefficients for ideal gas")
C_liq = gp.Parameter(m, name="C_liq", domain=[i, cc], description="Heat capacity coefficients for liquid phase")
C_vap = gp.Parameter(m, name="C_vap", domain=[i, cc], description="DIPPR coefficients for vaporization enthalpy")

# C_ig Data
data_ig = [
    ["1", 111.022862, -0.750243683, 0.00374664805, -6.16980174E-06, 3.65183052E-09],
    ["2", 78.1195715, -0.495919524, 0.00257066991, -4.30332398E-06, 2.57806954E-09],
    ["3", 150.319619, -0.966221476, 0.00404410804, -6.00376885E-06, 3.23582716E-09],
    ["4", 47.4579586, -0.349114826, 0.00180207897, -3.04885369E-06, 1.83440907E-09]
]
C_ig.setRecords(pd.DataFrame(data_ig, columns=["i", "1", "2", "3", "4", "5"]).melt(id_vars=["i"], var_name="cc", value_name="val"))

# C_liq Data
data_liq = [
    ["1", 2.42239762e+05, -2.74746461e+03, 1.16801221e+01, -2.20506997e-02, 1.56048214e-05],
    ["2", 1.21280234e+03, -1.30223888e+01, 5.71358761e-02, -1.12370042e-04, 8.73258381e-08],
    ["3", 3.08689696e+05, -3.49815711e+03, 1.48572135e+01, -2.80226414e-02, 1.98131733e-05],
    ["4", 1.20736602e+03, -1.29812644e+01, 5.93572571e-02, -1.16271343e-04, 8.66983296e-08]
]
C_liq.setRecords(pd.DataFrame(data_liq, columns=["i", "1", "2", "3", "4", "5"]).melt(id_vars=["i"], var_name="cc", value_name="val"))

# C_vap Data
data_vap = [
    ["1", 33774, 0.5107, -0.17304, 0.05181, 0],
    ["2", 65831, 1.1905, -1.7666, 1.0012, 0],
    ["3", 43172, 1.5334, -1.9, 0.83816, 0],
    ["4", 45290, 0.27343, 0.21645, -0.11756, 0]
]
C_vap.setRecords(pd.DataFrame(data_vap, columns=["i", "1", "2", "3", "4", "5"]).melt(id_vars=["i"], var_name="cc", value_name="val"))

# ---------------------------------------------------------------------------- #
# Calculated Parameters
# ---------------------------------------------------------------------------- #
Tbr      = gp.Parameter(m, name="Tbr", domain=[i])
alpha_Tb = gp.Parameter(m, name="alpha_Tb", domain=[i])
ai_Tb    = gp.Parameter(m, name="ai_Tb", domain=[i])
dadT_Tb  = gp.Parameter(m, name="dadT_Tb", domain=[i])
DH_vap   = gp.Parameter(m, name="DH_vap", domain=[i], description="Vaporization enthalpy at Tb [J/mol]")
DH_ig_Tb = gp.Parameter(m, name="DH_ig_Tb", domain=[i], description="DH_ig from T0 to TB [J/mol]")

# Perform assignments across set 'i'
Tbr[i] = Tb[i] / Tc[i]

alpha_Tb[i] = (1 + kappa[i] * (1 - Tbr[i]**0.5))**2

ai_Tb[i] = alpha_Tb[i] * ac[i]

dadT_Tb[i] = -ac[i] * kappa[i] * gmath.sqrt(alpha_Tb[i] * Tbr[i]) / Tb[i]

DH_vap[i] = C_vap[i, "1"] * (1 - Tbr[i])**(
    C_vap[i, "2"] + C_vap[i, "3"]*Tbr[i] + C_vap[i, "4"]*(Tbr[i]**2) + C_vap[i, "5"]*(Tbr[i]**3)
)

# GAMS sqr() and power() functions mapped natively to ** operator
DH_ig_Tb[i] = (
    C_ig[i, "1"] * (Tb[i] - T0)
    + C_ig[i, "2"] * (Tb[i]**2 - T0**2) / 2
    + C_ig[i, "3"] * (Tb[i]**3 - T0**3) / 3
    + C_ig[i, "4"] * (Tb[i]**4 - T0**4) / 4
    + C_ig[i, "5"] * (Tb[i]**5 - T0**5) / 5
)

# ---------------------------------------------------------------------------- #
# Variables
# ---------------------------------------------------------------------------- #
DH_ig    = gp.Variable(m, name="DH_ig", domain=[i, j], description="Ideal gas enthalpy change")
Hvi      = gp.Variable(m, name="Hvi", domain=[i, j], description="Ideal gas enthalpy of vapor phase + Hform")
Hv       = gp.Variable(m, name="Hv", domain=[j], description="Total vapor phase enthalpy")
DH_liq   = gp.Variable(m, name="DH_liq", domain=[i, j], description="Liquid enthalpy change from Tb to T")
Hv_Tbi_P = gp.Variable(m, name="Hv_Tbi_P", domain=[i, j], description="Vapor phase enthalpy at Tb")
Hli      = gp.Variable(m, name="Hli", domain=[i, j], description="Liquid enthalpy for each component")
Hl       = gp.Variable(m, name="Hl", domain=[j], description="Total liquid phase enthalpy")
HR_pure  = gp.Variable(m, name="HR_pure", domain=[i, j], description="Residual enthalpy pure substance")

Zvi      = gp.Variable(m, name="Zvi", type="positive", domain=[i, j])
v_mol_i  = gp.Variable(m, name="v_mol_i", type="positive", domain=[i, j])

# ---------------------------------------------------------------------------- #
# Macros -> Python Functions
# ---------------------------------------------------------------------------- #
def Betav_p(i_, j_): 
    return (bii[i_] * P[j_]) / (R * Tb[i_])

def qv_p(i_): 
    return ai_Tb[i_] / (bii[i_] * R * Tb[i_])

# ---------------------------------------------------------------------------- #
# Equations Declaration
# ---------------------------------------------------------------------------- #
calc_DH_ig   = gp.Equation(m, name="calc_DH_ig", domain=[i, j])
calc_Hvi     = gp.Equation(m, name="calc_Hvi", domain=[i, j])
calc_Hv      = gp.Equation(m, name="calc_Hv", domain=[j])

Zvi_eq       = gp.Equation(m, name="Zvi_eq", domain=[i, j])
v_eq         = gp.Equation(m, name="v_eq", domain=[i, j])
calc_HR_pure = gp.Equation(m, name="calc_HR_pure", domain=[i, j])

calc_DH_liq  = gp.Equation(m, name="calc_DH_liq", domain=[i, j])
calc_Hv_Tbi_P= gp.Equation(m, name="calc_Hv_Tbi_P", domain=[i, j])
calc_Hli     = gp.Equation(m, name="calc_Hli", domain=[i, j])
calc_Hl      = gp.Equation(m, name="calc_Hl", domain=[j])

# ---------------------------------------------------------------------------- #
# Equations Definition
# ---------------------------------------------------------------------------- #
# Using the cond_j ( $(ord(j) <= Ns) ) previously established:
# cond_j = j.where[gp.Ord(j) <= Ns]

calc_DH_ig[i, j] = DH_ig[i, j] == (
    C_ig[i, "1"] * (T[j] - T0)
    + C_ig[i, "2"] * (T[j]**2 - T0**2) / 2
    + C_ig[i, "3"] * (T[j]**3 - T0**3) / 3
    + C_ig[i, "4"] * (T[j]**4 - T0**4) / 4
    + C_ig[i, "5"] * (T[j]**5 - T0**5) / 5
)

calc_Hvi[i, j] = Hvi[i, j] == DH_ig[i, j] + Hform[i]

calc_Hv[j] = Hv[j] / H_factor == gp.Sum(i, y[i, j] * Hvi[i, j]) + HR[j]

Zvi_eq[i, j] = (
    -Zvi[i, j] + 1 + Betav_p(i, j) 
    - qv_p(i) * Betav_p(i, j) * (Zvi[i, j] - Betav_p(i, j)) / (Zvi[i, j] * (Zvi[i, j] + Betav_p(i, j))) == 0
)

v_eq[i, j] = v_mol_i[i, j] == Zvi[i, j] * R * Tb[i] / P[j]

calc_HR_pure[i, j] = HR_pure[i, j] == R * Tb[i] * (
    Zvi[i, j] - 1 + (Tb[i] * dadT_Tb[i] - ai_Tb[i]) / (bii[i] * R * Tb[i]) * gmath.log((v_mol_i[i, j] + bii[i]) / v_mol_i[i, j])
)

calc_DH_liq[i, j] = DH_liq[i, j] == (
    C_liq[i, "1"] * (T[j] - Tb[i])
    + C_liq[i, "2"] * (T[j]**2 - Tb[i]**2) / 2
    + C_liq[i, "3"] * (T[j]**3 - Tb[i]**3) / 3
    + C_liq[i, "4"] * (T[j]**4 - Tb[i]**4) / 4
    + C_liq[i, "5"] * (T[j]**5 - Tb[i]**5) / 5
)

calc_Hv_Tbi_P[i, j] = Hv_Tbi_P[i, j] == DH_ig_Tb[i] + Hform[i] + HR_pure[i, j]

calc_Hli[i, j] = Hli[i, j] == DH_liq[i, j] + Hv_Tbi_P[i, j] - DH_vap[i]

calc_Hl[j] = Hl[j] / H_factor == gp.Sum(i, x[i, j] * Hli[i, j])


# * ============================================================================ *
# * Chemical reaction rate
# * ============================================================================ *


# ---------------------------------------------------------------------------- #
# 1. Define the Subset
# ---------------------------------------------------------------------------- #
# Instead of NR1, NR2, NR3, we define a Set whose domain is [j].
# We pass the specific tray labels (as strings) into the records.
# records=[str(x) for x in range(3, 16)]
# reactive_trays = gp.Set(
#     m, 
#     name="reactive_trays", 
#     domain=[j], 
#     records=["3", "4", "5"], # List your reactive trays here
#     description="Subset of trays where reactions occur"
# )

# ---------------------------------------------------------------------------- #
# Variables (Same as before)
# ---------------------------------------------------------------------------- #
K_eq     = gp.Variable(m, name="K_eq", domain=[j])
k_rate   = gp.Variable(m, name="k_rate", domain=[j])
k_A      = gp.Variable(m, name="k_A", domain=[j])
Rxn_Rate = gp.Variable(m, name="Rxn_Rate", domain=[j])

def Xg(i_, j_): 
    return x[i_, j_] * gamma_nrtl[i_, j_]

# ---------------------------------------------------------------------------- #
# Equations Declaration (Same as before)
# ---------------------------------------------------------------------------- #
calc_K_eq    = gp.Equation(m, name="calc_K_eq", domain=[j])
calc_k_rate  = gp.Equation(m, name="calc_k_rate", domain=[j])
calc_k_A     = gp.Equation(m, name="calc_k_A", domain=[j])
calc_Rx_Rate = gp.Equation(m, name="calc_Rx_Rate", domain=[j])
assign_zero  = gp.Equation(m, name="assign_zero", domain=[j])

# ---------------------------------------------------------------------------- #
# 2. Define the Conditions using the Subset
# ---------------------------------------------------------------------------- #
# This is much cleaner and scales to any number of trays effortlessly.
cond_reactive = (gp.Ord(j) == NR1) | (gp.Ord(j) == NR2) | (gp.Ord(j) == NR3)

# The ~ operator perfectly inverts the subset to find the non-reactive trays
cond_non_reactive= ~((gp.Ord(j) == NR1) | (gp.Ord(j) == NR2) | (gp.Ord(j) == NR3))
# cond_non_reactive = (gp.Ord(j) != NR1) & (gp.Ord(j) != NR2) & (gp.Ord(j) != NR3)

# ---------------------------------------------------------------------------- #
# 3. Equations Definition
# ---------------------------------------------------------------------------- #
calc_K_eq[j].where[cond_reactive] = K_eq[j] == gmath.exp(
    10.387 + 4060.59 / T[j] - 2.89055 * gmath.log(T[j])
    - 0.01915144 * T[j] + 5.28586E-5 * T[j]**2 - 5.32977E-8 * T[j]**3
)

calc_k_rate[j].where[cond_reactive] = k_rate[j] == 7.41816E15 * gmath.exp(-60.4E3 / (R * T[j])) / 60

calc_k_A[j].where[cond_reactive] = k_A[j] == gmath.exp(-1.0707 + 1323.1 / T[j])

calc_Rx_Rate[j].where[cond_reactive] = Rxn_Rate[j] == (
    k_rate[j] * Xg("2", j) * (Xg("2", j) * Xg("3", j) - Xg("4", j) / K_eq[j]) 
    / (1 + k_A[j] * Xg("2", j))**3
)

# Set reaction rate to zero for non-reactive trays
assign_zero[j].where[cond_non_reactive] = Rxn_Rate[j] == 0



# * ============================================================================ *
# * MESHR model
# * ============================================================================ *

# ---------------------------------------------------------------------------- #
# Parameters (Specifications)
# ---------------------------------------------------------------------------- #
Spec_1 = gp.Parameter(m, name="Spec_1", description="Ethanol conversion")
Spec_1[...] = 0.85

Spec_2 = gp.Parameter(m, name="Spec_2", description="ETBE molar fraction on the bottom product")
Spec_2[...] = 0.83

# ---------------------------------------------------------------------------- #
# Domain Conditions (Masks)
# ---------------------------------------------------------------------------- #
# Define domains for interior trays, the condenser, and the reboiler
# cond_j = j.where[gp.Ord(j) <= Ns]
# 1. Store the logical expressions (the masks), NOT the .where() method
mask_interior = (gp.Ord(j) > 1) & (gp.Ord(j) < Ns)
mask_reboiler = (gp.Ord(j) == Ns)

# ---------------------------------------------------------------------------- #
# Efficiency Improvement: Feed Indicator Parameters
# ---------------------------------------------------------------------------- #
# 1. Declare the parameters
is_FE = gp.Parameter(m, name="is_FE", domain=[j], description="1 if tray is NFE, 0 otherwise")
is_FB = gp.Parameter(m, name="is_FB", domain=[j], description="1 if tray is NFB, 0 otherwise")

# 2. Initialize all trays to 0 (default state)
is_FE[...] = 0
is_FB[...] = 0

# 3. Assign 1 only to the trays that match the feed condition
# Initialize all to 0
is_FE[...] = 0
is_FB[...] = 0

# Directly assign 1 to the specific string index
is_FE[str(NFE)] = 1
is_FB[str(NFB)] = 1
# ---------------------------------------------------------------------------- #
# Equations Declaration
# ---------------------------------------------------------------------------- #
mol_balance_eq            = gp.Equation(m, name="mol_balance_eq", domain=[j])
mol_balance_condenser_eq  = gp.Equation(m, name="mol_balance_condenser_eq")
mol_balance_reboiler_eq   = gp.Equation(m, name="mol_balance_reboiler_eq", domain=[j])

comp_balance_eq           = gp.Equation(m, name="comp_balance_eq", domain=[i, j])
comp_balance_condenser_eq = gp.Equation(m, name="comp_balance_condenser_eq", domain=[i])
comp_balance_reboiler_eq  = gp.Equation(m, name="comp_balance_reboiler_eq", domain=[i, j])

eq_rel_eq                 = gp.Equation(m, name="eq_rel_eq", domain=[i, j])
summation_eq              = gp.Equation(m, name="summation_eq", domain=[j])

energy_balance_eq            = gp.Equation(m, name="energy_balance_eq", domain=[j])
energy_balance_condenser_eq  = gp.Equation(m, name="energy_balance_condenser_eq")
energy_balance_reboiler_eq   = gp.Equation(m, name="energy_balance_reboiler_eq", domain=[j])

# spec_1_eq = gp.Equation(m, name="spec_1_eq", domain=[j])
spec_2_eq = gp.Equation(m, name="spec_2_eq", domain=[j])
V1_eq     = gp.Equation(m, name="V1_eq")

# ---------------------------------------------------------------------------- #
# Equations Definition
# ---------------------------------------------------------------------------- #
# 1. Total Molar Balance
mol_balance_eq[j].where[mask_interior] = (
    L[j] + V[j] - V[j.lead(1)] - L[j.lag(1)]
    - FE * is_FE[j] - FB * is_FB[j]
    - gp.Sum(i, v_i[i] * m_cat * Rxn_Rate[j]) / F_factor == 0
)

mol_balance_condenser_eq[...] = (
    V["1"] + (L["1"] + D) - V["2"] == 0
)

mol_balance_reboiler_eq[j].where[mask_reboiler] = (
    V[j] + L[j] - L[j.lag(1)] == 0
)

# 2. Component Molar Balance
comp_balance_eq[i, j].where[mask_interior] = (
    L[j] * x[i, j] + V[j] * y[i, j] - V[j.lead(1)] * y[i, j.lead(1)] - L[j.lag(1)] * x[i, j.lag(1)]
    - FE * is_FE[j] * zE[i] - FB * is_FB[j] * zB[i] 
    - m_cat * v_i[i] * Rxn_Rate[j] / F_factor == 0
)

comp_balance_condenser_eq[i] = (
    V["1"] * y[i, "1"] + (L["1"] + D) * x[i, "1"] - V["2"] * y[i, "2"] == 0
)

comp_balance_reboiler_eq[i, j].where[mask_reboiler] = (
    V[j] * y[i, j] + L[j] * x[i, j] - L[j.lag(1)] * x[i, j.lag(1)] == 0
)

# 3. Equilibrium Relations & Summation
eq_rel_eq[i, j] = (
    K_part[i, j] * x[i, j] - y[i, j] == 0
)

summation_eq[j] = (
    gp.Sum(i, y[i, j] - x[i, j]) == 0
)

# 4. Energy Balance
energy_balance_eq[j].where[mask_interior] = (
    V[j] * Hv[j] + L[j] * Hl[j] - V[j.lead(1)] * Hv[j.lead(1)] - L[j.lag(1)] * Hl[j.lag(1)] 
    - FE * is_FE[j] * HFE - FB * is_FB[j] * HFB == 0
)

energy_balance_condenser_eq[...] = (
    V["1"] * Hv["1"] + (L["1"] + D) * Hl["1"] - V["2"] * Hv["2"] + Qc == 0
)

energy_balance_reboiler_eq[j].where[mask_reboiler] = (
    V[j] * Hv[j] + L[j] * Hl[j] - L[j.lag(1)] * Hl[j.lag(1)] - Qr == 0
)

# 5. Specifications
# Note: I included the commented-out spec_1_eq for completeness
# spec_1_eq[j].where[mask_reboiler] = (
#     (FE - D * x["2", "1"] - L[j] * x["2", j]) / FE == Spec_1
# )

spec_2_eq[j].where[mask_reboiler]  = (
    x["4", j] == Spec_2
)

V1_eq[...] = (
    V["1"] == 0
)

# * ============================================================================ *
# * Equipment Sizing, Costs & Economics (Refactored for NLP)
# * ============================================================================ *


# ---------------------------------------------------------------------------- #
# Parameters & Scalars
# ---------------------------------------------------------------------------- #
# Efficiency Improvement: Instead of defining FF as a GAMS formula, we calculate
# the constant in pure Python first. This simplifies the symbolic equation graph.
FF_value = 1.51 * (0.45359237 / 0.3048)**0.5
FF = gp.Parameter(m, name="FF", description="Flooding velocity estimation parameter")
FF[...] = FF_value

MS = gp.Parameter(m, name="MS", description="Marshall & Swift Parameter")
MS[...] = 1773.4

CostETBE = gp.Parameter(m, name="CostETBE", description="Price of ETBE bottom product [$/mol]")
CostETBE[...] = 25.3e-3

CostEth = gp.Parameter(m, name="CostEth", description="Price of Ethanol [$/mol]")
CostEth[...] = 15.0e-3

CostBut = gp.Parameter(m, name="CostBut", description="Price of Butenes [$/mol]")
CostBut[...] = 8.25e-3

c_steam = gp.Parameter(m, name="c_steam", description="Steam cost parameter [$/J]")
c_steam[...] = 4.54e-9

# ---------------------------------------------------------------------------- #
# Variables
# ---------------------------------------------------------------------------- #
D_col      = gp.Variable(m, name="D_col", domain=[j], description="Column diameter (ft)")
Dcol_max   = gp.Variable(m, name="Dcol_max", description="Maximum column diameter (ft)")
Mw_mix     = gp.Variable(m, name="Mw_mix", domain=[j], description="Molecular weights (kg/kmol)")

Tcond      = gp.Variable(m, name="Tcond", description="Condenser temperature (K)")
Treb       = gp.Variable(m, name="Treb", description="Reboiler Temperature (K)")
Breb       = gp.Variable(m, name="Breb", description="Bottoms flowrate")

# Unused/Commented out Area variables are still declared here for completeness
v_AreaCond = gp.Variable(m, name="v_AreaCond", description="Condenser heat transfer area (ft2)")
v_AreaReb  = gp.Variable(m, name="v_AreaReb", description="Reboiler heat transfer area (ft2)")

v_ColCost  = gp.Variable(m, name="v_ColCost", description="Column shell cost ($)")
v_TrayCost = gp.Variable(m, name="v_TrayCost", description="Tray cost ($)")
v_CondCost = gp.Variable(m, name="v_CondCost", description="Condenser cost ($)")
v_RebCost  = gp.Variable(m, name="v_RebCost", description="Reboiler cost ($)")
CAP_cost   = gp.Variable(m, name="CAP_cost", description="Capital cost ($/yr)")
OP_cost    = gp.Variable(m, name="OP_cost", description="Operational cost ($/yr)")
Profit     = gp.Variable(m, name="Profit", description="Annual Profit (Millions $)")
obj        = gp.Variable(m, name="obj", description="Objective Function Variable")

# ---------------------------------------------------------------------------- #
# CRITICAL: Prevent Solver Domain Errors (Logarithms and Fractional Powers)
# ---------------------------------------------------------------------------- #
# In the Condenser Cost: log((Tcond - 303.15) / (Tcond - 313.15))
# If Tcond <= 313.15, the denominator is <= 0, causing a fatal log(negative) crash.
Tcond.lo[...] = 313.2  

# In the Reboiler Cost: (433.15 - Treb)**0.65
# If Treb >= 433.15, the base of the fractional power is negative, causing a crash.
Treb.up[...] = 433.1  

# ---------------------------------------------------------------------------- #
# Equations Declaration
# ---------------------------------------------------------------------------- #
def_D_col    = gp.Equation(m, name="def_D_col", domain=[j])
def_Mw_mix   = gp.Equation(m, name="def_Mw_mix", domain=[j])
def_Dcol_max = gp.Equation(m, name="def_Dcol_max", domain=[j])

def_Tcond    = gp.Equation(m, name="def_Tcond")
def_Treb     = gp.Equation(m, name="def_Treb", domain=[j])
def_Breb     = gp.Equation(m, name="def_Breb", domain=[j])

eq_ColCost   = gp.Equation(m, name="eq_ColCost")
eq_TrayCost  = gp.Equation(m, name="eq_TrayCost")
eq_CondCost  = gp.Equation(m, name="eq_CondCost")
eq_RebCost   = gp.Equation(m, name="eq_RebCost")
eq_CAP_cost  = gp.Equation(m, name="eq_CAP_cost")
eq_OP_cost   = gp.Equation(m, name="eq_OP_cost")
def_Profit   = gp.Equation(m, name="def_Profit")
obj_def      = gp.Equation(m, name="obj_def")

# ---------------------------------------------------------------------------- #
# Equations Definition
# ---------------------------------------------------------------------------- #
def_Mw_mix[j] = Mw_mix[j] == gp.Sum(i, y[i, j] * Mw[i])

# Notice we use math.pi instead of a GAMS pi parameter
def_D_col[j].where[mask_interior] = D_col[j] == gmath.sqrt(
    4 * ((V[j] * F_factor * v_mol[j] / 60) / ((FF / gmath.sqrt(Mw_mix[j] * 1e-3 / v_mol[j])) * 0.88)) / np.pi
) * 3.28084

# The =G= operator naturally maps to >= in Python
def_Dcol_max[j].where[mask_interior] = Dcol_max >= D_col[j]

def_Tcond[...] = Tcond == T["1"]
def_Treb[j].where[mask_reboiler] = Treb == T[j]
def_Breb[j].where[mask_reboiler] = Breb == L[j]

eq_ColCost[...] = v_ColCost == (MS / 280) * (101.9 * (Dcol_max**1.066) * ((0.7315 * (Ns - 2) * 3.28084)**0.802) * 7.05)

eq_TrayCost[...] = v_TrayCost == (MS / 280) * (4.7 * (Dcol_max**1.55) * (0.7315 * (Ns - 2) * 3.28084) * 2.7)

eq_CondCost[...] = v_CondCost == (
    Qc * FH_factor / 60 / (150 / 0.17611 * (10 / gmath.log((Tcond - 303.15) / (Tcond - 313.15)))) * 10.7639
)**0.65 * 1709.8394439285714

eq_RebCost[...] = v_RebCost == (
    MS / 280 * 101.3 * ((Qr * FH_factor / 60 / ((250 / 0.17611) * (433.15 - Treb)) * 10.7639)**0.65 * 7.3525)
)

eq_CAP_cost[...] = CAP_cost == (1 / 3) * (v_TrayCost + v_ColCost + v_CondCost + v_RebCost + (7.7 * 3 * 0.4))

eq_OP_cost[...] = OP_cost == (
    (0.378e-9 * Qc + c_steam * Qr) * 8150 * 60 * FH_factor + 
    (FE * CostEth + FB * CostBut - CostETBE * Breb) * F_factor * 8150 * 60
)

def_Profit[...] = Profit * 1e6 == CAP_cost + OP_cost

obj_def[...] = obj == Profit

#  ============================================================================ *
#  Defining upper and lower bounds and scale
#  ============================================================================ *

# ---------------------------------------------------------------------------- #
# Basic Variables
# ---------------------------------------------------------------------------- #
L.lo[j] = 1e-5;  L.up[j] = 50;  L.l[j] = 0.5
V.lo[j] = 1e-5;  V.up[j] = 50;  V.l[j] = 0.5
V.lo["1"] = 0;   V.up["1"] = 0.001; V.l["1"] = 0

x.lo[i, j] = 0;  x.up[i, j] = 1;  x.l[i, j] = 0.25
y.lo[i, j] = 0;  y.up[i, j] = 1;  y.l[i, j] = 0.25

# For scalar variables (0-dimensional), we use [...] 
D.lo[...] = 0.01;     D.up[...] = 1;      D.l[...] = 0.5748006462583984
Qc.lo[...] = 0.01;    Qc.up[...] = 10;    Qc.l[...] = 0.5451343354854316
Qr.lo[...] = 0.01;    Qr.up[...] = 10;    Qr.l[...] = 0.4592022879232921
Breb.lo[...] = 0.001; Breb.up[...] = 1;   Breb.l[...] = 0.24

T.lo[j] = Tmin;  T.up[j] = Tmax;  T.scale[j] = TF_factor

FE.lo[...] = 0.00075; FE.up[...] = 37.43; FE.l[...] = 5.774 / F_factor

# ---------------------------------------------------------------------------- #
# Thermodynamics & Enthalpy Variables
# Note: We can use math.log(Tmin) natively because Tmin is a Python float!
# ---------------------------------------------------------------------------- #
logPsat.lo[i, j] = (
    kk[i, "1"] + kk[i, "2"] / (kk[i, "3"] + Tmin) 
    + kk[i, "4"] * Tmin + kk[i, "5"] * gmath.log(Tmin) 
    + kk[i, "6"] * (Tmin**kk[i, "7"])
)

logPsat.up[i, j] = (
    kk[i, "1"] + kk[i, "2"] / (kk[i, "3"] + Tmax) 
    + kk[i, "4"] * Tmax + kk[i, "5"] * gmath.log(Tmax) 
    + kk[i, "6"] * (Tmax**kk[i, "7"])
)
logPsat.scale[i, j] = 10

alpha_ij.lo[i, j] = 0.5;    alpha_ij.up[i, j] = 2
aii.lo[i, j] = 1;           aii.up[i, j] = 4
a.lo[j] = 1;                a.up[j] = 3
b.lo[j] = 1e-5;             b.up[j] = 1e-3;           b.scale[j] = 1e-5
dadT_ii.lo[i, j] = -0.009;  dadT_ii.up[i, j] = -0.001; dadT_ii.scale[i, j] = 1e-3
dadT.lo[j] = -0.009;        dadT.up[j] = -0.001;       dadT.scale[j] = 1e-3
K_part.lo[i, j] = 0.001;    K_part.up[i, j] = 10
phi.lo[i, j] = 0.1;         phi.up[i, j] = 1.2

DH_ig.lo[i, j] = (
    C_ig[i, "1"] * (Tmin - T0) + C_ig[i, "2"] * (Tmin**2 - T0**2) / 2
    + C_ig[i, "3"] * (Tmin**3 - T0**3) / 3 + C_ig[i, "4"] * (Tmin**4 - T0**4) / 4
    + C_ig[i, "5"] * (Tmin**5 - T0**5) / 5
)
DH_ig.up[i, j] = (
    C_ig[i, "1"] * (Tmax - T0) + C_ig[i, "2"] * (Tmax**2 - T0**2) / 2
    + C_ig[i, "3"] * (Tmax**3 - T0**3) / 3 + C_ig[i, "4"] * (Tmax**4 - T0**4) / 4
    + C_ig[i, "5"] * (Tmax**5 - T0**5) / 5
)
DH_ig.scale[i, j] = 1e3

Hvi.lo[i, j] = DH_ig.lo[i, j] + Hform[i]
Hvi.up[i, j] = DH_ig.up[i, j] + Hform[i]
Hvi.scale[i, j] = 1e5

HR.lo[j] = -2500;  HR.up[j] = -1100;  HR.scale[j] = 1e3

# GAMS smin/smax translate to gp.Smin/gp.Smax
Hv.lo[j] = (gp.Smin(i, Hvi.lo[i, j]) + HR.lo[j]) * H_factor
Hv.up[j] = (gp.Smax(i, Hvi.up[i, j]) + HR.up[j]) * H_factor

DH_liq.lo[i, j] = (
    C_liq[i, "1"] * (Tmin - Tb[i]) + C_liq[i, "2"] * (Tmin**2 - Tb[i]**2) / 2
    + C_liq[i, "3"] * (Tmin**3 - Tb[i]**3) / 3 + C_liq[i, "4"] * (Tmin**4 - Tb[i]**4) / 4
    + C_liq[i, "5"] * (Tmin**5 - Tb[i]**5) / 5
)
DH_liq.up[i, j] = (
    C_liq[i, "1"] * (Tmax - Tb[i]) + C_liq[i, "2"] * (Tmax**2 - Tb[i]**2) / 2
    + C_liq[i, "3"] * (Tmax**3 - Tb[i]**3) / 3 + C_liq[i, "4"] * (Tmax**4 - Tb[i]**4) / 4
    + C_liq[i, "5"] * (Tmax**5 - Tb[i]**5) / 5
)
DH_liq.scale[i, j] = 1e4

HR_pure.lo[i, j] = -3e3;  HR_pure.up[i, j] = -1e3; HR_pure.scale[i, j] = 1e3

Hv_Tbi_P.lo[i, j] = DH_ig_Tb[i] * 0.99 + Hform[i] + HR_pure.lo[i, j]
Hv_Tbi_P.up[i, j] = DH_ig_Tb[i] * 1.01 + Hform[i] + HR_pure.up[i, j]
Hv_Tbi_P.scale[i, j] = 1e4

Hli.lo[i, j] = DH_liq.lo[i, j] + Hv_Tbi_P.lo[i, j] - DH_vap[i]
Hli.up[i, j] = DH_liq.up[i, j] + Hv_Tbi_P.up[i, j] - DH_vap[i]
Hli.scale[i, j] = 1e5

# Following the original code logic (using Hvi for Hl bounds)
Hl.lo[j] = gp.Smin(i, Hvi.lo[i, j]) * H_factor
Hl.up[j] = gp.Smax(i, Hvi.up[i, j]) * H_factor

# ---------------------------------------------------------------------------- #
# Molar Volume & Compressibility
# ---------------------------------------------------------------------------- #
Z.lo[j] = 0.75; Z.up[j] = 0.9; Z.l[j] = 0.822
v_mol.lo[j] = Z.lo[j] * R * Tmin / 9.5e5
v_mol.up[j] = Z.up[j] * R * Tmax / 9.5e5
v_mol.scale[j] = 1e-3

Zvi.lo[i, j] = 0.75; Zvi.up[i, j] = 1; Zvi.l[i, j] = 0.9
v_mol_i.lo[i, j] = Zvi.lo[i, j] * R * Tmin / 9.5e5
v_mol_i.up[i, j] = Zvi.up[i, j] * R * Tmax / 9.5e5
v_mol_i.scale[i, j] = 1e-3

gamma_nrtl.lo[i, j] = 0.01; gamma_nrtl.up[i, j] = 20

# ---------------------------------------------------------------------------- #
# Efficiency Improvement: Pure Python Bound Calculations
# ---------------------------------------------------------------------------- #
# Since Tmax/Tmin are standard Python constants, we don't need GAMSPY to build 
# an equation graph here. We use pure standard Python math to calculate the float 
# and pass it directly to the bound assignment.
K_eq.lo[j] = gmath.exp(10.387 + 4060.59 / Tmax - 2.89055 * gmath.log(Tmax) - 0.01915144 * Tmax + 5.28586E-5 * Tmax**2 - 5.32977E-8 * Tmax**3)
K_eq.up[j] = gmath.exp(10.387 + 4060.59 / Tmin - 2.89055 * gmath.log(Tmin) - 0.01915144 * Tmin + 5.28586E-5 * Tmin**2 - 5.32977E-8 * Tmin**3)
K_eq.scale[j] = 10

k_rate.lo[j] = 7.41816E15 * gmath.exp(-60.4E3 / (R * Tmin)) / 60
k_rate.up[j] = 7.41816E15 * gmath.exp(-60.4E3 / (R * Tmax)) / 60
k_rate.scale[j] = 1e4

k_A.lo[j] = gmath.exp(-1.0707 + 1323.1 / Tmax)
k_A.up[j] = gmath.exp(-1.0707 + 1323.1 / Tmin)
k_A.scale[j] = 10

Rxn_Rate.lo[j] = -10; Rxn_Rate.up[j] = 10

# ---------------------------------------------------------------------------- #
# Equipment & Costing Bounds
# ---------------------------------------------------------------------------- #
Mw_mix.lo[j] = 45; Mw_mix.up[j] = 103; Mw_mix.scale[j] = 10

D_col.lo[j] = 0.001; D_col.up[j] = 2; D_col.l[j] = 0.03; D_col.scale[j] = 0.1
Dcol_max.lo[...] = 0.001; Dcol_max.up[...] = 2
# ============================================================================ #
# CRITICAL INITIALIZATIONS: Mimicking GAMS Default States
# ============================================================================ #

# 1. Column Profiles (Flat starts to prevent mass-balance singularities)
T.l[j] = 350
Tcond.l[...] = 330
Treb.l[...] = 400
L.l[j] = 0.5
V.l[j] = 0.5
V.l["1"] = 0.1  # Do not start condenser vapor at exact 0
x.l[i, j] = 0.25
y.l[i, j] = 0.25

# 2. Phase Equilibrium (K_part * x = y -> 1.0 * 0.25 = 0.25)
K_part.l[i, j] = 1.0
logPsat.l[i, j] = 11.5  
gamma_nrtl.l[i, j] = 1.0
phi.l[i, j] = 1.0

# 3. SRK & Mixture Properties
alpha_ij.l[i, j] = 1.0
aii.l[i, j] = 2.0
a.l[j] = 2.0
b.l[j] = 1e-4
dadT_ii.l[i, j] = -0.005
dadT.l[j] = -0.005
Z.l[j] = 0.822
Zvi.l[i, j] = 0.9
v_mol.l[j] = 0.003
v_mol_i.l[i, j] = 0.003
Mw_mix.l[j] = 60.0

# 4. Kinetics
K_eq.l[j] = 10.0
k_rate.l[j] = 100.0
k_A.l[j] = 10.0
Rxn_Rate.l[j] = 0.0

# 5. Enthalpies
DH_ig.l[i, j] = 5000.0
Hvi.l[i, j] = -150000.0
Hv.l[j] = 100.0
DH_liq.l[i, j] = 1000.0
HR_pure.l[i, j] = -2000.0
Hv_Tbi_P.l[i, j] = -150000.0
Hli.l[i, j] = -180000.0
Hl.l[j] = 100.0

#####################################################
# VALIDATION
# int
# Whether to enable all validations of GAMSPy. Set to 1 by default.
# GAMSPy validations are essential during development. Setting VALIDATION to 0 should only be done to improve the performance by skipping the validation steps after you are convinced that your model works as intended.
gp.set_options({"DOMAIN_VALIDATION": 1})
#######################################################

##
# 1. Define the Model
meshr_model = gp.Model(
    container=m,
    name="MESHR_Optimization",
    equations=m.getEquations(),
    problem="NLP",
    sense=gp.Sense.MIN,
    objective=obj
)

# define solver options 

options = gp.Options(
    relative_optimality_gap=1e-4,
    # absolute_optimality_gap=0,
    time_limit=60,
    threads=10,
    enable_scaling=True
)

# 2. Solve the Model
meshr_model.solve(
    solver="BARON",
    # Global GAMS engine settings
    options=options,
    output=sys.stdout
)
# options=gp.Options(
#     optfile=1  # Tells GAMS to look for a file named conopt.opt
# )
# Print the solver version
print(meshr_model.solver_version)
print(f"Solver Status: {meshr_model.status}")
print(f"Final Objective Value: {obj.toValue()}")
# ---------------------------------------------------------------------------- #
# 3. Access the Results
# ---------------------------------------------------------------------------- #
# Print the solver status to ensure it solved optimally
print(f"Solver Status: {meshr_model.status}")

# 2. Extract and print the exact violations
print("\n--- ANALYZING INFEASIBILITIES ---")
infeasibilities = meshr_model.computeInfeasibilities()

for name, df in infeasibilities.items():
    if not df.empty:
        print(f"\nViolation found in: {name}")
        print(df)
# Print the final objective value using .toValue()
print(f"Final Objective Value: {obj.toValue()}")

# You can access the final values of any other variable using .records
# For example, to view the liquid flow rates across all trays:
# print(L.records)
import matplotlib.pyplot as plt

# Grab the data
df = T.records
# Convert stage index to numeric for plotting
df['j'] = df['j'].astype(int)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(df['j'], df['level'], marker='o', linestyle='-')
plt.title("Optimized Temperature Profile")
plt.xlabel("Stage Number")
plt.ylabel("Temperature (K)")
plt.grid(True)
plt.show()

import os

# Create an output directory if it doesn't exist
output_dir = "optimization_results"
os.makedirs(output_dir, exist_ok=True)

# Define your list of variables
results_to_export = {
    "L": L,
    "V": V,
    "x": x,
    "y": y,
    "T": T,
    "Qr": Qr,
    "Qc": Qc,
    "D": D,
    "Dcol_max": Dcol_max
}

# Loop through and export each one
for name, var in results_to_export.items():
    # .records returns the Pandas DataFrame
    df = var.records
    
    # Save to CSV
    filename = os.path.join(output_dir, f"{name}_results.csv")
    df.to_csv(filename, index=False)
    print(f"Exported {name} to {filename}")