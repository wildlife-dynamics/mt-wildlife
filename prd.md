---
title: 'Mara Triangle Wildlife Sightings'
repo_name: 'mt-wildlife'
workflow_id: 'mt_wildlife'
created: '2026-03-31'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
data_sources: [set_smart_connection]
reference_workflows: [mt-patrols, download-smart-event, mt-wildlife-data, event-map, summary-table]
tasks_identified: [set_workflow_details, set_smart_connection, set_time_range, get_timezone_from_time_range, get_events_from_smart, convert_values_to_timezone, apply_reloc_coord_filter, apply_sql_query, normalize_json_column, set_list_of_string_vars, filter_row_values, exclude_row_values, summarize_df, apply_color_map, set_groupers, split_groups, create_point_layer, set_base_maps, set_string_var, draw_ecomap, persist_text, persist_df_wrapper, create_docx, gather_dashboard]
---

# PRD: Mara Triangle Wildlife Sightings

**Created:** 2026-03-31
**Repo:** `/Users/yunwu/MEP/wt/mt-wildlife/`
**Workflow ID:** `mt_wildlife`

## Overview

### Problem Statement

Mara Triangle conservancy needs a wildlife sighting analysis workflow that produces per-species maps, a summary table, and a DOCX report. Currently this requires running 5 separate workflows (`mt_event_download`, `mt_wd_data`, `mt_wd_summary`, `mt_wd_map`, `mt_wd_other_map`) with manual data passing between them. A single consolidated workflow eliminates this overhead and replaces a custom `mt_wildlife_sightings` task with standard core tasks (`normalize_json_column` + `apply_sql_query`).

### Solution

A single workflow that fetches SMART events, filters to wildlife direct observations, processes sighting data using SQL, generates per-species point maps for 8 featured species plus one combined "all others" map, produces a summary table (sightings count + individuals count by species), exports data, and assembles everything into a DOCX report.

### Scope

**In Scope:**
- Fetch events from SMART API (Mara Triangle conservancy)
- Filter to "Wildlife - direct observation" events using `apply_sql_query`
- Normalize extracted_attributes and derive Species + Count columns via SQL
- 8 per-species maps (African Buffalo, African Elephant, Lion, Leopard, Cheetah, Giraffe, Zebra, Wildebeest)
- 1 combined map for all other species
- Summary table: Sightings Count and Individuals Count by species
- Data export (sightings as CSV/Parquet)
- DOCX report with maps, summary table
- Static PNG maps (via create_docx screenshot conversion)

**Out of Scope:**
- Rhino sightings (separate workflow)
- Charts
- Interactive dashboard (gather_dashboard with empty widgets)
- Tooltips (static output only)

## Data Sources & Connections

| Source | Type | Connection | Notes |
| ----- | ---- | ---------- | ----- |
| SMART | Events | `set_smart_connection` | Mara Triangle, ca_uuid: 735606d2-c34e-49c3-a45b-7496ca834e58, connection name: mara |

## Reference Workflows

| Workflow | Relevance | Patterns Borrowed |
| -------- | --------- | ----------------- |
| mt-patrols | DOCX report, SMART connection, create_docx pattern | create_docx context items, SMART fetch, coordinate filter |
| download-smart-event | SMART event fetch, bounding box filter | get_events_from_smart params, ca_uuid, language_uuid |
| mt-wildlife-data (template) | Wildlife sighting processing, species splitting | filter_row_values/exclude_row_values, species list |
| event-map (template) | Point map generation, colormap, ecomap | create_point_layer style, draw_ecomap config, persist_text pattern |
| summary-table (template) | Summary table, summarize_df | summarize_df params |

## Task Pipeline

### Identified Tasks

