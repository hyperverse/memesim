"""
Simulation engine coordinating the two-tiered evolution process.
"""
import numpy as np
import logging
from core.grid import Grid
import config


logger = logging.getLogger(__name__)


class SimulationEngine:
    """
    Coordinates the simulation cycle:
    1. Internal dynamics (rehearsal, pool update, dominance election)
    2. External dynamics (neighbor selection, mirroring, invasion)
    3. State update
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
        Execute one generation of the simulation.
        Implements the complete cycle from the specification.
        """
        logger.debug(f"=== Generation {self.generation} ===")
        
        # Phase 1: Internal Dynamics
        self._internal_dynamics_phase()
        
        # Phase 2: External Dynamics
        self._external_dynamics_phase()
        
        # Increment generation counter
        self.generation += 1
        
        # Log generation statistics
        stats = self.grid.get_grid_stats()
        
        if config.USE_UTILITY_SELECTION:
            logger.info(
                f"Gen {self.generation}: "
                f"avg_C={stats['avg_dominant_complexity']:.4f}, "
                f"avg_U={stats['avg_dominant_utility']:.4f}, "
                f"avg_S={stats['avg_dominant_score']:.4f}, "
                f"diversity={stats['pattern_diversity']:.3f}, "
                f"unique={stats['unique_patterns']}"
            )
        else:
            logger.info(
                f"Gen {self.generation}: "
                f"avg_C={stats['avg_dominant_complexity']:.4f}, "
                f"min_C={stats['min_dominant_complexity']:.4f}, "
                f"max_C={stats['max_dominant_complexity']:.4f}, "
                f"unique_patterns={stats['unique_patterns']}, "
                f"total_patterns={stats['total_patterns']}"
            )
    
    def _internal_dynamics_phase(self):
        """
        Phase 1: Internal Dynamics
        
        Each agent:
        1.1 Self-Rehearsal: Copy a random meme with internal mutation
        1.2 Pool Update: Remove highest complexity if pool exceeds size
        1.3 Dominance Election: Select lowest complexity meme as dominant
        """
        logger.debug("Phase 1: Internal Dynamics")
        
        all_agents = self.grid.get_all_agents()
        
        for agent in all_agents:
            # 1.1 & 1.2: Internal rehearsal (includes pool management)
            agent.internal_rehearsal(self.rng)
            
            # Age all memes
            agent.age_memes()
            
            # 1.3: Dominance election (happens automatically when needed)
            dominant = agent.get_dominant_meme()
            
            if logger.isEnabledFor(logging.DEBUG):
                pool_stats = agent.get_pool_stats()
                if config.USE_UTILITY_SELECTION:
                    logger.debug(
                        f"Agent({agent.x},{agent.y}): "
                        f"dom_C={pool_stats['dominant_complexity']:.4f}, "
                        f"dom_U={pool_stats['dominant_utility']:.4f}, "
                        f"dom_S={pool_stats['dominant_score']:.4f}, "
                        f"pool_avg_U={pool_stats['avg_utility']:.4f}"
                    )
                else:
                    logger.debug(
                        f"Agent({agent.x},{agent.y}): "
                        f"dominant_C={pool_stats['dominant_complexity']:.4f}, "
                        f"pool_avg_C={pool_stats['avg_complexity']:.4f}, "
                        f"pool_size={pool_stats['pool_size']}"
                    )
    
    def _external_dynamics_phase(self):
        """
        Phase 2: External Dynamics
        
        Each agent:
        2.1 Target Selection: Select a random neighbor
        2.2 Mirroring & Error: Copy neighbor's dominant with external mutation
        2.3 External Invasion: Add to pool (remove highest H if full)
        
        IMPORTANT: This implements proper CA-style simultaneous update using
        double buffering. All agents read from the OLD grid state and write
        to NEW agent copies, then the grid is updated all at once.
        """
        logger.debug("Phase 2: External Dynamics")
        
        # Get current grid state (these are the agents we READ from)
        old_agents = self.grid.get_all_agents()
        
        # Create copies of all agents (these are the agents we WRITE to)
        new_agents = [agent.copy() for agent in old_agents]
        
        # Build a mapping from (x, y) to new agent for easy lookup
        new_agent_map = {(agent.x, agent.y): agent for agent in new_agents}
        
        # Process each agent using OLD grid for reading neighbors
        for new_agent in new_agents:
            # 2.1: Select random neighbor from OLD grid state
            old_neighbors = self.grid.get_moore_neighbors(new_agent.x, new_agent.y)
            selected_neighbor = self.rng.choice(old_neighbors)
            
            # 2.2 & 2.3: Copy dominant meme from OLD neighbor to NEW agent
            neighbor_dominant = selected_neighbor.get_dominant_meme()
            new_agent.receive_meme(neighbor_dominant, self.rng)
            
            if logger.isEnabledFor(logging.DEBUG):
                if config.USE_UTILITY_SELECTION:
                    logger.debug(
                        f"Agent({new_agent.x},{new_agent.y}) <- "
                        f"Agent({selected_neighbor.x},{selected_neighbor.y}): "
                        f"copied meme C={neighbor_dominant.complexity:.4f}, "
                        f"U={neighbor_dominant.utility:.4f}"
                    )
                else:
                    logger.debug(
                        f"Agent({new_agent.x},{new_agent.y}) <- "
                        f"Agent({selected_neighbor.x},{selected_neighbor.y}): "
                        f"copied meme with C={neighbor_dominant.complexity:.4f}"
                    )
        
        # State Update: Replace all agents in grid simultaneously
        self.grid.set_all_agents(new_agents)
    
    def get_generation(self) -> int:
        """Get the current generation number."""
        return self.generation

