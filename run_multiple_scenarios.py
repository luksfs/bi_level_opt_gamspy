import pandas as pd
import numpy as np
import pickle
from gamspy_model.meshr_class import ReactiveDistillationModel


def to_scalar(val):
    """Safely converts GAMSPy parameters, 1-element arrays, or series to standard Python float."""
    if hasattr(val, "toValue"):
        return float(val.toValue())
    if isinstance(val, (np.ndarray, pd.Series)):
        return float(val.item()) if val.size == 1 else float(val.flat[0])
    return float(val)


def to_numpy(val):
    """Forces an array-like object to a pure, standard float64 NumPy ndarray."""
    return np.asarray(val, dtype=np.float64).copy()


# 1. Load the sorted data and grab the top 10 rows
df = pd.read_csv('result/exhaustive_combined_sorted.csv', sep=';')
top_10_df = df.head(10)

# 2. Convert the dataframe rows into your scenarios list
scenarios = []
for index, row in top_10_df.iterrows():
    reactive_trays = []
    for col in ['NR1', 'NR2', 'NR3', 'NR4']:
        if col in row and pd.notna(row[col]) and row[col] > 0:
            reactive_trays.append(int(row[col]))
    
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

# Pre-extract model constants as pure Python floats so arithmetic doesn't create GAMSPy objects
F_factor = to_scalar(meshr.F_factor)
FH_factor = to_scalar(meshr.FH_factor)
m_cat = to_scalar(meshr.m_cat)
cost_eth = to_scalar(meshr.CostEth)
cost_but = to_scalar(meshr.CostBut)
cost_etbe = to_scalar(meshr.CostETBE)

# 4. Loop through the generated scenarios and solve
for config in scenarios:
    print(f"\nRunning Scenario: {config}")
    
    meshr.update_config(
        Ns=config["Ns"],
        NFE=config["NFE"],
        NFB=config["NFB"],
        reactive_trays=config["reactive"]
    )
    
    # Solve 
    result = meshr.solve(solver="BARON", dataframe=True, export=True)
    print(f"Result: {result['Status']} | Profit: {result['Profit']}")

    # --- EXTRACT ALL VARIABLES AS PURE NUMPY ARRAYS & PYTHON FLOATS ---
    Ns = config["Ns"]
    
    # Profiles (1D and 2D pure numpy arrays)
    L = to_numpy(meshr.L.records.level[0:Ns].values) * F_factor
    V = to_numpy(meshr.V.records.level[0:Ns].values) * F_factor
    x = to_numpy(meshr.x.records.level.values).reshape(4, 22)[:, 0:Ns].copy()
    y = to_numpy(meshr.y.records.level.values).reshape(4, 22)[:, 0:Ns].copy()
    T = to_numpy(meshr.T.records.level.values[0:Ns])

    # Activity
    gamma = to_numpy(meshr.gamma_nrtl.records.level.values).reshape(4, 22)[:, 0:Ns].copy()
    
    # Scalar Metrics (Pure Python floats)
    Qr = to_scalar(meshr.Qr.records.level.values) * FH_factor
    Qc = to_scalar(meshr.Qc.records.level.values) * FH_factor
    FE = to_scalar(meshr.FE.records.level.values) * F_factor
    FB = to_scalar(meshr.FB.records.value.values) * F_factor
    Dcol = to_scalar(meshr.Dcol.records.level.values)
    Breb = to_scalar(meshr.Breb.records.level.values) * F_factor
    D = to_scalar(meshr.D.records.level.values) * F_factor
    
    X_IB = float((FB * 0.3 - (Breb * x[2, Ns-1] + D * x[2, 0])) / (FB * 0.3))
    Tcond = to_scalar(meshr.Tcond.records.level.values)
    Treb = to_scalar(meshr.Treb.records.level.values)
    
    ColCost = to_scalar(meshr.v_ColCost.records.level.values) / 3.0
    TrayCost = to_scalar(meshr.v_TrayCost.records.level.values) / 3.0
    CondCost = to_scalar(meshr.v_CondCost.records.level.values) / 3.0
    RebCost = to_scalar(meshr.v_RebCost.records.level.values) / 3.0
    n_rx = float(np.sum(to_numpy(meshr.is_reactive.records.value.values)))
    cat_cost = 7.7 * n_rx * m_cat / 3.0
    cap_cost = to_scalar(meshr.CAP_cost.records.level.values) / 3.0

    c_steam = 4.54e-9
    steam_cost = c_steam * Qr * 8150 * 60
    cooling_cost = 0.378e-9 * Qc * 8150 * 60
    raw_products = FE * cost_eth * 8150 * 60 + FB * cost_but * 8150 * 60
    op_cost = to_scalar(meshr.OP_cost.records.level.values)
    revenue = Breb * cost_etbe * 8150 * 60

    # --- BUNDLE AND APPEND DATA ---
    scenario_dict = {
        "config": config,
        "solver_status": str(result['Status']),  # Cast away GAMSPy ModelStatus/SolveStatus enum
        "profit": to_scalar(result['Profit']),
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
            "L": L, "V": V, "x": x, "y": y, "T": T, "gamma": gamma
        }
    }
    
    all_scenarios_data.append(scenario_dict)

# 5. Save all detailed scenario results 
with open("result/top_10_meshr_results.pkl", "wb") as f:
    pickle.dump(all_scenarios_data, f)
print("\nAll top 10 scenarios processed and saved to top_10_meshr_results.pkl!")