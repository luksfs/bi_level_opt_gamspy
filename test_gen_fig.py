import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. LOAD PICKLE & UNWRAP GAMSPY ARRAYS
# ---------------------------------------------------------
with open("result/top_10_meshr_results.pkl", "rb") as f:
    data = pickle.load(f)

def to_scalar(val):
    """Safely convert 1-element GAMSPy/NumPy arrays to float."""
    if isinstance(val, (np.ndarray, list, pd.Series)):
        return float(np.squeeze(val))
    return float(val)

def format_rx_zone(rx):
    """Format reactive tray list/array as 'start-end' stage range."""
    if isinstance(rx, (list, tuple, np.ndarray)):
        idx = [i + 1 for i, v in enumerate(rx) if v > 0.5] if set(np.unique(rx)).issubset({0, 1}) else list(rx)
        return f"{min(idx)}-{max(idx)}" if len(idx) > 0 else "None"
    return str(rx)

rows = []
for rank, scen in enumerate(data, start=1):
    cfg = scen["config"]
    m = scen["metrics"]
    
    col_tray = to_scalar(m["ColCost"]) + to_scalar(m["TrayCost"])
    hex_cost = to_scalar(m["CondCost"]) + to_scalar(m["RebCost"])
    cat_cost = to_scalar(m["cat_cost"])
    util_cost = to_scalar(m["steam_cost"]) + to_scalar(m["cooling_cost"])
    react_cost = to_scalar(m["raw_products"])
    rev_prod = to_scalar(m["revenue"])
    
    tac_calc = col_tray + hex_cost + cat_cost + util_cost + react_cost
    nac_calc = tac_calc - rev_prod
    nac_solver = to_scalar(scen["profit"])
    
    rows.append({
        "Rank": rank,
        "Ns": int(to_scalar(cfg["Ns"])),
        "NFE": int(to_scalar(cfg["NFE"])),
        "NFB": int(to_scalar(cfg["NFB"])),
        "n_rx": int(to_scalar(m["n_rx"])),
        "Rx_Zone": format_rx_zone(cfg["reactive"]),
        "Dcol_m": to_scalar(m["Dcol"]),
        "X_IB_pct": to_scalar(m["X_IB"]) * 100.0,
        "Qr_kW": to_scalar(m["Qr"]) / 60000.0,  # if J/min -> kW
        "Qc_kW": to_scalar(m["Qc"]) / 60000.0,
        "Col_Tray": col_tray,
        "Heat_Exch": hex_cost,
        "Catalyst": cat_cost,
        "Utilities": util_cost,
        "Reactants": react_cost,
        "Revenue": rev_prod,
        "TAC": tac_calc,
        "NAC_calc": nac_calc,
        "NAC_solver": nac_solver,
        "Diff_check": nac_calc - nac_solver
    })

df = pd.DataFrame(rows).sort_values("NAC_solver").reset_index(drop=True)
df["Rank"] = np.arange(1, len(df) + 1)

print("=== NAC RECONCILIATION CHECK (NAC_calc vs. result['Profit']) ===")
print(df[["Rank", "NAC_solver", "NAC_calc", "Diff_check"]].to_string(index=False))

# Use NAC_calc (or NAC_solver if identical) as the baseline
base = df.iloc[0]
nac_base = abs(base["NAC_calc"])

# ---------------------------------------------------------
# 2. COMPUTE WEIGHTED DELTAS (% OF BASE NAC) & SELF-RELATIVE (%)
# ---------------------------------------------------------
cost_cols = ["Col_Tray", "Heat_Exch", "Catalyst", "Utilities", "Reactants"]
for col in cost_cols:
    df[f"dw_{col}"] = (df[col] - base[col]) / nac_base * 100.0
    df[f"dself_{col}"] = (df[col] - base[col]) / base[col] * 100.0

# Revenue sign reversed: lost revenue (< base) is a positive NAC penalty (> 0)
df["dw_Revenue"] = (base["Revenue"] - df["Revenue"]) / nac_base * 100.0
df["dself_Revenue"] = (df["Revenue"] - base["Revenue"]) / base["Revenue"] * 100.0
df["dNAC_pct"] = (df["NAC_calc"] - base["NAC_calc"]) / nac_base * 100.0

# ---------------------------------------------------------
# 3. EXPORT COMPARISON TABLES (CSV & LATEX)
# ---------------------------------------------------------
df.to_csv("result/top_10_comparison_full.csv", index=False)

table_cols = [
    "Rank", "Ns", "NFE", "NFB", "n_rx", "Dcol_m", "X_IB_pct",
    "Col_Tray", "Heat_Exch", "Catalyst", "Utilities", "Reactants", "Revenue",
    "NAC_calc", "dNAC_pct"
]
with open("result/top_10_comparison_table.tex", "w") as f:
    f.write(df[table_cols].to_latex(index=False, float_format="%.2f"))

# ---------------------------------------------------------
# 4. GENERATE 3-PANEL PUBLICATION FIGURE
# ---------------------------------------------------------
plt.rcParams.update({"font.size": 10, "axes.labelsize": 11, "axes.titlesize": 11})
fig = plt.figure(figsize=(14, 8), constrained_layout=True)
gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 3.2], height_ratios=[1.4, 1.0])

