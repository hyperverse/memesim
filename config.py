"""
Configuration parameters for the meme simulation.
"""

# Grid parameters
GRID_SIZE = 30  # N x N grid
MEME_LENGTH = 16  # L - length of binary pattern

# Agent parameters
POOL_SIZE = 5  # K - maximum number of memes per agent

# Mutation parameters
MU_BASE_INTERNAL = 0.1 # 0.01  # Base internal mutation rate (low for stable memory)
MU_BASE_EXTERNAL = 0.5 # 0.05  # Base external mutation rate (higher for noisy transmission)
COMPLEXITY_SCALE_FACTOR = 0.5 # 0.05  # k - scaling factor for complexity contribution to mutation

# Utility-based selection parameters
USE_UTILITY_SELECTION = True  # Toggle between pure fidelity and utility-based selection
ALPHA = 0.5 #1.0  # Weight for utility in combined score (higher = favor useful patterns)
BETA = 0.5   # Weight for complexity in combined score (higher = favor simple patterns)
# Combined score: S = (α × U) - (β × C)
# Expected behaviors:
#   α > β: Utility-driven, favors complex patterns near utility targets
#   α < β: Fidelity-driven, favors simple patterns with low mutation
#   α = β: Balanced, creates stable diversity around utility patterns

# Visualization parameters
CELL_SIZE = 8  # Size of each pixel in the 4x4 meme bitmap (total: 32x32 per agent)
FPS = 10  # Frames per second for visualization

# Simulation parameters
MAX_GENERATIONS = 1000  # Maximum number of generations to simulate (0 = infinite)

# Utility patterns 
INJECT_UTILITY_PATTERNS = True
UTILITY_PATTERNS = [
    # Utility patterns
    [0, 0, 0, 0,
     1, 1, 1, 1,
     0, 0, 0, 0,
     1, 1, 1, 1],  # Utility pattern 1: Alternating blocks
    [1, 1, 1, 1, 
     1, 1, 1, 1, 
     0, 0, 0, 0, 
     0, 0, 0, 0],  # Utility pattern 2: Half and half
    [0, 1, 0, 1, 
     1, 0, 1, 0, 
     0, 1, 0, 1, 
     1, 0, 1, 0],  # Utility pattern 3: Checkerboard
    [1, 1, 1, 1, 
     1, 0, 0, 1, 
     1, 0, 0, 1, 
     1, 1, 1, 1],  # Utility pattern 4: Square with a hole
    [1, 0, 0, 1, 
     0, 1, 1, 0, 
     0, 1, 1, 0, 
     1, 0, 0, 1]  # Utility pattern 5: Cross
]

