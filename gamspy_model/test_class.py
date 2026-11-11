# testing the class
from meshr_class import ReactiveDistillationModel
import numpy as np
import pickle
# from meshr_class_without_cat_res import ReactiveDistillationModel

# 1. Initialize the class (Builds the 22-stage matrix once)
meshr = ReactiveDistillationModel(max_stages=22)

# 2. Define the different column configurations you want to test
scenarios = [
    # {"Ns": 7, "NFE": 4, "NFB": 4, "reactive": [4]},            # 1 reactive tray, taller column
    # {"Ns": 8, "NFE": 4, "NFB": 5, "reactive": [3, 5]},          # 2 reactive trays, even taller
    # {"Ns": 9, "NFE": 5, "NFB": 6, "reactive": [3, 5, 6]},      # 3 reactive trays
    {"Ns": 9, "NFE": 4, "NFB": 6, "reactive": [2, 4, 5, 6]},      # 4 reactive trays


]
# [10, 5, 7, 3, 5, 6, 7]
# [10, 5, 7, 3, 5, 6, 7]
# Ns  = 10
# NFE = 5
# NFB = 7
# NR1 = 3
# NR2 = 5
# NR3 = 7

all_scenarios_data = []

# 3. Loop through and solve them instantly!
for config in scenarios:
    # This updates the parameters in milliseconds
    meshr.update_config(
        Ns=config["Ns"],
        NFE=config["NFE"],
        NFB=config["NFB"],
        reactive_trays=config["reactive"]
    )
    
    # Solve and print results
    result = meshr.solve(solver="BARON",dataframe=True,export=True)
    print(f"Result: {result['Status']} | Profit: {result['Profit']}")
    # result = meshr.solve(solver="BARON")
    # print(f"Result: {result['Status']} | Profit: {result['Profit']}")

    Ns = config["Ns"]
    L = meshr.L.records.level[0:Ns].values*meshr.F_factor
    V = meshr.V.records.level[0:Ns].values*meshr.F_factor
    x = meshr.x.records.level.values.reshape(4,22)[:,0:Ns]
    y = meshr.y.records.level.values.reshape(4,22)[:,0:Ns]
    T = meshr.T.records.level.values[0:Ns]
    Qr = meshr.Qr.records.level.values*meshr.FH_factor
    Qc = meshr.Qc.records.level.values*meshr.FH_factor
    # zB = np.array([0.7, 0, 0.3, 0])
    # zE = np.array([0, 1, 0, 0])
    FE = meshr.FE.records.level.values*meshr.F_factor
    FB = meshr.FB.records.value.values*meshr.F_factor
    Dcol = meshr.Dcol.records.level.values
    Breb = meshr.Breb.records.level.values*meshr.F_factor
    D = meshr.D.records.level.values*meshr.F_factor
    X_IB = ( FB*0.3 - (Breb*x[2, Ns-1] + D*x[2, 0]) )/(FB*.3)
    Tcond = meshr.Tcond.records.level.values
    Treb = meshr.Treb.records.level.values
    # Annualized Cap cost
    ColCost = meshr.v_ColCost.records.level.values/3
    TrayCost = meshr.v_TrayCost.records.level.values/3
    CondCost = meshr.v_CondCost.records.level.values/3
    RebCost = meshr.v_RebCost.records.level.values/3
    n_rx = np.sum(meshr.is_reactive.records.value.values)
    cat_cost = 7.7 * n_rx * meshr.m_cat/3
    cap_cost = meshr.CAP_cost.records.level.values/3

    # operational cost
    c_steam = 4.54e-9
    steam_cost = c_steam * Qr * 8150 * 60
    cooling_cost = 0.378e-9 * Qc * 8150 * 60
    raw_products = FE * meshr.CostEth.toValue() + FB * meshr.CostBut.toValue()
    op_cost = meshr.OP_cost.records.level.values/3

    revenue = Breb * meshr.CostETBE.toValue()

    scenario_dict = {
        "config": config,
        "solver_status": result['Status'],
        "profit": result['Profit'],
        # Store single-value metrics (Scalars)
        "metrics": {
            "Qr": Qr, "Qc": Qc, "FE": FE, "FB": FB, "Dcol": Dcol, 
            "Breb": Breb, "D": D, "X_IB": X_IB, "Tcond": Tcond, 
            "Treb": Treb, "ColCost": ColCost, "TrayCost": TrayCost, 
            "CondCost": CondCost, "RebCost": RebCost, "n_rx": n_rx, 
            "cat_cost": cat_cost, "cap_cost": cap_cost, 
            "steam_cost": steam_cost, "cooling_cost": cooling_cost, 
            "raw_products": raw_products, "op_cost": op_cost, "revenue": revenue
        },
        # Store profiles/matrices across the stages (Arrays)
        "profiles": {
            "L": L, "V": V, "x": x, "y": y, "T": T
        }
    }
    
    # Add this scenario's data to our master list
    all_scenarios_data.append(scenario_dict)

# Save to file
with open("meshr_results.pkl", "wb") as f:
    pickle.dump(all_scenarios_data, f)
    





