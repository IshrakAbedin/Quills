import random
from typing import List

def nonRepeatingRandomInRange(populationRange : int, count : int) -> List[int]:
    return random.sample(range(populationRange), count)

