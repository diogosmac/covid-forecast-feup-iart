import numpy as np

vehicles = 3
steps = 10

# - creates an array of subarrays
# - each subarray corresponds to one of the vehicles
# - each element of a subarray contains the ride that it is
#   processing at that step
on_mission = np.zeros(shape=(vehicles, steps), dtype=np.uint8)

print(on_mission)
