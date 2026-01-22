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