| # | Task | ID | Group | Purpose |
|---|------|----|-------|---------|
| 1 | set_workflow_details | workflow_details | — | Dashboard metadata |
| 2 | set_smart_connection | smart_client_name | — | SMART API connection |
| 3 | set_time_range | time_range | — | User time range |
| 4 | get_timezone_from_time_range | get_timezone | — | Extract timezone |
| 5 | get_events_from_smart | get_events | — | Fetch SMART events |
| 6 | convert_values_to_timezone | convert_tz | Process | Convert time column |
| 7 | apply_reloc_coord_filter | filter_coords | Process | Filter bad coordinates |
| 8 | apply_sql_query | filter_wildlife | Process | Filter event_type = Wildlife |
| 9 | normalize_json_column | normalize_attrs | Process | Flatten extracted_attributes |
| 10 | apply_sql_query | process_sightings | Process | Cast counts, sum → Count, rename Species, filter nulls |
| 11 | apply_color_map | sightings_colormap | Process | Color by Species (shared by both map pipelines) |
| 12 | set_list_of_string_vars | featured_list | Process | User-configurable featured species list |
| 13 | filter_row_values | featured_species | Split | Keep featured species |
| 14 | exclude_row_values | other_species | Split | Everything else (auto-derived) |
| 14 | summarize_df | wildlife_summary | Summary | Sightings Count + Individuals Count by Species |
| 15 | persist_df_wrapper | persist_summary | Summary | Export summary as CSV |
| 16 | set_groupers | species_groupers | Featured Maps | Group by Species |
| 17 | split_groups | split_species | Featured Maps | Split into per-species groups |
| 18 | create_point_layer | featured_point_layers | Featured Maps | Point layers per species |
| 19 | set_base_maps | base_map_defs | Featured Maps | Shared tile layers |
| 20 | set_string_var | set_featured_title | Featured Maps | Map title |
| 21 | draw_ecomap | featured_ecomap | Featured Maps | Render per-species maps |
| 22 | persist_text | featured_ecomap_html | Featured Maps | Save map HTML |
| 23 | create_point_layer | other_point_layer | Other Map | Single point layer |
| 24 | set_string_var | set_other_title | Other Map | Map title |
| 25 | draw_ecomap | other_ecomap | Other Map | Render combined map |
| 26 | persist_text | other_ecomap_html | Other Map | Save map HTML |
| 27 | persist_df_wrapper | persist_sightings | Export | Export sightings data |
| 28 | set_groupers | report_groupers | — | For create_docx sorting |
| 29 | create_docx | wildlife_report | — | Generate DOCX report |
| 30 | gather_dashboard | dashboard | — | Empty dashboard (required) |

### Spec.yaml Draft

