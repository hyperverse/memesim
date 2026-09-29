"""
Simulation engine for the recall exchange between neighboring agents.
"""
import numpy as np
import logging
from core.grid import Grid
import config


logger = logging.getLogger(__name__)


class SimulationEngine:
    """
    Coordinates one exchange per generation.

    Every agent hears one neighbor's broadcast, strengthens a close slot or
    writes the heard string onto the weakest slot, and broadcasts that slot.
    Reads come from the previous generation and writes land together.
    """
    
    def __init__(self, grid: Grid, rng: np.random.Generator):
        """
        Initialize the simulation engine.
        
        Args:
            grid: The grid of agents
            rng: Random number generator
        """
        self.grid = grid
        self.rng = rng
        self.generation = 0
    
    def step(self):
        """
        Execute one generation: each agent hears one neighbor and updates its pool.
        """
        logger.debug(f"=== Generation {self.generation} ===")
        
        n_strengthen, n_write = self._recall_exchange()
        self.generation += 1
        
        stats = self.grid.get_grid_stats()
        strengths = [
            agent.get_dominant_meme().strength
            for agent in self.grid.get_all_agents()
        ]
        logger.info(
            f"Gen {self.generation}: "
            f"strengthen={n_strengthen}, write={n_write}, "
            f"unique={stats['unique_patterns']}, "
            f"mean_broadcast_strength={float(np.mean(strengths)):.2f}"
        )
    
    def _recall_exchange(self) -> tuple[int, int]:
        """
        Hear one neighbor's previous broadcast and answer from the pool.
        
        All agents read the previous generation and write their new pools
        together.
        """
        new_agents = [agent.copy() for agent in self.grid.get_all_agents()]
        n_strengthen = 0
        n_write = 0
        
        for new_agent in new_agents:
            neighbors = self.grid.get_moore_neighbors(new_agent.x, new_agent.y)
            neighbor = self.rng.choice(neighbors)
            heard = neighbor.get_dominant_meme().pattern.copy()
            flips = self.rng.random(len(heard)) < config.HEARING_FLIP_RATE
            heard[flips] = 1 - heard[flips]
            
            outcome = new_agent.hear(heard)
            if outcome == "strengthen":
                n_strengthen += 1
            else:
                n_write += 1
            
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    f"Agent({new_agent.x},{new_agent.y}) <- "
                    f"Agent({neighbor.x},{neighbor.y}): {outcome}"
                )
        
        self.grid.set_all_agents(new_agents)
        return n_strengthen, n_write
    
    def get_generation(self) -> int:
        """Get the current generation number."""
        return self.generation

