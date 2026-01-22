# Netflix Content Analysis Report

**Generated:** 2026-01-22 21:30:06

---

## Executive Summary

This report presents a comprehensive analysis of Netflix's content catalog, covering 8,794 titles including movies and TV shows. The analysis examines content distribution, temporal trends, genre patterns, and geographic production.

---

## Key Findings

### Overall Statistics
- **Total Titles:** 8,794
- **Movies:** 6,128 (69.7%)
- **TV Shows:** 2,666 (30.3%)
- **Average Movie Duration:** 99.6 minutes
- **Average Content Age:** 11.8 years

### Content Insights
- **Top Genre:** Dramas
- **Top Producing Country:** United States
- **Multi-Country Productions:** 1,320 (15.0%)
- **Adult Content (TV-MA/R/NC-17):** 4,007 (45.6%)

---

## Analysis Components

### 1. Data Processing
- **Raw Data:** 8,794 titles loaded
- **Data Cleaning:** Handled missing values, removed duplicates
- **Feature Engineering:** Created 26 new features for analysis

### 2. Statistical Analysis
- Comprehensive statistical summaries generated
- Genre and country distribution analysis
- Temporal trend analysis (yearly, monthly, quarterly)
- Content categorization (age, duration, era)

### 3. Visualizations
- 10 professional visualizations created
- Distribution plots, time series, categorical comparisons
- Heatmaps showing temporal and categorical patterns

---

## Data Files Generated

### Processed Data
- `data/processed/netflix_cleaned.csv` - Cleaned dataset
- `data/processed/netflix_engineered.csv` - Feature-engineered dataset

### Analysis Results
- `data/processed/analysis_results/` - 16 CSV files with detailed analysis

### Visualizations
- `visualizations/` - 10 PNG visualizations (300 DPI)

---

## Methodology

### Data Pipeline
1. **Data Loading:** Raw Netflix dataset loaded and validated
2. **Data Cleaning:** Missing values handled, duplicates removed, types validated
3. **Feature Engineering:** Temporal features, categorical features, binary flags created
4. **Statistical Analysis:** Groupby aggregations, pivot tables, time series analysis
5. **Visualization:** Professional plots created with matplotlib/seaborn

### Key Features Engineered
- Duration in minutes/seasons (numeric extraction)
- Temporal features (year, month, quarter, day of week, content age)
- Binary flags (content type, length, recency, rating)
- Categorical features (age categories, duration groups, eras)
- Multi-value handling (genre counts, country counts, flags)

---

## Repository Structure
```
netflix-content-analysis/
├── data/
│   ├── raw/                    # Raw data (not tracked)
│   └── processed/              # Cleaned and engineered data
│       └── analysis_results/   # Analysis CSV files
├── src/                        # Source code modules
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── feature_engineer.py
│   ├── analyzer.py
│   └── visualizer.py
├── visualizations/             # Generated plots
├── main.py                     # Pipeline orchestration
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

---

**End of Report**
