import time
import random

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

goal=(23,23)
agent_positions={
    "alpha":(1, 1),
    "beta":(1, 1)}

visited={
    "alpha":set(),
    "beta":set()
}

shared_memory={
    "alpha_path":[],
    "beta_path":[],
    "agent_traces":{},  
    "danger":set()
}

def valid_moves(pos):
    x,y = pos
    moves = []
    for dx,dy in [(0, 1),(1, 0),(0, -1),(-1, 0)]:
        nx,ny=x + dx,y + dy
        if 0<= nx<25 and 0<= ny<25 and maze[ny][nx]==0:
            moves.append((nx, ny))
    return moves

def score_move(pos, goal, agent_id):
    if agent_id == "alpha":
      other_id= "beta"
    else:
      other_id= "alpha"

    gx,gy = goal#coordinates of goal
    x,y = pos

    dist_to_goal = abs(gx - x) + abs(gy - y)#manhattan distance

    if pos in visited[agent_id]:
      self_visited_penalty = True#penalties
    else:
      self_visited_penalty = False

    if f"{other_id}_path" in shared_memory and pos in shared_memory[f"{other_id}_path"]:
      other_trail_penalty = True#checking if both have the same path
    else:
      other_trail_penalty = False

    if "danger" in shared_memory and pos in shared_memory["danger"]:
      danger_zone_penalty = True#danger zones
    else:
      danger_zone_penalty = False

    signal_bonus = 0
    if pos in shared_memory.get("agent_traces", {}):
        signal_bonus = shared_memory["agent_traces"][pos] * 0.5

    score = -dist_to_goal#negative distance is better

    #penalties
    if self_visited_penalty:
        score =score-5  
    if other_trail_penalty:
        score =score-3
    if danger_zone_penalty:
        score =score-4

    #bonuses
    score=score+ signal_bonus

    # Add exploration bonus for unvisited areas
    if pos not in visited[agent_id] and pos not in visited[other_id]:
        score += 1

    return score + random.uniform(-0.5, 0.5)#noise

def update_signals():
    current_traces = list(shared_memory["agent_traces"].keys())
    for pos in current_traces:
        shared_memory["agent_traces"][pos] =shared_memory["agent_traces"][pos]*0.9
        if shared_memory["agent_traces"][pos]<0.1:
            del shared_memory["agent_traces"][pos]

    for agent_id in ["alpha", "beta"]:
        path = shared_memory.get(f"{agent_id}_path", [])

        #last 3 positions in the agent's path
        recent_moves = path[-3:]
        for step_index, pos in enumerate(recent_moves):
            # recent moves get stronger signal values
            strength=1.0-(step_index*0.3)
            shared_memory["agent_traces"][pos] = strength

def move(agent_id):
    current_pos=agent_positions[agent_id]
    visited[agent_id].add(current_pos)

    options = valid_moves(current_pos)
    if not options:#no valid moves,flag as danger
        shared_memory["danger"].add(current_pos)
        return False

    best=max(options, key=lambda move: score_move(move, goal, agent_id))
    agent_positions[agent_id]=best
    shared_memory[f"{agent_id}_path"].append(best)

    return best==goal

def print_maze():
    display = []
    for row in maze:
      display.append(row.copy())
    ax,ay = agent_positions['alpha']
    bx,by = agent_positions['beta']
    gx,gy = goal
    display[ay][ax] = 'A'
    display[by][bx] = 'B'
    display[gy][gx] = 'G'

    for pos, strength in shared_memory.get("agent_traces", {}).items():#marking trails with .
        x, y = pos
        if display[y][x] == 0:
            display[y][x] = '·'

    print("\nMaze (25×25):")
    for row in display:
        line = ''
        for cell in row:
            if cell== 1:
                line =line+ '|'
            elif cell== 0:
                line=line+ '.'
            else:
                line=line+ str(cell) + ' '
        print(line.strip())

def run():
    print_maze()

    for step in range(200):
        print(f"\nStep {step+1}")
        update_signals()
        a_done = move("alpha")
        b_done = move("beta")

        print(f"Alpha at {agent_positions['alpha']}, Beta at {agent_positions['beta']}")

        if step%2==0:
            print_maze()


    print_maze()
    print(f"Alpha visited: {len(visited['alpha'])} cells")
    print(f"Beta visited: {len(visited['beta'])} cells")
    print(f"signal trails: {len(shared_memory['agent_traces'])}")
    print(f"Danger zones: {len(shared_memory['danger'])}")
run()
