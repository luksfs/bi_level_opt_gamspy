from itertools import product
import numpy as np


def calculate_centroid(variable_ranges):
    """
    Calculate the centroid of a discrete feasible hyperspace.

    variable_ranges:
        Dictionary where each value is either:
        - a tuple (min, max)
        - a function that receives the already selected variables
          and returns (min, max)
    """

    points = [{}]

    for variable, range_definition in variable_ranges.items():

        new_points = []

        for point in points:

            # Fixed range
            if isinstance(range_definition, tuple):
                minimum, maximum = range_definition

            # Dependent range
            else:
                minimum, maximum = range_definition(point)

            for value in range(minimum, maximum + 1):
                new_point = point.copy()
                new_point[variable] = value
                new_points.append(new_point)

        points = new_points

    # Convert to array
    variables = list(variable_ranges.keys())

    X = np.array([
        [point[var] for var in variables]
        for point in points
    ])

    centroid = X.mean(axis=0)

    return dict(zip(variables, centroid)), points

variable_ranges = {

    "Ns": (5, 22),

    'NFE': (2,20),

    'NFB': (2,20),

    "R1": (2, 20),

    "R2": lambda x: (x["R1"] + 1, 20),

    "R3": lambda x: (x["R2"] + 1, 20),
 
    "R4": lambda x: (x["R3"] + 1, 20),
}

centroid, feasible_points = calculate_centroid(variable_ranges)

print(centroid)