```yaml
id: mt_wildlife

requirements:
  - name: ecoscope-workflows-core
    version: ">=0.22.17, <0.23.0"
    channel: https://repo.prefix.dev/ecoscope-workflows/
  - name: ecoscope-workflows-ext-ecoscope
    version: ">=0.22.17, <0.23.0"
    channel: https://repo.prefix.dev/ecoscope-workflows/
  - name: ecoscope-workflows-ext-custom
    version: ">=0.0.40, <0.1.0"
    channel: https://repo.prefix.dev/ecoscope-workflows-custom/

rjsf-overrides:
  properties:
    filter_coords.properties.bounding_box.default:
      min_x: 33.0
      min_y: -3.0
      max_x: 36.0
      max_y: 0.0
    filter_coords.properties.filter_point_coords.default:
      - {x: 180.0, y: 90.0}
      - {x: 0.0, y: 0.0}
      - {x: 1.0, y: 1.0}
    Process Sightings.properties.featured_list.properties.vars.default:
      - "African Buffalo"
      - "African Elephant"
      - "Lion"
      - "Leopard"
      - "Cheetah"
      - "Giraffe"
      - "Zebra"
      - "Wildebeest"
    Featured Species Maps.properties.base_map_defs.properties.base_maps.default:
      - url: "https://tiles.arcgis.com/tiles/POUcpLYXNckpLjnY/arcgis/rest/services/landDx_basemap_tiles_mapservice/MapServer/tile/{z}/{y}/{x}"
        opacity: 0.5
    persist_sightings.properties.filetypes.default: ["parquet"]
    persist_sightings.properties.filetypes.items.enum: ["csv", "parquet"]
    wildlife_report.properties.template_path.default: "https://raw.githubusercontent.com/wildlife-dynamics/mt-wildlife/main/resources/templates/mt_wildlife_report_template.docx"

  uiSchema:
    Process Sightings.filter_coords.filter_point_coords.items.ui:options.label: false

task-instance-defaults:
  skipif:
    conditions:
      - any_is_empty_df
      - any_dependency_skipped

workflow:
  # Setup
  - name: Workflow Details
    id: workflow_details
    task: set_workflow_details

  - name: Data Source
    id: smart_client_name
    task: set_smart_connection

  - name: Time Range
    id: time_range
    task: set_time_range
    partial:
      time_format: '%d %b %Y %H:%M:%S %Z'

  - name: Extract Timezone
    id: get_timezone
    task: get_timezone_from_time_range
    partial:
      time_range: ${{ workflow.time_range.return }}

  # Data Fetching
  - name: Get SMART Events
    id: get_events
    task: ecoscope_workflows_ext_ecoscope.tasks.io.get_events_from_smart
    partial:
      client: ${{ workflow.smart_client_name.return }}
      time_range: ${{ workflow.time_range.return }}
      ca_uuid: "735606d2-c34e-49c3-a45b-7496ca834e58"
      language_uuid: "13451893-86af-4ec0-beac-2b8e0c2482b5"

  # Phase 2 stand-in (uncomment to develop with local data):
  # - name: Load Events
  #   id: get_events
  #   task: ecoscope_workflows_ext_custom.tasks.io.load_df
  #   partial:
  #     deserialize_json: false

  # Processing
  - title: Process Sightings
    type: task-group
    description: "Process SMART events into wildlife sighting records."
    tasks:
      - name: Convert to Timezone
        id: convert_tz
        task: convert_values_to_timezone
        partial:
          df: ${{ workflow.get_events.return }}
          timezone: ${{ workflow.get_timezone.return }}
          columns: ["time"]

      - name: Filter Coordinates
        id: filter_coords
        task: apply_reloc_coord_filter
        partial:
          df: ${{ workflow.convert_tz.return }}

      - name: Filter Wildlife Observations
        id: filter_wildlife
        task: apply_sql_query
        partial:
          df: ${{ workflow.filter_coords.return }}
          query: "SELECT * FROM df WHERE event_type = 'Wildlife - direct observation'"

      - name: Normalize Extracted Attributes
        id: normalize_attrs
        task: normalize_json_column
        partial:
          df: ${{ workflow.filter_wildlife.return }}
          column: "extracted_attributes"

      - name: Process Sighting Columns
        id: process_sightings
        task: apply_sql_query
        partial:
          df: ${{ workflow.normalize_attrs.return }}
          query: >-
            SELECT *,
              (COALESCE(TRY_CAST("extracted_attributes__Number of Wildlife observed" AS DOUBLE), 0)
              + COALESCE(TRY_CAST("extracted_attributes__Number of Age or Sex Unknown" AS DOUBLE), 0)
              + COALESCE(TRY_CAST("extracted_attributes__Number of Adult Females" AS DOUBLE), 0)
              + COALESCE(TRY_CAST("extracted_attributes__Number of Adult Males" AS DOUBLE), 0)
              + COALESCE(TRY_CAST("extracted_attributes__Number of Young" AS DOUBLE), 0))
              AS "Count",
              "extracted_attributes__Species" AS "Species"
            FROM df
            WHERE "extracted_attributes__Species" IS NOT NULL

      - name: Apply Colormap
        id: sightings_colormap
        task: apply_color_map
        partial:
          df: ${{ workflow.process_sightings.return }}
          input_column_name: "Species"
          output_column_name: "species_colormap"
          colormap: "Dark2"

      - name: Set Featured Species List
        id: featured_list
        task: set_list_of_string_vars

      - name: Filter Featured Species
        id: featured_species
        task: filter_row_values
        partial:
          df: ${{ workflow.sightings_colormap.return }}
          column: "Species"
          values: ${{ workflow.featured_list.return }}

      - name: Filter Other Species
        id: other_species
        task: exclude_row_values
        partial:
          df: ${{ workflow.sightings_colormap.return }}
          column: "Species"
          values: ${{ workflow.featured_list.return }}

  # Summary
  - name: Summarize Wildlife Sightings
    id: wildlife_summary
    task: summarize_df
    partial:
      df: ${{ workflow.process_sightings.return }}
      groupby_cols: ["Species"]
      summary_params:
        - display_name: "Sightings Count"
          aggregator: count
          column: Count
        - display_name: "Individuals Count"
          aggregator: sum
          column: Count

  - name: Persist Summary
    id: persist_summary
    task: persist_df_wrapper
    partial:
      df: ${{ workflow.wildlife_summary.return }}
      root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
      filename_prefix: "wildlife_summary"
      filetypes: ["csv"]
      sanitize: false
    skipif:
      conditions:
        - never

  # Featured Species Maps
  - title: Featured Species Maps
    type: task-group
    description: "Generate one map per featured species."
    tasks:
      - name: Species Groupers
        id: species_groupers
        task: set_groupers
        partial:
          groupers:
            - index_name: "Species"

      - name: Split by Species
        id: split_species
        task: split_groups
        partial:
          df: ${{ workflow.featured_species.return }}
          groupers: ${{ workflow.species_groupers.return }}

      - name: Featured Map Title
        id: set_featured_title
        task: set_string_var
        partial:
          var: "Wildlife Sightings"

      - name: Base Maps
        id: base_map_defs
        task: set_base_maps

      - name: Create Featured Point Layers
        id: featured_point_layers
        task: create_point_layer
        skipif:
          conditions:
            - any_is_empty_df
            - any_dependency_skipped
            - all_geometry_are_none
        partial:
          layer_style:
            get_radius: 5.0
            fill_color_column: "species_colormap"
          legend:
            label_column: "Species"
            color_column: "species_colormap"
        mapvalues:
          argnames: geodataframe
          argvalues: ${{ workflow.split_species.return }}

      - name: Draw Featured Ecomaps
        id: featured_ecomap
        task: draw_ecomap
        partial:
          tile_layers: ${{ workflow.base_map_defs.return }}
          north_arrow_style:
            placement: "top-left"
          legend_style:
            title: "Species"
            format_title: true
            placement: "bottom-right"
          static: false
          title: null
          max_zoom: 13
        mapvalues:
          argnames: geo_layers
          argvalues: ${{ workflow.featured_point_layers.return }}

      - name: Persist Featured Ecomaps
        id: featured_ecomap_html
        task: persist_text
        partial:
          root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
          filename_suffix: "species_map"
        mapvalues:
          argnames: text
          argvalues: ${{ workflow.featured_ecomap.return }}

  # Other Species Map
  - title: Other Species Map
    type: task-group
    description: "Generate one combined map for all non-featured species."
    tasks:
      - name: Create Other Point Layer
        id: other_point_layer
        task: create_point_layer
        skipif:
          conditions:
            - any_is_empty_df
            - any_dependency_skipped
            - all_geometry_are_none
        partial:
          geodataframe: ${{ workflow.other_species.return }}
          layer_style:
            get_radius: 5.0
            fill_color_column: "species_colormap"
          legend:
            label_column: "Species"
            color_column: "species_colormap"

      - name: Other Map Title
        id: set_other_title
        task: set_string_var
        partial:
          var: "Wildlife Sightings - Other Species"

      - name: Draw Other Ecomap
        id: other_ecomap
        task: draw_ecomap
        partial:
          geo_layers: ${{ workflow.other_point_layer.return }}
          tile_layers: ${{ workflow.base_map_defs.return }}
          north_arrow_style:
            placement: "top-left"
          legend_style:
            title: "Species"
            format_title: true
            placement: "bottom-right"
          static: false
          title: null
          max_zoom: 13

      - name: Persist Other Ecomap
        id: other_ecomap_html
        task: persist_text
        partial:
          text: ${{ workflow.other_ecomap.return }}
          root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
          filename_suffix: "other_species_map"

  # Data Export
  - name: Persist Sightings Data
    id: persist_sightings
    task: persist_df_wrapper
    partial:
      df: ${{ workflow.process_sightings.return }}
      root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
      filename_prefix: "wildlife_sightings"
      sanitize: true
    skipif:
      conditions:
        - never

  # Report
  - name: Report Groupers
    id: report_groupers
    task: set_groupers
    partial:
      groupers:
        - index_name: "Species"

  - name: Create Wildlife Report
    id: wildlife_report
    task: ecoscope_workflows_ext_custom.tasks.results.create_docx
    partial:
      context:
        items:
          - item_type: timerange
            key: report_date
            value: ${{ workflow.time_range.return }}
            format: "%b %Y"
          - item_type: table
            key: summary
            value: ${{ workflow.wildlife_summary.return }}
          - item_type: image
            key: species_maps
            value: ${{ workflow.featured_ecomap_html.return }}
            screenshot_config:
              wait_for_timeout: 1000
              max_concurrent_pages: 2
              device_scale_factor: 1.0
          - item_type: image
            key: other_map
            value: ${{ workflow.other_ecomap_html.return }}
            screenshot_config:
              wait_for_timeout: 1000
              max_concurrent_pages: 2
      groupers: ${{ workflow.report_groupers.return }}
      output_dir: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
      filename_prefix: mt_wildlife_report
    skipif:
      conditions:
        - never

  # Dashboard (empty — report-driven)
  - name: Create Dashboard
    id: dashboard
    task: gather_dashboard
    partial:
      details: ${{ workflow.workflow_details.return }}
      widgets: []
      groupers:
        - index_name: "Species"
      time_range: ${{ workflow.time_range.return }}
```

