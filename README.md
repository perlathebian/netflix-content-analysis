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

## Features

- Modular, reusable code architecture
- Automated data cleaning pipeline
- Advanced feature engineering
- Statistical analysis with visualizations
- Export-ready results

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run full analysis
python main.py
```

---

_Enterprise-level data analysis demonstrating software engineering best practices_
