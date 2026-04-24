import numpy as np
import random

SEED = 42
NODES = 50
THRESHOLD = 70.0

def apply_seeds(custom_seed=None):
    """
    Universally anchors deterministic pseudo-random logic blocks mathematically mapping identical arrays securely.
    """
    active_seed = custom_seed if custom_seed is not None else SEED
    np.random.seed(active_seed)
    random.seed(active_seed)