### Task Gaps

None — all tasks exist in core/ecoscope/custom libraries. The custom `mt_wildlife_sightings` task is replaced by `normalize_json_column` + `apply_sql_query` (core tasks).

## Development Strategy

### Data Source Approach

3-phase approach — SMART is a remote API.

### Phase 1 — Bootstrap Data

**Download workflow:** Use `download-smart-event` at `/Users/yunwu/MEP/custom-workflows/mara-triangle/workflows/download-smart-event/` to fetch fresh raw events.

| Data | Source Task | Output Format | Output Path |
| ---- | ----------- | ------------- | ----------- |
| SMART events (raw) | get_events_from_smart | GeoParquet | `resources/mock-data/mara_triangle_raw_events.parquet` |

**Note:** Existing data at `~/.ecoscope-desktop/workflows/mt_event_download/outputs/mara_triangle_event.parquet` is already processed (coordinates filtered) — it cannot be used as Phase 2 input since the workflow applies its own filtering. Either download fresh raw data or generate synthetic test data.

### Phase 2 — Develop with Local Data

**load_df stand-in configuration:**

```yaml
# Replace SMART fetch with:
- name: Load Events
  id: get_events
  task: ecoscope_workflows_ext_custom.tasks.io.load_df
  partial:
    deserialize_json: false
```

