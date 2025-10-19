# Meme Simulation

In this project we draw inspiration from **Richard Dawkins' "The Selfish Gene"** and applying the concept of the **meme** to a computational model.

Goal is to simulate the phenomenological aspects of meme evolution in Python, focusing on the mirroring aspect and pattern-based memes, we use an

**Spatial Agent-Based Model (S-ABM)**

We simulate in a **2D grid** where agents (hosts) and their memes (patterns) only interact with neighbors.
This is a spatial simulation, very similar to a **Cellular Automaton (CA)**, but with complex, evolving 'states' (the memes).

## Defining the Meme as a Pattern

In this simulation, a meme is a **pattern of data** that can be copied and potentially altered.

## Shannon Entropy as a Measure of "Selfish" Replication

We use the **Shannon Entropy ($H$)** to modulate the copying fidelity and define the meme's "selfishness" as its inherent **informational complexity or pattern variability**.

The function to calculate the binary Shannon Entropy for the meme pattern (a fixed-length array of 0/1):

The entropy for a sequence of length $L$ with $N_0$ zeros and $N_1$ ones is:
$$H = - (p_0 \log_2 p_0 + p_1 \log_2 p_1)$$
where $p_0 = N_0/L$ and $p_1 = N_1/L$.

### 1\. The Meme's Pattern and Entropy

The Shannon Entropy of a binary pattern (a sequence of 0s and 1s) is maximized when the sequence is completely random (i.e., when $P(0) \approx 0.5$ and $P(1) \approx 0.5$). 
It is minimized (close to zero) when the sequence is highly predictable or uniform (e.g., `'11111111'` or `'01010101'`).

  * **High Entropy Meme:** Has a complex, variable, and information-rich pattern (close to random).
  * **Low Entropy Meme:** Has a simple, uniform, or highly redundant pattern.

### 2\. Modulating the Mirroring (Mutation Rate)

The *meme itself* determines how accurately it's mirrored (copied).

| If the Meme is... | $\implies$ It has... | $\implies$ Replication is... | $\implies$ The Mutation Rate ($\mu_{eff}$) is... |
| :--- | :--- | :--- | :--- |
| **Simple/Redundant** | **Low Entropy ($H \approx 0$)** | **High Fidelity (Easy to copy)** | **Low** |
| **Complex/Random** | **High Entropy ($H \approx H_{max}$)** | **Low Fidelity (Hard to copy)** | **High** |

This setup is crucial because it implies that the most **informational** patterns (high entropy) are the most prone to **copying errors (mutations)**. This sets up a **trade-off** that drives the evolution of the meme population:

$$\text{Selection Pressure: High Fidelity (Low }\mu_{eff}) \iff \text{Low Information (Low } H)$$
$$\text{Selection Pressure: High Information (High } H) \iff \text{Low Fidelity (High }\mu_{eff})$$

The "selfish" patterns that survive will be those that strike an **optimal balance** between complexity (to be "useful" or "interesting") and simplicity (to be successfully mirrored).

### 3\. Selection and Retention:

This determines which patterns survive.

  * **Survival (Fitness):** A meme's "fitness" can be defined as its **Replicability** and its **Longevity**.
      * **Replicability (Internal Fitness):** Memes that are **simpler** (e.g., have a lower complexity score, or maybe are closer to a particular 'target' pattern) might be copied with **higher accuracy** (lower effective mutation rate, $\mu$). *This is a key phenomenological focus, making the pattern itself influence copying fidelity.*
      * **Retention (External Fitness):** Agents have a **limited pool size** (e.g., max $K$ memes). If the agent successfully copies a meme, they must *drop* an existing one (e.g., the oldest, or the one with the lowest "fitness" score) to make room for the new one. **Competition** for space in the host's mind is a form of selection.


## The **"dominant meme"** 

The dominant meme is where the **internal selective pressure**, the "selfishness" within the agent's mind, is explicitly modeled.

In this Cellular Automaton (CA) structure, the "dominant meme" of an agent at $(x, y)$ is the one it chooses to **broadcast** to its neighbors in that generation.

We choose dominance Through Internal Competition to honor the complexity suggested by Dawkins (where memes compete for "brain space"), the agent must maintain a **pool of memes** and run an internal selection process.

### The Rule: Lowest Shannon Entropy Wins 🏆

The most fitting definition of the dominant meme is the one that has best satisfied the **replicator's imperative**: **to be copied accurately.**

1.  **Agent Pool:** Each agent $(x, y)$ stores a small, fixed list of memes (e.g., $K=5$ patterns) in its "mind."
2.  **Internal Competition:** At the start of every interaction cycle, the agent selects its $M_{dominant}$ from this pool based on its **intrinsic fitness (fidelity)**.
    * **The Dominant Meme is the one in the agent's pool with the LOWEST Shannon Entropy ($H$).**

