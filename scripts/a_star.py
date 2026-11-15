"""A* route planning over the Gale Crater mission DEM.

Cells are (row, col) tuples into the 2000 x 2000 elevation grid (row 0 = north).
A cell is blocked if its slope is >= SLOPE_LIMIT degrees. The route cost is the
3D distance walked in metres.
"""

import json
import os
import numpy as np
import math
import heapq
#import time #for testing


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SLOPE_LIMIT = 20    # degrees; must match the red threshold in 3_mission_slope.png
SURROUNDING_CELLS = (   # (row, col) offsets to the 8 neighbours of a cell
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
)


def load_data():
    """Load the elevation grid (metres) and its metadata (bbox, cell size)."""
    elevation = np.load(os.path.join(ROOT_DIR, "../data/gale_mission.npy")) # shape (2000, 2000)
    with open(os.path.join(ROOT_DIR, "../data/gale_mission.json"), encoding="utf-8") as f:
        meta = json.load(f)
    return elevation, meta


def compute_slope(elevation, cell_m):
    """Slope in degrees for every cell, in its steepest direction."""
    dz_dy, dz_dx = np.gradient(elevation, cell_m) # height change per metre
    # Combine both directions into the steepest gradient, then rise/run -> angle.
    slope = np.degrees(np.arctan(np.hypot(dz_dx, dz_dy)))
    return slope


def compute_blocked(slope):
    """Boolean grid: True where the slope is too steep to walk."""
    blocked = slope >= SLOPE_LIMIT
    return blocked


def neighbours(row, col, blocked, cell_m):
    """Walkable neighbours of a cell, as a list of ((row, col), step length in metres)."""
    result = list()
    straight_step = cell_m
    diagonal_step = round(cell_m * math.sqrt(2), 4) # diagonal of a square cell

    for offset_row, offset_col in SURROUNDING_CELLS:
        curr_row, curr_col = row + offset_row, col + offset_col
        # Bounds check first: a negative index would silently wrap to the other side of the grid.
        if 0 <= curr_row < blocked.shape[0] and 0 <= curr_col < blocked.shape[1] and not blocked[curr_row, curr_col]:
            if abs(offset_row) + abs(offset_col) == 2:   # both offsets non-zero -> diagonal
                result.append(((curr_row, curr_col), diagonal_step))
            else:
                result.append(((curr_row, curr_col), straight_step))
    return result


def edge_cost(a, b, elevation, step_m):
    """Cost of stepping from cell a to neighbour b: the 3D distance in metres.
    Never less than step_m, so the straight-line heuristic never overestimates.
    """
    diff_height = elevation[a] - elevation[b]
    return round(math.hypot(step_m, diff_height), 4)  # sqrt(step_m^2 + dz^2)


def heuristic(a, goal, cell_m):
    """A*'s guess of the remaining cost: straight-line distance in metres.
    It is never longer than the real route (admissible), which is what
    guarantees A* finds the shortest path.
    """
    return round(math.hypot(a[0] - goal[0], a[1] - goal[1]) * cell_m, 4)


def rebuild_path(came_from, start, goal):
    """Follow came_from back from goal to start; return the path as start -> goal."""
    current_cell = goal
    path = list()
    path.append(current_cell)

    while start != current_cell:
        current_cell = came_from[current_cell]   # one step back towards start
        path.append(current_cell)

    return path[::-1]   # built goal -> start, so reverse it


def a_star(start, goal, blocked, elevation, cell_m):
    """Cheapest walkable route from start to goal as a list of cells, or None if there is none.
    Raises ValueError if start or goal is outside the grid or blocked.
    """
    # Check bounds before blocked[...]: a negative index wouldn't crash, it would wrap around.
    for i in range(2):   # i = 0: row, i = 1: col
        if not(0 <= start[i] < blocked.shape[i]):
            raise ValueError("Start outside of map")

        if not(0 <= goal[i] < blocked.shape[i]):
            raise ValueError("Goal outside of map")

    if blocked[start]:
        raise ValueError("Start blocked")
    if blocked[goal]:
        raise ValueError("Goal blocked")

    cost_so_far = np.full(blocked.shape, np.inf)   # cheapest known cost from start to each cell; inf = not reached
    cost_so_far[start] = 0
    came_from = dict()   # cell -> the cell we reached it from (read by rebuild_path)
    visited = set()      # cells already fully explored

    # priority = cost so far + heuristic guess to the goal.
    open_heap = [(heuristic(start, goal, cell_m), start)]

    while open_heap:
        priority, current_cell = heapq.heappop(open_heap)

        # if we have reached the goal
        if current_cell == goal:
            return rebuild_path(came_from, start, goal)

        # if the cell has already been visited
        if current_cell in visited:
            continue
        visited.add(current_cell)
        row, col = current_cell
        
        for neighbour, step_m in neighbours(row, col, blocked, cell_m):
            new_cost = cost_so_far[current_cell] + edge_cost(current_cell, neighbour, elevation, step_m)
            if new_cost < cost_so_far[neighbour]:   # found a cheaper way to reach neighbour
                cost_so_far[neighbour] = new_cost
                came_from[neighbour] = current_cell
                priority = new_cost + heuristic(neighbour, goal, cell_m)
                heapq.heappush(open_heap, (priority, neighbour))
    return None   # heap empty: everything reachable was explored, the goal is not reachable


def run_a_star(start, goal): ## Format of start and goal are a grid cell (row, col)
    elevation, meta = load_data()
    cell_m = meta["cell_size_m"]["x"]
    blocked = compute_blocked(compute_slope(elevation, cell_m))
    path = a_star(start, goal, blocked, elevation, cell_m)
    return path


# For testing
#if __name__ == "__main__":
#    # Both cells are in the main walkable region (see a_star_next_steps.md).
#    start = (200, 1000)
#    goal = (1800, 1000)
#    elevation, meta = load_data()
#    cell_m = meta["cell_size_m"]["x"]
#    blocked = compute_blocked(compute_slope(elevation, cell_m))
#
#    # perf_counter() is only meaningful as a difference between two readings.
#    start_time = time.perf_counter()
#    path = a_star(start, goal, blocked, elevation, cell_m)
#    elapsed = time.perf_counter() - start_time
#    print(f"{len(path)} cells, {elapsed:.1f} s")
#
#    # Sanity check: the route must never pass through a blocked cell.
#    for cell in path:
#        if blocked[cell]:
#            print(f"{cell} is in blocked")
