"""this scripts analyze the simulations result and rank them by score."""

import fnmatch
import os

results = []

# Extract all the scores and associated parameters
for rootPath, dirNames, fileNames in os.walk('.'):  # TODO: get this as input
    for fileName in fnmatch.filter(fileNames, '*.txt'):
        with open(fileName) as f:
            values = f.readline().split()
            score = float(values[0])
            parameters = {
                'KP': values[1],
                'KI': values[2],
                'KD': values[3]
            }
            results.append((score, parameters))

# order results by score
ranked_results = sorted(results, key=lambda x: (-x[0], x[1]))

# print scores
for result in ranked_results:
    print(result)
