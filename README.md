# Mara Triangle Wildlife Sightings Workflow

## Introduction

This workflow helps you analyze wildlife sighting data collected by field rangers in the Mara Triangle conservancy. It pulls direct observation records from **SMART**, processes them into species-level summaries, and produces maps and a formatted Word report.

**What this workflow does:**
- Downloads wildlife observation events from **SMART**
- Filters to direct sightings and extracts species and individual counts
- Summarizes sighting and individual counts per species
- Creates interactive maps for each featured species, plus a combined map for all other species
- Generates a Word document report containing the summary table and maps
- Exports raw sighting data in CSV and/or Parquet format

**Who should use this:**
- Conservation managers monitoring wildlife populations in the Mara Triangle
- Researchers analyzing species distribution and abundance from patrol data
- Anyone needing to produce periodic wildlife sighting reports from SMART data

## Prerequisites

Before using this workflow, you need:

1. **Ecoscope Desktop** installed on your computer
   - If you haven't installed it yet, please follow the installation instructions for Ecoscope Desktop

2. **SMART Data Source** configured in Ecoscope Desktop
   - You must have already set up a connection to your SMART server
   - Your data source should be configured with proper authentication credentials
   - You'll need to know the name of your configured SMART data source

3. **Wildlife observation data in SMART**
   - Your SMART database should contain patrol events of type "Wildlife - direct observation"
   - Events should include species name and count attributes (e.g., "Number of Wildlife observed", "Number of Adult Females", etc.)

## Installation

1. Select "Workflow Templates" tab
2. Click "+ Add Template"
3. Copy and paste this URL https://github.com/wildlife-dynamics/mt-wildlife and wait for the workflow template to be downloaded and initialized
4. The template will now appear in your available template list

## Configuration Guide

After adding the template, click on it to configure. Settings are organized into sections displayed in order on the form.

### Basic Configuration

#### 1. Workflow Details
Add information that will help differentiate this workflow run from another.

- **Workflow Name** (required): A descriptive name for this workflow run
  - Example: `"Mara Triangle Wildlife Sightings"`
- **Workflow Description** (optional): Additional context about this run
  - Example: `"Wildlife sighting analysis for Mara Triangle conservancy."`

#### 2. Time Range
Choose the period of time to analyze.

- **Since** (required): The start date and time
  - Example: `2026-01-01T00:00:00`
- **Until** (required): The end date and time
  - Example: `2026-01-31T23:59:59`
- **Timezone** (optional): Your local timezone for displaying times
  - Example: `Africa/Nairobi (UTC+03:00)`
  - Note: If left blank, times will be displayed in UTC

#### 3. Data Source
Select which SMART connection to use for downloading events.

- **Data Source** (required): Select one of your configured SMART data sources
  - Note: This must match a SMART connection you have already set up in Ecoscope Desktop

#### 4. Process Sightings
Configure how wildlife sighting records are processed.

- **Species** (required): The list of featured species to track individually. Each featured species will get its own map. All other species observed will be grouped into a single "Other Species" map.
  - Default list: `"African Buffalo"`, `"African Elephant"`, `"Lion"`, `"Leopard"`, `"Cheetah"`, `"Giraffe"`, `"Zebra"`, `"Wildebeest"`
  - You can add or remove species from this list based on your monitoring priorities

#### 5. Persist Sightings Data
Choose the output format for your raw sighting data export.

- **Filetypes** (optional): The output format(s) for the exported data
  - Options: **CSV**, **Parquet**
  - Default: `parquet`
  - Note: You can select one or both formats

#### 6. Create Wildlife Report
Configure the Word document report generation.

- **Template Path** (required): Path or URL to the Word template (.docx) file
  - Default: A pre-configured template hosted on GitHub
  - Note: You generally do not need to change this unless you have a custom report template

### Advanced Configuration

These optional settings provide additional control. They are hidden by default — expand the "Advanced" sections to access them.

#### Filter Coordinates
Filter events to a specific geographic area. The defaults are set for the Mara Triangle region.

- **Bounding Box**: Restrict events to within these coordinates
  - Default: Min Longitude `33.0`, Min Latitude `-3.0`, Max Longitude `36.0`, Max Latitude `0.0`
  - Note: Only change this if you need to narrow or widen the geographic scope

- **Filter Exact Point Coordinates**: Exclude events recorded at specific coordinates (e.g., known GPS error points)
  - Default: Excludes coordinates `(180, 90)`, `(0, 0)`, and `(1, 1)` which are common GPS placeholder values
  - Note: Add coordinates here if you have known bad data points to exclude

#### Base Maps
Select tile layers to use as base layers in map outputs.

- **Base Maps**: Choose from preset map styles or add a custom tile layer
  - Options: **Open Street Map**, **Roadmap**, **Satellite**, **Terrain**, **LandDx**, **USGS Hillshade**, or **Custom Layer**
  - Default: Terrain
  - Note: The first layer in the list will be the bottommost layer displayed. You can add multiple layers.

## Running the Workflow

Once you've configured all the settings:

1. **Review your configuration**
   - Double-check your time range, data source, and featured species list

2. **Save and run**
   - Click "Submit" and the workflow will show up in the "My Workflows" table
   - Click "Run" and the workflow will begin processing

3. **Monitor progress and wait for completion**
   - You'll see status updates as the workflow runs
   - Processing time depends on:
     - The size of your date range
     - Number of wildlife observation events in the system
     - Number of featured species (each gets its own map)
   - The workflow completes with status "Success" or "Failed"

## Understanding Your Results

After the workflow completes successfully, you'll find your outputs in the designated output folder.

### Data Outputs

#### Wildlife Sightings Data
The raw processed sighting records, saved in the format(s) you selected.

