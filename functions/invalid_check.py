def check_bounds(y):
    # 1. Unpack FIRST so Ns is defined
    Ns, NFE, NFB, *NR = y

    # 2. Robust boundary check: True if outside [2, Ns-1]
    out_of_bounds = lambda x: x < 2 or x >= Ns-1

    # 3. Check for NR1 < NR2 < NR3 < NR4
    ordering_invalid = any(
        NR[i] >= NR[i + 1]
        for i in range(len(NR) - 1)
    )

    # 4. Consolidate all invalid triggers
    invalid = (
        out_of_bounds(NFE)
        or out_of_bounds(NFB)
        or any(out_of_bounds(r) for r in NR)
        or NFB < NFE
        or ordering_invalid
    )
    
    return invalid