Comment out `set_smart_connection` task.

**What to complete in Phase 2:**
- [ ] Full processing pipeline (filter → normalize → SQL → split)
- [ ] All 8 featured species maps validated visually
- [ ] Other species combined map validated
- [ ] Summary table validated
- [ ] Data export generated
- [ ] DOCX report renders with maps, table
- [ ] rjsf form configured and validated
- [ ] Base test case passing with local data

### Phase 3 — Reconnect Live Data Source

Uncomment `set_smart_connection` and `get_events_from_smart`. Remove `load_df` stand-in. Update test-cases.yaml for integration test.

```yaml
# Restore original fetch task:
- name: Get SMART Events
  id: get_events
  task: ecoscope_workflows_ext_ecoscope.tasks.io.get_events_from_smart
  partial:
    client: ${{ workflow.smart_client_name.return }}
    time_range: ${{ workflow.time_range.return }}
    ca_uuid: "735606d2-c34e-49c3-a45b-7496ca834e58"
    language_uuid: "13451893-86af-4ec0-beac-2b8e0c2482b5"
```

## Output Configuration

### Maps

| Map | Layer Type | Style Config | Legend | Notes |
| --- | ---------- | ------------ | ------ | ----- |
| Per-species (x8) | `create_point_layer` | `get_radius: 5.0`, `fill_color_column: species_colormap` | label: Species, color: species_colormap, bottom-right | One map per featured species, split via groupers |
| All others (x1) | `create_point_layer` | `get_radius: 5.0`, `fill_color_column: species_colormap` | label: Species, color: species_colormap, bottom-right | Single combined map, no splitting |

Colormap: `Dark2` (consistent with existing event-map template).

