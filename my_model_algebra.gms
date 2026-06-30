$onMultiR
$onUNDF
$onDotL
Set i(*);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_2FEx6YiWQZWZHbdMlJwL6Ain.gdx
$loadDC i
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Set j(*);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_VorS87TxQW2037mgb01YAQin.gdx
$loadDC j
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Set c(*);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_l6fKawymQgmfLSuf_PDY_win.gdx
$loadDC c
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Set cc(*);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_kiS9jZ_FSn_qpAEEeZvIDwin.gdx
$loadDC cc
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Alias(i,k);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Alias(i,h);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Alias(i,m_alias);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Ns "Current active stages" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter is_FE(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter is_FB(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter is_reactive(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Ns = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FE(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FB(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter P(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
P(j) = 950000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter v_i(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_C35cQaXGTOq2seZ9mVZVDgin.gdx
$loadDC v_i
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Tc(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_hQN18NE2T2iawPZbMcojrwin.gdx
$loadDC Tc
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Pc(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_BgYm2Q1DS_mfuqch1bAPuwin.gdx
$loadDC Pc
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter w(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_JG9sfzbPTBaHhjNHZakfNgin.gdx
$loadDC w
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Tb(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_pfYIvqr2TkOz1YtwVEbOCgin.gdx
$loadDC Tb
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Mw(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_bYxwtB9XS46__6Sq1pty8gin.gdx
$loadDC Mw
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Hform(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_Yfm32rlHQyC1IGKKEPj2vwin.gdx
$loadDC Hform
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter zE(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_Ur46QOKvTD6LgxjuKgeRwwin.gdx
$loadDC zE
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter zB(i);
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_Hltb5ZypTXi1QWoZiqc8YAin.gdx
$loadDC zB
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter kappa(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter ac(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter bii(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
kappa(i) = 0.48 + 1.574 * w(i) - 0.176 * power(w(i),2);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
ac(i) = 0.42747 * power(8.314463 * Tc(i),2) / Pc(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
bii(i) = 0.72036507432 * Tc(i) / Pc(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter HFE / -3.4564640738314174 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter HFB / -0.27173966027284036 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter FB / 0.7713270458735205 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Spec_1 / 0.85 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Spec_2 / 0.83 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter FF / 1.8420539101049511 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter MS / 1773.4 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter CostETBE / 0.0253 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter CostEth / 0.015 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter CostBut / 0.00825 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter c_steam / 4.54e-09 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter kk(i,c) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_0opkH3ZJTR_dI130R5Dpvwin.gdx
$loadDC kk
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter b_nrtl(i,i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter c_nrtl(i,i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_KPGOu8JhT8_VY4mERgZEtwin.gdx
$loadDC b_nrtl
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_CXyU7aVeT_61HVAXUk8qiQin.gdx
$loadDC c_nrtl
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter C_ig(i,cc) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter C_liq(i,cc) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter C_vap(i,cc) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_KrlV6xMnS1GyDH41qtI2Mwin.gdx
$loadDC C_ig
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_vVNHLpz2SHmQV5a4cL10PAin.gdx
$loadDC C_liq
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmphbywovwa\_aykBI2XjQsqbZsB1cpT1hAin.gdx
$loadDC C_vap
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Tbr(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter alpha_Tb(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter ai_Tb(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter dadT_Tb(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter DH_vap(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter DH_ig_Tb(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Tbr(i) = Tb(i) / Tc(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
alpha_Tb(i) = power(1 + kappa(i) * (1 - sqrt(Tbr(i))),2);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
ai_Tb(i) = alpha_Tb(i) * ac(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_Tb(i) = (-ac(i)) * kappa(i) * sqrt(alpha_Tb(i) * Tbr(i)) / Tb(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_vap(i) = C_vap(i,"1") * rPower(1 - Tbr(i),C_vap(i,"2") + C_vap(i,"3") * Tbr(i) + C_vap(i,"4") * power(Tbr(i),2) + C_vap(i,"5") * power(Tbr(i),3));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_ig_Tb(i) = C_ig(i,"1") * (Tb(i) - 298.15) + C_ig(i,"2") * (power(Tb(i),2) - 88893.42249999999) / 2 + C_ig(i,"3") * (power(Tb(i),3) - 26503573.918374993) / 3 + C_ig(i,"4") * (power(Tb(i),4) - 7902040563.763504) / 4 + C_ig(i,"5") * (power(Tb(i),5) - 2355993394086.0884) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable L(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable V(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable x(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable y(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable T(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable FE / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable D / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable Qc / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable Qr / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Breb / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Tcond / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Treb / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable D_col(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Dcol_max / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Mw_mix(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_ColCost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_TrayCost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_CondCost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_RebCost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable CAP_cost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable OP_cost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Profit / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable obj / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable logPsat(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Z(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_mol(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable phi(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable HR(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable alpha_ij(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable aii(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable a(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable b(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable dadT_ii(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable dadT(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable gamma_nrtl(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable K_part(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable DH_ig(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hvi(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hv(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable DH_liq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hv_Tbi_P(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hli(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hl(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable HR_pure(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable Zvi(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable v_mol_i(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable K_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable k_rate(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable k_A(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Rxn_Rate(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation psat_def(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
psat_def(i,j) $ (ord(j) <= Ns - 1) .. logPsat(i,j) =e= kk(i,"1") + kk(i,"2") / (kk(i,"3") + T(j)) + kk(i,"4") * T(j) + kk(i,"5") * log(T(j)) + kk(i,"6") * rPower(T(j),kk(i,"7"));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation cubic_eos(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
cubic_eos(j) $ (ord(j) <= Ns - 1) .. (-Z(j)) + 1 + b(j) * P(j) / (8.314463 * T(j)) - a(j) / (b(j) * 8.314463 * T(j)) * (b(j) * P(j)) / (8.314463 * T(j)) * (Z(j) - b(j) * P(j) / (8.314463 * T(j))) / (Z(j) * (Z(j) + b(j) * P(j) / (8.314463 * T(j)))) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation alpha_definition(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
alpha_definition(i,j) $ (ord(j) <= Ns - 1) .. alpha_ij(i,j) =e= power(1 + kappa(i) * (1 - sqrt(T(j) / Tc(i))),2);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation aii_definition(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
aii_definition(i,j) $ (ord(j) <= Ns - 1) .. aii(i,j) =e= alpha_ij(i,j) * ac(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation mixing_rule_b(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mixing_rule_b(j) $ (ord(j) <= Ns - 1) .. b(j) =e= sum(i,y(i,j) * bii(i));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation mixing_rule_a(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mixing_rule_a(j) $ (ord(j) <= Ns - 1) .. a(j) =e= sum(i,sum(k,y(i,j) * y(k,j) * sqrt(aii(i,j) * aii(k,j))));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation v_definition(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_definition(j) $ (ord(j) <= Ns - 1) .. v_mol(j) =e= Z(j) * 8.314463 * T(j) / P(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation fugacity_eq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
fugacity_eq(i,j) $ (ord(j) <= Ns - 1) .. phi(i,j) =e= exp(bii(i) * (Z(j) - 1) / b(j) - log(P(j) * (v_mol(j) - b(j)) / (8.314463 * T(j))) + a(j) / (b(j) * 8.314463 * T(j)) * (bii(i) / b(j) - 2 * sum(k,y(k,j) * sqrt(aii(i,j) * aii(k,j))) / a(j)) * log((v_mol(j) + b(j)) / v_mol(j)));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation dadT_ii_eq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_ii_eq(i,j) $ (ord(j) <= Ns - 1) .. dadT_ii(i,j) =e= (-(ac(i) * kappa(i))) * sqrt(alpha_ij(i,j) * (T(j) / Tc(i))) / T(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation dadT_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_eq(j) $ (ord(j) <= Ns - 1) .. dadT(j) =e= (-sum(i,sum(k,y(i,j) * y(k,j) * sqrt(dadT_ii(i,j) * dadT_ii(k,j)))));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation enthalpy_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
enthalpy_eq(j) $ (ord(j) <= Ns - 1) .. HR(j) =e= 8.314463 * T(j) * (Z(j) - 1 + (T(j) * dadT(j) - a(j)) / (b(j) * 8.314463 * T(j)) * log((v_mol(j) + b(j)) / v_mol(j)));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation Compute_gamma(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Compute_gamma(i,j) $ (ord(j) <= Ns - 1) .. gamma_nrtl(i,j) =e= exp(sum(h,x(h,j) * (b_nrtl(h,i) / T(j)) * exp((-c_nrtl(h,i)) * (b_nrtl(h,i) / T(j)))) / sum(k,x(k,j) * exp((-c_nrtl(k,i)) * (b_nrtl(k,i) / T(j)))) + sum(h,x(h,j) * exp((-c_nrtl(i,h)) * (b_nrtl(i,h) / T(j))) / sum(k,x(k,j) * exp((-c_nrtl(k,h)) * (b_nrtl(k,h) / T(j)))) * (b_nrtl(i,h) / T(j) - sum(m_alias,x(m_alias,j) * (b_nrtl(m_alias,h) / T(j)) * exp((-c_nrtl(m_alias,h)) * (b_nrtl(m_alias,h) / T(j)))) / sum(k,x(k,j) * exp((-c_nrtl(k,h)) * (b_nrtl(k,h) / T(j)))))));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation K_equation(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_equation(i,j) $ (ord(j) <= Ns - 1) .. K_part(i,j) * (phi(i,j) * P(j)) =e= gamma_nrtl(i,j) * exp(logPsat(i,j));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_DH_ig(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_DH_ig(i,j) $ (ord(j) <= Ns - 1) .. DH_ig(i,j) =e= C_ig(i,"1") * (T(j) - 298.15) + C_ig(i,"2") * (power(T(j),2) - 88893.42249999999) / 2 + C_ig(i,"3") * (power(T(j),3) - 26503573.918374993) / 3 + C_ig(i,"4") * (power(T(j),4) - 7902040563.763504) / 4 + C_ig(i,"5") * (power(T(j),5) - 2355993394086.0884) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_Hvi(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hvi(i,j) $ (ord(j) <= Ns - 1) .. Hvi(i,j) =e= DH_ig(i,j) + Hform(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_Hv(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hv(j) $ (ord(j) <= Ns - 1) .. Hv(j) / 1.2649862632900375e-05 =e= sum(i,y(i,j) * Hvi(i,j)) + HR(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation Zvi_eq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Zvi_eq(i,j) $ (ord(j) <= Ns - 1) .. (-Zvi(i,j)) + 1 + bii(i) * P(j) / (8.314463 * Tb(i)) - ai_Tb(i) / (bii(i) * 8.314463 * Tb(i)) * (bii(i) * P(j) / (8.314463 * Tb(i))) * (Zvi(i,j) - bii(i) * P(j) / (8.314463 * Tb(i))) / (Zvi(i,j) * (Zvi(i,j) + bii(i) * P(j) / (8.314463 * Tb(i)))) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation v_eq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_eq(i,j) $ (ord(j) <= Ns - 1) .. v_mol_i(i,j) =e= Zvi(i,j) * 8.314463 * Tb(i) / P(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_HR_pure(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_HR_pure(i,j) $ (ord(j) <= Ns - 1) .. HR_pure(i,j) =e= 8.314463 * Tb(i) * (Zvi(i,j) - 1 + (Tb(i) * dadT_Tb(i) - ai_Tb(i)) / (bii(i) * 8.314463 * Tb(i)) * log((v_mol_i(i,j) + bii(i)) / v_mol_i(i,j)));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_DH_liq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_DH_liq(i,j) $ (ord(j) <= Ns - 1) .. DH_liq(i,j) =e= C_liq(i,"1") * (T(j) - Tb(i)) + C_liq(i,"2") * (power(T(j),2) - power(Tb(i),2)) / 2 + C_liq(i,"3") * (power(T(j),3) - power(Tb(i),3)) / 3 + C_liq(i,"4") * (power(T(j),4) - power(Tb(i),4)) / 4 + C_liq(i,"5") * (power(T(j),5) - power(Tb(i),5)) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_Hv_Tbi_P(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hv_Tbi_P(i,j) $ (ord(j) <= Ns - 1) .. Hv_Tbi_P(i,j) =e= DH_ig_Tb(i) + Hform(i) + HR_pure(i,j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_Hli(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hli(i,j) $ (ord(j) <= Ns - 1) .. Hli(i,j) =e= DH_liq(i,j) + Hv_Tbi_P(i,j) - DH_vap(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_Hl(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hl(j) $ (ord(j) <= Ns - 1) .. Hl(j) / 1.2649862632900375e-05 =e= sum(i,x(i,j) * Hli(i,j));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_K_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_K_eq(j) $ (ord(j) <= Ns - 1) .. K_eq(j) =e= exp(10.387 + 4060.59 / T(j) - 2.89055 * log(T(j)) - 0.01915144 * T(j) + 5.28586e-05 * power(T(j),2) - 5.32977e-08 * power(T(j),3));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_k_rate(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_k_rate(j) $ (ord(j) <= Ns - 1) .. k_rate(j) =e= 7418160000000000.0 * exp((-60400.0) / (8.314463 * T(j))) / 60;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_k_A(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_k_A(j) $ (ord(j) <= Ns - 1) .. k_A(j) =e= exp((-1.0707) + 1323.1 / T(j));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation calc_Rx_Rate(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Rx_Rate(j) $ (ord(j) <= Ns - 1) .. Rxn_Rate(j) =e= is_reactive(j) * (k_rate(j) * (x("2",j) * gamma_nrtl("2",j)) * (x("2",j) * gamma_nrtl("2",j) * (x("3",j) * gamma_nrtl("3",j)) - x("4",j) * gamma_nrtl("4",j) / K_eq(j)) / power(1 + k_A(j) * (x("2",j) * gamma_nrtl("2",j)),3));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation mol_balance_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mol_balance_eq(j) $ (ord(j) > 0 and ord(j) < Ns - 1) .. L(j) + V(j) - V(j + 1) - L(j - 1) - FE * is_FE(j) - FB * is_FB(j) - sum(i,v_i(i) * 0.4 * Rxn_Rate(j)) / 7.4858 =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation mol_balance_condenser_eq / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mol_balance_condenser_eq .. V("0") + (L("0") + D) - V("1") =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation mol_balance_reboiler_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mol_balance_reboiler_eq(j) $ (ord(j) eq Ns - 1) .. V(j) + L(j) - L(j - 1) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation comp_balance_eq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
comp_balance_eq(i,j) $ (ord(j) > 0 and ord(j) < Ns - 1) .. L(j) * x(i,j) + V(j) * y(i,j) - V(j + 1) * y(i,j + 1) - L(j - 1) * x(i,j - 1) - FE * is_FE(j) * zE(i) - FB * is_FB(j) * zB(i) - 0.4 * v_i(i) * Rxn_Rate(j) / 7.4858 =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation comp_balance_condenser_eq(i) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
comp_balance_condenser_eq(i) .. V("0") * y(i,"0") + (L("0") + D) * x(i,"0") - V("1") * y(i,"1") =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation comp_balance_reboiler_eq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
comp_balance_reboiler_eq(i,j) $ (ord(j) eq Ns - 1) .. V(j) * y(i,j) + L(j) * x(i,j) - L(j - 1) * x(i,j - 1) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation eq_rel_eq(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_rel_eq(i,j) $ (ord(j) <= Ns - 1) .. K_part(i,j) * x(i,j) - y(i,j) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation summation_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
summation_eq(j) $ (ord(j) <= Ns - 1) .. sum(i,y(i,j) - x(i,j)) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation energy_balance_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
energy_balance_eq(j) $ (ord(j) > 0 and ord(j) < Ns - 1) .. V(j) * Hv(j) + L(j) * Hl(j) - V(j + 1) * Hv(j + 1) - L(j - 1) * Hl(j - 1) - FE * is_FE(j) * HFE - FB * is_FB(j) * HFB =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation energy_balance_condenser_eq / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
energy_balance_condenser_eq .. V("0") * Hv("0") + (L("0") + D) * Hl("0") - V("1") * Hv("1") + Qc =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation energy_balance_reboiler_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
energy_balance_reboiler_eq(j) $ (ord(j) eq Ns - 1) .. V(j) * Hv(j) + L(j) * Hl(j) - L(j - 1) * Hl(j - 1) - Qr =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation spec_2_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
spec_2_eq(j) $ (ord(j) eq Ns - 1) .. x("4",j) =e= Spec_2;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation V1_eq / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V1_eq .. V("0") =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation def_Mw_mix(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Mw_mix(j) $ (ord(j) <= Ns - 1) .. Mw_mix(j) =e= sum(i,y(i,j) * Mw(i));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation def_D_col(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_D_col(j) $ (ord(j) > 0 and ord(j) < Ns - 1) .. D_col(j) =e= sqrt(4 * (V(j) * 7.4858 * v_mol(j) / 60 / (FF / sqrt(Mw_mix(j) * 0.001 / v_mol(j)) * 0.88)) / 3.141592653589793) * 3.28084;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation def_Dcol_max(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Dcol_max(j) $ (ord(j) > 0 and ord(j) < Ns - 1) .. Dcol_max =g= D_col(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation def_Tcond / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Tcond .. Tcond =e= T("0");
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation def_Treb(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Treb(j) $ (ord(j) eq Ns - 1) .. Treb =e= T(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation def_Breb(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Breb(j) $ (ord(j) eq Ns - 1) .. Breb =e= L(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation eq_ColCost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_ColCost .. v_ColCost =e= MS / 280 * (101.9 * rPower(Dcol_max,1.066) * rPower(0.7315 * (Ns - 2) * 3.28084,0.802) * 7.05);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation eq_TrayCost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_TrayCost .. v_TrayCost =e= MS / 280 * (4.7 * rPower(Dcol_max,1.55) * (0.7315 * (Ns - 2) * 3.28084) * 2.7);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation eq_CondCost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_CondCost .. v_CondCost =e= rPower(Qc * 591769.2719073936 / 60 / (851.7403895292715 * (10 / log((Tcond - 303.15) / (Tcond - 313.15)))) * 10.7639,0.65) * 1709.8394439285714;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation eq_RebCost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_RebCost .. v_RebCost =e= MS / 280 * 101.3 * (rPower(Qr * 591769.2719073936 / 60 / (1419.5673158821191 * (433.15 - Treb)) * 10.7639,0.65) * 7.3525);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation eq_CAP_cost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_CAP_cost .. CAP_cost =e= 0.3333333333333333 * (v_TrayCost + v_ColCost + v_CondCost + v_RebCost + 7.7 * sum(j,is_reactive(j)) * 0.4);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation eq_OP_cost / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_OP_cost .. OP_cost =e= (3.78e-10 * Qc + c_steam * Qr) * 8150 * 60 * 591769.2719073936 + (FE * CostEth + FB * CostBut - CostETBE * Breb) * 7.4858 * 8150 * 60;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation def_Profit / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Profit .. Profit * 1000000.0 =e= CAP_cost + OP_cost;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation obj_def / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
obj_def .. obj =e= Profit;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation dummy_T(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dummy_T(j) $ (ord(j) > Ns - 1) .. T(j) =e= 350;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation dummy_L(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dummy_L(j) $ (ord(j) > Ns - 1) .. L(j) =e= 1e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation dummy_V(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dummy_V(j) $ (ord(j) > Ns - 1) .. V(j) =e= 1e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Equation dummy_x(i,j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dummy_x(i,j) $ (ord(j) > Ns - 1) .. x(i,j) =e= 0.25;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
L.lo(j) = 1e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
L.up(j) = 50;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
L.l(j) = 0.5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.lo(j) = 1e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.up(j) = 50;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.l(j) = 0.5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.lo("0") = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.up("0") = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.l("0") = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
x.lo(i,j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
x.up(i,j) = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
x.l(i,j) = 0.25;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
y.lo(i,j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
y.up(i,j) = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
y.l(i,j) = 0.25;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
D.lo = 0.01;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
D.up = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
D.l = 0.5748006462583984;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Qc.lo = 0.01;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Qc.up = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Qc.l = 0.5451343354854316;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Qr.lo = 0.01;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Qr.up = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Qr.l = 0.4592022879232921;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Breb.lo = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Breb.up = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Breb.l = 0.24;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
T.lo(j) = 330;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
T.up(j) = 410;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
T.scale(j) = 333.69;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
FE.lo = 0.00075;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
FE.up = 37.43;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
FE.l = 0.7713270458735205;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
logPsat.lo(i,j) = kk(i,"1") + kk(i,"2") / (kk(i,"3") + 330) + kk(i,"4") * 330 + kk(i,"5") * log(330) + kk(i,"6") * rPower(330,kk(i,"7"));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
logPsat.up(i,j) = kk(i,"1") + kk(i,"2") / (kk(i,"3") + 410) + kk(i,"4") * 410 + kk(i,"5") * log(410) + kk(i,"6") * rPower(410,kk(i,"7"));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
logPsat.scale(i,j) = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
alpha_ij.lo(i,j) = 0.5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
alpha_ij.up(i,j) = 2;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
aii.lo(i,j) = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
aii.up(i,j) = 4;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
a.lo(j) = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
a.up(j) = 3;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
b.lo(j) = 1e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
b.up(j) = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
b.scale(j) = 1e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_ii.lo(i,j) = (-0.009);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_ii.up(i,j) = (-0.001);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_ii.scale(i,j) = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT.lo(j) = (-0.009);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT.up(j) = (-0.001);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT.scale(j) = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_part.lo(i,j) = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_part.up(i,j) = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
phi.lo(i,j) = 0.1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
phi.up(i,j) = 1.2;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_ig.lo(i,j) = C_ig(i,"1") * 31.850000000000023 + C_ig(i,"2") * 20006.577500000014 / 2 + C_ig(i,"3") * 9433426.081625007 / 3 + C_ig(i,"4") * 3957169436.236496 / 4 + C_ig(i,"5") * 1557545905913.9116 / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_ig.up(i,j) = C_ig(i,"1") * 111.85000000000002 + C_ig(i,"2") * 79206.57750000001 / 2 + C_ig(i,"3") * 42417426.08162501 / 3 + C_ig(i,"4") * 20355569436.236496 / 4 + C_ig(i,"5") * 9229626705913.912 / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_ig.scale(i,j) = 1000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hvi.lo(i,j) = DH_ig.lo(i,j) + Hform(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hvi.up(i,j) = DH_ig.up(i,j) + Hform(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hvi.scale(i,j) = 100000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
HR.lo(j) = (-2500);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
HR.up(j) = (-1100);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
HR.scale(j) = 1000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hv.lo(j) = (smin(i,Hvi.lo(i,j)) + HR.lo(j)) * 1.2649862632900375e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hv.up(j) = (smax(i,Hvi.up(i,j)) + HR.up(j)) * 1.2649862632900375e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_liq.lo(i,j) = C_liq(i,"1") * (330 - Tb(i)) + C_liq(i,"2") * (108900 - power(Tb(i),2)) / 2 + C_liq(i,"3") * (35937000 - power(Tb(i),3)) / 3 + C_liq(i,"4") * (11859210000 - power(Tb(i),4)) / 4 + C_liq(i,"5") * (3913539300000 - power(Tb(i),5)) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_liq.up(i,j) = C_liq(i,"1") * (410 - Tb(i)) + C_liq(i,"2") * (168100 - power(Tb(i),2)) / 2 + C_liq(i,"3") * (68921000 - power(Tb(i),3)) / 3 + C_liq(i,"4") * (28257610000 - power(Tb(i),4)) / 4 + C_liq(i,"5") * (11585620100000 - power(Tb(i),5)) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_liq.scale(i,j) = 10000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
HR_pure.lo(i,j) = (-3000.0);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
HR_pure.up(i,j) = (-1000.0);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
HR_pure.scale(i,j) = 1000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hv_Tbi_P.lo(i,j) = DH_ig_Tb(i) * 0.99 + Hform(i) + HR_pure.lo(i,j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hv_Tbi_P.up(i,j) = DH_ig_Tb(i) * 1.01 + Hform(i) + HR_pure.up(i,j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hv_Tbi_P.scale(i,j) = 10000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hli.lo(i,j) = DH_liq.lo(i,j) + Hv_Tbi_P.lo(i,j) - DH_vap(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hli.up(i,j) = DH_liq.up(i,j) + Hv_Tbi_P.up(i,j) - DH_vap(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hli.scale(i,j) = 100000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hl.lo(j) = smin(i,Hvi.lo(i,j)) * 1.2649862632900375e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hl.up(j) = smax(i,Hvi.up(i,j)) * 1.2649862632900375e-05;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Z.lo(j) = 0.75;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Z.up(j) = 0.9;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Z.l(j) = 0.822;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol.lo(j) = Z.lo(j) * 8.314463 * 330 / 950000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol.up(j) = Z.up(j) * 8.314463 * 410 / 950000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol.scale(j) = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Zvi.lo(i,j) = 0.75;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Zvi.up(i,j) = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Zvi.l(i,j) = 0.9;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol_i.lo(i,j) = Zvi.lo(i,j) * 8.314463 * 330 / 950000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol_i.up(i,j) = Zvi.up(i,j) * 8.314463 * 410 / 950000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol_i.scale(i,j) = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
gamma_nrtl.lo(i,j) = 0.01;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
gamma_nrtl.up(i,j) = 20;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_eq.lo(j) = exp(20.29087804878049 - 2.89055 * log(410) - 7.8520904 + 8.88553066 - 3.6733307817000003);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_eq.up(j) = exp(22.691818181818185 - 2.89055 * log(330) - 6.3199752 + 5.75630154 - 1.9153594449);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_eq.scale(j) = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_rate.lo(j) = 7418160000000000.0 * exp(-22.013484578655653) / 60;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_rate.up(j) = 7418160000000000.0 * exp(-17.71817051452772) / 60;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_rate.scale(j) = 10000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_A.lo(j) = exp(2.1563731707317073);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_A.up(j) = exp(2.938693939393939);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_A.scale(j) = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Rxn_Rate.lo(j) = (-10);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Rxn_Rate.up(j) = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Mw_mix.lo(j) = 45;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Mw_mix.up(j) = 103;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Mw_mix.scale(j) = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
D_col.lo(j) = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
D_col.up(j) = 2;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
D_col.l(j) = 0.03;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
D_col.scale(j) = 0.1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Dcol_max.lo = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Dcol_max.up = 2;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Tcond.lo = 330;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Tcond.up = 380;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Tcond.scale = 333.69;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Treb.lo = 360;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Treb.up = 410;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Treb.scale = 333.69;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
L.l(j) = 0.5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.l(j) = 0.5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.l("0") = 0.1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
x.l(i,j) = 0.25;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
y.l(i,j) = 0.25;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_part.l(i,j) = 1.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
logPsat.l(i,j) = 11.5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
gamma_nrtl.l(i,j) = 1.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
phi.l(i,j) = 1.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
alpha_ij.l(i,j) = 1.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
aii.l(i,j) = 2.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
a.l(j) = 2.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
b.l(j) = 0.0001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_ii.l(i,j) = (-0.005);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT.l(j) = (-0.005);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Z.l(j) = 0.822;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Zvi.l(i,j) = 0.9;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol.l(j) = 0.003;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol_i.l(i,j) = 0.003;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Mw_mix.l(j) = 60.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_eq.l(j) = 10.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_rate.l(j) = 100.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_A.l(j) = 10.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Rxn_Rate.l(j) = 0.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_ig.l(i,j) = 5000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hvi.l(i,j) = (-150000.0);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hv.l(j) = (-1);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_liq.l(i,j) = 1000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
HR_pure.l(i,j) = (-2000.0);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hv_Tbi_P.l(i,j) = (-150000.0);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hli.l(i,j) = (-180000.0);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Hl.l(j) = (-1);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Model MESHR_Superstructure / psat_def,cubic_eos,alpha_definition,aii_definition,mixing_rule_b,mixing_rule_a,v_definition,fugacity_eq,dadT_ii_eq,dadT_eq,enthalpy_eq,Compute_gamma,K_equation,calc_DH_ig,calc_Hvi,calc_Hv,Zvi_eq,v_eq,calc_HR_pure,calc_DH_liq,calc_Hv_Tbi_P,calc_Hli,calc_Hl,calc_K_eq,calc_k_rate,calc_k_A,calc_Rx_Rate,mol_balance_eq,mol_balance_condenser_eq,mol_balance_reboiler_eq,comp_balance_eq,comp_balance_condenser_eq,comp_balance_reboiler_eq,eq_rel_eq,summation_eq,energy_balance_eq,energy_balance_condenser_eq,energy_balance_reboiler_eq,spec_2_eq,V1_eq,def_Mw_mix,def_D_col,def_Dcol_max,def_Tcond,def_Treb,def_Breb,eq_ColCost,eq_TrayCost,eq_CondCost,eq_RebCost,eq_CAP_cost,eq_OP_cost,def_Profit,obj_def,dummy_T,dummy_L,dummy_V,dummy_x /;
$offListing
Parameter autogenerated_domUsd_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_etAlg_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_etSolve_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_etSolver_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_iterUsd_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_marginals_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_maxInfes_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_meanInfes_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_modelStat_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_nodUsd_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_number_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numDepnd_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numDVar_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numEqu_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numInfes_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numNLIns_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numNLNZ_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numNOpt_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numNZ_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numRedef_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numVar_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_numVarProj_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_objEst_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_objVal_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_procUsed_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_resGen_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_resUsd_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_solveStat_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_sumInfes_m7E8D0NaoTWSyMQU_D1gWUQ;
Parameter autogenerated_sysVer_m7E8D0NaoTWSyMQU_D1gWUQ;
$onListing
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Ns = 10;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FE(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FB(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FE("4") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FB("6") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive("2") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive("4") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive("6") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
MESHR_Superstructure.scaleopt = 1;

solve MESHR_Superstructure using NLP MIN obj;

$offListing
autogenerated_domUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.domUsd;
autogenerated_etAlg_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etAlg;
autogenerated_etSolve_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etSolve;
autogenerated_etSolver_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etSolver;
autogenerated_iterUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.iterUsd;
autogenerated_marginals_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.marginals;
autogenerated_maxInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.maxInfes;
autogenerated_meanInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.meanInfes;
autogenerated_modelStat_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.modelStat;
autogenerated_nodUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.nodUsd;
autogenerated_number_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.number;
autogenerated_numDepnd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numDepnd;
autogenerated_numDVar_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numDVar;
autogenerated_numEqu_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numEqu;
autogenerated_numInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numInfes;
autogenerated_numNLIns_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNLIns;
autogenerated_numNLNZ_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNLNZ;
autogenerated_numNOpt_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNOpt;
autogenerated_numNZ_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNZ;
autogenerated_numRedef_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numRedef;
autogenerated_numVar_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numVar;
autogenerated_numVarProj_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numVarProj;
autogenerated_objEst_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.objEst;
autogenerated_objVal_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.objVal;
autogenerated_procUsed_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.procUsed;
autogenerated_resGen_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.resGen;
autogenerated_resUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.resUsd;
autogenerated_solveStat_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.solveStat;
autogenerated_sumInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.sumInfes;
autogenerated_sysVer_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.sysVer;
$onListing
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Ns = 12;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FE(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FB(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FE("6") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FB("8") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive("4") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
MESHR_Superstructure.scaleopt = 1;

solve MESHR_Superstructure using NLP MIN obj;

$offListing
autogenerated_domUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.domUsd;
autogenerated_etAlg_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etAlg;
autogenerated_etSolve_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etSolve;
autogenerated_etSolver_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etSolver;
autogenerated_iterUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.iterUsd;
autogenerated_marginals_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.marginals;
autogenerated_maxInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.maxInfes;
autogenerated_meanInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.meanInfes;
autogenerated_modelStat_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.modelStat;
autogenerated_nodUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.nodUsd;
autogenerated_number_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.number;
autogenerated_numDepnd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numDepnd;
autogenerated_numDVar_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numDVar;
autogenerated_numEqu_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numEqu;
autogenerated_numInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numInfes;
autogenerated_numNLIns_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNLIns;
autogenerated_numNLNZ_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNLNZ;
autogenerated_numNOpt_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNOpt;
autogenerated_numNZ_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNZ;
autogenerated_numRedef_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numRedef;
autogenerated_numVar_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numVar;
autogenerated_numVarProj_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numVarProj;
autogenerated_objEst_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.objEst;
autogenerated_objVal_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.objVal;
autogenerated_procUsed_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.procUsed;
autogenerated_resGen_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.resGen;
autogenerated_resUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.resUsd;
autogenerated_solveStat_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.solveStat;
autogenerated_sumInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.sumInfes;
autogenerated_sysVer_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.sysVer;
$onListing
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Ns = 15;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FE(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FB(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive(j) = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FE("7") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_FB("9") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive("4") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive("5") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive("6") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
is_reactive("7") = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
MESHR_Superstructure.scaleopt = 1;

solve MESHR_Superstructure using NLP MIN obj;

$offListing
autogenerated_domUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.domUsd;
autogenerated_etAlg_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etAlg;
autogenerated_etSolve_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etSolve;
autogenerated_etSolver_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.etSolver;
autogenerated_iterUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.iterUsd;
autogenerated_marginals_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.marginals;
autogenerated_maxInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.maxInfes;
autogenerated_meanInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.meanInfes;
autogenerated_modelStat_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.modelStat;
autogenerated_nodUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.nodUsd;
autogenerated_number_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.number;
autogenerated_numDepnd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numDepnd;
autogenerated_numDVar_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numDVar;
autogenerated_numEqu_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numEqu;
autogenerated_numInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numInfes;
autogenerated_numNLIns_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNLIns;
autogenerated_numNLNZ_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNLNZ;
autogenerated_numNOpt_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNOpt;
autogenerated_numNZ_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numNZ;
autogenerated_numRedef_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numRedef;
autogenerated_numVar_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numVar;
autogenerated_numVarProj_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.numVarProj;
autogenerated_objEst_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.objEst;
autogenerated_objVal_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.objVal;
autogenerated_procUsed_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.procUsed;
autogenerated_resGen_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.resGen;
autogenerated_resUsd_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.resUsd;
autogenerated_solveStat_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.solveStat;
autogenerated_sumInfes_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.sumInfes;
autogenerated_sysVer_m7E8D0NaoTWSyMQU_D1gWUQ = MESHR_Superstructure.sysVer;
$onListing
$offDotL
$offUNDF
$offMulti
