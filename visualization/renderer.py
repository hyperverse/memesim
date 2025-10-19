"""
Pygame-based renderer for visualizing the meme simulation.
"""
import pygame
import numpy as np
from core.grid import Grid
import config
import logging


logger = logging.getLogger(__name__)


class Renderer:
    """
    Renders the simulation grid using Pygame.
    Each agent is displayed as a 4x4 bitmap of its dominant meme.
    """
    
    def __init__(self, grid: Grid):
        """
        Initialize the Pygame renderer.
        
        Args:
            grid: The simulation grid to render
        """
        self.grid = grid
        
        # Calculate window size
        # Each agent is rendered as a 4x4 grid, each pixel is CELL_SIZE
        self.agent_display_size = 4 * config.CELL_SIZE
        self.window_size = self.agent_display_size * grid.size
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Meme Simulation")
        
        # Colors
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_GRAY = (128, 128, 128)
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        
        # State
        self.paused = False
        self.running = True
        
        logger.info(f"Renderer initialized: {self.window_size}x{self.window_size} pixels")
    
    def render(self, generation: int):
        """
        Render the current state of the grid.
        
        Args:
            generation: Current generation number
        """
        self.screen.fill(self.COLOR_GRAY)
        
        # Render each agent
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                agent = self.grid.get_agent(x, y)
                self._render_agent(agent, x, y)
        
        # Update display
        pygame.display.flip()
        
        # Control FPS
        self.clock.tick(config.FPS)
    
    def _render_agent(self, agent, grid_x: int, grid_y: int):
        """
        Render a single agent as a 4x4 bitmap of its dominant meme.
        
        Args:
            agent: The agent to render
            grid_x: Agent's x position on grid
            grid_y: Agent's y position on grid
        """
        dominant_meme = agent.get_dominant_meme()
        pattern = dominant_meme.pattern
        
        # Convert 16-length pattern to 4x4 grid
        pattern_2d = pattern.reshape(4, 4)
        
        # Calculate screen position
        screen_x = grid_x * self.agent_display_size
        screen_y = grid_y * self.agent_display_size
        
        # Draw each pixel of the 4x4 meme pattern
        for py in range(4):
            for px in range(4):
                color = self.COLOR_WHITE if pattern_2d[py, px] == 1 else self.COLOR_BLACK
                
                pixel_rect = pygame.Rect(
                    screen_x + px * config.CELL_SIZE,
                    screen_y + py * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE
                )
                pygame.draw.rect(self.screen, color, pixel_rect)
    
    def handle_events(self) -> bool:
        """
        Handle Pygame events.
        
        Returns:
            True if simulation should continue, False if it should quit
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return False
                
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    status = "PAUSED" if self.paused else "RESUMED"
                    logger.info(f"Simulation {status}")
        
        return True
    
    def is_paused(self) -> bool:
        """Check if the simulation is paused."""
        return self.paused
    
    def is_running(self) -> bool:
        """Check if the simulation is still running."""
        return self.running
    
    def quit(self):
        """Clean up and quit Pygame."""
        pygame.quit()
        logger.info("Renderer closed")

