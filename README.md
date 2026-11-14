# mars-path-finder

🚀 NASA Space Apps Challenge 2026 | An interactive Mars exploration map powered by NASA data, designed to help astronauts plan Marswalks, analyze terrain hazards, and explore scientific locations.

## Data sources

All data comes from NASA's **[JPL Mars Trek](https://trek.nasa.gov/mars/)**, a web portal that publishes Mars mission data as downloadable map layers.

| Dataset (Mars Trek layer) | Mission / instrument | Used for |
| --- | --- | --- |
| MRO HiRISE, Gale Crater DEM (`Gale_DEM_SMG_1m`) | Mars Reconnaissance Orbiter, HiRISE | **Elevation data the app runs on** ([`data/`](data/README.md)), and the elevation and slope maps |
| MRO HiRISE, Curiosity Roving Site Mosaic | Mars Reconnaissance Orbiter, HiRISE | Orbital photo of the mission area ([`docs/`](docs/README.md)) |
| MRO CTX, Gale Crater Mosaic | Mars Reconnaissance Orbiter, CTX | Overview picture of Gale Crater ([`docs/`](docs/README.md)) |
| Viking VIS, Global Color Mosaic | Viking orbiters | Picture of the whole planet ([`docs/`](docs/README.md)) |

- The elevation data is downloaded once with [`scripts/fetch_data.py`](scripts/README.md) and committed,
  so the app works offline.
- Mission area: 5 × 5 km at the foot of Mount Sharp in Gale Crater, near the route of NASA's Curiosity rover.

Credits: NASA/JPL-Caltech Mars Trek; HiRISE: NASA/JPL-Caltech/University of Arizona;
CTX: NASA/JPL-Caltech/MSSS; Viking: NASA/USGS.
