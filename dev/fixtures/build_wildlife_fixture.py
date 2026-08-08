"""
Generates the two mock fixtures used by the mock test case:

  - get-events-wildlife.example-return.parquet
      Mock for ecoscope.platform.tasks.io.get_events. Schema mirrors the
      platform's get-events example return (point events, include_display_values).

  - process-events-details-wildlife.example-return.parquet
      Mock for ecoscope.platform.tasks.io.process_events_details. Also io-tagged,
      so under mock_io: true its example_return clobbers anything upstream.
      Mirrors the get_events fixture plus the columns the task adds
      (event_details with title-mapped keys/values, reported_by_name).

All rows are SYNTHETIC: deterministic seeded RNG, uuid5-derived ids, jittered
grid coordinates in the Maasai Mara area, and made-up counts. No rows are
copied from any real EarthRanger instance. Re-run this script (instead of
editing the parquets by hand) if upstream schemas change.
"""

import uuid
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point

OUT_GET_EVENTS = Path(__file__).parent / "get-events-wildlife.example-return.parquet"
OUT_PROCESS = Path(__file__).parent / "process-events-details-wildlife.example-return.parquet"

NAMESPACE = uuid.UUID("00000000-0000-0000-0000-00000000beef")
rng = np.random.default_rng(20260808)

# Species display titles as mapped by process_events_details(map_to_titles=True)
# from the mmnr wildlife_sightings event type schema, with a rough sighting weight
# and count range each (synthetic, only loosely shaped like real data).
SPECIES = [
    ("Wildebeest", 6, (50, 5000)),
    ("Lion", 5, (1, 12)),
    ("Elephant", 5, (1, 30)),
    ("Zebra", 4, (10, 400)),
    ("Buffalo", 3, (5, 300)),
    ("Giraffe - Maasai", 3, (1, 15)),
    ("Cheetah (inform Monitoring Team)", 2, (1, 4)),
    ("Leopard", 2, (1, 2)),
    ("Impala", 2, (5, 60)),
    ("Topi", 2, (2, 40)),
    ("Hippo", 1, (1, 5)),
    ("Serval", 1, (1, 1)),
]

reporter = {
    "additional": {"region": None},
    "common_name": None,
    "content_type": "observations.subject",
    "country": None,
    "created_at": "2025-02-07T13:58:57.000000Z",
    "id": str(uuid.uuid5(NAMESPACE, "reporter-1")),
    "image_url": "/static/er_mobile.svg",
    "is_active": True,
    "name": "Ranger 1",
    "region": None,
    "sex": None,
    "subject_subtype": "er_mobile",
    "subject_type": "person",
    "tracks_available": False,
    "updated_at": "2025-02-07T13:58:57.000000Z",
    "user": None,
}

# Maasai Mara-ish bounding box for synthetic sighting locations
LON_MIN, LON_MAX = 34.90, 35.30
LAT_MIN, LAT_MAX = -1.60, -1.20

species_pool = [s for s, weight, _ in SPECIES for _ in range(weight)]
N_ROWS = 40

rows = []
for i in range(N_ROWS):
    name = species_pool[int(rng.integers(len(species_pool)))]
    lo, hi = next(cr for s, _, cr in SPECIES if s == name)
    rows.append(
        {
            "id": str(uuid.uuid5(NAMESPACE, f"event-{i}")),
            "time": pd.Timestamp("2026-07-01T06:00:00Z")
            + pd.Timedelta(minutes=int(rng.integers(0, 30 * 24 * 60))),
            "event_type": "wildlife_sightings",
            "event_category": "field_ranger",
            "title": "Wildlife",
            "priority": 0,
            "priority_label": "Gray",
            "state": "active",
            "reported_by": reporter,
            "geometry": Point(
                round(float(rng.uniform(LON_MIN, LON_MAX)), 6),
                round(float(rng.uniform(LAT_MIN, LAT_MAX)), 6),
            ),
            "serial_number": str(90000 + i),
            "event_type_display": "Wildlife sightings",
            "species": name,
            "count": int(rng.integers(lo, hi + 1)),
        }
    )

df = pd.DataFrame(rows).sort_values("time", ignore_index=True)
details = [
    {"Count": r["count"], "Species": r["species"], "Sighting type": "Visual"}
    for _, r in df.iterrows()
]
df = df.drop(columns=["species", "count"])

gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
gdf.to_parquet(OUT_GET_EVENTS, index=False)
print(f"wrote {OUT_GET_EVENTS} ({len(gdf)} rows)")

# process_events_details mock: same rows, drop `reported_by`, add the
# columns this task contributes (event_details, reported_by_name).
processed = gdf.drop(columns=["reported_by"]).copy()
processed["event_details"] = details
processed["reported_by_name"] = "Ranger 1"
processed.to_parquet(OUT_PROCESS, index=False)
print(f"wrote {OUT_PROCESS} ({len(processed)} rows)")
