"""
Meme class representing a replicable pattern with Shannon entropy calculation.
"""
import numpy as np
from typing import List
import config


class Meme:
    """
    A meme is a binary pattern that can be copied with potential mutations.
    Its Shannon entropy / complexity determines its copying fidelity.
    """
    
    def __init__(self, pattern: List[int], age: int = 0):
        """
        Initialize a meme with a binary pattern.
        
        Args:
            pattern: List of 0s and 1s of length config.MEME_LENGTH
            age: The age of this meme (generations since creation)
        """
        assert len(pattern) == config.MEME_LENGTH, f"Pattern must be length {config.MEME_LENGTH}"
        assert all(bit in [0, 1] for bit in pattern), "Pattern must contain only 0s and 1s"
        
        self.pattern = np.array(pattern, dtype=np.int8)
        self.age = age
        self._entropy = None  # Cached entropy value
        self._complexity = None  # Cached complexity value
        self._utility = None  # Cached utility value
    
    @property
    def complexity(self) -> float:
        """
        Calculate the complexity of the binary pattern.
        """
        # Maximum entropy for a binary pattern
        entrop_max = np.log2(len(self.pattern))

        return self.entropy / entrop_max
    
    def hamming_distance(self, other_meme: 'Meme') -> float:
        """
        Calculate normalized Hamming distance to another meme.
        
        Args:
            other_meme: The meme to compare against
            
        Returns:
            Normalized Hamming distance in [0, 1] where 0 = identical, 1 = completely different
        """
        # Count differing bits
        diff_bits = np.sum(self.pattern != other_meme.pattern)
        # Normalize by pattern length
        return diff_bits / len(self.pattern)
    
    @property
    def utility(self) -> float:
        """
        Calculate the utility of the binary pattern based on proximity to utility patterns.
        
        Utility is defined as inverse Hamming distance to the nearest utility pattern:
        U = 1 - min_hamming_distance
        
        Returns:
            Utility value in [0, 1] where 1 = perfect match to a utility pattern
        """
        if self._utility is not None:
            return self._utility
        
        # If no utility patterns defined, return 0
        if not hasattr(config, 'UTILITY_PATTERNS') or not config.UTILITY_PATTERNS:
            self._utility = 0.0
            return self._utility
        
        # Calculate minimum Hamming distance to all utility patterns
        min_distance = float('inf')
        for utility_pattern in config.UTILITY_PATTERNS:
            utility_meme = Meme(utility_pattern)
            distance = self.hamming_distance(utility_meme)
            min_distance = min(min_distance, distance)
        
        # Convert distance to utility (inverse)
        self._utility = 1.0 - min_distance
        return self._utility
    
    @property
    def entropy(self) -> float:
        """
        Calculate Shannon entropy H of the binary pattern.
        
        H = -(p_0 * log2(p_0) + p_1 * log2(p_1))
        where p_0 = N_0/L and p_1 = N_1/L
        
        Returns:
            Shannon entropy (0 to H_max, where H_max is maximum entropy)
        """
        if self._entropy is not None:
            return self._entropy
        
        # Count zeros and ones
        n_ones = np.sum(self.pattern)
        n_zeros = len(self.pattern) - n_ones
        
        # Calculate probabilities
        p_0 = n_zeros / len(self.pattern)
        p_1 = n_ones / len(self.pattern)
        
        # Calculate entropy (handle log(0) case)
        entropy = 0.0
        if p_0 > 0:
            entropy -= p_0 * np.log2(p_0)
        if p_1 > 0:
            entropy -= p_1 * np.log2(p_1)
        
        self._entropy = entropy
        return self._entropy
    
    def copy_with_mutation(self, mu_base: float, rng: np.random.Generator) -> 'Meme':
        """
        Create a copy of this meme with mutations based on its complexity.
        
        The effective mutation rate is:
        mu_eff = mu_base + k * complexity(source)
        
        Args:
            mu_base: Base mutation rate (mu_int or mu_ext)
            rng: Random number generator
            
        Returns:
            A new Meme instance (potentially mutated copy)
        """
        # Calculate effective mutation rate based on complexity
        mu_eff = mu_base + config.COMPLEXITY_SCALE_FACTOR * self.complexity
        
        # Copy pattern and apply mutations
        new_pattern = self.pattern.copy()
        
        # Each bit has mu_eff probability of flipping
        mutation_mask = rng.random(len(new_pattern)) < mu_eff
        new_pattern[mutation_mask] = 1 - new_pattern[mutation_mask]
        
        return Meme(new_pattern.tolist(), age=0)
    
    def increment_age(self):
        """Increment the age of this meme."""
        self.age += 1
    
    def combined_score(self, alpha: float, beta: float) -> float:
        """
        Calculate the combined fitness score balancing utility and complexity.
        
        S = (α × U) - (β × C)
        
        Args:
            alpha: Weight for utility (higher = favor useful patterns)
            beta: Weight for complexity (higher = favor simple patterns)
            
        Returns:
            Combined score (higher is better)
        """
        return (alpha * self.utility) - (beta * self.complexity)
    
    def __repr__(self) -> str:
        pattern_str = ''.join(str(bit) for bit in self.pattern)
        return f"Meme(pattern={pattern_str}, C={self.complexity:.3f}, U={self.utility:.3f}, age={self.age})"
    
    @staticmethod
    def random(rng: np.random.Generator) -> 'Meme':
        """
        Create a random meme with white noise pattern.
        
        Args:
            rng: Random number generator
            
        Returns:
            A new Meme with random binary pattern
        """
        pattern = rng.integers(0, 2, size=config.MEME_LENGTH).tolist()
        return Meme(pattern)

