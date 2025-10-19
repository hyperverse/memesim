# The Meme Simulation

* Language: Python
* Virtual environment: uv
  * Adding packages: `uv add <package>`
  * Update .venv: `uv sync`

See @MemeSimulation.md for a description of the project.

## Running the Simulation

```bash
python main.py
```

### Controls
- **SPACE**: Pause/Resume the simulation
- **ESC**: Quit the simulation

### Configuration

Edit `config.py` to adjust simulation parameters:
- `GRID_SIZE`: Size of the grid (default: 50×50)
- `MEME_LENGTH`: Length of binary patterns (default: 16)
- `POOL_SIZE`: Maximum memes per agent (default: 5)
- `MU_BASE_INTERNAL`: Internal mutation rate (default: 0.01)
- `MU_BASE_EXTERNAL`: External mutation rate (default: 0.05)
- `ENTROPY_SCALE_FACTOR`: Entropy contribution to mutation (default: 0.1)
- `FPS`: Frames per second (default: 10)
- `USE_SEED_PATTERNS`: Enable/disable seed pattern injection (default: True)

### Logging

The simulation generates detailed logs in the `logs/` directory:
- **INFO level**: Per-generation metrics (average entropy, pattern diversity, etc.)
- **DEBUG level**: Per-agent details (position, pool state, dominant meme)

Change the log level in `main.py` by setting `log_level = "DEBUG"` for detailed logging.

## Project Structure

```
memesim/
├── core/
│   ├── meme.py       # Meme class with Shannon entropy
│   ├── agent.py      # Agent class with meme pool
│   └── grid.py       # Spatial grid with Moore neighborhood
├── simulation/
│   └── engine.py     # Two-tiered evolution cycle
├── visualization/
│   └── renderer.py   # Pygame-based visualization
├── utils/
│   └── logging_config.py  # Logging setup
├── config.py         # Simulation parameters
└── main.py           # Entry point
```

