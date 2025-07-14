# Emergent Maze Coordination with Symbolic Agents

Most people today think of “agents” as tool-using LLMs with goal inference.  
This project explores something different — no models, no language, no learning.

Instead, this is a **procedural multi-agent simulation** where coordination emerges through:
- Shared memory
- Trail signals
- Local decision rules

No dialogue. No central controller.

---

## ❌ It’s Not:
- Not LLM-based  
- Not autonomous in the modern AI sense

## ✅ It Is:
- **Agents**: Simple Python functions with symbolic logic  
- **Communication**: Trail signals stored in shared memory (with decay)  
- **Goal**: Navigate a 25×25 maze from `(1, 1)` to `(23, 23)`

---

## System Overview

### Agents
- `Alpha` and `Beta`
- Fully independent
- No shared planning or communication

### Maze
- 25×25 grid
- Includes walls and trap zones

---

## Coordination

- Agents write **signal trails** into shared memory  
- Trails **decay over time** (simulating influence fade)  
- Agents indirectly influence each other through memory traces  
- No precomputed paths, no machine learning

---

## Logic Flow

Each agent performs the following on each step:

1. **Scan** for valid moves  
2. **Score** each move based on:
   - Distance to goal (Manhattan)
   - Penalties: self-visits, other agent trails, danger zones
   - Bonuses: fresh unexplored areas, pheromone strength
3. **Select** the best move
4. **Update** its position and trail in shared memory
5. **React** to the environment as it changes

**No thinking. Just symbolic coordination via local rules.**

---

## Results

- Alpha visited 46 tiles  
- Beta reached the goal in 46 steps  
- No collisions, no shortcuts  
- Trails subtly guided behavior  
- Agents completed the task with no explicit messages

---

## Visuals

- Heatmap of trail intensity over time  
- Beta’s final path overlayed on the maze  

