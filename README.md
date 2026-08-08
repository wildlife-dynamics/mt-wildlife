# Mara Triangle Wildlife Sightings Workflow

## Introduction

This workflow helps you analyze wildlife sighting data collected by field rangers in the Mara Triangle conservancy. It pulls wildlife sighting events from **EarthRanger**, processes them into species-level summaries, and produces maps and a formatted Word report.

**What this workflow does:**
- Downloads "Wildlife sightings" events from **EarthRanger**
- Extracts species and individual counts from each event's details
- Summarizes sighting and individual counts per species
- Creates interactive maps for each featured species, plus a combined map for all other species
- Generates a Word document report containing the summary table and maps
- Exports raw sighting data in CSV and/or Parquet format

**Who should use this:**
- Conservation managers monitoring wildlife populations in the Mara Triangle
- Researchers analyzing species distribution and abundance from ranger observations
- Anyone needing to produce periodic wildlife sighting reports from EarthRanger data

## Prerequisites

Before using this workflow, you need:

1. **Ecoscope Desktop** installed on your computer
   - If you haven't installed it yet, please follow the installation instructions for Ecoscope Desktop

2. **EarthRanger Data Source** configured in Ecoscope Desktop
   - You must have already set up a connection to your EarthRanger site (e.g. `mmnr.pamdas.org`)
   - Your data source should be configured with proper authentication credentials
   - You'll need to know the name of your configured EarthRanger data source

3. **Wildlife sighting data in EarthRanger**
   - Your EarthRanger site should contain events of type **Wildlife sightings** (`wildlife_sightings`)
   - Events should include the **Species** and **Count** detail fields
   - Only events with a recorded location are included in the analysis

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
  - Example: `2026-07-01T00:00:00`
- **Until** (required): The end date and time
  - Example: `2026-07-31T23:59:59`
- **Timezone** (optional): Your local timezone for displaying times
  - Example: `Africa/Nairobi (UTC+03:00)`
  - Note: If left blank, times will be displayed in UTC

#### 3. Data Source
Select which EarthRanger connection to use for downloading events.

- **Data Source** (required): Select one of your configured EarthRanger data sources
  - Note: This must match an EarthRanger connection you have already set up in Ecoscope Desktop (e.g. `mmnr`)

#### 4. Process Sightings
Configure how wildlife sighting records are processed.

- **Species** (required): The list of featured species to track individually. Each featured species will get its own map. All other species observed will be grouped into a single "Other Species" map.
  - Default list: `"Buffalo"`, `"Elephant"`, `"Lion"`, `"Leopard"`, `"Cheetah (inform Monitoring Team)"`, `"Giraffe - Maasai"`, `"Zebra"`, `"Wildebeest"`
  - You can add or remove species from this list based on your monitoring priorities
  - Important: Species names must match the display titles used in your EarthRanger event form **exactly**, including punctuation — e.g. `"Giraffe - Maasai"`, not `"Giraffe"`

#### 5. Base Maps
Select tile layers to use as base layers in map outputs.

- **Base Maps**: Choose from preset map styles or add a custom tile layer
  - Options: **Open Street Map**, **Roadmap**, **Satellite**, **Terrain**, **LandDx**, **USGS Hillshade**, or **Custom Layer**
  - Default: Terrain
  - Note: The first layer in the list will be the bottommost layer displayed. You can add multiple layers.

#### 6. Persist Sightings Data
Choose the output format for your raw sighting data export.

- **Filetypes** (optional): The output format(s) for the exported data
  - Options: **CSV**, **Parquet**
  - Default: `parquet`
  - Note: You can select one or both formats

#### 7. Create Wildlife Report
Configure the Word document report generation.

- **Template Path** (required): Path or URL to the Word template (.docx) file
  - Default: A pre-configured template hosted on GitHub
  - Note: You generally do not need to change this unless you have a custom report template

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
     - Number of wildlife sighting events in the system
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
  - `id`: Unique identifier for the EarthRanger event
  - `serial_number`: The event's serial number in EarthRanger
  - `time`: Date and time of the sighting (converted to your selected timezone)
  - `geometry`: Geographic point location
  - `Species`: Name of the species observed
  - `Count`: Number of individuals observed

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
**Goal**: Generate a standard monthly wildlife report for July 2026

**Configuration**:
- **Workflow Name**: `"Mara Triangle Wildlife Sightings"`
- **Time Range**:
  - Since: `2026-07-01T00:00:00`
  - Until: `2026-07-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Species**: Use the default list (Buffalo, Elephant, Lion, Leopard, Cheetah (inform Monitoring Team), Giraffe - Maasai, Zebra, Wildebeest)
- **Filetypes**: `parquet`

**Result**: A Word report with summary table and maps for each of the 8 featured species, plus one map for all other species observed.

---

### Example 2: Big Cat Focus
**Goal**: Produce a report focused specifically on big cat species

**Configuration**:
- **Workflow Name**: `"Big Cat Sightings - Q3 2026"`
- **Time Range**:
  - Since: `2026-07-01T00:00:00`
  - Until: `2026-09-30T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Species**: `"Lion"`, `"Leopard"`, `"Cheetah (inform Monitoring Team)"`
- **Filetypes**: `csv` and `parquet`

**Result**: Individual maps for Lion, Leopard, and Cheetah. All other species appear on the combined "Other Species" map. Both CSV and Parquet data exports are produced.

---

### Example 3: Full Year Analysis with CSV Export
**Goal**: Export a full year of sighting data for external analysis in Excel

**Configuration**:
- **Workflow Name**: `"Annual Wildlife Sightings 2026"`
- **Time Range**:
  - Since: `2026-01-01T00:00:00`
  - Until: `2026-12-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Species**: Use the default list
- **Filetypes**: `csv`

**Result**: A CSV file you can open in Excel with every sighting record, plus the summary table and Word report.

---

### Example 4: Custom Species List
**Goal**: Track specific species of interest beyond the default list

**Configuration**:
- **Workflow Name**: `"Expanded Species Monitoring - Aug 2026"`
- **Time Range**:
  - Since: `2026-08-01T00:00:00`
  - Until: `2026-08-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Species**: `"Elephant"`, `"Giraffe - Maasai"`, `"Zebra"`, `"Wildebeest"`, `"Hippo"`, `"Hyena - Spotted"`

**Result**: Individual maps for each of the 6 specified species, with all remaining species on the "Other Species" map.

## Troubleshooting

### Common Issues and Solutions

#### No data returned
**Problem**: The workflow completes but produces empty results or no sighting records.

**Solutions**:
- Verify your time range covers a period when sightings were actually recorded
- Confirm that your EarthRanger site contains events of type "Wildlife sightings" (`wildlife_sightings`) within the selected date range
- Check that your EarthRanger data source connection is working correctly in Ecoscope Desktop
- Note: Events without a recorded location are excluded from the analysis

#### EarthRanger connection error
**Problem**: The workflow fails with an authentication or connection error.

**Solutions**:
- Verify your EarthRanger data source is properly configured in Ecoscope Desktop
- Check that your EarthRanger server is accessible from your network
- Try re-entering your EarthRanger credentials in the data source configuration

#### Featured species maps are missing
**Problem**: Some or all featured species maps are not generated.

**Solutions**:
- Verify that the species names in your featured list match the display titles in your EarthRanger event form **exactly** (including capitalization and punctuation — e.g. `"Cheetah (inform Monitoring Team)"`, `"Giraffe - Maasai"`)
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
