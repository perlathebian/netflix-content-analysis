# Netflix Content Analysis

## Overview

Production-ready data analysis pipeline for Netflix movies and TV shows dataset. Demonstrates modular code architecture, feature engineering, and statistical analysis.

## Project Status

In Progress

## Tech Stack

- **Language:** Python 3
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Architecture:** Modular OOP design

## Project Structure

```
├── src/              # Source code modules
├── data/             # Raw and processed datasets
├── visualizations/   # Generated plots (PNG)
├── results/          # Analysis outputs (CSV, JSON)
└── main.py          # Entry point
```

## Modules

### `data_loader.py`

- **Purpose:** Load and validate Netflix dataset
- **Features:**
  - Comprehensive error handling (missing file, empty file, corrupt CSV)
  - Metadata extraction (file size, row count, memory usage)
  - Basic dataset overview (shape, dtypes, sample rows)
- **Key Methods:**
  - `load_data()`: Load CSV with validation
  - `get_basic_info()`: Display dataset summary

### `data_cleaner.py`

- **Purpose:** Systematic data cleaning pipeline
- **Features:**
  - Missing value analysis with statistics
  - Domain-specific missing value handling (Unknown Director, Not Rated, etc.)
  - Duplicate removal
  - Data type validation and conversion (datetime, int64)
  - Comprehensive cleaning report (before/after metrics)
- **Key Methods:**
  - `clean()`: Execute full cleaning pipeline
  - `export_cleaned_data()`: Save cleaned dataset
- **Results:**
  - Original: 8,807 rows → Cleaned: 8,794 rows (0.15% removed)
  - Handled 4,304 missing values
  - Removed 3 duplicates

### `feature_engineer.py`

- **Purpose:** Transform cleaned data into analysis-ready features
- **Features Created:** 26 engineered features
  - **Duration:** Numeric minutes/seasons extracted from text
  - **Temporal:** Year, month, quarter, day of week, content age
  - **Binary Flags:** Content type, length, recency, adult rating, genres
  - **Categorical:** Age categories, duration groups, release eras
  - **Multi-Value:** Primary genre/country, counts, co-production flags
- **Key Methods:**
  - `engineer_features()`: Execute full pipeline
  - `export_engineered_data()`: Save feature-rich dataset
- **Output:**
  - Original: 12 columns → Engineered: 38 columns
  - Ready for statistical analysis and visualization

### `analyzer.py`

- **Purpose:** Perform comprehensive statistical analysis and generate insights
- **Analysis Types:**
  - **Statistical Summary:** Overall metrics (8,794 titles, 69.72% movies, avg 98.46 min)
  - **Content Type Analysis:** Age categories, duration groups, release eras
  - **Genre/Country Analysis:** Top 10 distributions, genre counts
  - **Time Series:** Yearly, monthly, quarterly trends
  - **Advanced Groupby:** Multi-dimensional aggregations
  - **Pivot Tables:** Cross-tabulations (type × era, year × type, genre × type)
- **Key Methods:**
  - `run_full_analysis()`: Execute all analyses
  - `export_results()`: Save 16 CSV files to processed folder
- **Output:**
  - 16 analysis result files ready for visualization and reporting

### `visualizer.py`

- **Purpose:** Create quality data visualizations
- **Visualization Types:**
  - **Distribution Plots:** Movie duration (histogram + box plot), content age, genre counts
  - **Time Series:** Yearly content additions with trends, monthly seasonality
  - **Categorical Comparisons:** Top 10 genres, top 10 countries, rating-type breakdowns
  - **Heatmaps:** Year-month patterns (last 10 years), genre-type relationships
- **Styling:**
  - Professional color schemes (not default matplotlib)
  - 300 DPI resolution (print/portfolio quality)
  - Seaborn statistical styling
  - Clear labels, titles, legends
- **Key Methods:**
  - `create_all_visualizations()`: Generate all 10 plots
- **Output:**
  - 10 PNG files in `visualizations/` folder
  - Ready for GitHub display and presentations

## Features

- Modular, reusable code architecture
- Automated data cleaning pipeline
- Advanced feature engineering
- Statistical analysis with visualizations
- Export-ready results

## Usage

### Quick Start

Run the complete analysis pipeline:

```bash
# Install dependencies
pip install -r requirements.txt

# Download Netflix dataset from Kaggle and place in data/raw/netflix.csv
# Link: https://www.kaggle.com/datasets/shivamb/netflix-shows

# Run full pipeline
python main.py
```

### What Happens

The pipeline executes 6 steps:

1. **Load Data** - Validates and loads raw CSV
2. **Clean Data** - Handles missing values, removes duplicates, validates types
3. **Engineer Features** - Creates 26 analytical features
4. **Analyze Data** - Generates 16 statistical analysis files
5. **Visualize** - Creates 10 professional plots (300 DPI)
6. **Report** - Generates `ANALYSIS_REPORT.md` with findings

### Outputs

- **Processed Data:** `data/processed/netflix_cleaned.csv`, `netflix_engineered.csv`
- **Analysis Results:** `data/processed/analysis_results/` (16 CSV files)
- **Visualizations:** `visualizations/` (10 PNG files)
- **Report:** `ANALYSIS_REPORT.md`
