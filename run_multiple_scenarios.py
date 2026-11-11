import pandas as pd
import numpy as np
import pickle
from gamspy_model.meshr_class import ReactiveDistillationModel  #

# 1. Load the sorted data and grab the top 10 rows
df = pd.read_csv('result/exhaustive_combined_sorted.csv', sep=';')
top_10_df = df.head(10)

# 2. Convert the dataframe rows into your scenarios list
scenarios = []
for index, row in top_10_df.iterrows():
    # Collect all valid reactive trays from NR1, NR2, NR3, NR4
    reactive_trays = []
    for col in ['NR1', 'NR2', 'NR3', 'NR4']:
        if col in row and pd.notna(row[col]) and row[col] > 0:
            reactive_trays.append(int(row[col]))
    
    # Build the dictionary for this scenario
    config = {
        "Ns": int(row['Ns']),
        "NFE": int(row['NFE']),
        "NFB": int(row['NFB']),
        "reactive": reactive_trays
    }
    scenarios.append(config)

# 3. Initialize your model
meshr = ReactiveDistillationModel(max_stages=22)
all_scenarios_data = []

# 4. Loop through the generated scenarios and solve
for config in scenarios:
    print(f"\nRunning Scenario: {config}")
    
    # Update the parameters 
    meshr.update_config(
        Ns=config["Ns"],
        NFE=config["NFE"],
        NFB=config["NFB"],
        reactive_trays=config["reactive"]
    )
    
    # Solve 
    result = meshr.solve(solver="BARON", dataframe=True, export=True)
    print(f"Result: {result['Status']} | Profit: {result['Profit']}")

    # --- EXTRACT ALL VARIABLES ---
    Ns = config["Ns"]
    L = meshr.L.records.level[0:Ns].values * meshr.F_factor
    V = meshr.V.records.level[0:Ns].values * meshr.F_factor
    x = meshr.x.records.level.values.reshape(4,22)[:,0:Ns]
    y = meshr.y.records.level.values.reshape(4,22)[:,0:Ns]
    T = meshr.T.records.level.values[0:Ns]
    Qr = meshr.Qr.records.level.values * meshr.FH_factor
    Qc = meshr.Qc.records.level.values * meshr.FH_factor
    FE = meshr.FE.records.level.values * meshr.F_factor
    FB = meshr.FB.records.value.values * meshr.F_factor
    Dcol = meshr.Dcol.records.level.values
    Breb = meshr.Breb.records.level.values * meshr.F_factor
    D = meshr.D.records.level.values * meshr.F_factor
    X_IB = (FB*0.3 - (Breb*x[2, Ns-1] + D*x[2, 0])) / (FB*.3)
    Tcond = meshr.Tcond.records.level.values
    Treb = meshr.Treb.records.level.values
    
    ColCost = meshr.v_ColCost.records.level.values / 3
    TrayCost = meshr.v_TrayCost.records.level.values / 3
    CondCost = meshr.v_CondCost.records.level.values / 3
    RebCost = meshr.v_RebCost.records.level.values / 3
    n_rx = np.sum(meshr.is_reactive.records.value.values)
    cat_cost = 7.7 * n_rx * meshr.m_cat / 3
    cap_cost = meshr.CAP_cost.records.level.values / 3

    c_steam = 4.54e-9
    steam_cost = c_steam * Qr * 8150 * 60
    cooling_cost = 0.378e-9 * Qc * 8150 * 60
    raw_products = FE * meshr.CostEth.toValue()* 8150 * 60 + FB * meshr.CostBut.toValue()* 8150 * 60
    op_cost = meshr.OP_cost.records.level.values
    revenue = Breb * meshr.CostETBE.toValue()* 8150 * 60

    # --- BUNDLE AND APPEND DATA ---
    scenario_dict = {
        "config": config,
        "solver_status": result['Status'],
        "profit": result['Profit'],
        "metrics": {
            "Qr": Qr, "Qc": Qc, "FE": FE, "FB": FB, "Dcol": Dcol, 
            "Breb": Breb, "D": D, "X_IB": X_IB, "Tcond": Tcond, 
            "Treb": Treb, "ColCost": ColCost, "TrayCost": TrayCost, 
            "CondCost": CondCost, "RebCost": RebCost, "n_rx": n_rx, 
            "cat_cost": cat_cost, "cap_cost": cap_cost, 
            "steam_cost": steam_cost, "cooling_cost": cooling_cost, 
            "raw_products": raw_products, "op_cost": op_cost, "revenue": revenue
        },
        "profiles": {
            "L": L, "V": V, "x": x, "y": y, "T": T
        }
    }
    
    all_scenarios_data.append(scenario_dict)

# 5. Save all detailed scenario results 
with open("result/top_10_meshr_results.pkl", "wb") as f:
    pickle.dump(all_scenarios_data, f)
print("\nAll top 10 scenarios processed and saved to top_10_meshr_results.pkl!")