ax_base = fig.add_subplot(gs[:, 0])   # Panel A: Rank 1 Baseline Waterfall
ax_delta = fig.add_subplot(gs[0, 1])  # Panel B: NAC-Weighted Diverging Deltas
ax_self = fig.add_subplot(gs[1, 1], sharex=ax_delta)  # Panel C: Self-Relative Sizing

colors = {
    "Col_Tray": "#1b4965",   # Dark Navy (CAPEX)
    "Heat_Exch": "#62b6cb",  # Teal Blue (CAPEX)
    "Catalyst": "#d95f02",   # Rust Orange (OPEX - Reactive)
    "Utilities": "#e7298a",  # Magenta/Red (OPEX - Thermal)
    "Reactants": "#e6ab02",  # Amber Gold (OPEX - Feed)
    "Revenue": "#2b9348"     # Green (Product Revenue)
}
labels_map = {
    "Col_Tray": "Column + Trays",
    "Heat_Exch": "Condenser + Reboiler",
    "Catalyst": "Catalyst",
    "Utilities": "Steam + Cooling Water",
    "Reactants": "Reactants (Eth + But)",
    "Revenue": "Product Revenue (ETBE)"
}

# --- Panel A: Rank 1 Baseline (TAC vs. Revenue -> NAC) ---
bottom_tac = 0.0
for col in cost_cols:
    val = base[col] / 1e3  # in k$/yr
    ax_base.bar("TAC\n(Expenses)", val, bottom=bottom_tac, color=colors[col], width=0.55)
    bottom_tac += val

rev_k = base["Revenue"] / 1e3
nac_k = base["NAC_calc"] / 1e3
ax_base.bar("Product\nRevenue", rev_k, color=colors["Revenue"], width=0.55)
ax_base.bar("Net Annual\nCost (NAC)", nac_k, color="#333333", width=0.55)
ax_base.set_ylabel("Annualized Value ($k/yr)")
ax_base.set_title("A. Rank 1 Baseline Breakdown")
ax_base.grid(axis="y", linestyle="--", alpha=0.4)

# --- Panel B: Diverging NAC-Weighted Deltas (Ranks 2-10) ---
ranks_2_10 = df.iloc[1:]
x_pos = np.arange(len(ranks_2_10))
pos_bottom = np.zeros(len(ranks_2_10))
neg_bottom = np.zeros(len(ranks_2_10))

for col in cost_cols + ["Revenue"]:
    vals = ranks_2_10[f"dw_{col}"].values
    pos_vals = np.maximum(vals, 0)
    neg_vals = np.minimum(vals, 0)
    
    ax_delta.bar(x_pos, pos_vals, bottom=pos_bottom, color=colors[col],
                 label=labels_map[col], width=0.55, edgecolor="white", linewidth=0.5)
    ax_delta.bar(x_pos, neg_vals, bottom=neg_bottom, color=colors[col],
                 width=0.55, edgecolor="white", linewidth=0.5)
    pos_bottom += pos_vals
    neg_bottom += neg_vals

ax_delta.plot(x_pos, ranks_2_10["dNAC_pct"], "ko-", linewidth=1.8, markersize=6, label="Net $\\Delta$NAC (%)")
ax_delta.axhline(0, color="black", linewidth=1)
ax_delta.set_ylabel("Contribution to $\\Delta$NAC (% of $\\mathrm{NAC}_{\\mathrm{base}}$)")
ax_delta.set_title("B. Component Cost Penalties (+) and Savings (-) Relative to Rank 1")
ax_delta.legend(ncol=4, loc="upper left", frameon=True, fontsize=9)
ax_delta.grid(axis="y", linestyle="--", alpha=0.4)

# --- Panel C: Self-Relative Sizing Change (%) + Discrete Geometry Labels ---
width = 0.25
for idx, col in enumerate(["Col_Tray", "Heat_Exch", "Catalyst"]):
    ax_self.bar(x_pos + (idx - 1) * width, ranks_2_10[f"dself_{col}"],
                width=width, color=colors[col], label=labels_map[col])

ax_self.axhline(0, color="black", linewidth=1)
ax_self.set_ylabel("Self-Relative Sizing $\\delta C_i$ (%)")
ax_self.set_title("C. Unit-Level Capital & Catalyst Sizing Shifts vs. Rank 1")
ax_self.grid(axis="y", linestyle="--", alpha=0.4)

x_labels = [
    f"Rank {int(r.Rank)}\nNs={int(r.Ns)}, Nr={int(r.n_rx)}\nNFE={int(r.NFE)}, NFB={int(r.NFB)}"
    for _, r in ranks_2_10.iterrows()
]
ax_self.set_xticks(x_pos)
ax_self.set_xticklabels(x_labels, fontsize=9)

plt.savefig("result/top_10_nac_breakdown.pdf", dpi=300)
plt.savefig("result/top_10_nac_breakdown.png", dpi=300)
print("Saved plots and tables to result/ directory.")