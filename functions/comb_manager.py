import itertools

class CombinationManager:
    def __init__(self):
        # We store history as a SET of TUPLES from the start.
        self.history_set = set()

    def generate_new_batch(self, input_list):
        # 1. Define ranges
        expanded_ranges = [[x - 1, x, x + 1] for x in input_list]
        
        new_items = []

        # 2. Iterate
        # 'combo' is a tuple (immutable)
        for combo in itertools.product(*expanded_ranges):
            
            # Check against the persistent history
            if combo in self.history_set:
                continue

            # 3. Add to output AND history
            # We add to history now so it's blocked for future runs immediately
            self.history_set.add(combo)
            
            # We convert to list for the output (if you prefer lists)
            new_items.append(list(combo))

        return new_items
