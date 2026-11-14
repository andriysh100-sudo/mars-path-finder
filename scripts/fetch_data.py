"""Download the mission-area elevation data (DEM) from NASA Mars Trek and save it for offline use.

Run this ONCE (with internet), then commit the two output files:
    data/gale_mission.npy   elevation grid in metres (float32, shape = rows x cols)
    data/gale_mission.json  metadata: area, cell size, source, ...

The app only reads those files, so it works without internet afterwards.

Usage (from the repo root):
    python scripts/fetch_data.py
"""

import json
import math
import struct
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# --- Settings: change these to fetch a different area -------------------------------------------

NAME = "gale_mission"

# Mission area in degrees (west, south, east, north). 5 x 5 km at the foot of Mount Sharp.
BBOX = (137.24767, -4.89918, 137.33233, -4.81482)

# Grid size in cells. 2000 x 2000 over 5 km = 2.5 m per cell.
# The NASA server allows at most 15000 (width) x 4100 (height) per request.
WIDTH, HEIGHT = 2000, 2000

# "MRO HiRISE, Gale Crater DEM" (1 m/pixel) served by JPL Mars Trek.
SERVICE = "https://trek.nasa.gov/mars/trekarcgis/rest/services/Gale_DEM_SMG_1m/ImageServer"

# Mars radius used by the data's coordinate system (IAU 2000 Mars sphere, EPSG 104905).
MARS_RADIUS_M = 3_396_190

OUT_DIR = Path(__file__).resolve().parent.parent / "data"

# -------------------------------------------------------------------------------------------------


def download_tiff(bbox, width, height):
    """Ask the NASA server to cut out `bbox` and return it as a GeoTIFF of float32 elevations."""
    if width > 15000 or height > 4100:
        raise ValueError("Too big for one request (max 15000 x 4100 cells).")
    west, south, east, north = bbox
    url = (
        f"{SERVICE}/exportImage?bbox={west},{south},{east},{north}&bboxSR=104905"
        f"&size={width},{height}&format=tiff&pixelType=F32"
        f"&interpolation=RSP_BilinearInterpolation&f=image"
    )
    print(f"Downloading {width} x {height} cells from NASA Mars Trek ...")
    with urllib.request.urlopen(url, timeout=300) as response:
        data = response.read()
    if data[:4] not in (b"II*\x00", b"MM\x00*"):
        raise RuntimeError(f"Server did not return a TIFF. Start of reply: {data[:200]!r}")
    print(f"  received {len(data) / 1e6:.1f} MB")
    return data, url