### Why This is "Selfish":

This rule models the ultimate form of meme selfishness:

* **Fidelity Bias:** Memes with low entropy are patterns that are **intrinsically easier to mirror** (lowest effective mutation rate $\mu_{eff}$).
* **Winning the Mind:** By making the lowest-entropy meme the "dominant" (most transmittable) one, we ensure that the **patterns best designed for faithful replication** are the ones the agent is most likely to pass on.
* **The Agent's Role:** The agent acts as a filter, naturally favoring the spread of patterns that possess the highest inherent survival mechanism.

### The Role of Replication (External Update):

When the agent successfully replicates a new meme ($M'_{new}$) from a neighbor, it incorporates it into its pool. If the pool is full, it must **selectively forget** a pattern (e.g., the oldest, or perhaps the one with the highest entropy, to maintain its bias toward fidelity). This dynamic ensures continuous internal and external selection pressure.

## The Universal Meme Life Cycle (Replicator Dynamics)

Definition of the fundamental "life process" for any collection of memes (whether in a single mind or a population).

### 1. Retention & Selection (Competition for Space)
Meme survival depends on its ability to persist against rivals.
* **Mechanism:** When a new meme is created, it must displace an existing one. The fitness metric determines which meme survives.
* **Rule:** **Low Entropy ($H$)** grants a selective advantage (the pattern is inherently more stable and resistant to copying error, making it a better replicator).

### 2. Replication (Copying & Transmission)
The act of creating a new copy.
* **Mechanism:** A source meme is read and written into a new location (a slot in the pool, or a slot in a neighboring agent's pool).

### 3. Variation (Mutation & Error)
Copying is imperfect, leading to new patterns.
* **Mechanism:** The **copying fidelity** is inversely proportional to the source meme's **Shannon Entropy ($H$)**. This means complex (high-$H$) patterns are more likely to generate variants (mutate).
    $$\mu_{eff} = \mu_{base} + k \cdot H_{source}$$

## Applying the Process: Internal vs. External Scales

By applying this universal cycle at two levels, we create a nested system of evolution:

### 1. Internal Dynamics (The Mind: Evolution within the Agent)

The agent's meme pool is a miniature ecosystem where patterns compete for dominance and space. This models **how individuals select and prioritize** the ideas they encounter.

| Aspect | Internal Process | Resulting Phenomenon |
| :--- | :--- | :--- |
| **Replication** | **Self-Rehearsal:** An agent copies a meme from its own pool into an empty slot, or replaces an old one. | The agent reinforces patterns it already holds, especially those with low $H$. |
| **Mutation** | **Memory Decay/Reinterpretation:** The mutation rate ($\mu_{int}$) is applied during this self-copying. This rate should be **low** ($\mu_{int} < \mu_{ext}$) to model stable memory. | Simple patterns (low $H$) become even more stable. Complex patterns (high $H$) slowly degrade or simplify over time due to internal error. |
| **Selection** | **Dominance Election:** The agent chooses the **Lowest-$H$ meme** to be its $M_{dominant}$ for external transmission. | The agent is biased toward transmitting patterns with the highest intrinsic fidelity. |

### 2. External Dynamics (The Population: Evolution between Agents)

This is the spatial spread and competition for the limited space in other agents' minds. This models **cultural transmission**.

| Aspect | External Process | Resulting Phenomenon |
| :--- | :--- | :--- |
| **Replication** | **Social Transmission:** Agent $A$ copies $M_{dominant}$ from neighbor $B$ and adds it to $A$'s pool. | Memes spread spatially. |
| **Mutation** | **Copying Error/Misunderstanding:** The external mutation rate ($\mu_{ext}$) is applied, based on the *source meme's $H$*. This rate should be **higher** than the internal one. | Highly complex memes (high $H$) are drastically altered or simplified when transmitted, creating rapid variants but decreasing stability. |
| **Selection** | **Invasion:** The new meme $M'_{new}$ (the copy from $B$) must displace an existing meme in $A$'s pool (e.g., the oldest or highest-$H$ one). | Only the most persistent, stable patterns (low $H$) manage to successfully invade and stabilize in the population. |


## Implementation Concept:

### 1\. Meme

A Meme is an object with:

* The meme representation: an **array** of [0,1] with a length $L$
* The memes **Shannon Entropy ($H$)** is calculated to determine copying fidelity.
* additional fields like the age or fitness

### 2\. Agents (Hosts)

Each agent is an object representing the hosts (individuals) that carry and attempt to replicate the memes.

#### Agent Attributes:

  * Located at $(x, y)$ on the grid. 
  * Meme Pool: A collection of one or more `Meme` objects the agent currently "knows."
  * index for a **single dominant meme** to be passed on.

#### Agent Behavior (Core Actions):

  * **Selection:** The agent chooses a meme from its pool to replicate.
  * **Replication (Mirroring):** The agent attempts to copy a chosen meme and *pass it* to another agent. This is the **mirroring aspect** where errors (mutations) occur.

### 3\. Setting Up the 2D Environment

The simulation space will be a grid representing the population.

* **The Grid:** Use a 2D NumPy array. Each cell holds one **Agent**.
  * **Create Agents:** Start with a fixed number of agents ($N$).
    * **Seed Memes:** Assign a random set of initial memes (patterns) to the agents.
  * **Agent State:** Each agent's most crucial state is its **current dominant meme** (the pattern it's currently transmitting).

#### Key Spatial Parameters:

* **Size:** Define the grid dimensions (e.g., $N \times N$, like $50 \times 50$).
* **Boundary Conditions:**
    * **Toroidal (Wrap-Around):** The most common choice. The top edge is a neighbor of the bottom edge, and the left edge neighbors the right. This avoids edge effects.
    * **Fixed/Reflecting:** Edges have no neighbors beyond them.
* **Neighborhood:** Define which cells an agent interacts with:
    * **Von Neumann:** North, South, East, West (4 neighbors).
    * **Moore:** Includes diagonals (8 neighbors). (Recommended for richer dynamics). 

#### Visualization

Lets set the length of all memes to $L$=16 and visualize each agent as a 4x4 square bitmap of its dominant meme.

Structure the code so it can be expanded with further visualizations. 

### 4\. The Core Simulation Cycle (Generation $T \to T+1$)

The simulation advances in discrete steps. A "New Grid" is calculated based on the "Old Grid" to ensure all interactions are simultaneous (a key feature of Cellular Automata).

### 1. Internal Dynamics: Preparing for Transmission

In this stage, every agent $A_{x,y}$ processes its own mind (meme pool) and determines what it is *ready* to transmit.

| Step | Process | Action | Goal |
| :--- | :--- | :--- | :--- |
| **1.1 Self-Rehearsal/Decay** | **Internal Replication & Mutation** | Each agent randomly selects a meme ($M_{old}$) from its pool and attempts to "rehearse" (copy) it, creating $M_{rehearsal}$. This copy is subject to the **internal mutation rate ($\mu_{int}$)**, which is based on $H(M_{old})$. | Models memory decay or subconscious reinterpretation, driving complex patterns toward simplification/stability. |
| **1.2 Internal Selection** | **Pool Update (Competition)** | $M_{rehearsal}$ is added to the agent's pool. If the pool size limit ($K$) is exceeded, the agent removes the meme with the **Highest Shannon Entropy ($H$)** (the least stable/most complex pattern). | Enforces internal selection pressure, prioritizing storage of highly stable (low-H) patterns. |
| **1.3 Dominance Election** | **Identify $M_{dominant}$** | The agent selects the meme from its updated pool that has the **Lowest Shannon Entropy ($H$)**. This is the single pattern the agent will *broadcast* this generation. | Models the agent's bias toward transmitting the pattern that is inherently best at being copied (the "most selfish" replicator). |

---

### 2. External Dynamics: Interaction and Invasion

Every agent $A_{x,y}$ now looks at its neighborhood to receive new ideas and calculate its state for the next generation ($A'_{x,y}$).

| Step | Process | Action | Goal |
| :--- | :--- | :--- | :--- |
| **2.1 Target Selection** | **Observation** | $A_{x,y}$ surveys its Moore neighborhood (8 cells) and the $M_{dominant}$ of each neighbor. $A_{x,y}$ randomly selects one neighbor, $B$, as the source of imitation. | Introduces randomness into cultural selection (which neighbor the agent talks to). |
| **2.2 Mirroring & Error** | **External Replication & Mutation** | $A_{x,y}$ attempts to copy $B$'s $M_{dominant}$ ($M_{source}$), creating a new pattern, $M_{invasion}$. This copy is subject to the **external mutation rate ($\mu_{ext}$)**, which is based on $H(M_{source})$. ($\mu_{ext} > \mu_{int}$). | Models noisy social transmission. High-H patterns are prone to distortion when communicated. |
| **2.3 External Invasion** | **Pool Replacement** | $M_{invasion}$ is added to the $A_{x,y}$'s pool. If the pool size limit ($K$) is exceeded, $A_{x,y}$ removes the meme with the **Highest Shannon Entropy ($H$)**. | A successful new pattern must displace the least stable old pattern in the mind. |

### 3. State Update

* All agents $A_{x,y}$ simultaneously switch their state to $A'_{x,y}$ (using the updated meme pool calculated in step 2.3). The cycle repeats.

***

## Key Phenomenological Implications

This two-tiered structure allows to distinguish between two kinds of meme survival:

1.  **Internal Stability (Retention):** Driven by the low $\mu_{int}$ and the selection rule (1.2). This favors patterns that are easy to *remember* or are resistant to mental decay.
2.  **External Stability (Spread):** Driven by the high $\mu_{ext}$ and the dominance rule (1.3). This favors patterns that are easy to *communicate* and resist misunderstanding.

The patterns that win globally will be those that have the **lowest possible Shannon Entropy** while still being distinct enough from a uniform pattern (e.g., `'00000000'`) to survive random internal mutations. 
We expect to observe how low-entropy "replicator cores" emerge and colonize the grid.

## Analysis: Entropy Plummets to Zero

The convergence to the lowest possible entropy states (all $0$s or all $1$s) is the logical, emergent outcome of the selection rules implemented.

### 1. Zero Entropy is the Fidelity King

* **The Problem:** The fitness function is defined solely by **replicative fidelity**, which is the inverse of the mutation rate $\mu_{eff}$.
    $$\mu_{eff} = \mu_{base} + k \cdot H_{source}$$
* **The Result:** The pattern with the absolute lowest Shannon Entropy ($H=0$) has the lowest possible mutation rate, $\mu_{base}$. This makes $H=0$ the global **"replicator optimum."**
    * **Uniform Patterns:** The patterns '0000000000000000' and '1111111111111111' have $p_0=1$ or $p_1=1$, resulting in $H=0$.
    * **The "Selfish" Victory:** Since the rules favor the most stable, easiest-to-copy patterns, the selection pressure relentlessly drives all other memes toward these two uniform states.

### 2. The Dominance of Internal Selection

There is a second factor: the **Internal Selection (Pool Replacement)** rule.

* **Rule:** When a new meme is added, the meme with the **Highest Entropy ($H_{max}$)** is removed.
* **Effect:** This rule acts as a powerful, non-random internal filter that *accelerates* the decline in entropy. It ensures that any mutation that results in a lower-entropy pattern (even slightly) is retained, while any higher-entropy pattern (the more informational ones) are purged from the agent's mind first.
* **The Feedback Loop:** Low-entropy memes are prioritized for transmission, and new high-entropy mutations are quickly forgotten. This creates a relentless, one-way entropy drain.

***

## Introducing Complexity and Stable Diversity

To prevent total convergence and achieve a stable, diverse configuration, we need to introduce a **second dimension of fitness** that counteracts the purity of replicative fidelity. The memes must acquire some **"functional" value** that favors complexity.

### 1. Introduce a "Function" or "Utility" Fitness

Memes should compete not just on how well they are copied, but on what they **do** for the agent.

* **Definition:** Define a **Target Pattern ($M_{target}$)** that is *complex*
  => see @config.py the predefined UTILITY_PATTERNS.
* **Utility Score:** Assign a high **Utility Score ($U$)** to a meme $M$ if it is close to $M_{target}$ (e.g., using **inverse Hamming Distance** to $M_{target}$).
* **The Trade-Off:** Now, the overall success of a meme must balance its $U$ (utility/complexity) and its $\mu_{eff}$ (fidelity/simplicity).

### 2. Implement Utility-Based Selection

The new selection rules cause that agents to sometimes prioritize utility over fidelity.

#### A. Modify Dominance Election (Internal)

Change how the agent chooses its $M_{dominant}$ for transmission:

* **Old Rule (Pure Fidelity):** Choose the meme with the lowest $H$.
* **New Rule (Utility-Weighted):** Choose the meme that maximizes a combined score, $S$:
    $$S = (\alpha \cdot \text{Utility Score}) - (\beta \cdot H)$$
    where $\alpha$ and $\beta$ are weights. By setting $\alpha$ high, agents are now incentivized to transmit patterns close to the complex $M_{target}$, even if they are riskier to copy.

#### B. Modify Pool Replacement (Internal and External)

Change which meme is forgotten (deleted) when the pool is full:

* **Old Rule (Pure Fidelity):** Remove the highest $H$ meme.
* **New Rule (Utility-Weighted):** Remove the meme with the **lowest combined score ($S$)** or the **lowest Utility Score ($U$)**. This ensures that memes that have utility are retained, regardless of their high entropy.

### 3. Expected Outcome with Utility

By introducing a complex target pattern and utility-weighted selection a dynamic tension is created:

* **Low-H Memes:** Still exist as stable, background patterns.
* **High-H Memes:** Are favored for their utility, creating **islands of complexity** around the $M_{target}$ pattern.
* **Stable Equilibrium:** The system will stabilize at a non-zero average entropy, reflecting patterns that are complex enough to be useful (high $U$) but simple enough to resist complete decay (low $H$ relative to their utility competitors). The **entropy will be maximized, subject to the constraint of replicative fidelity**. This creates a much richer evolutionary scenario. 
