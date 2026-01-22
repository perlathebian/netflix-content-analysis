"""
Feature engineering module for Netflix dataset analysis.
Creates derived features from cleaned data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re


class FeatureEngineer:
    """
    Creates new features from cleaned Netflix dataset.
    
    Attributes:
        df (pd.DataFrame): Working dataset with engineered features
        feature_summary (dict): Summary of all created features
    """
    
    def __init__(self, df):
        """
        Initialize FeatureEngineer with cleaned DataFrame.
        
        Args:
            df (pd.DataFrame): Cleaned dataset
        """
        self.df = df.copy()
        self.feature_summary = {}
    
    def extract_duration_features(self):
        """
        Extract numeric duration features from duration column.
        """
        print("\n" + "="*60)
        print("EXTRACTING DURATION FEATURES")
        print("="*60)
        
        # Initialize new columns with NaN
        self.df['duration_minutes'] = np.nan
        self.df['duration_seasons'] = np.nan
        
        # Extract minutes for movies
        movie_mask = self.df['type'] == 'Movie'
        self.df.loc[movie_mask, 'duration_minutes'] = (
            self.df.loc[movie_mask, 'duration']
            .str.extract(r'(\d+)', expand=False)
            .astype(float)
        )
        
        # Extract seasons for TV shows
        tv_mask = self.df['type'] == 'TV Show'
        self.df.loc[tv_mask, 'duration_seasons'] = (
            self.df.loc[tv_mask, 'duration']
            .str.extract(r'(\d+)', expand=False)
            .astype(float)
        )
        
        movies_processed = movie_mask.sum()
        tv_processed = tv_mask.sum()
        
        print(f"Extracted duration for {movies_processed:,} movies")
        print(f"Extracted duration for {tv_processed:,} TV shows")
        
        self.feature_summary['duration_features'] = {
            'duration_minutes': 'Numeric duration for movies',
            'duration_seasons': 'Numeric duration for TV shows'
        }
    
    def create_temporal_features(self):
        """
        Create time-based features from date_added column.
        """
        print("\n" + "="*60)
        print("CREATING TEMPORAL FEATURES")
        print("="*60)
        
        # Ensure date_added is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df['date_added']):
            self.df['date_added'] = pd.to_datetime(self.df['date_added'], errors='coerce')
        
        # Extract year, month, quarter
        self.df['year_added'] = self.df['date_added'].dt.year
        self.df['month_added'] = self.df['date_added'].dt.month
        self.df['month_name'] = self.df['date_added'].dt.month_name()
        self.df['quarter_added'] = self.df['date_added'].dt.quarter
        self.df['day_of_week'] = self.df['date_added'].dt.day_name()
        
        # Content age (current year - release year)
        current_year = pd.Timestamp.now().year
        self.df['content_age'] = current_year - self.df['release_year']
        
        print(f"Created temporal features: year, month, quarter, day_of_week")
        print(f"Calculated content age (current year: {current_year})")
        
        self.feature_summary['temporal_features'] = {
            'year_added': 'Year content was added to Netflix',
            'month_added': 'Month number (1-12)',
            'month_name': 'Month name (January, February, etc.)',
            'quarter_added': 'Quarter (1-4)',
            'day_of_week': 'Day of week content was added',
            'content_age': 'Age of content (current year - release year)'
        }
    
    def create_binary_flags(self):
        """
        Create binary flag features for key content attributes.
        """
        print("\n" + "="*60)
        print("CREATING BINARY FLAGS")
        print("="*60)
        
        # Content type flags
        self.df['is_movie'] = (self.df['type'] == 'Movie').astype(int)
        self.df['is_tv_show'] = (self.df['type'] == 'TV Show').astype(int)
        
        # Long content flag (movies >120 min, TV shows >3 seasons)
        self.df['is_long_content'] = (
            ((self.df['is_movie'] == 1) & (self.df['duration_minutes'] > 120)) |
            ((self.df['is_tv_show'] == 1) & (self.df['duration_seasons'] > 3))
        ).astype(int)
        
        # Recent content flag (added in last 3 years)
        current_year = pd.Timestamp.now().year
        self.df['is_recent_addition'] = (
            self.df['year_added'] >= (current_year - 3)
        ).astype(int)
        
        # Adult content flag
        adult_ratings = ['TV-MA', 'R', 'NC-17']
        self.df['is_adult_content'] = (
            self.df['rating'].isin(adult_ratings)
        ).astype(int)
        
        print(f"Created binary flags:")
        print(f"   - Content type: is_movie, is_tv_show")
        print(f"   - Long content: is_long_content")
        print(f"   - Recent additions: is_recent_addition")
        print(f"   - Adult content: is_adult_content")
        
        self.feature_summary['binary_flags'] = {
            'is_movie': 'Binary flag for movies (1=Movie, 0=TV Show)',
            'is_tv_show': 'Binary flag for TV shows',
            'is_long_content': 'Movies >120 min or TV shows >3 seasons',
            'is_recent_addition': 'Content added in last 3 years',
            'is_adult_content': 'Rated TV-MA, R, or NC-17'
        }
    
    def create_categorical_features(self):
        """
        Create categorical groupings from numeric features.
        """
        print("\n" + "="*60)
        print("CREATING CATEGORICAL FEATURES")
        print("="*60)
        
        # Content age categories
        self.df['content_age_category'] = pd.cut(
            self.df['content_age'],
            bins=[0, 2, 5, 100],
            labels=['New', 'Recent', 'Catalog'],
            include_lowest=True
        )
        
        # Duration categories for movies only
        movie_mask = self.df['is_movie'] == 1
        self.df.loc[movie_mask, 'duration_category'] = pd.cut(
            self.df.loc[movie_mask, 'duration_minutes'],
            bins=[0, 90, 120, 300],
            labels=['Short', 'Medium', 'Long'],
            include_lowest=True
        )
        
        # Release era categories
        self.df['release_era'] = pd.cut(
            self.df['release_year'],
            bins=[1900, 1980, 2000, 2010, 2030],
            labels=['Classic', 'Retro', 'Modern', 'Contemporary'],
            include_lowest=True
        )
        
        print(f"Created categorical features:")
        print(f"   - Content age: New, Recent, Catalog")
        print(f"   - Duration: Short, Medium, Long (movies only)")
        print(f"   - Release era: Classic, Retro, Modern, Contemporary")
        
        self.feature_summary['categorical_features'] = {
            'content_age_category': 'New (0-2 yrs), Recent (3-5 yrs), Catalog (6+ yrs)',
            'duration_category': 'Short (<90 min), Medium (90-120), Long (>120) - movies only',
            'release_era': 'Classic (<1980), Retro (1980-2000), Modern (2000-2010), Contemporary (2010+)'
        }
    
    def handle_multi_value_fields(self):
        """
        Extract features from multi-value fields (genres, countries).
        """
        print("\n" + "="*60)
        print("HANDLING MULTI-VALUE FIELDS")
        print("="*60)
        
        # Extract primary genre (the onw that was listed first)
        self.df['primary_genre'] = (
            self.df['listed_in']
            .str.split(',')
            .str[0]
            .str.strip()
        )
        
        # Count number of genres
        self.df['genre_count'] = (
            self.df['listed_in']
            .str.split(',')
            .str.len()
        )
        
        # Extract primary country(also one that was present first)
        self.df['primary_country'] = (
            self.df['country']
            .str.split(',')
            .str[0]
            .str.strip()
        )
        
        # Count number of countries (indicates international co-production)
        self.df['country_count'] = (
            self.df['country']
            .str.split(',')
            .str.len()
        )
        
        # Multi-country production flag
        self.df['is_multi_country'] = (
            self.df['country_count'] > 1
        ).astype(int)
        
        # Check for specific popular genres (binary flags)
        self.df['is_drama'] = (
            self.df['listed_in'].str.contains('Drama', case=False, na=False)
        ).astype(int)
        
        self.df['is_comedy'] = (
            self.df['listed_in'].str.contains('Comed', case=False, na=False)
        ).astype(int)
        
        self.df['is_documentary'] = (
            self.df['listed_in'].str.contains('Documentar', case=False, na=False)
        ).astype(int)
        
        self.df['is_international'] = (
            self.df['listed_in'].str.contains('International', case=False, na=False)
        ).astype(int)
        
        # Check for US content
        self.df['is_us_content'] = (
            self.df['country'].str.contains('United States', case=False, na=False)
        ).astype(int)
        
        print(f"Extracted multi-value features:")
        print(f"   - Primary genre and country")
        print(f"   - Genre count and country count")
        print(f"   - Genre flags: drama, comedy, documentary, international")
        print(f"   - Country flags: US content, multi-country")
        
        self.feature_summary['multi_value_features'] = {
            'primary_genre': 'First listed genre',
            'genre_count': 'Number of genres listed',
            'primary_country': 'First listed country',
            'country_count': 'Number of countries (co-production indicator)',
            'is_multi_country': 'Multiple countries involved',
            'is_drama': 'Contains Drama genre',
            'is_comedy': 'Contains Comedy genre',
            'is_documentary': 'Contains Documentary genre',
            'is_international': 'Contains International designation',
            'is_us_content': 'Produced in/with United States'
        }
    
    def engineer_features(self):
        """
        Execute full feature engineering pipeline.
        
        Returns:
            pd.DataFrame: Dataset with engineered features
        """
        print("\nStarting Feature Engineering Pipeline...")
        
        self.extract_duration_features()
        self.create_temporal_features()
        self.create_binary_flags()
        self.create_categorical_features()
        self.handle_multi_value_fields()
        
        self.print_feature_summary()
        
        print("\nFeature engineering complete!")
        print(f"   Total features created: {len(self.get_engineered_features())}")
        
        return self.df
    
    def get_engineered_features(self):
        """
        Get list of all engineered feature names.
        
        Returns:
            list: Feature names
        """
        engineered_cols = [
            'duration_minutes', 'duration_seasons',
            'year_added', 'month_added', 'month_name', 'quarter_added', 'day_of_week', 'content_age',
            'is_movie', 'is_tv_show', 'is_long_content', 'is_recent_addition', 'is_adult_content',
            'content_age_category', 'duration_category', 'release_era',
            'primary_genre', 'genre_count', 'primary_country', 'country_count', 'is_multi_country',
            'is_drama', 'is_comedy', 'is_documentary', 'is_international', 'is_us_content'
        ]
        return engineered_cols
    
    def print_feature_summary(self):
        """
        Print summary of all engineered features.
        """
        print("\n" + "="*60)
        print("FEATURE ENGINEERING SUMMARY")
        print("="*60)
        
        for category, features in self.feature_summary.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for feature, description in features.items():
                print(f"  • {feature}: {description}")
    
    def export_engineered_data(self, output_path):
        """
        Export dataset with engineered features.
        
        Args:
            output_path (str): Path to save data
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.df.to_csv(output_path, index=False)
        print(f"\nEngineered data exported to: {output_path}")


if __name__ == "__main__":
    # Testing the FeatureEngineer
    from data_loader import DataLoader
    from data_cleaner import DataCleaner
    
    # Loading and cleaning data
    loader = DataLoader("data/raw/netflix.csv")
    df = loader.load_data()
    
    cleaner = DataCleaner(df)
    df_cleaned = cleaner.clean()
    
    # Engineering features
    engineer = FeatureEngineer(df_cleaned)
    df_engineered = engineer.engineer_features()
    
    # Exporting engineered data
    engineer.export_engineered_data("data/processed/netflix_engineered.csv")