- **File formats**: CSV and/or Parquet (based on your selection)
- **Opens in**: Microsoft Excel, Google Sheets (CSV); Python/R (Parquet)
- **Contents**: One row per sighting event with the following columns:
  - `uuid`: Unique identifier for the event
  - `X`: Longitude of the sighting
  - `Y`: Latitude of the sighting
  - `time`: Date and time of the sighting (converted to your selected timezone)
  - `geometry`: Geographic point location
  - `Species`: Name of the species observed
  - `Count`: Total number of individuals observed (sum of all age/sex categories)

#### Wildlife Summary
An aggregated summary table grouped by species.

- **File format**: CSV
- **Contents**: One row per species with:
  - `Species`: Species name
  - `Sightings Count`: Number of separate sighting events
  - `Individuals Count`: Total number of individuals observed across all sightings

### Visual Outputs

#### Featured Species Maps
One interactive map per featured species, showing the locations of all sightings for that species.

- **Format**: Interactive HTML maps
- **Features**:
  - Color-coded point markers at each sighting location
  - Species legend in the bottom-right corner
  - North arrow in the top-left corner
  - Hover over points to see details

#### Other Species Map
A single combined map showing sightings for all species not in your featured list.

- **Format**: Interactive HTML map
- **Features**: Same as featured species maps, with all non-featured species shown together with distinct colors

### Wildlife Report
A formatted Word document (.docx) containing:
- Report date range
- Wildlife summary table
- Featured species maps (as images)
- Other species map (as image)

This report is ready for printing or sharing with stakeholders.

## Common Use Cases & Examples

Here are some typical scenarios and how to configure the workflow for each:

### Example 1: Monthly Sightings Report
**Goal**: Generate a standard monthly wildlife report for January 2026

**Configuration**:
- **Workflow Name**: `"Mara Triangle Wildlife Sightings"`
- **Time Range**:
  - Since: `2026-01-01T00:00:00`
  - Until: `2026-01-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Species**: Use the default list (African Buffalo, African Elephant, Lion, Leopard, Cheetah, Giraffe, Zebra, Wildebeest)
- **Filetypes**: `parquet`

**Result**: A Word report with summary table and maps for each of the 8 featured species, plus one map for all other species observed.

---

### Example 2: Big Cat Focus
**Goal**: Produce a report focused specifically on big cat species

**Configuration**:
- **Workflow Name**: `"Big Cat Sightings - Q1 2026"`
- **Time Range**:
  - Since: `2026-01-01T00:00:00`
  - Until: `2026-03-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Species**: `"Lion"`, `"Leopard"`, `"Cheetah"`
- **Filetypes**: `csv` and `parquet`

**Result**: Individual maps for Lion, Leopard, and Cheetah. All other species appear on the combined "Other Species" map. Both CSV and Parquet data exports are produced.

---

### Example 3: Full Year Analysis with CSV Export
**Goal**: Export a full year of sighting data for external analysis in Excel

**Configuration**:
- **Workflow Name**: `"Annual Wildlife Sightings 2025"`
- **Time Range**:
  - Since: `2025-01-01T00:00:00`
  - Until: `2025-12-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Species**: Use the default list
- **Filetypes**: `csv`

**Result**: A CSV file you can open in Excel with every sighting record, plus the summary table and Word report.

---

### Example 4: Custom Species List
**Goal**: Track specific species of interest beyond the default list

**Configuration**:
- **Workflow Name**: `"Expanded Species Monitoring - Feb 2026"`
- **Time Range**:
  - Since: `2026-02-01T00:00:00`
  - Until: `2026-02-28T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Species**: `"African Elephant"`, `"Giraffe"`, `"Zebra"`, `"Wildebeest"`, `"Hippopotamus"`, `"Hyena"`

**Result**: Individual maps for each of the 6 specified species, with all remaining species on the "Other Species" map.

## Troubleshooting

### Common Issues and Solutions

#### No data returned
**Problem**: The workflow completes but produces empty results or no sighting records.

**Solutions**:
- Verify your time range covers a period when patrols were actually conducted
- Confirm that your SMART database contains events of type "Wildlife - direct observation" within the selected date range
- Check that your SMART data source connection is working correctly in Ecoscope Desktop

#### SMART connection error
**Problem**: The workflow fails with an authentication or connection error.

**Solutions**:
- Verify your SMART data source is properly configured in Ecoscope Desktop
- Check that your SMART server is accessible from your network
- Try re-entering your SMART credentials in the data source configuration

#### Featured species maps are missing
**Problem**: Some or all featured species maps are not generated.

**Solutions**:
- Verify that the species names in your featured list match exactly what is recorded in SMART (including capitalization and spelling)
- Check whether the selected species were actually observed during the chosen time range
- If no sightings exist for a species, the workflow will skip its map

#### Report generation fails
**Problem**: The workflow fails during the "Create Wildlife Report" step.

**Solutions**:
- Ensure the template path is correct and accessible. The default template URL requires internet access
- If using a custom template, verify the file exists at the specified path
- Check that the template contains the expected Jinja2 placeholders

#### Workflow runs very slowly
**Problem**: The workflow takes a very long time to complete.

**Solutions**:
- Try a shorter date range first to verify the workflow works correctly
- Large date ranges with many events will naturally take longer to process
- Each featured species generates its own map, so reducing the species list can improve performance
- Note: The first run may be slower as the system initializes — subsequent runs are typically faster

#### Unexpected coordinate data
**Problem**: Sighting points appear in wrong locations on the maps.

**Solutions**:
- Review the bounding box settings under Advanced Configuration to ensure they cover your area of interest
- Check the "Filter Exact Point Coordinates" setting — default values exclude common GPS error coordinates like `(0, 0)` and `(180, 90)`
- If you have known bad GPS coordinates in your data, add them to the filter list
