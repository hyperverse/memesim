# Persisting patterns without a handed-in goal

Reading of memesim and counterflow, September 2026. Saved from the Pattern
Persistence canvas. It describes the fidelity rule, before the recall exchange.
The running rule is [NOTES.md](NOTES.md). The 1000-generation recall run is
[recall-exchange-run.md](recall-exchange-run.md).

At the time of this reading, utility selection and pattern injection were both
off, so the live run was the pure-fidelity regime.

- **H = 0.** The only stable attractors of that regime.
- **Count, not shape.** What Shannon entropy sees.
- **k-WTA.** What stopped collapse in counterflow.
- **Mismatch.** What made storage faithful.

## Why memesim drains to all zeros or all ones

Each agent holds a pool of length-16 bit strings. Every generation it rehearses
a random string with bit-flip noise, forgets the highest-complexity string if
the pool is full, and broadcasts the lowest-complexity string. A random neighbor
is copied the same way, with more noise. Complexity is normalized Shannon
entropy of the bit counts, and the flip rate rises with that number.

Nothing in that loop depends on which bits are set, only on how many. The
pattern does not change the agent, the neighbor, or the next input. The only
quantity under selection is copying fidelity, and the mutation rule makes
fidelity best exactly when the string is constant. All zeros and all ones are
the two strings with entropy zero, so they are the global optimum of the rule
that was written down. The spec's hope that the population would settle on a
balance of complexity and simplicity has no second force to balance against.

**Entropy does not see structure.** Binary Shannon entropy is a function of the
fraction of ones. The checkerboard and a shuffled string with eight ones have
the same score. The design note treats `01010101` as low entropy; under the
formula in `meme.py` it is maximum entropy. Selection cannot prefer a pattern
for its arrangement.

| Pressure | What it rewards | Where the population goes |
|---|---|---|
| Pure fidelity (the config at the time of this reading) | Lowest entropy, easiest copy | All zeros or all ones |
| Utility patterns (the fix) | Hamming closeness to five drawings in `config.py` | Those drawings, or the nearest of them |
| Counterflow dictionary | Explain the incoming vector, with competition for units | A sparse code of the input statistics |
| Mismatch-gated item memory (specified, not run) | Keep a specific vector when recall fails | Distinct recurring patterns, forgotten by disuse |

## Utility patterns are a goal pasted on

`UTILITY_PATTERNS` scores a meme by one minus its Hamming distance to the
nearest hand-drawn bitmap. Dominance and forgetting then maximize
`S = αU − βC`. That stops the collapse, because a second score now pulls away
from the constant strings. The pull is toward the bitmaps in the file. The meme
still does nothing; the author declared five pictures useful. With the weights
in config the tradeoff is also lopsided: complexity is entropy divided by
`log2(16)`, so it lives in 0 to 0.25, while utility lives in 0 to 1. Equal α
and β do not balance the two.

## What counterflow already settled

Counterflow was built as the follow-up: store structure from an input stream
with no loss, no label, and no target pattern. Two streams share the synapses.
The forward stream encodes the input into a sparse code. The backward stream
regenerates the input. The learning signal is the local mismatch. On
TinyStories-8M layer activations the tied rule stores the layer; plain Hebb on
the same net does not.

| Finding | Evidence | Consequence for a meme grid |
|---|---|---|
| Competition prevents collapse | k-WTA: no dead units, features stay distinct, including the plain-Hebb control | A fixed pool that keeps several winners can hold more than one pattern. The two-stream rule is not what creates diversity. |
| Mismatch creates fidelity | `hebb_only` FVU about 8; tied rule with settling about 0.30 to 0.38 | Copying a neighbor is not storage. Storage is keeping the pattern that accounts for what arrived. |
| Tied weights store, they do not predict | Layer l to l+1: tied FVU 0.54 to 0.71; separate pipes 0.20 to 0.28 | Reconstructing the heard pattern can share one representation. Mapping "what I sent" to "what came back" needs two. |
| A dictionary averages; an item memory keeps a pattern | Hopfield retrieval 0.93 from a 0.45 cue; no dictionary net retrieved the item | Persisting a particular meme wants a slot written when novelty is high, strengthened when the same thing returns. |

## Where input and output can sit

Memesim, under the fidelity rule, has neither. Agents emit a dominant string and
ingest a noisy copy, but emission is chosen by entropy and ingestion does not
check whether the copy matches anything. Counterflow only stores when there is
a stream to be faithful to. The design choice is what that stream is.

**Whole simulation.** One memory, one external tape or world rule as input,
reconstruction as the output. Patterns persist because they compress the world.
Agent-to-agent copying is optional. It answers storage cleanly and leaves
cultural transmission behind. Without an external stream, reconstructing the
grid only memorizes a state the fidelity rule is already erasing.

**Agent to agent.** Each exchange is the stream. The heard neighbor string is
the input. The agent's reply from its pool is the output. Same space in and
out: one slot both matches and regenerates, which is the tied case that worked.
If the stored fact is the pair "I sent this, they answered that", the two sides
differ and the pipes should be separate, which is what the counterflow
layer-to-layer experiment required.

The smallest loop that can keep a non-trivial pattern: hear a neighbor, pick
the pool slot closest to what was heard, and take the Hamming distance as the
mismatch. A small mismatch strengthens that slot. A large mismatch writes the
heard string into the weakest slot. Broadcast the reconstruction. Entropy-biased
bit flips can remain as noise. They should not also be the selection rule.

## Dawkins

The goal of a meme, in Dawkins, is defined. A meme is a replicator. It persists
by being copied more than its rivals. Usefulness to the host is one way that
can happen, and it is not the definition. Genes have the same criterion. What a gene also has is a phenotype:
an effect that changes its own copying rate. Memesim modeled only copying
fidelity, so the winners are the strings the noise damages least. Utility
patterns invent a phenotype by fiat. A mismatch against the neighbor's stream
is a phenotype the system can compute: the pattern that, when replayed, accounts
for what arrives next. That is predictive coding more than the selfish gene, and
it does not require a drawing in the config.
