# Agent-to-agent exchange

The running simulation stores patterns by recall between neighbors. A second
exchange is described here and is not implemented. A later version can put the
choice of exchange, and the rest of communication and selection, under genes
that differ between agents and mutate over time.

The 1000-generation run is [recall-exchange-run.md](recall-exchange-run.md).
The earlier fidelity reading is [pattern-persistence.md](pattern-persistence.md).

## Variant 1 — recall what was heard

Implemented in `Agent.hear` and `SimulationEngine`.

Each generation, every agent hears one random Moore neighbor. The heard string
is that neighbor's current broadcast with a flat per-bit flip
(`HEARING_FLIP_RATE`). The flip rate does not depend on entropy. All agents
read the previous generation and update together.

The agent compares the heard string with each slot by Hamming distance.

- If the closest slot is at or below `MISMATCH_THRESHOLD`, that slot's strength
  increases by one. Its bits stay as they are. Ties at the same distance go to
  the stronger slot.
- If every slot is farther than the threshold, the heard string is copied, bit
  for bit, onto the weakest slot, and that slot's strength is reset to
  `INITIAL_STRENGTH`.

The agent then broadcasts the slot this hearing selected: the strengthened one,
or the slot just written. The cell drawn on the grid is that broadcast.

Closeness only chooses the branch. A close hearing does not move a stored
string toward what was heard. What persists is the particular string that was
written, including the flips it carried at that moment. Later hearings inside
the threshold vote for that copy and do not correct it.

Entropy and the utility patterns do not choose a slot and do not choose what is
sent. The earlier fidelity and utility code is still in the tree and is not on
this path.

## Variant 2 — pair what was sent with what came back

Not implemented.

The stored fact is a pair: the pattern this agent broadcast, and the pattern
that came back from the neighbor afterward. The two sides are different
strings, so they need separate representations. One slot cannot both be the
key and the content. The counterflow layer-to-layer runs are the reason: tied
weights store a pattern that is reconstructed as itself, and they fail when the
return stream is a different vector.

A pair is kept when the same sending is followed by the same reply often enough
to fall inside a match. A sending followed by something unfamiliar is written
as a new pair. A string that leaves the neighbor answering something
unrecognizable stays a poor match and is not consolidated.

## Later: genes for communication and selection

Not implemented.

The whole communication and selection can be carried by each agent as a small
set of genes, rather than as one setting for the grid. Agents can then differ.
One agent can recall what it hears. Another can store the pairing of what it
sent with what came back. The genes also hold the rest of the exchange: which
neighbor is heard, the mismatch threshold, the hearing noise, how strength
changes, which slot is broadcast, and how large the pool is.

Those genes mutate over time, so the rule on an agent can change during a run.
This note does not decide whether genes also spread from agent to agent, or
only change on the agent that carries them. Memes remain the patterns in the
pool. Genes, when added, are the control of how an agent hears, stores, and
sends.
