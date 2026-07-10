# testing the class
# from meshr_class import ReactiveDistillationModel
from gamspy_model.meshr_class import ReactiveDistillationModel

# 1. Initialize the class (Builds the 22-stage matrix once)
meshr = ReactiveDistillationModel(max_stages=22)

# 2. Define the different column configurations you want to test
scenarios = [
    {"Ns": 10, "NFE": 5, "NFB": 7, "reactive": [3, 5, 7]},      # 3 reactive trays
    # {"Ns": 12, "NFE": 6, "NFB": 8, "reactive": [4]},            # 1 reactive tray, taller column
    # {"Ns": 15, "NFE": 7, "NFB": 9, "reactive": [4, 5, 6, 7]}    # 4 reactive trays, even taller
]
# Ns  = 10
# NFE = 5
# NFB = 7
# NR1 = 3
# NR2 = 5
# NR3 = 7

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
    result = meshr.solve(solver="BARON",export=False)
    print(f"Result: {result['Status']} | Profit: {result['Profit']}")
    # result = meshr.solve(solver="BARON")
    # print(f"Result: {result['Status']} | Profit: {result['Profit']}")