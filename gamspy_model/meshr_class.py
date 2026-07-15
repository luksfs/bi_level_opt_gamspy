import gamspy as gp
import gamspy.math as gmath
import numpy as np
import pandas as pd
import sys
import os

class ReactiveDistillationModel:
    def __init__(self, max_stages=22):
        """
        Initializes the Container, Sets, and structural Equations.
        max_stages defines the absolute maximum size of the column matrix.
        """
        self.m = gp.Container()
        self.max_stages = max_stages
        
        print("Compiling MESHR Superstructure (This only happens once)...")
        self._build_sets()
        self._build_parameters()
        self._build_variables()
        self._build_equations()
        self._initialize_bounds_and_scales()
        
        # Compile the Model object
        self.model = gp.Model(
            container=self.m,
            name="MESHR_Superstructure",
            equations=self.m.getEquations(),
            problem="NLP",
            sense=gp.Sense.MIN,
            objective=self.obj,

        )
        print("Compilation complete.")

    def _build_sets(self):
        self.i = gp.Set(self.m, name="i", records=[str(x) for x in range(1, 5)])
        self.j = gp.Set(self.m, name="j", records=[str(x) for x in range(1, self.max_stages + 1)])
        self.c = gp.Set(self.m, name="c", records=[str(x) for x in range(1, 8)])
        self.cc = gp.Set(self.m, name="cc", records=[str(x) for x in range(1, 6)])
        
        # Aliases
        self.k = gp.Alias(self.m, name="k", alias_with=self.i)
        self.h = gp.Alias(self.m, name="h", alias_with=self.i)
        self.m_alias = gp.Alias(self.m, name="m_alias", alias_with=self.i)

    def _build_parameters(self):
        # 1. Structural Parameters (These make the superstructure dynamic)
        self.Ns = gp.Parameter(self.m, name="Ns", description="Current active stages")
        self.is_FE = gp.Parameter(self.m, name="is_FE", domain=[self.j])
        self.is_FB = gp.Parameter(self.m, name="is_FB", domain=[self.j])
        self.is_reactive = gp.Parameter(self.m, name="is_reactive", domain=[self.j])
        
        # Initialize defaults
        self.Ns[...] = 10
        self.is_FE[...] = 0
        self.is_FB[...] = 0
        self.is_reactive[...] = 0

        # 2. Physics & Cost Parameters (From original code)
        self.P = gp.Parameter(self.m, name="P", domain=[self.j])
        self.P[...] = 9.5e5
        
        self.m_cat = 0.4
        self.R = 8.314463
        self.Tmin = 330
        self.Tmax = 410

        # Catalyst volume calc and flooding velocity
        self.rho_cat = 770 # kg/m3
        self.phi_c = 0.3
        # self.h_pack = 0.3048 # m
        self.ht = gp.Parameter(self.m, "ht", records=0.4572)
        self.rho_cat = gp.Parameter(self.m, "rho_cat", records=770)
        self.phi_c = gp.Parameter(self.m, "phi_c", records=0.3)
        self.h_pack = gp.Parameter(self.m, "h_pack")
        self.rhoL =gp.Parameter(self.m, "rhoL", records=580e3)
        self.sigma_g = gp.Parameter(self.m, "sigma_g", records=7.2)

        self.a1 = gp.Parameter(self.m, "a1", records=1.0262)
        self.a2 = gp.Parameter(self.m, "a2", records=0.63513)
        self.a3 = gp.Parameter(self.m, "a3", records=0.20097)

        self.h_pack[...] = self.ht / 2

        self.v_i = gp.Parameter(self.m, name="v_i", domain=[self.i], records=[("1", 0), ("2", -1), ("3", -1), ("4", 1)])
        self.Tc = gp.Parameter(self.m, name="Tc", domain=[self.i], records=[("1", 419.5), ("2", 514), ("3", 417.9), ("4", 509.4)])
        self.Pc = gp.Parameter(self.m, name="Pc", domain=[self.i], records=[("1", 4.02E6), ("2", 6.137E6), ("3", 4.0E6), ("4", 2.934E6)])
        self.w = gp.Parameter(self.m, name="w", domain=[self.i], records=[("1", 0.184495), ("2", 0.643558), ("3", 0.19484), ("4", 0.316231)])
        self.Tb = gp.Parameter(self.m, name="Tb", domain=[self.i], records=[("1", 342.6), ("2", 421.5), ("3", 341.8), ("4", 441.4)])
        self.Mw = gp.Parameter(self.m, name="Mw", domain=[self.i], records=[("1", 56.10752), ("2", 46.06904), ("3", 56.10752), ("4", 102.17656)])
        self.Hform = gp.Parameter(self.m, name="Hform", domain=[self.i], records=[("1", -500), ("2", -234950), ("3", -17100), ("4", -313900)])
        self.zE = gp.Parameter(self.m, name="zE", domain=[self.i], records=[("1", 0), ("2", 1), ("3", 0), ("4", 0)])
        self.zB = gp.Parameter(self.m, name="zB", domain=[self.i], records=[("1", 0.7), ("2", 0), ("3", 0.3), ("4", 0)])

        # SRK Derived Parameters
        self.Omega_a = 0.42747
        self.Omega_b = 0.08664
        self.kappa = gp.Parameter(self.m, name="kappa", domain=[self.i])
        self.ac = gp.Parameter(self.m, name="ac", domain=[self.i])
        self.bii = gp.Parameter(self.m, name="bii", domain=[self.i])
        self.kappa[self.i] = 0.480 + 1.574 * self.w[self.i] - 0.176 * self.w[self.i]**2
        self.ac[self.i] = self.Omega_a * (self.R * self.Tc[self.i])**2 / self.Pc[self.i]
        self.bii[self.i] = self.Omega_b * self.R * self.Tc[self.i] / self.Pc[self.i]

        # Feed & Scaling
        hfb_d_val, hfe_d_val = -21481.62933928521, -273241.2338487912
        self.F_factor = 1.7118 + 5.774
        self.FH_factor = 1.7118 * abs(hfe_d_val) + 5.774 * abs(hfb_d_val)
        self.H_factor = self.F_factor / self.FH_factor
        self.TF_factor = (342.38 + 325) / 2
        
        self.HFE = gp.Parameter(self.m, name="HFE", records=hfe_d_val * self.H_factor)
        self.HFB = gp.Parameter(self.m, name="HFB", records=hfb_d_val * self.H_factor)
        self.FB = gp.Parameter(self.m, name="FB", records=5.774 / self.F_factor)

        # Specifications & Costs
        self.Spec_1 = gp.Parameter(self.m, name="Spec_1", records=0.85)
        self.Spec_2 = gp.Parameter(self.m, name="Spec_2", records=0.83)
        self.FF = gp.Parameter(self.m, name="FF", records=1.51 * (0.45359237 / 0.3048)**0.5)
        self.MS = gp.Parameter(self.m, name="MS", records=1773.4)
        self.CostETBE = gp.Parameter(self.m, name="CostETBE", records=25.3e-3)
        self.CostEth = gp.Parameter(self.m, name="CostEth", records=15.0e-3)
        self.CostBut = gp.Parameter(self.m, name="CostBut", records=8.25e-3)
        self.c_steam = gp.Parameter(self.m, name="c_steam", records=4.54e-9)

        # --- Data Tables ---
        self._load_tables()

    def _load_tables(self):
        # Antoine
        self.kk = gp.Parameter(self.m, name="kk", domain=[self.i, self.c])
        kk_data = [
            ["1", 51.836, -4019.2, 0, 0, -4.5229, 4.8833E-17, 6],
            ["2", 73.304, -7122.3, 0, 0, -7.1424, 2.8853E-06, 2],
            ["3", 78.01,  -4634.1, 0, 0, -8.9575, 1.3413E-05, 2],
            ["4", 64.188, -5820.2, 0, 0, -6.1343, 2.1405E-17, 6]
        ]
        self.kk.setRecords(pd.DataFrame(kk_data, columns=["i", "1", "2", "3", "4", "5", "6", "7"]).melt(id_vars=["i"], var_name="c", value_name="value"))

        # NRTL
        self.b_nrtl = gp.Parameter(self.m, name="b_nrtl", domain=[self.i, self.i])
        self.c_nrtl = gp.Parameter(self.m, name="c_nrtl", domain=[self.i, self.i])
        b_data = [("1", "2", 595.529982), ("1", "3", 110.239086), ("1", "4", 226.373398), ("2", "1", 164.57256), ("2", "3", 141.963213), ("2", "4", 187.104064), ("3", "1", -95.4252161),("3", "2", 623.581001), ("3", "4", 219.73407), ("4", "1", -177.88565), ("4", "2", 344.481315), ("4", "3", -172.59152)]
        c_data = [("1", "1", 0.0), ("1", "2", 0.3), ("1", "3", 0.3), ("1", "4", 0.3), ("2", "1", 0.3), ("2", "2", 0.0), ("2", "3", 0.3), ("2", "4", 0.3), ("3", "1", 0.3), ("3", "2", 0.3), ("3", "3", 0.0), ("3", "4", 0.3), ("4", "1", 0.3), ("4", "2", 0.3), ("4", "3", 0.3), ("4", "4", 0.0)]
        self.b_nrtl.setRecords(pd.DataFrame(b_data, columns=["i_1", "i_2", "value"]))
        self.c_nrtl.setRecords(pd.DataFrame(c_data, columns=["i_1", "i_2", "value"]))

        # Heat Capacities
        self.C_ig = gp.Parameter(self.m, name="C_ig", domain=[self.i, self.cc])
        self.C_liq = gp.Parameter(self.m, name="C_liq", domain=[self.i, self.cc])
        self.C_vap = gp.Parameter(self.m, name="C_vap", domain=[self.i, self.cc])
        ig_data = [["1", 111.022862, -0.750243683, 0.00374664805, -6.16980174E-06, 3.65183052E-09], ["2", 78.1195715, -0.495919524, 0.00257066991, -4.30332398E-06, 2.57806954E-09], ["3", 150.319619, -0.966221476, 0.00404410804, -6.00376885E-06, 3.23582716E-09], ["4", 47.4579586, -0.349114826, 0.00180207897, -3.04885369E-06, 1.83440907E-09]]
        liq_data = [["1", 2.42239762e+05, -2.74746461e+03, 1.16801221e+01, -2.20506997e-02, 1.56048214e-05], ["2", 1.21280234e+03, -1.30223888e+01, 5.71358761e-02, -1.12370042e-04, 8.73258381e-08], ["3", 3.08689696e+05, -3.49815711e+03, 1.48572135e+01, -2.80226414e-02, 1.98131733e-05], ["4", 1.20736602e+03, -1.29812644e+01, 5.93572571e-02, -1.16271343e-04, 8.66983296e-08]]
        vap_data = [["1", 33774, 0.5107, -0.17304, 0.05181, 0], ["2", 65831, 1.1905, -1.7666, 1.0012, 0], ["3", 43172, 1.5334, -1.9, 0.83816, 0], ["4", 45290, 0.27343, 0.21645, -0.11756, 0]]
        self.C_ig.setRecords(pd.DataFrame(ig_data, columns=["i", "1", "2", "3", "4", "5"]).melt(id_vars=["i"], var_name="cc", value_name="val"))
        self.C_liq.setRecords(pd.DataFrame(liq_data, columns=["i", "1", "2", "3", "4", "5"]).melt(id_vars=["i"], var_name="cc", value_name="val"))
        self.C_vap.setRecords(pd.DataFrame(vap_data, columns=["i", "1", "2", "3", "4", "5"]).melt(id_vars=["i"], var_name="cc", value_name="val"))

        # Pre-calculated Thermodynamic Scalars
        self.Tbr = gp.Parameter(self.m, name="Tbr", domain=[self.i])
        self.alpha_Tb = gp.Parameter(self.m, name="alpha_Tb", domain=[self.i])
        self.ai_Tb = gp.Parameter(self.m, name="ai_Tb", domain=[self.i])
        self.dadT_Tb = gp.Parameter(self.m, name="dadT_Tb", domain=[self.i])
        self.DH_vap = gp.Parameter(self.m, name="DH_vap", domain=[self.i])
        self.DH_ig_Tb = gp.Parameter(self.m, name="DH_ig_Tb", domain=[self.i])
        self.T0 = 298.15
        
        self.Tbr[self.i] = self.Tb[self.i] / self.Tc[self.i]
        self.alpha_Tb[self.i] = (1 + self.kappa[self.i] * (1 - self.Tbr[self.i]**0.5))**2
        self.ai_Tb[self.i] = self.alpha_Tb[self.i] * self.ac[self.i]
        self.dadT_Tb[self.i] = -self.ac[self.i] * self.kappa[self.i] * gmath.sqrt(self.alpha_Tb[self.i] * self.Tbr[self.i]) / self.Tb[self.i]
        self.DH_vap[self.i] = self.C_vap[self.i, "1"] * (1 - self.Tbr[self.i])**(self.C_vap[self.i, "2"] + self.C_vap[self.i, "3"]*self.Tbr[self.i] + self.C_vap[self.i, "4"]*(self.Tbr[self.i]**2) + self.C_vap[self.i, "5"]*(self.Tbr[self.i]**3))
        self.DH_ig_Tb[self.i] = (self.C_ig[self.i, "1"] * (self.Tb[self.i] - self.T0) + self.C_ig[self.i, "2"] * (self.Tb[self.i]**2 - self.T0**2) / 2 + self.C_ig[self.i, "3"] * (self.Tb[self.i]**3 - self.T0**3) / 3 + self.C_ig[self.i, "4"] * (self.Tb[self.i]**4 - self.T0**4) / 4 + self.C_ig[self.i, "5"] * (self.Tb[self.i]**5 - self.T0**5) / 5)

    def _build_variables(self):
        # Column Profile
        self.L = gp.Variable(self.m, name="L", domain=[self.j], type="Positive")
        self.V = gp.Variable(self.m, name="V", domain=[self.j], type="Positive")
        self.x = gp.Variable(self.m, name="x", domain=[self.i, self.j], type="Positive")
        self.y = gp.Variable(self.m, name="y", domain=[self.i, self.j], type="Positive")
        self.T = gp.Variable(self.m, name="T", domain=[self.j], type="Positive")
        
        # Performance & Economics
        self.FE = gp.Variable(self.m, name="FE", type="Positive")
        self.D = gp.Variable(self.m, name="D", type="Positive")
        self.Qc = gp.Variable(self.m, name="Qc", type="Positive")
        self.Qr = gp.Variable(self.m, name="Qr", type="Positive")
        self.Breb = gp.Variable(self.m, name="Breb")
        self.Tcond = gp.Variable(self.m, name="Tcond")
        self.Treb = gp.Variable(self.m, name="Treb")
        
        # self.D_col = gp.Variable(self.m, name="D_col")
        # self.Dcol_max = gp.Variable(self.m, name="Dcol_max")
        self.Dcol = gp.Variable(self.m, "Dcol")

        self.Mw_mix_V = gp.Variable(self.m, "Mw_mix_V", domain=self.j)
        self.Mw_mix_L = gp.Variable(self.m, "Mw_mix_L", domain=self.j)

        self.Flv = gp.Variable(self.m, "Flv", domain=self.j)
        self.CF =gp.Variable(self.m, "CF", domain=self.j)

        self.ufl = gp.Variable(self.m, "ufl", domain=self.j)
        self.uf = gp.Variable(self.m, "uf", domain=self.j)
        
        self.v_ColCost = gp.Variable(self.m, name="v_ColCost")
        self.v_TrayCost = gp.Variable(self.m, name="v_TrayCost")
        self.v_CondCost = gp.Variable(self.m, name="v_CondCost")
        self.v_RebCost = gp.Variable(self.m, name="v_RebCost")
        self.CAP_cost = gp.Variable(self.m, name="CAP_cost")
        self.OP_cost = gp.Variable(self.m, name="OP_cost")
        self.Profit = gp.Variable(self.m, name="Profit")
        self.obj = gp.Variable(self.m, name="obj")

        # Thermodynamics
        self.logPsat = gp.Variable(self.m, name="logPsat", type="positive", domain=[self.i, self.j])
        self.Z = gp.Variable(self.m, name="Z", domain=[self.j])
        self.v_mol = gp.Variable(self.m, name="v_mol", domain=[self.j])
        self.phi = gp.Variable(self.m, name="phi", domain=[self.i, self.j])
        self.HR = gp.Variable(self.m, name="HR", domain=[self.j])
        self.alpha_ij = gp.Variable(self.m, name="alpha_ij", domain=[self.i, self.j])
        self.aii = gp.Variable(self.m, name="aii", domain=[self.i, self.j])
        self.a = gp.Variable(self.m, name="a", domain=[self.j])
        self.b = gp.Variable(self.m, name="b", domain=[self.j])
        self.dadT_ii = gp.Variable(self.m, name="dadT_ii", domain=[self.i, self.j])
        self.dadT = gp.Variable(self.m, name="dadT", domain=[self.j])
        
        self.gamma_nrtl = gp.Variable(self.m, name="gamma_nrtl", domain=[self.i, self.j])
        self.K_part = gp.Variable(self.m, name="K_part", type="positive", domain=[self.i, self.j])
        
        self.DH_ig = gp.Variable(self.m, name="DH_ig", domain=[self.i, self.j])
        self.Hvi = gp.Variable(self.m, name="Hvi", domain=[self.i, self.j])
        self.Hv = gp.Variable(self.m, name="Hv", domain=[self.j])
        self.DH_liq = gp.Variable(self.m, name="DH_liq", domain=[self.i, self.j])
        self.Hv_Tbi_P = gp.Variable(self.m, name="Hv_Tbi_P", domain=[self.i, self.j])
        self.Hli = gp.Variable(self.m, name="Hli", domain=[self.i, self.j])
        self.Hl = gp.Variable(self.m, name="Hl", domain=[self.j])
        self.HR_pure = gp.Variable(self.m, name="HR_pure", domain=[self.i, self.j])
        self.Zvi = gp.Variable(self.m, name="Zvi", type="positive", domain=[self.i, self.j])
        self.v_mol_i = gp.Variable(self.m, name="v_mol_i", type="positive", domain=[self.i, self.j])

        # Kinetics
        self.K_eq = gp.Variable(self.m, name="K_eq", domain=[self.j])
        self.k_rate = gp.Variable(self.m, name="k_rate", domain=[self.j])
        self.k_A = gp.Variable(self.m, name="k_A", domain=[self.j])
        self.Rxn_Rate = gp.Variable(self.m, name="Rxn_Rate", domain=[self.j])

    def _build_equations(self):
        # -------------------------------------------------------------------- #
        # LOCAL MACROS (Replaces explicit variables to prevent math errors)
        # -------------------------------------------------------------------- #
        # def Tr_m(i_, j_): return self.T[j_] / self.Tc[i_]
        # def Betav_m(j_): return (self.b[j_] * self.P[j_]) / (self.R * self.T[j_])
        # def qv_m(j_): return self.a[j_] / (self.b[j_] * self.R * self.T[j_])
        # def tao_nrtl_m(i_, k_, j_): return 

        # def g_nrtl_m(i_, k_, j_): return gmath.exp(-self.c_nrtl[i_, k_] * ( self.b_nrtl[i_, k_] / self.T[j_] ) )

        # def Xg_m(i_, j_): return self.x[i_, j_] * self.gamma_nrtl[i_, j_]
        # def Betav_p_m(i_, j_): return (self.bii[i_] * self.P[j_]) / (self.R * self.Tb[i_])
        # def qv_p_m(i_): return self.ai_Tb[i_] / (self.bii[i_] * self.R * self.Tb[i_])

        # -------------------------------------------------------------------- #
        # DYNAMIC MASKS (These dynamically evaluate based on self.Ns!)
        # -------------------------------------------------------------------- #
        cond_condenser = gp.Ord(self.j) == 1
        cond_interior  = (gp.Ord(self.j) > 1) & (gp.Ord(self.j) < self.Ns)
        cond_reboiler  = gp.Ord(self.j) == self.Ns
        cond_active    = gp.Ord(self.j) <= self.Ns
        cond_inactive  = gp.Ord(self.j) > self.Ns

        # -------------------------------------------------------------------- #
        # EQUATIONS
        # -------------------------------------------------------------------- #
        i, j, k, h, m_alias = self.i, self.j, self.k, self.h, self.m_alias

        # Antoine
        self.psat_def = gp.Equation(self.m, name="psat_def", domain=[i, j])
        self.psat_def[i, j].where[cond_active] = self.logPsat[i, j] == (
            self.kk[i, "1"] + self.kk[i, "2"] / (self.kk[i, "3"] + self.T[j]) 
            + self.kk[i, "4"] * self.T[j] + self.kk[i, "5"] * gmath.log(self.T[j]) 
            + self.kk[i, "6"] * (self.T[j] ** self.kk[i, "7"])
        )

        # SRK
        self.cubic_eos = gp.Equation(self.m, name="cubic_eos", domain=[j])
        self.cubic_eos[j].where[cond_active] = -self.Z[j] + 1 + ( self.b[j] * self.P[j]) / (self.R * self.T[j] ) - (  self.a[j] / (self.b[j] * self.R * self.T[j]) ) * ( self.b[j] * self.P[j]) / (self.R * self.T[j] ) * (self.Z[j] - ( self.b[j] * self.P[j]) / (self.R * self.T[j] )) / (self.Z[j] * (self.Z[j] + ( self.b[j] * self.P[j]) / (self.R * self.T[j] ))) == 0
        
        self.alpha_definition = gp.Equation(self.m, name="alpha_definition", domain=[i, j])
        self.alpha_definition[i, j].where[cond_active] = self.alpha_ij[i, j] == (1 + self.kappa[i] * (1 - gmath.sqrt(( self.T[j] / self.Tc[i] ))))**2
        
        self.aii_definition = gp.Equation(self.m, name="aii_definition", domain=[i, j])
        self.aii_definition[i, j].where[cond_active] = self.aii[i, j] == self.alpha_ij[i, j] * self.ac[i]

        self.mixing_rule_b = gp.Equation(self.m, name="mixing_rule_b", domain=[j])
        self.mixing_rule_b[j].where[cond_active] = self.b[j] == gp.Sum(i, self.y[i, j] * self.bii[i])

        self.mixing_rule_a = gp.Equation(self.m, name="mixing_rule_a", domain=[j])
        self.mixing_rule_a[j].where[cond_active] = self.a[j] == gp.Sum(i, gp.Sum(k, self.y[i, j] * self.y[k, j] * gmath.sqrt(self.aii[i, j] * self.aii[k, j])))

        self.v_definition = gp.Equation(self.m, name="v_definition", domain=[j])
        self.v_definition[j].where[cond_active] = self.v_mol[j] == self.Z[j] * self.R * self.T[j] / self.P[j]

        self.fugacity_eq = gp.Equation(self.m, name="fugacity_eq", domain=[i, j])
        self.fugacity_eq[i, j].where[cond_active] = self.phi[i, j] == gmath.exp(
            self.bii[i] * (self.Z[j] - 1) / self.b[j] - gmath.log(self.P[j] * (self.v_mol[j] - self.b[j]) / (self.R * self.T[j])) +
            (self.a[j] / (self.b[j] * self.R * self.T[j])) * (self.bii[i] / self.b[j] - 2 * gp.Sum(k, self.y[k, j] * gmath.sqrt(self.aii[i, j] * self.aii[k, j])) / self.a[j]) * gmath.log((self.v_mol[j] + self.b[j]) / self.v_mol[j])
        )

        self.dadT_ii_eq = gp.Equation(self.m, name="dadT_ii_eq", domain=[i, j])
        self.dadT_ii_eq[i, j].where[cond_active] = self.dadT_ii[i, j] == -(self.ac[i] * self.kappa[i]) * gmath.sqrt(self.alpha_ij[i, j] * ( self.T[j] / self.Tc[i] )) / self.T[j]

        self.dadT_eq = gp.Equation(self.m, name="dadT_eq", domain=[j])
        self.dadT_eq[j].where[cond_active] = self.dadT[j] == -gp.Sum(i, gp.Sum(k, self.y[i, j] * self.y[k, j] * gmath.sqrt(self.dadT_ii[i, j] * self.dadT_ii[k, j])))

        self.enthalpy_eq = gp.Equation(self.m, name="enthalpy_eq", domain=[j])
        self.enthalpy_eq[j].where[cond_active] = self.HR[j] == self.R * self.T[j] * (self.Z[j] - 1 + (self.T[j] * self.dadT[j] - self.a[j]) / (self.b[j] * self.R * self.T[j]) * gmath.log((self.v_mol[j] + self.b[j]) / self.v_mol[j]))

        # NRTL
        self.Compute_gamma = gp.Equation(self.m, name="Compute_gamma", domain=[i, j])
        self.Compute_gamma[i, j].where[cond_active] = self.gamma_nrtl[i, j] == gmath.exp(
            gp.Sum(h, self.x[h, j] * ( self.b_nrtl[h, i] / self.T[j] ) * ( gmath.exp(-self.c_nrtl[h, i] * (self.b_nrtl[h, i] / self.T[j]) ) )) / gp.Sum(k, self.x[k, j] * ( gmath.exp(-self.c_nrtl[k, i] * (self.b_nrtl[k, i] / self.T[j]) ) )) +
            gp.Sum(h, (self.x[h, j] * ( gmath.exp(-self.c_nrtl[i, h] * (self.b_nrtl[i, h] / self.T[j]) ) )) / gp.Sum(k, self.x[k, j] * ( gmath.exp(-self.c_nrtl[k, h] * (self.b_nrtl[k, h] / self.T[j]) ) )) *
            (( self.b_nrtl[i, h] / self.T[j] ) - gp.Sum(m_alias, self.x[m_alias, j] * ( self.b_nrtl[m_alias, h] / self.T[j] ) * ( gmath.exp(-self.c_nrtl[m_alias, h] * (self.b_nrtl[m_alias, h] / self.T[j]) ) )) / gp.Sum(k, self.x[k, j] * ( gmath.exp(-self.c_nrtl[k, h] * (self.b_nrtl[k, h] / self.T[j]) ) ))))
        )

        self.K_equation = gp.Equation(self.m, name="K_equation", domain=[i, j])
        self.K_equation[i, j].where[cond_active] = self.K_part[i, j] * (self.phi[i, j] * self.P[j]) == self.gamma_nrtl[i, j] * gmath.exp(self.logPsat[i, j])

        # Enthalpies
        self.calc_DH_ig = gp.Equation(self.m, name="calc_DH_ig", domain=[i, j])
        self.calc_DH_ig[i, j].where[cond_active] = self.DH_ig[i, j] == (self.C_ig[i, "1"] * (self.T[j] - self.T0) + self.C_ig[i, "2"] * (self.T[j]**2 - self.T0**2) / 2 + self.C_ig[i, "3"] * (self.T[j]**3 - self.T0**3) / 3 + self.C_ig[i, "4"] * (self.T[j]**4 - self.T0**4) / 4 + self.C_ig[i, "5"] * (self.T[j]**5 - self.T0**5) / 5)

        self.calc_Hvi = gp.Equation(self.m, name="calc_Hvi", domain=[i, j])
        self.calc_Hvi[i, j].where[cond_active] = self.Hvi[i, j] == self.DH_ig[i, j] + self.Hform[i]

        self.calc_Hv = gp.Equation(self.m, name="calc_Hv", domain=[j])
        self.calc_Hv[j].where[cond_active] = self.Hv[j] / self.H_factor == gp.Sum(i, self.y[i, j] * self.Hvi[i, j]) + self.HR[j]

        self.Zvi_eq = gp.Equation(self.m, name="Zvi_eq", domain=[i, j])
        self.Zvi_eq[i, j].where[cond_active] = -self.Zvi[i, j] + 1 + ( (self.bii[i] * self.P[j]) / (self.R * self.Tb[i]) ) - ( self.ai_Tb[i] / (self.bii[i] * self.R * self.Tb[i]) ) * ( (self.bii[i] * self.P[j]) / (self.R * self.Tb[i]) ) * (self.Zvi[i, j] - ( (self.bii[i] * self.P[j]) / (self.R * self.Tb[i]) )) / (self.Zvi[i, j] * (self.Zvi[i, j] + ( (self.bii[i] * self.P[j]) / (self.R * self.Tb[i]) ))) == 0

        self.v_eq = gp.Equation(self.m, name="v_eq", domain=[i, j])
        self.v_eq[i, j].where[cond_active] = self.v_mol_i[i, j] == self.Zvi[i, j] * self.R * self.Tb[i] / self.P[j]

        self.calc_HR_pure = gp.Equation(self.m, name="calc_HR_pure", domain=[i, j])
        self.calc_HR_pure[i, j].where[cond_active] = self.HR_pure[i, j] == self.R * self.Tb[i] * (self.Zvi[i, j] - 1 + (self.Tb[i] * self.dadT_Tb[i] - self.ai_Tb[i]) / (self.bii[i] * self.R * self.Tb[i]) * gmath.log((self.v_mol_i[i, j] + self.bii[i]) / self.v_mol_i[i, j]))

        self.calc_DH_liq = gp.Equation(self.m, name="calc_DH_liq", domain=[i, j])
        self.calc_DH_liq[i, j].where[cond_active] = self.DH_liq[i, j] == (self.C_liq[i, "1"] * (self.T[j] - self.Tb[i]) + self.C_liq[i, "2"] * (self.T[j]**2 - self.Tb[i]**2) / 2 + self.C_liq[i, "3"] * (self.T[j]**3 - self.Tb[i]**3) / 3 + self.C_liq[i, "4"] * (self.T[j]**4 - self.Tb[i]**4) / 4 + self.C_liq[i, "5"] * (self.T[j]**5 - self.Tb[i]**5) / 5)

        self.calc_Hv_Tbi_P = gp.Equation(self.m, name="calc_Hv_Tbi_P", domain=[i, j])
        self.calc_Hv_Tbi_P[i, j].where[cond_active] = self.Hv_Tbi_P[i, j] == self.DH_ig_Tb[i] + self.Hform[i] + self.HR_pure[i, j]

        self.calc_Hli = gp.Equation(self.m, name="calc_Hli", domain=[i, j])
        self.calc_Hli[i, j].where[cond_active] = self.Hli[i, j] == self.DH_liq[i, j] + self.Hv_Tbi_P[i, j] - self.DH_vap[i]

        self.calc_Hl = gp.Equation(self.m, name="calc_Hl", domain=[j])
        self.calc_Hl[j].where[cond_active] = self.Hl[j] / self.H_factor == gp.Sum(i, self.x[i, j] * self.Hli[i, j])

        # Kinetics (Uses the binary parameter `is_reactive` to turn reactions on/off)
        self.calc_K_eq = gp.Equation(self.m, name="calc_K_eq", domain=[j])
        self.calc_K_eq[j].where[cond_active] = self.K_eq[j] == gmath.exp(10.387 + 4060.59 / self.T[j] - 2.89055 * gmath.log(self.T[j]) - 0.01915144 * self.T[j] + 5.28586E-5 * self.T[j]**2 - 5.32977E-8 * self.T[j]**3)

        self.calc_k_rate = gp.Equation(self.m, name="calc_k_rate", domain=[j])
        self.calc_k_rate[j].where[cond_active] = self.k_rate[j] == 7.41816E15 * gmath.exp(-60.4E3 / (self.R * self.T[j])) / 60

        self.calc_k_A = gp.Equation(self.m, name="calc_k_A", domain=[j])
        self.calc_k_A[j].where[cond_active] = self.k_A[j] == gmath.exp(-1.0707 + 1323.1 / self.T[j])

        self.calc_Rx_Rate = gp.Equation(self.m, name="calc_Rx_Rate", domain=[j])
        self.calc_Rx_Rate[j].where[cond_active] = self.Rxn_Rate[j] == self.is_reactive[j] * (
            self.k_rate[j] * ( self.x["2", j] * self.gamma_nrtl["2", j] ) * (( self.x["2", j] * self.gamma_nrtl["2", j] ) * ( self.x["3", j] * self.gamma_nrtl["3", j] ) - ( self.x["4", j] * self.gamma_nrtl["4", j] ) / self.K_eq[j]) / (1 + self.k_A[j] * ( self.x["2", j] * self.gamma_nrtl["2", j] ))**3
        )

        # MESHR Balances
        self.mol_balance_eq = gp.Equation(self.m, name="mol_balance_eq", domain=[j])
        self.mol_balance_eq[j].where[cond_interior] = self.L[j] + self.V[j] - self.V[j.lead(1)] - self.L[j.lag(1)] - self.FE * self.is_FE[j] - self.FB * self.is_FB[j] - gp.Sum(i, self.v_i[i] * self.m_cat * self.Rxn_Rate[j]) / self.F_factor == 0

        self.mol_balance_condenser_eq = gp.Equation(self.m, name="mol_balance_condenser_eq")
        self.mol_balance_condenser_eq[...] = self.V["1"] + (self.L["1"] + self.D) - self.V["2"] == 0

        self.mol_balance_reboiler_eq = gp.Equation(self.m, name="mol_balance_reboiler_eq", domain=[j])
        self.mol_balance_reboiler_eq[j].where[cond_reboiler] = self.V[j] + self.L[j] - self.L[j.lag(1)] == 0

        self.comp_balance_eq = gp.Equation(self.m, name="comp_balance_eq", domain=[i, j])
        self.comp_balance_eq[i, j].where[cond_interior] = self.L[j] * self.x[i, j] + self.V[j] * self.y[i, j] - self.V[j.lead(1)] * self.y[i, j.lead(1)] - self.L[j.lag(1)] * self.x[i, j.lag(1)] - self.FE * self.is_FE[j] * self.zE[i] - self.FB * self.is_FB[j] * self.zB[i] - self.m_cat * self.v_i[i] * self.Rxn_Rate[j] / self.F_factor == 0

        self.comp_balance_condenser_eq = gp.Equation(self.m, name="comp_balance_condenser_eq", domain=[i])
        self.comp_balance_condenser_eq[i] = self.V["1"] * self.y[i, "1"] + (self.L["1"] + self.D) * self.x[i, "1"] - self.V["2"] * self.y[i, "2"] == 0

        self.comp_balance_reboiler_eq = gp.Equation(self.m, name="comp_balance_reboiler_eq", domain=[i, j])
        self.comp_balance_reboiler_eq[i, j].where[cond_reboiler] = self.V[j] * self.y[i, j] + self.L[j] * self.x[i, j] - self.L[j.lag(1)] * self.x[i, j.lag(1)] == 0

        self.eq_rel_eq = gp.Equation(self.m, name="eq_rel_eq", domain=[i, j])
        self.eq_rel_eq[i, j].where[cond_active] = self.K_part[i, j] * self.x[i, j] - self.y[i, j] == 0

        self.summation_eq = gp.Equation(self.m, name="summation_eq", domain=[j])
        self.summation_eq[j].where[cond_active] = gp.Sum(i, self.y[i, j] - self.x[i, j]) == 0

        self.energy_balance_eq = gp.Equation(self.m, name="energy_balance_eq", domain=[j])
        self.energy_balance_eq[j].where[cond_interior] = self.V[j] * self.Hv[j] + self.L[j] * self.Hl[j] - self.V[j.lead(1)] * self.Hv[j.lead(1)] - self.L[j.lag(1)] * self.Hl[j.lag(1)] - self.FE * self.is_FE[j] * self.HFE - self.FB * self.is_FB[j] * self.HFB == 0

        self.energy_balance_condenser_eq = gp.Equation(self.m, name="energy_balance_condenser_eq")
        self.energy_balance_condenser_eq[...] = self.V["1"] * self.Hv["1"] + (self.L["1"] + self.D) * self.Hl["1"] - self.V["2"] * self.Hv["2"] + self.Qc == 0

        self.energy_balance_reboiler_eq = gp.Equation(self.m, name="energy_balance_reboiler_eq", domain=[j])
        self.energy_balance_reboiler_eq[j].where[cond_reboiler] = self.V[j] * self.Hv[j] + self.L[j] * self.Hl[j] - self.L[j.lag(1)] * self.Hl[j.lag(1)] - self.Qr == 0

        self.spec_2_eq = gp.Equation(self.m, name="spec_2_eq", domain=[j])
        self.spec_2_eq[j].where[cond_reboiler] = self.x["4", j] == self.Spec_2

        self.V1_eq = gp.Equation(self.m, name="V1_eq")
        self.V1_eq[...] = self.V["1"] == 0

        # Economics
        self.Flv_def = gp.Equation(self.m, "Flv_def", domain=j)
        self.CF_def = gp.Equation(self.m, "CF_def", domain=j)
        self.flooding_vel_eq = gp.Equation(self.m, "flooding_vel_eq", domain=j)

        self.def_Dcol = gp.Equation(self.m, "def_Dcol", domain=j)

        self.uf_res_1 = gp.Equation(self.m, "uf_res_1", domain=j)
        self.uf_res_2 = gp.Equation(self.m, "uf_res_2", domain=j)

        self.def_Mw_mix_V = gp.Equation(self.m, "def_Mw_mix_V", domain=j)
        self.def_Mw_mix_L = gp.Equation(self.m, "def_Mw_mix_L", domain=j)

        self.def_catal_vol = gp.Equation(self.m, "def_catal_vol")
        
        self.def_Mw_mix_V[j].where[cond_interior]  = (
            self.Mw_mix_V[j]
            == gp.Sum(self.i, self.y[i, j] * self.Mw[i])
        )

        self.def_Mw_mix_L[j].where[cond_interior] = (
            self.Mw_mix_L[j]
            == gp.Sum(i, self.x[i, j]*self.Mw[i])
        )

        self.Flv_def[j].where[cond_interior] = (
            self.Flv[j]
            == self.L[j]
            / self.V[j]
            * self.Mw_mix_L[j]
            / self.Mw_mix_V[j]
            * gmath.sqrt(
                self.Mw_mix_V[j] / self.v_mol[j] / self.rhoL
            )
        )
        self.CF_def[j].where[cond_interior] = (
            gmath.log10(self.CF[j])
            ==
            - self.a1
            - self.a2 * gmath.log10(self.Flv[j])
            - self.a3 * gmath.sqr(gmath.log10(self.Flv[j]))
        )

        self.flooding_vel_eq[j].where[cond_interior] = (
            self.ufl[j]
            ==
            (self.sigma_g / 20) ** 0.2
            * gmath.sqrt(
                (self.Mw_mix_V[j] / self.v_mol[j])
                / (self.rhoL - self.Mw_mix_V[j] / self.v_mol[j])
            )
            * self.CF[j]
            * 0.3048
            * 60
        )

        self.def_Dcol[j].where[cond_interior] = (
            self.uf[j]
            ==
            4*self.V[j]*self.v_mol[j]/(np.pi*gmath.sqr(self.Dcol)*0.88)
        )

        self.uf_res_1[j].where[cond_interior] = (
            self.uf[j] <= 0.8 * self.ufl[j]
        )

        self.uf_res_2[j].where[cond_interior] = (
            self.uf[j] >= 0.4 * self.ufl[j]
        )   

        self.def_catal_vol[...] = (
            self.m_cat / self.rho_cat
            <=
            self.phi_c
            * (np.pi / 4)
            * self.Dcol**2
            * self.h_pack
        )     
        # self.def_Mw_mix = gp.Equation(self.m, name="def_Mw_mix", domain=[j])
        # self.def_Mw_mix[j].where[cond_active] = self.Mw_mix[j] == gp.Sum(i, self.y[i, j] * self.Mw[i])

        # self.def_D_col = gp.Equation(self.m, name="def_D_col", domain=[j])
        # self.def_D_col[j].where[cond_interior] = self.D_col[j] == gmath.sqrt(4 * ((self.V[j] * self.F_factor * self.v_mol[j] / 60) / ((self.FF / gmath.sqrt(self.Mw_mix[j] * 1e-3 / self.v_mol[j])) * 0.88)) / np.pi) * 3.28084

        # self.def_Dcol_max = gp.Equation(self.m, name="def_Dcol_max", domain=[j])
        # self.def_Dcol_max[j].where[cond_interior] = self.Dcol_max >= self.D_col[j]

        #catalyst volume limit
        self.def_catal_vol = gp.Equation(self.m, name="def_catal_vol")
        self.def_catal_vol = self.m_cat/self.rho_cat <= self.phi_c*(np.pi/4)*( self.Dcol )**2*self.h_pack

        self.def_Tcond = gp.Equation(self.m, name="def_Tcond")
        self.def_Tcond[...] = self.Tcond == self.T["1"]
        
        self.def_Treb = gp.Equation(self.m, name="def_Treb", domain=[j])
        self.def_Treb[j].where[cond_reboiler] = self.Treb == self.T[j]
        
        self.def_Breb = gp.Equation(self.m, name="def_Breb", domain=[j])
        self.def_Breb[j].where[cond_reboiler] = self.Breb == self.L[j]

        self.eq_ColCost = gp.Equation(self.m, name="eq_ColCost")
        self.eq_ColCost[...] = self.v_ColCost == (self.MS / 280) * (101.9 * ((self.Dcol*3.28084)**1.066) * ((self.ht*1.2 * (self.Ns - 2) * 3.28084)**0.802) * 7.05)

        self.eq_TrayCost = gp.Equation(self.m, name="eq_TrayCost")
        self.eq_TrayCost[...] = self.v_TrayCost == (self.MS / 280) * (4.7 * ((self.Dcol*3.28084)**1.55) * (self.ht*1.2* (self.Ns - 2) * 3.28084) * 2.7)

        self.eq_CondCost = gp.Equation(self.m, name="eq_CondCost")
        self.eq_CondCost[...] = self.v_CondCost == (self.Qc * self.FH_factor / 60 / (150 / 0.17611 * (10 / gmath.log((self.Tcond - 303.15) / (self.Tcond - 313.15)))) * 10.7639)**0.65 * 1709.8394439285714

        self.eq_RebCost = gp.Equation(self.m, name="eq_RebCost")
        self.eq_RebCost[...] = self.v_RebCost == (self.MS / 280 * 101.3 * ((self.Qr * self.FH_factor / 60 / ((250 / 0.17611) * (433.15 - self.Treb)) * 10.7639)**0.65 * 7.3525))

        self.eq_CAP_cost = gp.Equation(self.m, name="eq_CAP_cost")
        self.eq_CAP_cost[...] = self.CAP_cost == (1 / 3) * (self.v_TrayCost + self.v_ColCost + self.v_CondCost + self.v_RebCost + (7.7 * gp.Sum(j, self.is_reactive[j]) * 0.4))

        self.eq_OP_cost = gp.Equation(self.m, name="eq_OP_cost")
        self.eq_OP_cost[...] = self.OP_cost == ((0.378e-9 * self.Qc + self.c_steam * self.Qr) * 8150 * 60 * self.FH_factor + (self.FE * self.CostEth + self.FB * self.CostBut - self.CostETBE * self.Breb) * self.F_factor * 8150 * 60)

        self.def_Profit = gp.Equation(self.m, name="def_Profit")
        self.def_Profit[...] = self.Profit * 1e6 == self.CAP_cost + self.OP_cost

        self.obj_def = gp.Equation(self.m, name="obj_def")
        self.obj_def[...] = self.obj == self.Profit

        # -------------------------------------------------------------------- #
        # GHOST TRAY DUMMY EQUATIONS (Prevents division by zero in inactive space)
        # -------------------------------------------------------------------- #
        self.dummy_T = gp.Equation(self.m, name="dummy_T", domain=[j])
        self.dummy_T[j].where[cond_inactive] = self.T[j] == 350
        
        self.dummy_L = gp.Equation(self.m, name="dummy_L", domain=[j])
        self.dummy_L[j].where[cond_inactive] = self.L[j] == 1e-5
        
        self.dummy_V = gp.Equation(self.m, name="dummy_V", domain=[j])
        self.dummy_V[j].where[cond_inactive] = self.V[j] == 1e-5
        
        self.dummy_x = gp.Equation(self.m, name="dummy_x", domain=[i, j])
        self.dummy_x[i, j].where[cond_inactive] = self.x[i, j] == 0.25

    def _initialize_bounds_and_scales(self):
        #  ============================================================================ *
        #  Defining upper and lower bounds and scale
        #  ============================================================================ *

        # ---------------------------------------------------------------------------- #
        # Basic Variables
        # ---------------------------------------------------------------------------- #
        self.L.lo[self.j] = 1e-5;  self.L.up[self.j] = 50;  self.L.l[self.j] = 0.5
        self.V.lo[self.j] = 1e-5;  self.V.up[self.j] = 50;  self.V.l[self.j] = 0.5
        self.V.lo["1"] = 0;        self.V.up["1"] = 0.001;  self.V.l["1"] = 0

        self.x.lo[self.i, self.j] = 0;  self.x.up[self.i, self.j] = 1;  self.x.l[self.i, self.j] = 0.25
        self.y.lo[self.i, self.j] = 0;  self.y.up[self.i, self.j] = 1;  self.y.l[self.i, self.j] = 0.25

        # For scalar variables (0-dimensional), we use [...] 
        self.D.lo[...] = 0.01;      self.D.up[...] = 1;       self.D.l[...] = 0.5748006462583984
        self.Qc.lo[...] = 0.01;     self.Qc.up[...] = 10;     self.Qc.l[...] = 0.5451343354854316
        self.Qr.lo[...] = 0.01;     self.Qr.up[...] = 10;     self.Qr.l[...] = 0.4592022879232921
        self.Breb.lo[...] = 0.001;  self.Breb.up[...] = 1;    self.Breb.l[...] = 0.24

        self.T.lo[self.j] = self.Tmin;  self.T.up[self.j] = self.Tmax;  self.T.scale[self.j] = self.TF_factor

        self.FE.lo[...] = 0.00075; self.FE.up[...] = 37.43; self.FE.l[...] = 5.774 / self.F_factor

        # ---------------------------------------------------------------------------- #
        # Thermodynamics & Enthalpy Variables
        # ---------------------------------------------------------------------------- #
        self.logPsat.lo[self.i, self.j] = (
            self.kk[self.i, "1"] + self.kk[self.i, "2"] / (self.kk[self.i, "3"] + self.Tmin) 
            + self.kk[self.i, "4"] * self.Tmin + self.kk[self.i, "5"] * gmath.log(self.Tmin) 
            + self.kk[self.i, "6"] * (self.Tmin**self.kk[self.i, "7"])
        )

        self.logPsat.up[self.i, self.j] = (
            self.kk[self.i, "1"] + self.kk[self.i, "2"] / (self.kk[self.i, "3"] + self.Tmax) 
            + self.kk[self.i, "4"] * self.Tmax + self.kk[self.i, "5"] * gmath.log(self.Tmax) 
            + self.kk[self.i, "6"] * (self.Tmax**self.kk[self.i, "7"])
        )
        self.logPsat.scale[self.i, self.j] = 10

        self.alpha_ij.lo[self.i, self.j] = 0.5;    self.alpha_ij.up[self.i, self.j] = 2
        self.aii.lo[self.i, self.j] = 1;           self.aii.up[self.i, self.j] = 4
        self.a.lo[self.j] = 1;                     self.a.up[self.j] = 3
        self.b.lo[self.j] = 1e-5;                  self.b.up[self.j] = 1e-3;             self.b.scale[self.j] = 1e-5
        self.dadT_ii.lo[self.i, self.j] = -0.009;  self.dadT_ii.up[self.i, self.j] = -0.001; self.dadT_ii.scale[self.i, self.j] = 1e-3
        self.dadT.lo[self.j] = -0.009;             self.dadT.up[self.j] = -0.001;        self.dadT.scale[self.j] = 1e-3
        self.K_part.lo[self.i, self.j] = 0.001;    self.K_part.up[self.i, self.j] = 10
        self.phi.lo[self.i, self.j] = 0.1;         self.phi.up[self.i, self.j] = 1.2

        self.DH_ig.lo[self.i, self.j] = (
            self.C_ig[self.i, "1"] * (self.Tmin - self.T0) + self.C_ig[self.i, "2"] * (self.Tmin**2 - self.T0**2) / 2
            + self.C_ig[self.i, "3"] * (self.Tmin**3 - self.T0**3) / 3 + self.C_ig[self.i, "4"] * (self.Tmin**4 - self.T0**4) / 4
            + self.C_ig[self.i, "5"] * (self.Tmin**5 - self.T0**5) / 5
        )
        self.DH_ig.up[self.i, self.j] = (
            self.C_ig[self.i, "1"] * (self.Tmax - self.T0) + self.C_ig[self.i, "2"] * (self.Tmax**2 - self.T0**2) / 2
            + self.C_ig[self.i, "3"] * (self.Tmax**3 - self.T0**3) / 3 + self.C_ig[self.i, "4"] * (self.Tmax**4 - self.T0**4) / 4
            + self.C_ig[self.i, "5"] * (self.Tmax**5 - self.T0**5) / 5
        )
        self.DH_ig.scale[self.i, self.j] = 1e3

        self.Hvi.lo[self.i, self.j] = self.DH_ig.lo[self.i, self.j] + self.Hform[self.i]
        self.Hvi.up[self.i, self.j] = self.DH_ig.up[self.i, self.j] + self.Hform[self.i]
        self.Hvi.scale[self.i, self.j] = 1e5

        self.HR.lo[self.j] = -2500;  self.HR.up[self.j] = -1100;  self.HR.scale[self.j] = 1e3

        # GAMS smin/smax translate to gp.Smin/gp.Smax
        self.Hv.lo[self.j] = (gp.Smin(self.i, self.Hvi.lo[self.i, self.j]) + self.HR.lo[self.j]) * self.H_factor
        self.Hv.up[self.j] = (gp.Smax(self.i, self.Hvi.up[self.i, self.j]) + self.HR.up[self.j]) * self.H_factor

        self.DH_liq.lo[self.i, self.j] = (
            self.C_liq[self.i, "1"] * (self.Tmin - self.Tb[self.i]) + self.C_liq[self.i, "2"] * (self.Tmin**2 - self.Tb[self.i]**2) / 2
            + self.C_liq[self.i, "3"] * (self.Tmin**3 - self.Tb[self.i]**3) / 3 + self.C_liq[self.i, "4"] * (self.Tmin**4 - self.Tb[self.i]**4) / 4
            + self.C_liq[self.i, "5"] * (self.Tmin**5 - self.Tb[self.i]**5) / 5
        )
        self.DH_liq.up[self.i, self.j] = (
            self.C_liq[self.i, "1"] * (self.Tmax - self.Tb[self.i]) + self.C_liq[self.i, "2"] * (self.Tmax**2 - self.Tb[self.i]**2) / 2
            + self.C_liq[self.i, "3"] * (self.Tmax**3 - self.Tb[self.i]**3) / 3 + self.C_liq[self.i, "4"] * (self.Tmax**4 - self.Tb[self.i]**4) / 4
            + self.C_liq[self.i, "5"] * (self.Tmax**5 - self.Tb[self.i]**5) / 5
        )
        self.DH_liq.scale[self.i, self.j] = 1e4

        self.HR_pure.lo[self.i, self.j] = -3e3;  self.HR_pure.up[self.i, self.j] = -1e3; self.HR_pure.scale[self.i, self.j] = 1e3

        self.Hv_Tbi_P.lo[self.i, self.j] = self.DH_ig_Tb[self.i] * 0.99 + self.Hform[self.i] + self.HR_pure.lo[self.i, self.j]
        self.Hv_Tbi_P.up[self.i, self.j] = self.DH_ig_Tb[self.i] * 1.01 + self.Hform[self.i] + self.HR_pure.up[self.i, self.j]
        self.Hv_Tbi_P.scale[self.i, self.j] = 1e4

        self.Hli.lo[self.i, self.j] = self.DH_liq.lo[self.i, self.j] + self.Hv_Tbi_P.lo[self.i, self.j] - self.DH_vap[self.i]
        self.Hli.up[self.i, self.j] = self.DH_liq.up[self.i, self.j] + self.Hv_Tbi_P.up[self.i, self.j] - self.DH_vap[self.i]
        self.Hli.scale[self.i, self.j] = 1e5

        # Following the original code logic (using Hvi for Hl bounds)
        self.Hl.lo[self.j] = gp.Smin(self.i, self.Hvi.lo[self.i, self.j]) * self.H_factor
        self.Hl.up[self.j] = gp.Smax(self.i, self.Hvi.up[self.i, self.j]) * self.H_factor

        # ---------------------------------------------------------------------------- #
        # Molar Volume & Compressibility
        # ---------------------------------------------------------------------------- #
        self.Z.lo[self.j] = 0.75; self.Z.up[self.j] = 0.9; self.Z.l[self.j] = 0.822
        self.v_mol.lo[self.j] = self.Z.lo[self.j] * self.R * self.Tmin / 9.5e5
        self.v_mol.up[self.j] = self.Z.up[self.j] * self.R * self.Tmax / 9.5e5
        self.v_mol.scale[self.j] = 1e-3

        self.Zvi.lo[self.i, self.j] = 0.75; self.Zvi.up[self.i, self.j] = 1; self.Zvi.l[self.i, self.j] = 0.9
        self.v_mol_i.lo[self.i, self.j] = self.Zvi.lo[self.i, self.j] * self.R * self.Tmin / 9.5e5
        self.v_mol_i.up[self.i, self.j] = self.Zvi.up[self.i, self.j] * self.R * self.Tmax / 9.5e5
        self.v_mol_i.scale[self.i, self.j] = 1e-3

        self.gamma_nrtl.lo[self.i, self.j] = 0.01; self.gamma_nrtl.up[self.i, self.j] = 20

        # ---------------------------------------------------------------------------- #
        # Efficiency Improvement: Pure Python Bound Calculations
        # ---------------------------------------------------------------------------- #
        self.K_eq.lo[self.j] = gmath.exp(10.387 + 4060.59 / self.Tmax - 2.89055 * gmath.log(self.Tmax) - 0.01915144 * self.Tmax + 5.28586E-5 * self.Tmax**2 - 5.32977E-8 * self.Tmax**3)
        self.K_eq.up[self.j] = gmath.exp(10.387 + 4060.59 / self.Tmin - 2.89055 * gmath.log(self.Tmin) - 0.01915144 * self.Tmin + 5.28586E-5 * self.Tmin**2 - 5.32977E-8 * self.Tmin**3)
        self.K_eq.scale[self.j] = 10

        self.k_rate.lo[self.j] = 7.41816E15 * gmath.exp(-60.4E3 / (self.R * self.Tmin)) / 60
        self.k_rate.up[self.j] = 7.41816E15 * gmath.exp(-60.4E3 / (self.R * self.Tmax)) / 60
        self.k_rate.scale[self.j] = 1e4

        self.k_A.lo[self.j] = gmath.exp(-1.0707 + 1323.1 / self.Tmax)
        self.k_A.up[self.j] = gmath.exp(-1.0707 + 1323.1 / self.Tmin)
        self.k_A.scale[self.j] = 10

        self.Rxn_Rate.lo[self.j] = -10; self.Rxn_Rate.up[self.j] = 10

        # ---------------------------------------------------------------------------- #
        # Equipment & Costing Bounds
        # ---------------------------------------------------------------------------- #
        self.Mw_mix_V.lo[self.j] = 46.069; self.Mw_mix_V.up[self.j] = 102.177; self.Mw_mix_V.scale[self.j] = 10
        self.Mw_mix_L.lo[self.j] = 46.069; self.Mw_mix_L.up[self.j] = 102.177; self.Mw_mix_L.scale[self.j] = 10

        self.Dcol.lo = 0.01; self.Dcol.up = 2; self.Dcol.l = 0.1; self.Dcol.scale = 0.1
        
        self.CF.lo[self.j] = 1e-2
        self.CF.up[self.j] = 2
        self.uf.lo[self.j] = 0.01
        self.uf.up[self.j] = 20
        self.ufl.lo[self.j] = 0.01
        self.ufl.up[self.j] = 20
        self.Flv.lo[self.j] = 0.001
        self.Flv.up[self.j] = 20
        self.CF.l[self.j] = 0.2
        self.uf.l[self.j] = 0.5
        self.ufl.l[self.j] = 0.7
        self.Flv.l[self.j] = 0.1
        # ============================================================================ #
        # CRITICAL INITIALIZATIONS: Mimicking GAMS Default States
        # ============================================================================ #

        self.Tcond.lo[...] = 330;      self.Tcond.up[...] = self.Tmin+50; self.Tcond.scale[...] = self.TF_factor
        self.Treb.lo[...] = self.Tmax-50;  self.Treb.up[...] = self.Tmax;     self.Treb.scale[...] = self.TF_factor

        self.L.l[self.j] = 0.5
        self.V.l[self.j] = 0.5
        self.V.l["1"] = 0.1  # Do not start condenser vapor at exact 0
        self.x.l[self.i, self.j] = 0.25
        self.y.l[self.i, self.j] = 0.25

        # 2. Phase Equilibrium (K_part * x = y -> 1.0 * 0.25 = 0.25)
        self.K_part.l[self.i, self.j] = 1.0
        self.logPsat.l[self.i, self.j] = 11.5  
        self.gamma_nrtl.l[self.i, self.j] = 1.0
        self.phi.l[self.i, self.j] = 1.0

        # 3. SRK & Mixture Properties
        self.alpha_ij.l[self.i, self.j] = 1.0
        self.aii.l[self.i, self.j] = 2.0
        self.a.l[self.j] = 2.0
        self.b.l[self.j] = 1e-4
        self.dadT_ii.l[self.i, self.j] = -0.005
        self.dadT.l[self.j] = -0.005
        self.Z.l[self.j] = 0.822
        self.Zvi.l[self.i, self.j] = 0.9
        self.v_mol.l[self.j] = 0.003
        self.v_mol_i.l[self.i, self.j] = 0.003
        self.Mw_mix_V.l[self.j] = 60.0
        self.Mw_mix_L.l[self.j] = 60.0

        # 4. Kinetics
        self.K_eq.l[self.j] = 10.0
        self.k_rate.l[self.j] = 100.0
        self.k_A.l[self.j] = 10.0
        self.Rxn_Rate.l[self.j] = 0.0

        # 5. Enthalpies
        self.DH_ig.l[self.i, self.j] = 5000.0
        self.Hvi.l[self.i, self.j] = -150000.0
        self.Hv.l[self.j] = -1
        self.DH_liq.l[self.i, self.j] = 1000.0
        self.HR_pure.l[self.i, self.j] = -2000.0
        self.Hv_Tbi_P.l[self.i, self.j] = -150000.0
        self.Hli.l[self.i, self.j] = -180000.0
        self.Hl.l[self.j] = -1

    def update_config(self, Ns, NFE, NFB, reactive_trays):
        """
        Updates the superstructure parameters instantly. No compilation required.
        """
        # # Count start in 0 - this was to adapt the solution for starting at stage-0
        # NFE = NFE+1
        # NFB = NFB+1
        # reactive_trays = [x+1 for x in reactive_trays]
        
        self.NFE = NFE
        self.Ns_d = Ns # I am already using Ns for gamspy
        self.NFB = NFB
        self.reactive_trays = reactive_trays
        
        self.Ns[...] = Ns
        self.is_FE[...] = 0
        self.is_FB[...] = 0
        self.is_reactive[...] = 0
        
        self.is_FE[str(NFE)] = 1
        self.is_FB[str(NFB)] = 1
        for rt in reactive_trays:
            self.is_reactive[str(rt)] = 1

    def solve(self, solver="CONOPT", export = False, dataframe = False):
        NR_string = ['NR1','NR2','NR3','NR4','NR5','NR6']
        text_NRx = ", ".join(
            f"{name} = {value}"
            for name, value in zip(NR_string, self.reactive_trays)
        )
        # print(f"\nSolving with Ns={self.Ns.toValue()}, 
        #     NFE={self.is_FE.records[self.is_FE.records['value']==1]['j'].values[0]}")
        print(
            f"\nSolving with Ns={self.Ns_d}, "
            f"NFE={self.NFE}, "
            f"NFB={self.NFB}, "
            f"{text_NRx}"
        )
        
        if (self.reactive_trays[0] == 1 or self.NFE == 1) or (self.NFB == self.Ns_d or self.reactive_trays[-1] == self.Ns_d):
            print('Violated the discrete bounds')
            return {
                "Status": 'fail',
                "Profit": 1e5
            }
        
        self.model.solve(
            solver=solver,
            options=gp.Options(time_limit=160,
                               enable_scaling=True,
                               relative_optimality_gap=1e-4,
                               threads=10
                               ),
            # output=sys.stdout #for debuging
        )
    
        # 3. Access elapsed time
        total_elapsed = self.model.total_solve_time
        solver_only_elapsed = self.model.solve_model_time

        if export:
            self.m.write('results.gdx')
        if dataframe:
            rows = []
            for var in self.m.data.values():
                if hasattr(var, "records"):
                    try:
                        if var.dimension >= 1:
                            df = var.records.copy()
                            df["variable"] = var.name
                            rows.append(df)
                    except Exception:
                        pass
            self.df_results = pd.concat(rows, ignore_index=True)

        print(f"Total solve statement time: {total_elapsed} seconds")
        print(f"Solver execution time: {solver_only_elapsed} seconds")
        print(self.model.status)

        if self.model.status.value == 1 or self.model.status.value == 2:
            print(f'Solver success. Fobj = {self.obj.toValue():.4e}')
            return {
                "Status": self.model.status,
                "Profit": self.obj.toValue()
            }
        else:
            print('solver failed')
            return {
                "Status": self.model.status,
                "Profit": 1e5
            }
        