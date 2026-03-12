from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import copy
import sys
import os

# Force Python to look inside the /api folder for imported files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import _bot as bot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class GameState(BaseModel):
    orbs_grid: List[List[int]]
    occupied: List[List[str]]
    player: str
    row: int = -1
    col: int = -1

def move(orbs_grid, occupied, start_row, start_col, player):
    rows = len(orbs_grid)
    cols = len(orbs_grid[0])

    frames = [] #To store the animation of chain reaction

    orbs_grid[start_row][start_col] += 1
    occupied[start_row][start_col] = player

    frames.append({
        "orbs_grid": copy.deepcopy(orbs_grid),
        "occupied": copy.deepcopy(occupied)
    })

    queue = [(start_row, start_col)]

    while queue:
        wave_size = len(queue)
        is_exploded = False

        for _ in range(wave_size):
            r, c = queue.pop(0)

            is_corner = True if r in [0, rows - 1] and c in [0, cols - 1] else False
            is_edge = True if r in [0, rows - 1] or c in [0, cols - 1] else False

            if is_corner:
                limit = 2
            elif is_edge:
                limit = 3
            else:
                limit = 4
            
            if orbs_grid[r][c] >= limit:
                is_exploded = True
                orbs_grid[r][c] -= limit
                if orbs_grid[r][c] == 0:
                    occupied[r][c] = 'n'

                if orbs_grid[r][c] >= limit:
                    queue.append((r, c))

                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

                for dr, dc in directions:
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < rows and 0 <= nc < cols:
                        orbs_grid[nr][nc] += 1
                        occupied[nr][nc] = player
                        queue.append((nr, nc))

        if is_exploded:
            frames.append({
                "orbs_grid": copy.deepcopy(orbs_grid),
                "occupied": copy.deepcopy(occupied)
            })
    return frames


@app.post("/api/human_move")
def human_move(state: GameState):
    animations_frames = move(state.orbs_grid, state.occupied, state.row, state.col, state.player)
    return {"frames": animations_frames}

@app.post("/api/bot_move")
def bot_move(state: GameState):
    b_row, b_col = bot.get_best_move(state.orbs_grid, state.occupied, state.player)

    animation_frames = move(state.orbs_grid, state.occupied, b_row, b_col, state.player)
    
    return {
        "bot_row": b_row,
        "bot_col": b_col,
        "frames": animation_frames
    }