$onMultiR
$onUNDF
$onDotL
Set i(*) "Number of components";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_CSvhZaUBQgOaUn3JNLGKCQin.gdx
$loadDC i
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Set j(*) "Number of stages";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_MtMuQPipRneSH3n00jpf_gin.gdx
$loadDC j
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter P(j) "Pressure (Pa)" / /;
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
Parameter m_cat "catalyst mass [kg]" / 0.4 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Tmin "Minimum temperature limit" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Tmin = 330;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Tmax "Maximum temperature limit" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Tmax = 410;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter R "Gas constant J K-1 kmol-1" / 8.314463 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter v_i(i) "Reaction coefficient";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_9nQdSNQ1T1mHvCi6iT42agin.gdx
$loadDC v_i
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Tc(i) "Critical Temperature [K]";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_4nT__C20TV_nLV5y6rDRUAin.gdx
$loadDC Tc
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter zE(i) "Molar fraction of ethanol";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_KyxjLcQ9R8iwPxsGod_jLAin.gdx
$loadDC zE
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter zB(i) "Molar fraction of butenes";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_fgOXs5izTnCdU_z05ik3wwin.gdx
$loadDC zB
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Mw(i) "Molecular weights (kg/kmol)";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_FQK8Ki1qSDiAGk8LnSjefQin.gdx
$loadDC Mw
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Pc(i) "Critical pressure (Pa)";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_5dC6UGL5SG6pjq6fL8t75Qin.gdx
$loadDC Pc
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter w(i) "Acentric factor";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_cCgjj7iEQDi6iKsW9ZPLFgin.gdx
$loadDC w
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Tb(i) "Boiling temperature (K)";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_miXE8Vf6SAangOcdYCIB_win.gdx
$loadDC Tb
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Hform(i) "Heat of formation (J/mol)";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_WrDpEC6OTNy0ftFpOH4vLQin.gdx
$loadDC Hform
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Omega_a "SRK parameter" / 0.42747 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Omega_b "SRK parameter" / 0.08664 /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter kappa(i) "SRK equation parameter" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter ac(i) "Component-specific parameter" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter bii(i) "SRK b-parameter" / /;
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
ac(i) = Omega_a * power(R * Tc(i),2) / Pc(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
bii(i) = Omega_b * R * Tc(i) / Pc(i);
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
positive Variable L(j) "Liquid flowrate [mol/min]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable V(j) "Vapor flowrate [mol/min]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable x(i,j) "Liquid fraction" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable y(i,j) "Vapor fraction" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable T(j) "Temperature [K]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable FE "Etanol feed molar flowrate [mol/min]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable D "Destillate product flowrate (mol/min)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable Qc "Condenser Duty (J/min)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable Qr "Reboiler Duty (J/min)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Z(j) "Compressibility factor" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_mol(j) "Molar volume" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable phi(i,j) "Fugacity coefficient" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable HR(j) "Residual enthalpy" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable alpha_ij(i,j) "Alpha parameter" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable aii(i,j) "Component-wise SRK aii parameter" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable a(j) "Mixture parameter a" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable b(j) "Mixture parameter b" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable dadT_ii(i,j) "Partial derivative of a to T" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable dadT(j) "Total temperature derivative of a" / /;
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
Set c(*) "Antoine coefficient columns";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\__znJNN9qTsOaB7IY63zDCQin.gdx
$loadDC c
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
positive Variable logPsat(i,j) "Saturation Pressure (Pa)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter kk(i,c) "psat antoine parameters" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_fQdGKZTCRz2TSCENg8Qdvwin.gdx
$loadDC kk
$gdxIn
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
psat_def(i,j) .. logPsat(i,j) =e= kk(i,"1") + kk(i,"2") / (kk(i,"3") + T(j)) + kk(i,"4") * T(j) + kk(i,"5") * log(T(j)) + kk(i,"6") * rPower(T(j),kk(i,"7"));
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
Equation v_definition(j) / /;
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
Equation enthalpy_eq(j) / /;
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
Equation aii_definition(i,j) / /;
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
Equation mixing_rule_a(j) / /;
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
Equation dadT_eq(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
cubic_eos(j) .. (-Z(j)) + 1 + b(j) * P(j) / (R * T(j)) - a(j) / (b(j) * R * T(j)) * (b(j) * P(j) / (R * T(j))) * (Z(j) - b(j) * P(j) / (R * T(j))) / (Z(j) * (Z(j) + b(j) * P(j) / (R * T(j)))) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
alpha_definition(i,j) .. alpha_ij(i,j) =e= power(1 + kappa(i) * (1 - sqrt(T(j) / Tc(i))),2);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
aii_definition(i,j) .. aii(i,j) =e= alpha_ij(i,j) * ac(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mixing_rule_b(j) .. b(j) =e= sum(i,y(i,j) * bii(i));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mixing_rule_a(j) .. a(j) =e= sum(i,sum(k,y(i,j) * y(k,j) * sqrt(aii(i,j) * aii(k,j))));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_definition(j) .. v_mol(j) =e= Z(j) * R * T(j) / P(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
fugacity_eq(i,j) .. phi(i,j) =e= exp(bii(i) * (Z(j) - 1) / b(j) - log(P(j) * (v_mol(j) - b(j)) / (R * T(j))) + a(j) / (b(j) * R * T(j)) * (bii(i) / b(j) - 2 * sum(k,y(k,j) * sqrt(aii(i,j) * aii(k,j))) / a(j)) * log((v_mol(j) + b(j)) / v_mol(j)));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_ii_eq(i,j) .. dadT_ii(i,j) =e= (-(ac(i) * kappa(i))) * sqrt(alpha_ij(i,j) * (T(j) / Tc(i))) / T(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
dadT_eq(j) .. dadT(j) =e= (-sum(i,sum(k,y(i,j) * y(k,j) * sqrt(dadT_ii(i,j) * dadT_ii(k,j)))));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
enthalpy_eq(j) .. HR(j) =e= R * T(j) * (Z(j) - 1 + (T(j) * dadT(j) - a(j)) / (b(j) * R * T(j)) * log((v_mol(j) + b(j)) / v_mol(j)));
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
Parameter b_nrtl(i,i) "NRTL b parameter" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter c_nrtl(i,i) "NRTL c parameter" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_ecf6FljKT__mVfgoudiQBAin.gdx
$loadDC b_nrtl
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_fNSrHOLNRpamY83hJV8nBAin.gdx
$loadDC c_nrtl
$gdxIn
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
Equation Compute_gamma(i,j) / /;
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
Compute_gamma(i,j) .. gamma_nrtl(i,j) =e= exp(sum(h,x(h,j) * (b_nrtl(h,i) / T(j)) * exp((-c_nrtl(h,i)) * (b_nrtl(h,i) / T(j)))) / sum(k,x(k,j) * exp((-c_nrtl(k,i)) * (b_nrtl(k,i) / T(j)))) + sum(h,x(h,j) * exp((-c_nrtl(i,h)) * (b_nrtl(i,h) / T(j))) / sum(k,x(k,j) * exp((-c_nrtl(k,h)) * (b_nrtl(k,h) / T(j)))) * (b_nrtl(i,h) / T(j) - sum(m_alias,x(m_alias,j) * (b_nrtl(m_alias,h) / T(j)) * exp((-c_nrtl(m_alias,h)) * (b_nrtl(m_alias,h) / T(j)))) / sum(k,x(k,j) * exp((-c_nrtl(k,h)) * (b_nrtl(k,h) / T(j)))))));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_equation(i,j) .. K_part(i,j) * (phi(i,j) * P(j)) =e= gamma_nrtl(i,j) * exp(logPsat(i,j));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Set cc(*) "Coefficient columns";
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_B6QQ6kG2RqC5MSGVaM80ugin.gdx
$loadDC cc
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter T0 "Reference temperature [K]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
T0 = 298.15;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter e / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
e = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter sigma / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
sigma = 1;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter C_ig(i,cc) "Heat capacity coefficients for ideal gas" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter C_liq(i,cc) "Heat capacity coefficients for liquid phase" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter C_vap(i,cc) "DIPPR coefficients for vaporization enthalpy" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_8UZyVNnjQi2g4k19a0HB_Ain.gdx
$loadDC C_ig
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_YBhpGXrSSLyBy6Xyg8rsnwin.gdx
$loadDC C_liq
$gdxIn
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
$gdxIn C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_QqocJpHTSWKx1Q46uU3sawin.gdx
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
Parameter DH_vap(i) "Vaporization enthalpy at Tb [J/mol]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter DH_ig_Tb(i) "DH_ig from T0 to TB [J/mol]" / /;
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
DH_ig_Tb(i) = C_ig(i,"1") * (Tb(i) - T0) + C_ig(i,"2") * (power(Tb(i),2) - power(T0,2)) / 2 + C_ig(i,"3") * (power(Tb(i),3) - power(T0,3)) / 3 + C_ig(i,"4") * (power(Tb(i),4) - power(T0,4)) / 4 + C_ig(i,"5") * (power(Tb(i),5) - power(T0,5)) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable DH_ig(i,j) "Ideal gas enthalpy change" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hvi(i,j) "Ideal gas enthalpy of vapor phase + Hform" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hv(j) "Total vapor phase enthalpy" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable DH_liq(i,j) "Liquid enthalpy change from Tb to T" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hv_Tbi_P(i,j) "Vapor phase enthalpy at Tb" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hli(i,j) "Liquid enthalpy for each component" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Hl(j) "Total liquid phase enthalpy" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable HR_pure(i,j) "Residual enthalpy pure substance" / /;
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
Equation calc_DH_ig(i,j) / /;
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
Equation calc_Hv(j) / /;
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
Equation v_eq(i,j) / /;
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
Equation calc_DH_liq(i,j) / /;
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
Equation calc_Hli(i,j) / /;
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
calc_DH_ig(i,j) .. DH_ig(i,j) =e= C_ig(i,"1") * (T(j) - T0) + C_ig(i,"2") * (power(T(j),2) - power(T0,2)) / 2 + C_ig(i,"3") * (power(T(j),3) - power(T0,3)) / 3 + C_ig(i,"4") * (power(T(j),4) - power(T0,4)) / 4 + C_ig(i,"5") * (power(T(j),5) - power(T0,5)) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hvi(i,j) .. Hvi(i,j) =e= DH_ig(i,j) + Hform(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hv(j) .. Hv(j) / 1.2649862632900375e-05 =e= sum(i,y(i,j) * Hvi(i,j)) + HR(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Zvi_eq(i,j) .. (-Zvi(i,j)) + 1 + bii(i) * P(j) / (R * Tb(i)) - ai_Tb(i) / (bii(i) * R * Tb(i)) * (bii(i) * P(j) / (R * Tb(i))) * (Zvi(i,j) - bii(i) * P(j) / (R * Tb(i))) / (Zvi(i,j) * (Zvi(i,j) + bii(i) * P(j) / (R * Tb(i)))) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_eq(i,j) .. v_mol_i(i,j) =e= Zvi(i,j) * R * Tb(i) / P(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_HR_pure(i,j) .. HR_pure(i,j) =e= R * Tb(i) * (Zvi(i,j) - 1 + (Tb(i) * dadT_Tb(i) - ai_Tb(i)) / (bii(i) * R * Tb(i)) * log((v_mol_i(i,j) + bii(i)) / v_mol_i(i,j)));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_DH_liq(i,j) .. DH_liq(i,j) =e= C_liq(i,"1") * (T(j) - Tb(i)) + C_liq(i,"2") * (power(T(j),2) - power(Tb(i),2)) / 2 + C_liq(i,"3") * (power(T(j),3) - power(Tb(i),3)) / 3 + C_liq(i,"4") * (power(T(j),4) - power(Tb(i),4)) / 4 + C_liq(i,"5") * (power(T(j),5) - power(Tb(i),5)) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hv_Tbi_P(i,j) .. Hv_Tbi_P(i,j) =e= DH_ig_Tb(i) + Hform(i) + HR_pure(i,j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hli(i,j) .. Hli(i,j) =e= DH_liq(i,j) + Hv_Tbi_P(i,j) - DH_vap(i);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Hl(j) .. Hl(j) / 1.2649862632900375e-05 =e= sum(i,x(i,j) * Hli(i,j));
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
Equation calc_K_eq(j) / /;
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
Equation calc_k_A(j) / /;
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
Equation assign_zero(j) / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_K_eq(j) $ (ord(j) eq 3 or ord(j) eq 5 or ord(j) eq 7) .. K_eq(j) =e= exp(10.387 + 4060.59 / T(j) - 2.89055 * log(T(j)) - 0.01915144 * T(j) + 5.28586e-05 * power(T(j),2) - 5.32977e-08 * power(T(j),3));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_k_rate(j) $ (ord(j) eq 3 or ord(j) eq 5 or ord(j) eq 7) .. k_rate(j) =e= 7418160000000000.0 * exp((-60400.0) / (R * T(j))) / 60;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_k_A(j) $ (ord(j) eq 3 or ord(j) eq 5 or ord(j) eq 7) .. k_A(j) =e= exp((-1.0707) + 1323.1 / T(j));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
calc_Rx_Rate(j) $ (ord(j) eq 3 or ord(j) eq 5 or ord(j) eq 7) .. Rxn_Rate(j) =e= k_rate(j) * (x("2",j) * gamma_nrtl("2",j)) * (x("2",j) * gamma_nrtl("2",j) * (x("3",j) * gamma_nrtl("3",j)) - x("4",j) * gamma_nrtl("4",j) / K_eq(j)) / power(1 + k_A(j) * (x("2",j) * gamma_nrtl("2",j)),3);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
assign_zero(j) $ ((not (ord(j) eq 3 or ord(j) eq 5 or ord(j) eq 7))) .. Rxn_Rate(j) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Spec_1 "Ethanol conversion" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Spec_1 = 0.85;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter Spec_2 "ETBE molar fraction on the bottom product" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Spec_2 = 0.83;
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
Equation mol_balance_condenser_eq / /;
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
Equation comp_balance_eq(i,j) / /;
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
Equation comp_balance_reboiler_eq(i,j) / /;
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
Equation summation_eq(j) / /;
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
Equation energy_balance_condenser_eq / /;
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
Equation spec_2_eq(j) / /;
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
mol_balance_eq(j) $ (ord(j) > 1 and ord(j) < 10) .. L(j) + V(j) - V(j + 1) - L(j - 1) - FE * (ord(j) eq 5) - FB * (ord(j) eq 7) - sum(i,v_i(i) * m_cat * Rxn_Rate(j)) / 7.4858 =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mol_balance_condenser_eq .. V("1") + (L("1") + D) - V("2") =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
mol_balance_reboiler_eq(j) $ (ord(j) eq 10) .. V(j) + L(j) - L(j - 1) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
comp_balance_eq(i,j) $ (ord(j) > 1 and ord(j) < 10) .. L(j) * x(i,j) + V(j) * y(i,j) - V(j + 1) * y(i,j + 1) - L(j - 1) * x(i,j - 1) - FE * (ord(j) eq 5) * zE(i) - FB * (ord(j) eq 7) * zB(i) - m_cat * v_i(i) * Rxn_Rate(j) / 7.4858 =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
comp_balance_condenser_eq(i) .. V("1") * y(i,"1") + (L("1") + D) * x(i,"1") - V("2") * y(i,"2") =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
comp_balance_reboiler_eq(i,j) $ (ord(j) eq 10) .. V(j) * y(i,j) + L(j) * x(i,j) - L(j - 1) * x(i,j - 1) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_rel_eq(i,j) .. K_part(i,j) * x(i,j) - y(i,j) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
summation_eq(j) .. sum(i,y(i,j) - x(i,j)) =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
energy_balance_eq(j) $ (ord(j) > 1 and ord(j) < 10) .. V(j) * Hv(j) + L(j) * Hl(j) - V(j + 1) * Hv(j + 1) - L(j - 1) * Hl(j - 1) - FE * (ord(j) eq 5) * HFE - FB * (ord(j) eq 7) * HFB =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
energy_balance_condenser_eq .. V("1") * Hv("1") + (L("1") + D) * Hl("1") - V("2") * Hv("2") + Qc =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
energy_balance_reboiler_eq(j) $ (ord(j) eq 10) .. V(j) * Hv(j) + L(j) * Hl(j) - L(j - 1) * Hl(j - 1) - Qr =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
spec_2_eq(j) $ (ord(j) eq 10) .. x("4",j) =e= Spec_2;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V1_eq .. V("1") =e= 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter FF "Flooding velocity estimation parameter" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
FF = 1.8420539101049511;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter MS "Marshall & Swift Parameter" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
MS = 1773.4;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter CostETBE "Price of ETBE bottom product [$/mol]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
CostETBE = 0.0253;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter CostEth "Price of Ethanol [$/mol]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
CostEth = 0.015;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter CostBut "Price of Butenes [$/mol]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
CostBut = 0.00825;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Parameter c_steam "Steam cost parameter [$/J]" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
c_steam = 4.54e-09;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable D_col(j) "Column diameter (ft)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Dcol_max "Maximum column diameter (ft)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Mw_mix(j) "Molecular weights (kg/kmol)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Tcond "Condenser temperature (K)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Treb "Reboiler Temperature (K)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Breb "Bottoms flowrate" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_AreaCond "Condenser heat transfer area (ft2)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_AreaReb "Reboiler heat transfer area (ft2)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_ColCost "Column shell cost ($)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_TrayCost "Tray cost ($)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_CondCost "Condenser cost ($)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable v_RebCost "Reboiler cost ($)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable CAP_cost "Capital cost ($/yr)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable OP_cost "Operational cost ($/yr)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable Profit "Annual Profit (Millions $)" / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
free Variable obj "Objective Function Variable" / /;
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
Equation def_Mw_mix(j) / /;
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
Equation def_Tcond / /;
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
Equation def_Breb(j) / /;
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
Equation eq_TrayCost / /;
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
Equation eq_RebCost / /;
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
Equation eq_OP_cost / /;
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
Equation obj_def / /;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Mw_mix(j) .. Mw_mix(j) =e= sum(i,y(i,j) * Mw(i));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_D_col(j) $ (ord(j) > 1 and ord(j) < 10) .. D_col(j) =e= sqrt(4 * (V(j) * 7.4858 * v_mol(j) / 60 / (FF / sqrt(Mw_mix(j) * 0.001 / v_mol(j)) * 0.88)) / 3.141592653589793) * 3.28084;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Dcol_max(j) $ (ord(j) > 1 and ord(j) < 10) .. Dcol_max =g= D_col(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Tcond .. Tcond =e= T("1");
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Treb(j) $ (ord(j) eq 10) .. Treb =e= T(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
def_Breb(j) $ (ord(j) eq 10) .. Breb =e= L(j);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_ColCost .. v_ColCost =e= MS / 280 * (101.9 * rPower(Dcol_max,1.066) * 10.695425665923146 * 7.05);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_TrayCost .. v_TrayCost =e= MS / 280 * (4.7 * rPower(Dcol_max,1.55) * 19.199475680000003 * 2.7);
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
eq_RebCost .. v_RebCost =e= MS / 280 * 101.3 * (rPower(Qr * 591769.2719073936 / 60 / (1419.5673158821191 * (433.15 - Treb)) * 10.7639,0.65) * 7.3525);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
eq_CAP_cost .. CAP_cost =e= 0.3333333333333333 * (v_TrayCost + v_ColCost + v_CondCost + v_RebCost + 9.24);
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
def_Profit .. Profit * 1000000.0 =e= CAP_cost + OP_cost;
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
V.lo("1") = 0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.up("1") = 0.001;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
V.l("1") = 0;
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
T.lo(j) = Tmin;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
T.up(j) = Tmax;
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
logPsat.lo(i,j) = kk(i,"1") + kk(i,"2") / (kk(i,"3") + Tmin) + kk(i,"4") * Tmin + kk(i,"5") * log(Tmin) + kk(i,"6") * rPower(Tmin,kk(i,"7"));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
logPsat.up(i,j) = kk(i,"1") + kk(i,"2") / (kk(i,"3") + Tmax) + kk(i,"4") * Tmax + kk(i,"5") * log(Tmax) + kk(i,"6") * rPower(Tmax,kk(i,"7"));
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
DH_ig.lo(i,j) = C_ig(i,"1") * (Tmin - T0) + C_ig(i,"2") * (power(Tmin,2) - power(T0,2)) / 2 + C_ig(i,"3") * (power(Tmin,3) - power(T0,3)) / 3 + C_ig(i,"4") * (power(Tmin,4) - power(T0,4)) / 4 + C_ig(i,"5") * (power(Tmin,5) - power(T0,5)) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_ig.up(i,j) = C_ig(i,"1") * (Tmax - T0) + C_ig(i,"2") * (power(Tmax,2) - power(T0,2)) / 2 + C_ig(i,"3") * (power(Tmax,3) - power(T0,3)) / 3 + C_ig(i,"4") * (power(Tmax,4) - power(T0,4)) / 4 + C_ig(i,"5") * (power(Tmax,5) - power(T0,5)) / 5;
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
DH_liq.lo(i,j) = C_liq(i,"1") * (Tmin - Tb(i)) + C_liq(i,"2") * (power(Tmin,2) - power(Tb(i),2)) / 2 + C_liq(i,"3") * (power(Tmin,3) - power(Tb(i),3)) / 3 + C_liq(i,"4") * (power(Tmin,4) - power(Tb(i),4)) / 4 + C_liq(i,"5") * (power(Tmin,5) - power(Tb(i),5)) / 5;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
DH_liq.up(i,j) = C_liq(i,"1") * (Tmax - Tb(i)) + C_liq(i,"2") * (power(Tmax,2) - power(Tb(i),2)) / 2 + C_liq(i,"3") * (power(Tmax,3) - power(Tb(i),3)) / 3 + C_liq(i,"4") * (power(Tmax,4) - power(Tb(i),4)) / 4 + C_liq(i,"5") * (power(Tmax,5) - power(Tb(i),5)) / 5;
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
v_mol.lo(j) = Z.lo(j) * R * Tmin / 950000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol.up(j) = Z.up(j) * R * Tmax / 950000.0;
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
v_mol_i.lo(i,j) = Zvi.lo(i,j) * R * Tmin / 950000.0;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
v_mol_i.up(i,j) = Zvi.up(i,j) * R * Tmax / 950000.0;
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
K_eq.lo(j) = exp(10.387 + 4060.59 / Tmax - 2.89055 * log(Tmax) - 0.01915144 * Tmax + 5.28586e-05 * power(Tmax,2) - 5.32977e-08 * power(Tmax,3));
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
K_eq.up(j) = exp(10.387 + 4060.59 / Tmin - 2.89055 * log(Tmin) - 0.01915144 * Tmin + 5.28586e-05 * power(Tmin,2) - 5.32977e-08 * power(Tmin,3));
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
k_rate.lo(j) = 7418160000000000.0 * exp((-60400.0) / (R * Tmin)) / 60;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_rate.up(j) = 7418160000000000.0 * exp((-60400.0) / (R * Tmax)) / 60;
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
k_A.lo(j) = exp((-1.0707) + 1323.1 / Tmax);
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
k_A.up(j) = exp((-1.0707) + 1323.1 / Tmin);
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
Tcond.up = Tmin + 50;
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
Treb.lo = Tmax - 50;
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
Treb.up = Tmax;
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
V.l("1") = 0.1;
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
Model MESHR_Optimization / psat_def,cubic_eos,v_definition,fugacity_eq,enthalpy_eq,alpha_definition,aii_definition,mixing_rule_b,mixing_rule_a,dadT_ii_eq,dadT_eq,Compute_gamma,K_equation,calc_DH_ig,calc_Hvi,calc_Hv,Zvi_eq,v_eq,calc_HR_pure,calc_DH_liq,calc_Hv_Tbi_P,calc_Hli,calc_Hl,calc_K_eq,calc_k_rate,calc_k_A,calc_Rx_Rate,assign_zero,mol_balance_eq,mol_balance_condenser_eq,mol_balance_reboiler_eq,comp_balance_eq,comp_balance_condenser_eq,comp_balance_reboiler_eq,eq_rel_eq,summation_eq,energy_balance_eq,energy_balance_condenser_eq,energy_balance_reboiler_eq,spec_2_eq,V1_eq,def_D_col,def_Mw_mix,def_Dcol_max,def_Tcond,def_Treb,def_Breb,eq_ColCost,eq_TrayCost,eq_CondCost,eq_RebCost,eq_CAP_cost,eq_OP_cost,def_Profit,obj_def /;
$offListing
Parameter autogenerated_domUsd_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_etAlg_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_etSolve_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_etSolver_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_iterUsd_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_marginals_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_maxInfes_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_meanInfes_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_modelStat_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_nodUsd_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_number_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numDepnd_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numDVar_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numEqu_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numInfes_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numNLIns_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numNLNZ_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numNOpt_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numNZ_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numRedef_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numVar_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_numVarProj_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_objEst_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_objVal_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_procUsed_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_resGen_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_resUsd_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_solveStat_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_sumInfes_mJFz0MaNXRxSNY_gYwDYrrg;
Parameter autogenerated_sysVer_mJFz0MaNXRxSNY_gYwDYrrg;
$onListing
$offDotL
$offUNDF
$offMulti
$onMultiR
$onUNDF
$onDotL
MESHR_Optimization.scaleopt = 1;

solve MESHR_Optimization using NLP MIN obj;

$offListing
autogenerated_domUsd_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.domUsd;
autogenerated_etAlg_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.etAlg;
autogenerated_etSolve_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.etSolve;
autogenerated_etSolver_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.etSolver;
autogenerated_iterUsd_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.iterUsd;
autogenerated_marginals_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.marginals;
autogenerated_maxInfes_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.maxInfes;
autogenerated_meanInfes_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.meanInfes;
autogenerated_modelStat_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.modelStat;
autogenerated_nodUsd_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.nodUsd;
autogenerated_number_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.number;
autogenerated_numDepnd_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numDepnd;
autogenerated_numDVar_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numDVar;
autogenerated_numEqu_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numEqu;
autogenerated_numInfes_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numInfes;
autogenerated_numNLIns_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numNLIns;
autogenerated_numNLNZ_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numNLNZ;
autogenerated_numNOpt_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numNOpt;
autogenerated_numNZ_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numNZ;
autogenerated_numRedef_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numRedef;
autogenerated_numVar_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numVar;
autogenerated_numVarProj_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.numVarProj;
autogenerated_objEst_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.objEst;
autogenerated_objVal_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.objVal;
autogenerated_procUsed_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.procUsed;
autogenerated_resGen_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.resGen;
autogenerated_resUsd_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.resUsd;
autogenerated_solveStat_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.solveStat;
autogenerated_sumInfes_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.sumInfes;
autogenerated_sysVer_mJFz0MaNXRxSNY_gYwDYrrg = MESHR_Optimization.sysVer;
execute_unload 'C:\Users\Lucas\AppData\Local\Temp\tmpv5hrz1c1\_c4d_29V9RquITJ_Fv_xIfA.gdx', autogenerated_domUsd_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_etAlg_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_etSolve_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_etSolver_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_iterUsd_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_marginals_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_maxInfes_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_meanInfes_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_modelStat_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_nodUsd_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_number_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numDepnd_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numDVar_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numEqu_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numInfes_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numNLIns_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numNLNZ_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numNOpt_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numNZ_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numRedef_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numVar_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_numVarProj_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_objEst_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_objVal_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_procUsed_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_resGen_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_resUsd_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_solveStat_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_sumInfes_mJFz0MaNXRxSNY_gYwDYrrg,autogenerated_sysVer_mJFz0MaNXRxSNY_gYwDYrrg;
$onListing
$offDotL
$offUNDF
$offMulti
