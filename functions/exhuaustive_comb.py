from itertools import combinations

def generate_scenarios_optimized(Nsmax, n_reactive):
    """
    Generate all feasible configurations.

    Parameters
    ----------
    Nsmax : int
        Maximum number of stages.
    n_reactive : int
        Number of reactive trays (1-5).

    Returns
    -------
    list
        List of configuration dictionaries.
    """
    # Updated to allow up to 5 reactive trays
    if n_reactive not in [1, 2, 3, 4, 5]:
        raise ValueError("n_reactive must be between 1 and 5.")

    scenarios = []

    for Ns in range(5, Nsmax + 1):
        
        # 1. Trays available: 2 up to Ns-2 (excluding Ns-1)
        valid_trays = range(2, Ns - 1)
        
        # 2. combinations() automatically yields strictly ascending, unique tuples.
        # This perfectly satisfies NR1 < NR2 < NR3 < NR4 < NR5 < Ns-1.
        # We pre-convert the tuples to lists here to save time in the inner loop.
        reactive_configs = [list(c) for c in combinations(valid_trays, n_reactive)]

        # 3. Use generator expression to build the dicts at C-speed
        # NFE and NFB max out at Ns-2 because range is exclusive of Ns-1
        scenarios.extend(
            {
                "Ns": Ns,
                "NFE": NFE,
                "NFB": NFB,
                "reactive": r
            }
            for NFE in range(2, Ns - 1)
            for NFB in range(NFE, Ns - 1)
            for r in reactive_configs
        )

    print(f"Generated {len(scenarios):,} configurations.")
    return scenarios