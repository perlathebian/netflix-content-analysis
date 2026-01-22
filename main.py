"""
Main pipeline for Netflix content analysis.
Orchestrates all modules to run complete analysis workflow.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer
from src.analyzer import Analyzer
from src.visualizer import Visualizer


class NetflixAnalysisPipeline:
    """
    Complete analysis pipeline for Netflix dataset.
    
    Coordinates all analysis modules from data loading to visualization.
    """
    
    def __init__(self, data_path="data/raw/netflix.csv"):
        """
        Initialize pipeline with data path.
        
        Args:
            data_path (str): Path to raw Netflix data
        """
        self.data_path = data_path
        self.results = {}
        self.start_time = None
        self.end_time = None
    
    def run(self):
        """
        Execute complete analysis pipeline.
        
        Returns:
            dict: Results from all analysis steps
        """
        self.start_time = datetime.now()
        
        print("="*70)
        print("NETFLIX CONTENT ANALYSIS PIPELINE")
        print("="*70)
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        try:
            # Step 1: Load Data
            print("\n" + "─"*70)
            print("STEP 1: LOADING DATA")
            print("─"*70)
            loader = DataLoader(self.data_path)
            df_raw = loader.load_data()
            loader.get_basic_info()
            self.results['raw_data'] = df_raw
            
            # Step 2: Clean Data
            print("\n" + "─"*70)
            print("STEP 2: CLEANING DATA")
            print("─"*70)
            cleaner = DataCleaner(df_raw)
            df_cleaned = cleaner.clean()
            cleaner.export_cleaned_data("data/processed/netflix_cleaned.csv")
            self.results['cleaned_data'] = df_cleaned
            
            # Step 3: Engineer Features
            print("\n" + "─"*70)
            print("STEP 3: ENGINEERING FEATURES")
            print("─"*70)
            engineer = FeatureEngineer(df_cleaned)
            df_engineered = engineer.engineer_features()
            engineer.export_engineered_data("data/processed/netflix_engineered.csv")
            self.results['engineered_data'] = df_engineered
            
            # Step 4: Analyze Data
            print("\n" + "─"*70)
            print("STEP 4: ANALYZING DATA")
            print("─"*70)
            analyzer = Analyzer(df_engineered)
            analysis_results = analyzer.run_full_analysis()
            analyzer.export_results("data/processed/analysis_results")
            self.results['analysis'] = analysis_results
            
            # Step 5: Create Visualizations
            print("\n" + "─"*70)
            print("STEP 5: CREATING VISUALIZATIONS")
            print("─"*70)
            visualizer = Visualizer(df_engineered, output_dir="visualizations")
            figures = visualizer.create_all_visualizations()
            self.results['visualizations'] = figures
            
            # Step 6: Generate Summary Report
            print("\n" + "─"*70)
            print("STEP 6: GENERATING SUMMARY REPORT")
            print("─"*70)
            self.generate_summary_report()
            
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            
            print("\n" + "="*70)
            print("PIPELINE COMPLETED SUCCESSFULLY")
            print("="*70)
            print(f"Completed at: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Total duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
            print("="*70)
            
            return self.results
            
        except FileNotFoundError as e:
            print(f"\nERROR: Data file not found - {e}")
            print(f"Please ensure the Netflix dataset is at: {self.data_path}")
            sys.exit(1)
            
        except Exception as e:
            print(f"\nPIPELINE ERROR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def generate_summary_report(self):
        """
        Generate a comprehensive summary report of the analysis.
        """
        report_path = Path("ANALYSIS_REPORT.md")
        
        df = self.results['engineered_data']
        
        # Calculate key metrics
        total_titles = len(df)
        total_movies = df['is_movie'].sum()
        total_tv_shows = df['is_tv_show'].sum()
        avg_movie_duration = df[df['is_movie'] == 1]['duration_minutes'].mean()
        avg_content_age = df['content_age'].mean()
        
        top_genre = df['primary_genre'].value_counts().index[0]
        top_country = df['primary_country'].value_counts().index[0]
        
        # Create report content
        report = f"""# Netflix Content Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report presents a comprehensive analysis of Netflix's content catalog, covering {total_titles:,} titles including movies and TV shows. The analysis examines content distribution, temporal trends, genre patterns, and geographic production.

---

## Key Findings

### Overall Statistics
- **Total Titles:** {total_titles:,}
- **Movies:** {total_movies:,} ({total_movies/total_titles*100:.1f}%)
- **TV Shows:** {total_tv_shows:,} ({total_tv_shows/total_titles*100:.1f}%)
- **Average Movie Duration:** {avg_movie_duration:.1f} minutes
- **Average Content Age:** {avg_content_age:.1f} years

### Content Insights
- **Top Genre:** {top_genre}
- **Top Producing Country:** {top_country}
- **Multi-Country Productions:** {df['is_multi_country'].sum():,} ({df['is_multi_country'].sum()/total_titles*100:.1f}%)
- **Adult Content (TV-MA/R/NC-17):** {df['is_adult_content'].sum():,} ({df['is_adult_content'].sum()/total_titles*100:.1f}%)

---

## Analysis Components

### 1. Data Processing
- **Raw Data:** {total_titles:,} titles loaded
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
"""
        
        # Write report to file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Summary report generated: {report_path}")
    
    def print_key_insights(self):
        """
        Print key insights to console for quick reference.
        """
        df = self.results['engineered_data']
        
        print("\n" + "="*70)
        print("KEY INSIGHTS")
        print("="*70)
        
        # Insight 1: Content Growth
        yearly_counts = df.groupby('year_added').size()
        recent_growth = ((yearly_counts.iloc[-1] - yearly_counts.iloc[-5]) / yearly_counts.iloc[-5] * 100)
        print(f"\nContent Growth:")
        print(f"   • 5-year growth rate: {recent_growth:.1f}%")
        
        # Insight 2: Movie vs TV Show ratio
        movie_pct = (df['is_movie'].sum() / len(df) * 100)
        print(f"\nContent Mix:")
        print(f"   • Movies: {movie_pct:.1f}%")
        print(f"   • TV Shows: {100-movie_pct:.1f}%")
        
        # Insight 3: Duration insights
        avg_duration = df[df['is_movie'] == 1]['duration_minutes'].mean()
        median_duration = df[df['is_movie'] == 1]['duration_minutes'].median()
        print(f"\nMovie Duration:")
        print(f"   • Average: {avg_duration:.1f} minutes")
        print(f"   • Median: {median_duration:.1f} minutes")
        
        # Insight 4: Top genres
        top_3_genres = df['primary_genre'].value_counts().head(3)
        print(f"\nTop 3 Genres:")
        for genre, count in top_3_genres.items():
            pct = (count / len(df) * 100)
            print(f"   • {genre}: {count:,} titles ({pct:.1f}%)")
        
        # Insight 5: International content
        multi_country_pct = (df['is_multi_country'].sum() / len(df) * 100)
        print(f"\nInternational Collaboration:")
        print(f"   • Multi-country productions: {multi_country_pct:.1f}%")
        
        # Insight 6: Content freshness
        new_content = df[df['content_age_category'] == 'New'].shape[0]
        new_pct = (new_content / len(df) * 100)
        print(f"\nContent Freshness:")
        print(f"   • New content (0-2 years): {new_content:,} titles ({new_pct:.1f}%)")
        
        print("="*70)


def main():
    """
    Main entry point for the analysis pipeline.
    """
    pipeline = NetflixAnalysisPipeline(data_path="data/raw/netflix.csv")
    results = pipeline.run()
    pipeline.print_key_insights()


if __name__ == "__main__":
    main()