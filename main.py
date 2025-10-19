"""
Main entry point for the meme simulation.
"""
import numpy as np
import logging
import sys

import config
from utils.logging_config import setup_logging
from core.grid import Grid
from simulation.engine import SimulationEngine
from visualization.renderer import Renderer


def main():
    """Run the meme simulation."""
    # Setup logging (use "DEBUG" for detailed per-agent logs)
    log_level = "INFO"  # Change to "DEBUG" for detailed logging
    log_file = setup_logging(log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("MEME SIMULATION - Starting")
    logger.info("=" * 60)
    logger.info(f"Grid Size: {config.GRID_SIZE}x{config.GRID_SIZE}")
    logger.info(f"Meme Length: {config.MEME_LENGTH}")
    logger.info(f"Pool Size: {config.POOL_SIZE}")
    logger.info(f"Internal Mutation Rate: {config.MU_BASE_INTERNAL}")
    logger.info(f"External Mutation Rate: {config.MU_BASE_EXTERNAL}")
    logger.info(f"Entropy Scale Factor: {config.ENTROPY_SCALE_FACTOR}")
    
    # Initialize random number generator with fixed seed for reproducibility
    # Remove seed parameter for random behavior each run
    rng = np.random.default_rng(seed=42)
    
    # Create the grid
    logger.info("Initializing grid with white noise memes...")
    grid = Grid(config.GRID_SIZE, rng)
    
    # Optional: Inject seed patterns
    if config.USE_SEED_PATTERNS:
        logger.info(f"Injecting {len(config.SEED_PATTERNS)} seed patterns...")
        grid.inject_seed_patterns(config.SEED_PATTERNS)
    
    # Create simulation engine
    engine = SimulationEngine(grid, rng)
    
    # Create renderer
    logger.info("Initializing visualization...")
    renderer = Renderer(grid)
    
    # Initial statistics
    initial_stats = grid.get_grid_stats()
    logger.info(f"Initial Stats: {initial_stats}")
    
    # Main simulation loop
    logger.info("=" * 60)
    logger.info("Starting main simulation loop")
    logger.info("Controls: SPACE = pause/resume, ESC = quit")
    logger.info("=" * 60)
    
    try:
        while renderer.is_running():
            # Handle events
            if not renderer.handle_events():
                break
            
            # Render current state
            renderer.render(engine.get_generation())
            
            # Step simulation if not paused
            if not renderer.is_paused():
                engine.step()
                
                # Check if we've reached max generations
                if config.MAX_GENERATIONS > 0 and engine.get_generation() >= config.MAX_GENERATIONS:
                    logger.info(f"Reached maximum generations ({config.MAX_GENERATIONS})")
                    break
    
    except KeyboardInterrupt:
        logger.info("Simulation interrupted by user")
    
    finally:
        # Final statistics
        final_stats = grid.get_grid_stats()
        logger.info("=" * 60)
        logger.info("SIMULATION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Final Generation: {engine.get_generation()}")
        logger.info(f"Final Stats: {final_stats}")
        logger.info(f"Log saved to: {log_file}")
        
        # Clean up
        renderer.quit()


if __name__ == "__main__":
    main()
