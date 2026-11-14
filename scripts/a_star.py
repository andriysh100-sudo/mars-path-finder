import json
import os
import numpy as np

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SLOPE_LIMIT = 20
SURROUNDING_CELLS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
)



def lonlat_to_cell(lon, lat, elevation, meta):
    west, south, east, north = meta["bbox_west_south_east_north_deg"]
    rows, cols = elevation.shape

    col = int((lon - west) / (east - west) * cols)
    row = int((north - lat) / (north - south) * rows)   # north is row 0
    return row, col

def cell_to_lonlat(row, col, elevation, meta):
    west, south, east, north = meta["bbox_west_south_east_north_deg"]
    rows, cols = elevation.shape

    lon = west + (col + 0.5) / cols * (east - west)
    lat = north - (row + 0.5) / rows * (north - south)
    return lon, lat

def compute_slope(elevation, meta):
    dz_dy, dz_dx = np.gradient(elevation, meta["cell_size_m"]["x"])               # height change per metre
    slope = np.degrees(np.arctan(np.hypot(dz_dx, dz_dy)))
    return slope

def load_data():
    elevation = np.load(os.path.join(ROOT_DIR, "../data/gale_mission.npy"))   # shape (2000, 2000)
    with open(os.path.join(ROOT_DIR, "../data/gale_mission.json"), encoding="utf-8") as f:
        meta = json.load(f)
    return elevation, meta

def compute_blocked(slope):
    blocked = slope >= SLOPE_LIMIT
    return blocked

def neighbours(row, col, blocked, cell_m):
    result = list()
    straight_step = cell_m
    diagonal_step = round(cell_m * (2**0.5), 4)

    for offset_row, offset_col in SURROUNDING_CELLS:
        curr_row, curr_col = row + offset_row, col + offset_col
        if 0 <= curr_row < blocked.shape[0] and 0 <= curr_col < blocked.shape[1] and not blocked[curr_row, curr_col]:
            if abs(offset_row) + abs(offset_col) == 2:
                result.append(((curr_row, curr_col), diagonal_step))
            else:
                result.append(((curr_row, curr_col), straight_step))
    return result, 

def edge_cost(a, b, elevation, step_m):

    return

def heuristic(a, goal):
    return

def a_star(start, goal):
    return


if __name__ == "__main__":
    elevation, meta = load_data()
    blocked = compute_blocked(compute_slope(elevation, meta))
    good_neighbours, step_m = neighbours(0, 40, blocked, meta["cell_size_m"]["x"])

    edge_cost((1000, 1000), (1000, 999), elevation, step_m)
    print(good_neighbours)
    ##print(blocked)
    ##print(blocked.mean())
    ##print(blocked.shape)