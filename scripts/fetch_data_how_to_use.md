# Scripts

## `fetch_data.py`: download the elevation data

Downloads the mission area's elevation data (DEM) from NASA Mars Trek and saves it in `data/`
so the app works offline.

**You only need this if you want to change or re-download the data.** The output files are
already committed, so after cloning the repo the app works without running anything.

### Requirements

- Python 3 with NumPy (`pip install numpy`)
- Internet access (only while the script runs)

### Run it

From the repo root:

```
python scripts/fetch_data.py
```

Output:

```
Downloading 2000 x 2000 cells from NASA Mars Trek ...
  received 16.8 MB
Saved ...\data\gale_mission.npy  (16.0 MB)
Saved ...\data\gale_mission.json
  cells: 2000 x 2000, cell size: 2.50 x 2.50 m
  elevation: -4416.66 .. -3303.38 m
```

Then commit the two files in `data/`.

### Change the area or resolution

Edit the settings at the top of the script:

| Setting | Meaning |
| --- | --- |
| `NAME` | Output file name (`data/<NAME>.npy` and `.json`) |
| `BBOX` | Area in degrees: `(west, south, east, north)`. Longitude is degrees **east**, latitude negative = south |
| `WIDTH, HEIGHT` | Grid size in cells. Cell size = area width / `WIDTH` |

Useful numbers:

- On Mars, **0.01° ≈ 593 m** (latitude; longitude is about the same this close to the equator).
- 5 km ≈ 0.0844°, 10 km ≈ 0.1688°.
- Example: 10 × 10 km at 2.5 m per cell → `WIDTH, HEIGHT = 4000, 4000`.

Limits:

- The server allows at most **15000 × 4100 cells per request** (the script refuses larger sizes).
- The data only exists inside 137.12–137.73°E, 4.25–4.92°S (the HiRISE Gale DEM). Outside that the
  script warns that cells have no data.
- Don't use cells coarser than ~2.5 m for the pathfinder: big cells average away boulders and cliffs
  and make the terrain look safer than it is.
- File size grows quickly: `WIDTH × HEIGHT × 4` bytes (4000 × 4000 = 64 MB). GitHub rejects files over 100 MB.