Base maps: LandDx basemap tiles at 0.5 opacity.

Ecomap: `static: false`, `max_zoom: 13`, north arrow top-left, legend bottom-right. HTML converted to PNG by `create_docx` screenshot_config.

### Charts

None.

### Data Exports

| Export | Format | Sanitize | Notes |
| ------ | ------ | -------- | ----- |
| All sightings | Parquet (default, configurable) | true | All processed wildlife sightings, skipif: never |
| Summary table | CSV | false | Species x (Sightings Count, Individuals Count), skipif: never |

### Widget & Dashboard Assembly

Dashboard has empty widgets (`widgets: []`) — this workflow is report-driven. The dashboard exists for metadata/grouper context only.

## Form Configuration (rjsf)

### Parameter Visibility

| Parameter | Basic / Advanced | Default | Notes |
| --------- | ---------------- | ------- | ----- |
| workflow_details | Basic | — | Name and description |
| smart_client_name | Basic | — | SMART connection |
| time_range | Basic | — | Since/until |
| get_events (ca_uuid, language_uuid) | Advanced (partial) | Mara Triangle UUIDs | Hardcoded in spec |
| filter_coords.bounding_box | Advanced | Mara Triangle bbox | Via rjsf-overrides |
| filter_coords.filter_point_coords | Advanced | Bad coord filter | Labels hidden via uiSchema |
| featured_list.vars | Advanced | 8 species list | User-configurable, default via rjsf-overrides |
| featured_species.values | N/A | — | Wired from featured_list.return |
| other_species.values | N/A | — | Wired from featured_list.return (auto-complement) |
| base_map_defs | Advanced | LandDx tiles | Via rjsf-overrides |
| persist_sightings.filetypes | Advanced | ["parquet"] | Constrained to csv/parquet |
| wildlife_report.template_path | Advanced | GitHub-hosted template | DOCX template URL |

### rjsf-overrides Draft

```yaml
rjsf-overrides:
  properties:
    filter_coords.properties.bounding_box.default:
      min_x: 33.0
      min_y: -3.0
      max_x: 36.0
      max_y: 0.0
    filter_coords.properties.filter_point_coords.default:
      - {x: 180.0, y: 90.0}
      - {x: 0.0, y: 0.0}
      - {x: 1.0, y: 1.0}
    Process Sightings.properties.featured_list.properties.vars.default:
      - "African Buffalo"
      - "African Elephant"
      - "Lion"
      - "Leopard"
      - "Cheetah"
      - "Giraffe"
      - "Zebra"
      - "Wildebeest"
    Featured Species Maps.properties.base_map_defs.properties.base_maps.default:
      - url: "https://tiles.arcgis.com/tiles/POUcpLYXNckpLjnY/arcgis/rest/services/landDx_basemap_tiles_mapservice/MapServer/tile/{z}/{y}/{x}"
        opacity: 0.5
    persist_sightings.properties.filetypes.default: ["parquet"]
    persist_sightings.properties.filetypes.items.enum: ["csv", "parquet"]
    wildlife_report.properties.template_path.default: "https://raw.githubusercontent.com/wildlife-dynamics/mt-wildlife/main/resources/templates/mt_wildlife_report_template.docx"

  uiSchema:
    Process Sightings.filter_coords.filter_point_coords.items.ui:options.label: false
```

### Validation Checklist

- [x] Bounding box defaults to Mara Triangle region
- [x] Featured species list user-configurable via set_list_of_string_vars with rjsf default; both filter tasks wired from same source
- [x] Base map defaults to LandDx tiles
- [x] Export filetypes constrained to csv/parquet
- [x] Coordinate filter point labels hidden
- [x] DOCX template URL defaults to main branch

## Test Strategy

### Test Cases

| Case Name | mock_io | Purpose |
| --------- | ------- | ------- |
| base | false | Integration test against real SMART API |

### Data Source Testing

| Data Source | mock_io: false requirements |
| ----------- | --------------------------- |
| SMART | Real SMART API with mara connection, recent time range |

### skipif Conditions

