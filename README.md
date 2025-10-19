# The Meme Simulation

Simulating a combination of evolutionary theory, information theory, and cellular automata.

Implemented with Cursor / Claude 4.5 Sonnet.

## Tooling

* Language: Python
* Virtual environment: uv
  * Adding packages: `uv add <package>`
  * Update .venv: `uv sync`

See @MemeSimulation.md for a description of the project.

## Running the Simulation

```bash
uv run main.py
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
- `COMPLEXITY_SCALE_FACTOR`: Complexity contribution to mutation (default: 0.1)
- `FPS`: Frames per second (default: 10)
- `USE_SEED_PATTERNS`: Enable/disable seed pattern injection (default: True)

### Logging

The simulation generates detailed logs in the `logs/` directory:
- **INFO level**: Per-generation metrics (average complexity, pattern diversity, etc.)
- **DEBUG level**: Per-agent details (position, pool state, dominant meme)

Change the log level in `main.py` by setting `log_level = "DEBUG"` for detailed logging.

## Project Structure

```
memesim/
├── core/
│   ├── meme.py       # Meme class with Shannon Entropy and complexity
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

