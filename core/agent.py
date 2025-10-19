"""
Agent class representing a host that carries and replicates memes.
"""
import numpy as np
import copy
from typing import List, Optional
from core.meme import Meme
import config


class Agent:
    """
    An agent is a host located at (x, y) that maintains a pool of memes
    and performs internal and external replication.
    """
    
    def __init__(self, x: int, y: int, initial_memes: List[Meme]):
        """
        Initialize an agent with a position and initial meme pool.
        
        Args:
            x: X coordinate on grid
            y: Y coordinate on grid
            initial_memes: Initial list of memes (should not exceed POOL_SIZE)
        """
        self.x = x
        self.y = y
        self.meme_pool: List[Meme] = initial_memes[:config.POOL_SIZE]
        assert len(self.meme_pool) > 0, "Agent must have at least one meme"
    
    def get_dominant_meme(self) -> Meme:
        """
        Select the dominant meme from the pool.
        
        If utility selection is enabled: Select meme with HIGHEST combined score S = (α × U) - (β × C)
        Otherwise: Select meme with LOWEST complexity (original behavior)
        
        Returns:
            The dominant meme from the pool
        """
        if config.USE_UTILITY_SELECTION:
            # Select meme with highest combined score
            return max(
                self.meme_pool, 
                key=lambda m: m.combined_score(config.ALPHA, config.BETA)
            )
        else:
            # Original behavior: lowest complexity
            return min(self.meme_pool, key=lambda m: m.complexity)
    
    def internal_rehearsal(self, rng: np.random.Generator):
        """
        Perform internal rehearsal: randomly select a meme and copy it
        with internal mutation rate.
        
        This models memory decay/reinterpretation.
        
        Args:
            rng: Random number generator
        """
        # Select a random meme from pool
        source_meme = rng.choice(self.meme_pool)
        
        # Copy it with internal mutation
        rehearsed_meme = source_meme.copy_with_mutation(
            config.MU_BASE_INTERNAL, rng
        )
        
        # Add to pool (will be cleaned up if needed)
        self._add_to_pool(rehearsed_meme)
    
    def receive_meme(self, source_meme: Meme, rng: np.random.Generator):
        """
        Receive a meme from a neighbor (external transmission).
        The meme is copied with external mutation rate and added to pool.
        
        Args:
            source_meme: The dominant meme from a neighbor
            rng: Random number generator
        """
        # Copy with external mutation (higher error rate)
        invaded_meme = source_meme.copy_with_mutation(
            config.MU_BASE_EXTERNAL, rng
        )
        
        # Add to pool
        self._add_to_pool(invaded_meme)
    
    def _add_to_pool(self, meme: Meme):
        """
        Add a meme to the pool. If pool is full, remove the least fit meme.
        
        If utility selection is enabled: Remove meme with LOWEST combined score S = (α × U) - (β × C)
        Otherwise: Remove meme with HIGHEST complexity (original behavior)
        
        Args:
            meme: Meme to add to pool
        """
        self.meme_pool.append(meme)
        
        # If pool exceeds size limit, remove least fit meme
        if len(self.meme_pool) > config.POOL_SIZE:
            if config.USE_UTILITY_SELECTION:
                # Remove meme with lowest combined score
                min_score_idx = min(
                    range(len(self.meme_pool)),
                    key=lambda i: self.meme_pool[i].combined_score(config.ALPHA, config.BETA)
                )
                self.meme_pool.pop(min_score_idx)
            else:
                # Original behavior: remove highest complexity
                max_complexity_idx = max(
                    range(len(self.meme_pool)),
                    key=lambda i: self.meme_pool[i].complexity
                )
                self.meme_pool.pop(max_complexity_idx)
    
    def age_memes(self):
        """Increment the age of all memes in the pool."""
        for meme in self.meme_pool:
            meme.increment_age()
    
    def get_pool_stats(self) -> dict:
        """
        Get statistics about the current meme pool.
        
        Returns:
            Dictionary with pool statistics
        """
        complexities = [m.complexity for m in self.meme_pool]
        utilities = [m.utility for m in self.meme_pool]
        ages = [m.age for m in self.meme_pool]
        scores = [m.combined_score(config.ALPHA, config.BETA) for m in self.meme_pool]
        
        dominant = self.get_dominant_meme()
        
        return {
            'pool_size': len(self.meme_pool),
            'avg_complexity': np.mean(complexities),
            'min_complexity': np.min(complexities),
            'max_complexity': np.max(complexities),
            'avg_utility': np.mean(utilities),
            'min_utility': np.min(utilities),
            'max_utility': np.max(utilities),
            'avg_score': np.mean(scores),
            'avg_age': np.mean(ages),
            'dominant_complexity': dominant.complexity,
            'dominant_utility': dominant.utility,
            'dominant_score': dominant.combined_score(config.ALPHA, config.BETA),
        }
    
    def copy(self) -> 'Agent':
        """
        Create a deep copy of this agent with copied meme pool.
        This is needed for proper state update in the CA simulation.
        
        Returns:
            A new Agent instance with deep-copied meme pool
        """
        # Deep copy all memes in the pool
        copied_memes = []
        for meme in self.meme_pool:
            # Create new meme with copied pattern and same age
            copied_pattern = meme.pattern.copy()
            copied_meme = Meme(copied_pattern.tolist(), age=meme.age)
            copied_memes.append(copied_meme)
        
        # Create new agent with copied memes
        new_agent = Agent(self.x, self.y, copied_memes)
        return new_agent
    
    def __repr__(self) -> str:
        return f"Agent({self.x}, {self.y}) with {len(self.meme_pool)} memes"

