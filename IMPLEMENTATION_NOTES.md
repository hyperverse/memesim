# Implementation Notes

## State Update (Double Buffering)

The simulation implements proper **Cellular Automaton (CA) style simultaneous update** using double buffering to ensure all agents are updated based on the same "old" state of the grid.

### Why Double Buffering?

From MemeSimulation.md:
> "A 'New Grid' is calculated based on the 'Old Grid' to ensure all interactions are simultaneous (a key feature of Cellular Automata)."

Without double buffering, agents that are processed later in a loop would interact with agents that have already been updated in the current generation, breaking the simultaneity requirement of CA.

### Implementation Details

**Location**: `simulation/engine.py` - `_external_dynamics_phase()`

The external dynamics phase now works as follows:

1. **Read Phase**: Get all current agents from the grid (OLD state)
   ```python
   old_agents = self.grid.get_all_agents()
   ```

2. **Copy Phase**: Create deep copies of all agents (NEW state to write to)
   ```python
   new_agents = [agent.copy() for agent in old_agents]
   ```

3. **Update Phase**: Process each NEW agent by reading from OLD neighbors
   ```python
   for new_agent in new_agents:
       old_neighbors = self.grid.get_moore_neighbors(new_agent.x, new_agent.y)
       selected_neighbor = self.rng.choice(old_neighbors)
       neighbor_dominant = selected_neighbor.get_dominant_meme()
       new_agent.receive_meme(neighbor_dominant, self.rng)
   ```

4. **Write Phase**: Replace entire grid with updated agents simultaneously
   ```python
   self.grid.set_all_agents(new_agents)
   ```

### Supporting Methods

**`Agent.copy()` in `core/agent.py`**:
- Creates a deep copy of an agent with its entire meme pool
- Ensures memes are also copied (not just referenced)
- Preserves agent position and meme ages

**`Grid.set_all_agents()` in `core/grid.py`**:
- Replaces all agents in the grid at once
- Takes a flat list in row-major order
- Reshapes back into the 2D grid structure

### Benefits

1. ✅ **Correctness**: All agents interact with the same generation state
2. ✅ **CA Compliance**: Follows standard cellular automaton update rules
3. ✅ **Reproducibility**: Given same seed, results are deterministic
4. ✅ **Clarity**: Explicit separation of read and write phases

### Performance Note

The double buffering adds some memory overhead (copying all agents), but this is acceptable for:
- Typical grid sizes (30×30 to 100×100)
- The guarantee of correctness
- Clearer simulation semantics

For very large grids, this could be optimized by only copying meme pools rather than entire agents.

