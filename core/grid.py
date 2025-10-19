"""
Grid class managing the spatial 2D environment for the simulation.
"""
import numpy as np
from typing import List, Tuple
from core.agent import Agent
from core.meme import Meme
import config


class Grid:
    """
    A 2D grid of agents with toroidal boundary conditions.
    Supports Moore neighborhood (8 neighbors including diagonals).
    """
    
    def __init__(self, size: int, rng: np.random.Generator):
        """
        Initialize a grid of agents with random memes.
        
        Args:
            size: Grid dimension (size x size)
            rng: Random number generator
        """
        self.size = size
        self.rng = rng
        self.agents = np.empty((size, size), dtype=object)
        
        # Initialize all agents with random memes
        for x in range(size):
            for y in range(size):
                initial_memes = [
                    Meme.random(rng) for _ in range(config.POOL_SIZE)
                ]
                self.agents[x, y] = Agent(x, y, initial_memes)
    
    def inject_patterns(self, patterns: List[List[int]]):
        """
        Inject specific seed patterns into random locations on the grid.
        
        Args:
            patterns: List of binary patterns to inject
        """
        for pattern in patterns:
            # Choose random location
            x = self.rng.integers(0, self.size)
            y = self.rng.integers(0, self.size)
            
            # Create seed meme and add to agent's pool
            seed_meme = Meme(pattern)
            agent = self.agents[x, y]
            agent._add_to_pool(seed_meme)
    
    def get_moore_neighbors(self, x: int, y: int) -> List[Agent]:
        """
        Get the 8 Moore neighbors of an agent (including diagonals).
        Uses toroidal boundary conditions (wrap-around).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of 8 neighboring agents
        """
        neighbors = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip self
                
                # Toroidal wrap-around
                nx = (x + dx) % self.size
                ny = (y + dy) % self.size
                
                neighbors.append(self.agents[nx, ny])
        
        return neighbors
    
    def get_agent(self, x: int, y: int) -> Agent:
        """
        Get the agent at position (x, y).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Agent at that position
        """
        return self.agents[x, y]
    
    def get_all_agents(self) -> List[Agent]:
        """
        Get a flat list of all agents in the grid.
        
        Returns:
            List of all agents
        """
        return self.agents.flatten().tolist()
    
    def set_all_agents(self, agents: List[Agent]):
        """
        Update the grid with a new list of agents.
        Agents must be in row-major order matching the grid dimensions.
        
        Args:
            agents: List of agents (length must equal size * size)
        """
        assert len(agents) == self.size * self.size, \
            f"Agent list must contain {self.size * self.size} agents"
        
        # Reshape flat list back into 2D grid
        idx = 0
        for x in range(self.size):
            for y in range(self.size):
                self.agents[x, y] = agents[idx]
                idx += 1
    
    def get_grid_stats(self) -> dict:
        """
        Calculate statistics across all agents in the grid.
        
        Returns:
            Dictionary with grid-wide statistics
        """
        all_agents = self.get_all_agents()
        
        # Collect dominant meme metrics
        dominant_complexities = []
        dominant_utilities = []
        dominant_scores = []
        
        for agent in all_agents:
            dominant = agent.get_dominant_meme()
            dominant_complexities.append(dominant.complexity)
            dominant_utilities.append(dominant.utility)
            dominant_scores.append(dominant.combined_score(
                config.ALPHA if hasattr(config, 'ALPHA') else 1.0,
                config.BETA if hasattr(config, 'BETA') else 0.5
            ))
        
        # Collect all pool metrics
        all_complexities = []
        all_utilities = []
        
        for agent in all_agents:
            for meme in agent.meme_pool:
                all_complexities.append(meme.complexity)
                all_utilities.append(meme.utility)
        
        # Collect unique patterns (as tuples for hashing)
        unique_patterns = set()
        for agent in all_agents:
            for meme in agent.meme_pool:
                unique_patterns.add(tuple(meme.pattern))
        
        return {
            # Dominant meme statistics
            'avg_dominant_complexity': np.mean(dominant_complexities),
            'std_dominant_complexity': np.std(dominant_complexities),
            'min_dominant_complexity': np.min(dominant_complexities),
            'max_dominant_complexity': np.max(dominant_complexities),
            'avg_dominant_utility': np.mean(dominant_utilities),
            'std_dominant_utility': np.std(dominant_utilities),
            'min_dominant_utility': np.min(dominant_utilities),
            'max_dominant_utility': np.max(dominant_utilities),
            'avg_dominant_score': np.mean(dominant_scores),
            
            # Pool-wide statistics
            'avg_pool_complexity': np.mean(all_complexities),
            'avg_pool_utility': np.mean(all_utilities),
            
            # Diversity metrics
            'unique_patterns': len(unique_patterns),
            'total_patterns': len(all_complexities),
            'pattern_diversity': len(unique_patterns) / len(all_complexities) if all_complexities else 0,
        }