def read_tiff(data):
    """Read an uncompressed, single-band float32 TIFF (the format the server returns) into a numpy array.

    A TIFF file starts with a table of "tags" (width, height, where the pixel data is, ...).
    The pixels are stored in square tiles (or horizontal strips), which we copy into one array.
    """
    order = "<" if data[:2] == b"II" else ">"  # byte order: little- or big-endian
    ifd_offset = struct.unpack(order + "I", data[4:8])[0]
    n_tags = struct.unpack(order + "H", data[ifd_offset:ifd_offset + 2])[0]

    type_sizes = {3: (2, "H"), 4: (4, "I")}  # SHORT and LONG: the only tag types we need
    tags = {}
    for i in range(n_tags):
        entry = data[ifd_offset + 2 + 12 * i: ifd_offset + 14 + 12 * i]
        tag, typ, count = struct.unpack(order + "HHI", entry[:8])
        if typ not in type_sizes:
            continue
        size, fmt = type_sizes[typ]
        if size * count <= 4:  # small values are stored directly in the entry
            raw = entry[8:8 + size * count]
        else:  # larger values are stored elsewhere; the entry holds their offset
            offset = struct.unpack(order + "I", entry[8:12])[0]
            raw = data[offset:offset + size * count]
        tags[tag] = struct.unpack(order + fmt * count, raw)

    width, height = tags[256][0], tags[257][0]
    if tags.get(259, (1,))[0] != 1:
        raise RuntimeError("Compressed TIFFs are not supported.")
    if tags.get(258, (32,))[0] != 32 or tags.get(339, (3,))[0] != 3:
        raise RuntimeError("Expected 32-bit float pixels.")

    dtype = np.dtype(np.float32).newbyteorder(order)
    grid = np.empty((height, width), dtype=np.float32)

    if 322 in tags:  # tiled: tiles are stored left-to-right, top-to-bottom
        tile_w, tile_h = tags[322][0], tags[323][0]
        tiles_across = math.ceil(width / tile_w)
        for k, offset in enumerate(tags[324]):
            ty, tx = divmod(k, tiles_across)
            tile = np.frombuffer(data, dtype, tile_w * tile_h, offset).reshape(tile_h, tile_w)
            y0, x0 = ty * tile_h, tx * tile_w
            h, w = min(tile_h, height - y0), min(tile_w, width - x0)  # edge tiles are padded
            grid[y0:y0 + h, x0:x0 + w] = tile[:h, :w]
    else:  # stripped: rows stored one after another in a few chunks
        raw = b"".join(data[o:o + c] for o, c in zip(tags[273], tags[279]))
        grid[:] = np.frombuffer(raw, dtype, width * height).reshape(height, width)
    return grid


def cell_size_m(bbox, width, height):
    """Size of one grid cell in metres. A degree of longitude shrinks by cos(latitude)."""
    west, south, east, north = bbox
    m_per_deg = MARS_RADIUS_M * math.pi / 180
    lat_mid = math.radians((south + north) / 2)
    return (east - west) * m_per_deg * math.cos(lat_mid) / width, (north - south) * m_per_deg / height


def main():
    data, url = download_tiff(BBOX, WIDTH, HEIGHT)
    elevation = read_tiff(data)

    # Sanity checks: real Gale elevations are a few km below Mars "sea level".
    # Missing data shows up as 0, NaN or a huge negative number.
    invalid = ~np.isfinite(elevation) | (elevation < -10_000) | (elevation >= 0)
    if invalid.any():
        print(f"  WARNING: {invalid.mean():.2%} of cells have no data")

    dx, dy = cell_size_m(BBOX, WIDTH, HEIGHT)
    OUT_DIR.mkdir(exist_ok=True)
    np.save(OUT_DIR / f"{NAME}.npy", elevation)

    meta = {
        "name": NAME,
        "description": "Elevation (metres, relative to the Mars datum) for the mission area at the foot of Mount Sharp, Gale Crater.",
        "units": "metres",
        "dtype": "float32",
        "shape_rows_cols": [HEIGHT, WIDTH],
        "row_0_is": "north edge",
        "col_0_is": "west edge",
        "bbox_west_south_east_north_deg": list(BBOX),
        "longitude": "degrees east",
        "cell_size_m": {"x": round(dx, 4), "y": round(dy, 4)},
        "elevation_min_m": round(float(np.nanmin(elevation[~invalid])), 2),
        "elevation_max_m": round(float(np.nanmax(elevation[~invalid])), 2),
        "invalid_cells": int(invalid.sum()),
        "source": "MRO HiRISE Gale Crater DEM (Gale_DEM_SMG_1m) via NASA/JPL Mars Trek",
        "source_url": url,
        "downloaded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (OUT_DIR / f"{NAME}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Saved {OUT_DIR / (NAME + '.npy')}  ({elevation.nbytes / 1e6:.1f} MB)")
    print(f"Saved {OUT_DIR / (NAME + '.json')}")
    print(f"  cells: {WIDTH} x {HEIGHT}, cell size: {dx:.2f} x {dy:.2f} m")
    print(f"  elevation: {meta['elevation_min_m']} .. {meta['elevation_max_m']} m")


if __name__ == "__main__":
    main()
