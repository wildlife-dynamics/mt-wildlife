"""Anonymize wildlife event data for public use.

Applies:
- GPS coordinate offset (shifts location while preserving spatial relationships)
- UUID regeneration with consistent mapping
- Patrol ID replacement
- Attribute UUID regeneration inside JSON blobs
"""

import json
import struct
import uuid

import numpy as np
import pandas as pd

INPUT_PATH = "/Users/yunwu/MEP/wt/mt-wildlife/resources/mock-data/mara_triangle_raw_events.parquet"
OUTPUT_PATH = "/Users/yunwu/MEP/wt/mt-wildlife/resources/mock-data/mara_triangle_raw_events.parquet"

# Coordinate offset: same as patrol anonymization
LON_OFFSET = -2.15
LAT_OFFSET = 1.73


def make_uuid_map(original_uuids, rng: np.random.Generator) -> dict[str, str]:
    """Create a consistent mapping from original UUIDs to new random UUIDs."""
    unique = sorted(set(str(u) for u in original_uuids if pd.notna(u)))
    return {
        old: str(uuid.UUID(int=int.from_bytes(rng.bytes(16), "big")))
        for old in unique
    }


def make_wkb_point(lon: float, lat: float) -> bytes:
    """Create a WKB Point (little-endian) from lon/lat."""
    return struct.pack("<bIdd", 1, 1, lon, lat)


def remap_attributes_json(attrs_json: str, uuid_map: dict[str, str]) -> str:
    """Remap attribute_uuid values inside a JSON attributes blob."""
    if pd.isna(attrs_json):
        return attrs_json
    items = json.loads(attrs_json)
    for item in items:
        old = item.get("attribute_uuid", "")
        if old in uuid_map:
            item["attribute_uuid"] = uuid_map[old]
    return json.dumps(items)


def main():
    df = pd.read_parquet(INPUT_PATH)
    rng = np.random.default_rng(42)

    print(f"Read {len(df)} rows from {INPUT_PATH}")

    # 1. Offset coordinates
    df["X"] = df["X"] + LON_OFFSET
    df["Y"] = df["Y"] + LAT_OFFSET

    # 2. Rebuild geometry as WKB
    df["geometry"] = [make_wkb_point(lon, lat) for lon, lat in zip(df["X"], df["Y"])]

    # 3. Regenerate row-level UUIDs
    for col in ["uuid", "category_uuid", "wp_group_uuid", "patrol_uuid"]:
        uuid_map = make_uuid_map(df[col], rng)
        df[col] = df[col].map(uuid_map)

    # 4. Replace patrol_id with fake sequential IDs
    original_ids = sorted(df["patrol_id"].dropna().unique())
    patrol_id_map = {old: f"ANON_{i:06d}" for i, old in enumerate(original_ids)}
    df["patrol_id"] = df["patrol_id"].map(patrol_id_map)

    # 5. Remap attribute UUIDs inside JSON blobs
    # Collect all attribute_uuids from all rows
    attr_uuids = set()
    for attrs in df["attributes"].dropna():
        for item in json.loads(attrs):
            attr_uuids.add(item["attribute_uuid"])
    attr_uuid_map = make_uuid_map(attr_uuids, rng)

    df["attributes"] = df["attributes"].apply(
        lambda x: remap_attributes_json(x, attr_uuid_map)
    )

    # Cast string columns
    string_cols = [
        "uuid", "category_uuid", "wp_group_uuid", "event_type",
        "patrol_uuid", "patrol_id", "attributes", "extracted_attributes",
        "event_category", "reported_by",
    ]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype("string[python]")

    df.to_parquet(OUTPUT_PATH, index=False)
    print(f"Written {len(df)} rows to {OUTPUT_PATH}")
    print(f"  Event types: {df['event_type'].unique().tolist()}")
    print(f"  Patrol IDs (sample): {df['patrol_id'].unique()[:5].tolist()}")


if __name__ == "__main__":
    main()