| Task | Conditions | Rationale |
| ---- | ---------- | --------- |
| (all tasks) | any_is_empty_df, any_dependency_skipped | Global default |
| featured_point_layers | + all_geometry_are_none | Skip if no valid geometries |
| other_point_layer | + all_geometry_are_none | Skip if no valid geometries |
| persist_sightings | never | Always export even if empty |
| persist_summary | never | Always export |
| wildlife_report | never | Always generate report |

### Validation Approach

- Integration test: verify full pipeline against real SMART API
- Verify SQL processing produces Count and Species columns
- Verify 8 featured species maps + 1 other map generated
- Verify summary table has correct columns (Sightings Count, Individuals Count)
- Verify DOCX report renders with all sections
- Verify data exports written

## Dashboard Layout

### layout.json Draft

```json
[]
```

Empty — report-driven workflow with no dashboard widgets.

## Implementation Plan

### Tasks

- [ ] Task 1: Bootstrap raw event data for Phase 2 development
  - Action: Download fresh raw SMART events using `download-smart-event` workflow, or generate synthetic test data matching raw SMART event schema (geometry, uuid, event_type, time, extracted_attributes JSON). Note: existing data at `~/.ecoscope-desktop/workflows/mt_event_download/outputs/mara_triangle_event.parquet` is already filtered/processed and cannot be used as raw input.

- [ ] Task 2: Create spec.yaml with Phase 2 load_df
  - File: `spec.yaml`
  - Action: Full pipeline from load_df through create_docx

- [ ] Task 3: Create DOCX report template
  - File: `resources/templates/mt_wildlife_report_template.docx`
  - Action: Template with placeholders for report_date, summary table, species_maps, other_map

- [ ] Task 4: Create test-cases.yaml
  - File: `test-cases.yaml`
  - Action: Base test case with local data

- [ ] Task 5: Compile, test, validate outputs
  - Action: Compile, run tests, visually inspect maps/table/report

- [ ] Task 6: Configure rjsf-overrides
  - File: `spec.yaml` (rjsf-overrides section)
  - Action: Set defaults, constrain filetypes, hide technical params

- [ ] Task 7: Reconnect SMART API (Phase 3)
  - File: `spec.yaml`, `test-cases.yaml`
  - Action: Restore SMART fetch, add integration test case

### Acceptance Criteria

- [ ] AC 1: Given SMART event data, when the workflow runs, then wildlife sightings are filtered using `apply_sql_query` (no custom task dependency)
- [ ] AC 2: Given processed sightings, when split by species, then 8 per-species point maps are generated with Dark2 colormap and legend
- [ ] AC 3: Given non-featured species, when mapped, then one combined "Other Species" map is generated
- [ ] AC 4: Given all sightings, when summarized by species, then table shows Sightings Count and Individuals Count
- [ ] AC 5: Given maps and summary, when DOCX is generated, then report contains date, summary table, all species maps, and other species map
- [ ] AC 6: Given no wildlife observations for the time range, then skipif conditions prevent errors and report is still generated
- [ ] AC 7: Given the rjsf form, then species list and bounding box have correct defaults for Mara Triangle

## Additional Context

### Dependencies

- ecoscope-workflows-core >= 0.22.17
- ecoscope-workflows-ext-ecoscope >= 0.22.17
- ecoscope-workflows-ext-custom >= 0.0.40
- DOCX template to be created and hosted on GitHub (wildlife-dynamics/mt-wildlife)

### Notes

- Replaces 5 separate workflows: mt_event_download, mt_wd_data, mt_wd_summary, mt_wd_map, mt_wd_other_map
- Custom `mt_wildlife_sightings` task replaced by `normalize_json_column` + `apply_sql_query` — eliminates dependency on `ecoscope-workflows-ext-mt`
- SQL Count column sums all count fields (Number of Wildlife observed + age/sex breakdowns) matching existing behavior — may double-count if "Number of Wildlife observed" is already a total
- SMART tasks use fully-qualified names (`ecoscope_workflows_ext_ecoscope.tasks.io.get_events_from_smart`)
- The `load_df` stand-in is kept as a comment in spec.yaml for easy Phase 2/3 switching
- Static PNG output handled by `create_docx` screenshot conversion (not separate `html_to_png` task)
- Dashboard is intentionally empty — all output goes to DOCX report
