"""
Configuration parameters for the meme simulation.
"""

# Grid parameters
GRID_SIZE = 30  # N x N grid
MEME_LENGTH = 16  # L - length of binary pattern

# Agent parameters
POOL_SIZE = 5  # K - maximum number of memes per agent

# Mutation parameters
MU_BASE_INTERNAL = 0.9 # 0.01  # Base internal mutation rate (low for stable memory)
MU_BASE_EXTERNAL = 0.9 # 0.05  # Base external mutation rate (higher for noisy transmission)
ENTROPY_SCALE_FACTOR = 0.05  # k - scaling factor for entropy contribution to mutation

# Visualization parameters
CELL_SIZE = 8  # Size of each pixel in the 4x4 meme bitmap (total: 32x32 per agent)
FPS = 10  # Frames per second for visualization

# Simulation parameters
MAX_GENERATIONS = 1000  # Maximum number of generations to simulate (0 = infinite)

# Seed patterns (optional initialization)
# Set to True to inject seed patterns into the grid
USE_SEED_PATTERNS = True
SEED_PATTERNS = [
    # Simple low-entropy patterns
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],  # Alternating blocks
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Half and half
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # Checkerboard
]

