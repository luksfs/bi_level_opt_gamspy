from itertools import combinations_with_replacement

def generate_scenarios(Nsmax, n_reactive):
    """
    Generate all feasible configurations.

    Parameters
    ----------
    Nsmax : int
        Maximum number of stages.
    n_reactive : int
        Number of reactive trays (1-4).

    Returns
    -------
    list
        List of configuration dictionaries.
    """
    if n_reactive not in [1, 2, 3, 4]:
            raise ValueError("n_reactive must be between 1 and 4.")

    scenarios = []

    for Ns in range(5, Nsmax + 1):
        
        # 1. Because NR1 >= NR2 >= ... >= NR_n, no tray can exceed NR1's maximum.
        # NR1's maximum is (Ns - n_reactive). We just need combinations from this range.
        valid_trays = range(2, Ns - n_reactive + 1)
        
        # 2. combinations_with_replacement yields sorted ascending tuples e.g., (2, 3).
        # We reverse them [::-1] to make them descending e.g., (3, 2) to satisfy NR1 >= NR2.
        reactive_configs = [
            list(combo)[::-1] 
            for combo in combinations_with_replacement(valid_trays, n_reactive)
        ]

        # 3. Use list comprehension/generator expression to build the dicts at C-speed
        scenarios.extend(
            {
                "Ns": Ns,
                "NFE": NFE,
                "NFB": NFB,
                "reactive": r
            }
            for NFE in range(2, Ns)
            for NFB in range(NFE, Ns)
            for r in reactive_configs
        )

    print(f"Generated {len(scenarios):,} configurations.")
    return scenarios