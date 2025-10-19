"""
Meme class representing a replicable pattern with Shannon entropy calculation.
"""
import numpy as np
from typing import List
import config


class Meme:
    """
    A meme is a binary pattern that can be copied with potential mutations.
    Its Shannon entropy determines its copying fidelity.
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
    
    @property
    def entropy(self) -> float:
        """
        Calculate Shannon entropy H of the binary pattern.
        
        H = -(p_0 * log2(p_0) + p_1 * log2(p_1))
        where p_0 = N_0/L and p_1 = N_1/L
        
        Returns:
            Shannon entropy (0 to 1, where 1 is maximum entropy)
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
        Create a copy of this meme with mutations based on its entropy.
        
        The effective mutation rate is:
        mu_eff = mu_base + k * H(source)
        
        Args:
            mu_base: Base mutation rate (mu_int or mu_ext)
            rng: Random number generator
            
        Returns:
            A new Meme instance (potentially mutated copy)
        """
        # Calculate effective mutation rate based on entropy
        mu_eff = mu_base + config.ENTROPY_SCALE_FACTOR * self.entropy
        
        # Copy pattern and apply mutations
        new_pattern = self.pattern.copy()
        
        # Each bit has mu_eff probability of flipping
        mutation_mask = rng.random(len(new_pattern)) < mu_eff
        new_pattern[mutation_mask] = 1 - new_pattern[mutation_mask]
        
        return Meme(new_pattern.tolist(), age=0)
    
    def increment_age(self):
        """Increment the age of this meme."""
        self.age += 1
    
    def __repr__(self) -> str:
        pattern_str = ''.join(str(bit) for bit in self.pattern)
        return f"Meme(pattern={pattern_str}, H={self.entropy:.3f}, age={self.age})"
    
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

