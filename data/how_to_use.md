# Data

Elevation data for the mission area at the foot of Mount Sharp, Gale Crater (5 × 5 km).
Created by [`scripts/fetch_data.py`](../scripts/README.md). Pictures of the area are in [`docs/`](../docs/README.md).

| File | Contents |
| --- | --- |
| `gale_mission.npy` | Elevation grid: NumPy array, `float32`, shape `(2000, 2000)`, metres |
| `gale_mission.json` | Metadata: area, cell size, elevation range, source, download date |

## What the numbers mean

- Each value is the **height in metres** of one cell, relative to the Mars datum ("sea level").
  Values are negative because Gale Crater is ~4.4 km below it.
- Each cell is **2.5 × 2.5 m** on the ground.
- `grid[row, col]`: **row 0 = north edge**, **col 0 = west edge**. So rows go north → south and
  columns go west → east, just like an image.

## Load it

```python
import json
import numpy as np

elevation = np.load("data/gale_mission.npy")      # shape (2000, 2000)
with open("data/gale_mission.json", encoding="utf-8") as f:
    meta = json.load(f)

cell_m = meta["cell_size_m"]["x"]                  # 2.5
print(elevation[0, 0])                             # height of the north-west corner, in metres
```

## Convert between coordinates and grid cells

Waypoints are given in longitude/latitude; the pathfinder works with `(row, col)`.

```python
west, south, east, north = meta["bbox_west_south_east_north_deg"]
rows, cols = elevation.shape

def lonlat_to_cell(lon, lat):
    col = int((lon - west) / (east - west) * cols)
    row = int((north - lat) / (north - south) * rows)   # north is row 0
    return row, col

def cell_to_lonlat(row, col):
    lon = west + (col + 0.5) / cols * (east - west)
    lat = north - (row + 0.5) / rows * (north - south)
    return lon, lat
```

## Compute slope

Slope is what decides whether a cell is walkable (see `CLAUDE.md`: ~20° limit).

```python
dz_dy, dz_dx = np.gradient(elevation, cell_m)               # height change per metre
slope_deg = np.degrees(np.arctan(np.hypot(dz_dx, dz_dy)))
blocked = slope_deg >= 20                                    # ~26% of this area
```

## Credits

MRO HiRISE Gale Crater DEM (`Gale_DEM_SMG_1m`) via NASA/JPL-Caltech Mars Trek
(<https://trek.nasa.gov/mars/>). The exact download URL is stored in `gale_mission.json`.
