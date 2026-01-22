"""
Analysis module for Netflix dataset.
Performs statistical analysis and generates insights.
"""

import pandas as pd
import numpy as np
from pathlib import Path


class Analyzer:
    """
    Performs comprehensive analysis on Netflix dataset.
    
    Attributes:
        df (pd.DataFrame): Dataset with engineered features
        results (dict): Dictionary storing all analysis results
    """
    
    def __init__(self, df):
        """
        Initialize Analyzer with engineered dataset.
        
        Args:
            df (pd.DataFrame): Dataset with engineered features
        """
        self.df = df.copy()
        self.results = {}
    
    def generate_statistical_summary(self):
        """
        Generate comprehensive statistical summary.
        
        Returns:
            pd.DataFrame: Summary statistics
        """
        print("\n" + "="*60)
        print("GENERATING STATISTICAL SUMMARY")
        print("="*60)
        
        summary_stats = {}
        
        # Total counts
        summary_stats['Total Titles'] = len(self.df)
        summary_stats['Total Movies'] = self.df['is_movie'].sum()
        summary_stats['Total TV Shows'] = self.df['is_tv_show'].sum()
        
        # Percentages
        summary_stats['% Movies'] = (self.df['is_movie'].sum() / len(self.df) * 100).round(2)
        summary_stats['% TV Shows'] = (self.df['is_tv_show'].sum() / len(self.df) * 100).round(2)
        
        # Average durations
        summary_stats['Avg Movie Duration (min)'] = self.df['duration_minutes'].mean().round(2)
        summary_stats['Avg TV Show Seasons'] = self.df['duration_seasons'].mean().round(2)
        
        # Content age statistics
        summary_stats['Avg Content Age (years)'] = self.df['content_age'].mean().round(2)
        summary_stats['Newest Content (years)'] = self.df['content_age'].min()
        summary_stats['Oldest Content (years)'] = self.df['content_age'].max()
        
        # Rating distribution
        summary_stats['Adult Content Count'] = self.df['is_adult_content'].sum()
        summary_stats['% Adult Content'] = (self.df['is_adult_content'].sum() / len(self.df) * 100).round(2)
        
        # International content
        summary_stats['Multi-Country Productions'] = self.df['is_multi_country'].sum()
        summary_stats['% Multi-Country'] = (self.df['is_multi_country'].sum() / len(self.df) * 100).round(2)
        
        # Genre statistics
        summary_stats['Avg Genres per Title'] = self.df['genre_count'].mean().round(2)
        summary_stats['Max Genres'] = self.df['genre_count'].max()
        
        # Convert to DataFrame for better display
        summary_df = pd.DataFrame(list(summary_stats.items()), columns=['Metric', 'Value'])
        
        print("\n" + summary_df.to_string(index=False))
        
        self.results['statistical_summary'] = summary_df
        return summary_df
    
    def analyze_content_types(self):
        """
        Analyze content breakdown by type, duration, and age.
        
        Returns:
            dict: Dictionary of analysis DataFrames
        """
        print("\n" + "="*60)
        print("ANALYZING CONTENT TYPES")
        print("="*60)
        
        results = {}
        
        # Content age category distribution
        age_dist = self.df['content_age_category'].value_counts().reset_index()
        age_dist.columns = ['Age Category', 'Count']
        age_dist['Percentage'] = (age_dist['Count'] / age_dist['Count'].sum() * 100).round(2)
        age_dist = age_dist.sort_values('Count', ascending=False)
        
        results['content_age_distribution'] = age_dist
        print("\nContent Age Distribution:")
        print(age_dist.to_string(index=False))
        
        # Duration categories (movies only)
        duration_dist = self.df[self.df['is_movie'] == 1]['duration_category'].value_counts().reset_index()
        duration_dist.columns = ['Duration Category', 'Count']
        duration_dist['Percentage'] = (duration_dist['Count'] / duration_dist['Count'].sum() * 100).round(2)
        
        results['movie_duration_distribution'] = duration_dist
        print("\nMovie Duration Distribution:")
        print(duration_dist.to_string(index=False))
        
        # Release era distribution
        era_dist = self.df['release_era'].value_counts().reset_index()
        era_dist.columns = ['Release Era', 'Count']
        era_dist['Percentage'] = (era_dist['Count'] / era_dist['Count'].sum() * 100).round(2)
        
        results['release_era_distribution'] = era_dist
        print("\nRelease Era Distribution:")
        print(era_dist.to_string(index=False))
        
        self.results['content_type_analysis'] = results
        return results
    
    def analyze_genres_and_countries(self):
        """
        Analyze genre and country distributions.
        
        Returns:
            dict: Dictionary of analysis DataFrames
        """
        print("\n" + "="*60)
        print("ANALYZING GENRES AND COUNTRIES")
        print("="*60)
        
        results = {}
        
        # Top 10 genres
        top_genres = self.df['primary_genre'].value_counts().head(10).reset_index()
        top_genres.columns = ['Genre', 'Count']
        top_genres['Percentage'] = (top_genres['Count'] / len(self.df) * 100).round(2)
        
        results['top_genres'] = top_genres
        print("\nTop 10 Genres:")
        print(top_genres.to_string(index=False))
        
        # Top 10 countries
        top_countries = self.df['primary_country'].value_counts().head(10).reset_index()
        top_countries.columns = ['Country', 'Count']
        top_countries['Percentage'] = (top_countries['Count'] / len(self.df) * 100).round(2)
        
        results['top_countries'] = top_countries
        print("\nTop 10 Countries:")
        print(top_countries.to_string(index=False))
        
        # Genre count analysis
        genre_count_dist = self.df['genre_count'].value_counts().sort_index().reset_index()
        genre_count_dist.columns = ['Number of Genres', 'Count']
        genre_count_dist['Percentage'] = (genre_count_dist['Count'] / genre_count_dist['Count'].sum() * 100).round(2)
        
        results['genre_count_distribution'] = genre_count_dist
        print("\nGenre Count Distribution:")
        print(genre_count_dist.to_string(index=False))
        
        self.results['genre_country_analysis'] = results
        return results
    
    def perform_time_series_analysis(self):
        """
        Analyze content addition trends over time.
        
        Returns:
            dict: Dictionary of time series DataFrames
        """
        print("\n" + "="*60)
        print("PERFORMING TIME SERIES ANALYSIS")
        print("="*60)
        
        results = {}
        
        # Content added per year
        yearly_additions = self.df.groupby('year_added').agg({
            'show_id': 'count',
            'is_movie': 'sum',
            'is_tv_show': 'sum'
        }).reset_index()
        yearly_additions.columns = ['Year', 'Total Titles', 'Movies', 'TV Shows']
        yearly_additions = yearly_additions.sort_values('Year')
        
        results['yearly_additions'] = yearly_additions
        print("\nContent Added Per Year:")
        print(yearly_additions.to_string(index=False))
        
        # Content added per month (across all years)
        monthly_additions = self.df.groupby('month_name').size().reset_index(name='Count')
        
        # Reorder months chronologically
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly_additions['month_name'] = pd.Categorical(monthly_additions['month_name'], 
                                                          categories=month_order, 
                                                          ordered=True)
        monthly_additions = monthly_additions.sort_values('month_name')
        
        results['monthly_additions'] = monthly_additions
        print("\nContent Added Per Month (All Years Combined):")
        print(monthly_additions.to_string(index=False))
        
        # Quarterly trends
        quarterly_additions = self.df.groupby('quarter_added').agg({
            'show_id': 'count',
            'is_movie': 'sum',
            'is_tv_show': 'sum'
        }).reset_index()
        quarterly_additions.columns = ['Quarter', 'Total Titles', 'Movies', 'TV Shows']
        
        results['quarterly_additions'] = quarterly_additions
        print("\nContent Added Per Quarter:")
        print(quarterly_additions.to_string(index=False))
        
        self.results['time_series_analysis'] = results
        return results
    
    def perform_advanced_groupby(self):
        """
        Perform advanced multi-dimensional groupby analysis.
        
        Returns:
            dict: Dictionary of groupby analysis DataFrames
        """
        print("\n" + "="*60)
        print("PERFORMING ADVANCED GROUPBY ANALYSIS")
        print("="*60)
        
        results = {}
        
        # Average duration by genre (top 10 genres, movies only)
        top_10_genres = self.df['primary_genre'].value_counts().head(10).index.tolist()
        movie_genre_duration = self.df[
            (self.df['is_movie'] == 1) & 
            (self.df['primary_genre'].isin(top_10_genres))
        ].groupby('primary_genre')['duration_minutes'].agg(['mean', 'median', 'min', 'max', 'count']).reset_index()
        
        movie_genre_duration.columns = ['Genre', 'Avg Duration', 'Median Duration', 'Min', 'Max', 'Count']
        movie_genre_duration = movie_genre_duration.round(2)
        movie_genre_duration = movie_genre_duration.sort_values('Avg Duration', ascending=False)
        
        results['genre_duration_analysis'] = movie_genre_duration
        print("\nAverage Movie Duration by Genre (Top 10 Genres):")
        print(movie_genre_duration.to_string(index=False))
        
        # Content by country and type (top 10 countries)
        top_10_countries = self.df['primary_country'].value_counts().head(10).index.tolist()
        country_type = self.df[self.df['primary_country'].isin(top_10_countries)].groupby(
            ['primary_country', 'type']
        ).size().reset_index(name='Count')
        
        results['country_type_breakdown'] = country_type
        print("\nContent Breakdown by Country and Type (Top 10 Countries):")
        print(country_type.to_string(index=False))
        
        # Rating distribution by content type
        rating_type = self.df.groupby(['rating', 'type']).size().reset_index(name='Count')
        rating_type = rating_type.sort_values('Count', ascending=False)
        
        results['rating_type_distribution'] = rating_type
        print("\nRating Distribution by Content Type:")
        print(rating_type.head(15).to_string(index=False))
        
        self.results['advanced_groupby'] = results
        return results
    
    def create_pivot_tables(self):
        """
        Create pivot tables for cross-tabulation analysis.
        
        Returns:
            dict: Dictionary of pivot tables
        """
        print("\n" + "="*60)
        print("CREATING PIVOT TABLES")
        print("="*60)
        
        results = {}
        
        # Content type by release era
        type_era_pivot = pd.pivot_table(
            self.df,
            values='show_id',
            index='release_era',
            columns='type',
            aggfunc='count',
            fill_value=0
        )
        
        results['type_by_era'] = type_era_pivot
        print("\nContent Type by Release Era:")
        print(type_era_pivot)
        
        # Content additions by year and type (last 10 years)
        recent_years = sorted(self.df['year_added'].dropna().unique())[-10:]
        recent_df = self.df[self.df['year_added'].isin(recent_years)]
        
        year_type_pivot = pd.pivot_table(
            recent_df,
            values='show_id',
            index='year_added',
            columns='type',
            aggfunc='count',
            fill_value=0
        )
        
        results['year_by_type'] = year_type_pivot
        print("\nContent Additions by Year and Type (Last 10 Years):")
        print(year_type_pivot)
        
        # Top genres by content type
        top_5_genres = self.df['primary_genre'].value_counts().head(5).index.tolist()
        genre_df = self.df[self.df['primary_genre'].isin(top_5_genres)]
        
        genre_type_pivot = pd.pivot_table(
            genre_df,
            values='show_id',
            index='primary_genre',
            columns='type',
            aggfunc='count',
            fill_value=0
        )
        
        results['genre_by_type'] = genre_type_pivot
        print("\nTop Genres by Content Type:")
        print(genre_type_pivot)
        
        self.results['pivot_tables'] = results
        return results
    
    def run_full_analysis(self):
        """
        Execute complete analysis pipeline.
        
        Returns:
            dict: All analysis results
        """
        print("\nStarting Comprehensive Analysis...")
        
        self.generate_statistical_summary()
        self.analyze_content_types()
        self.analyze_genres_and_countries()
        self.perform_time_series_analysis()
        self.perform_advanced_groupby()
        self.create_pivot_tables()
        
        print("\nAnalysis complete!")
        print(f"   Total analysis components: {len(self.results)}")
        
        return self.results
    
    def export_results(self, output_dir="data/processed/analysis_results"):
        """
        Export all analysis results to CSV files.
        
        Args:
            output_dir (str): Directory to save results
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\nExporting analysis results to {output_dir}...")
        
        files_created = []
        
        # Export each result
        for analysis_name, result in self.results.items():
            if isinstance(result, pd.DataFrame):
                # Single DataFrame
                filename = f"{analysis_name}.csv"
                filepath = output_path / filename
                result.to_csv(filepath, index=False)
                files_created.append(filename)
            elif isinstance(result, dict):
                # Dictionary of DataFrames
                for sub_name, sub_df in result.items():
                    if isinstance(sub_df, pd.DataFrame):
                        filename = f"{analysis_name}_{sub_name}.csv"
                        filepath = output_path / filename
                        sub_df.to_csv(filepath, index=False)
                        files_created.append(filename)
        
        print(f"Exported {len(files_created)} analysis files:")
        for file in files_created:
            print(f"   • {file}")


if __name__ == "__main__":
    # Testing the Analyzer
    from data_loader import DataLoader
    from data_cleaner import DataCleaner
    from feature_engineer import FeatureEngineer
    
    # Loading, cleaning, and engineering features
    loader = DataLoader("data/raw/netflix.csv")
    df = loader.load_data()
    
    cleaner = DataCleaner(df)
    df_cleaned = cleaner.clean()
    
    engineer = FeatureEngineer(df_cleaned)
    df_engineered = engineer.engineer_features()
    
    # Running analysis
    analyzer = Analyzer(df_engineered)
    results = analyzer.run_full_analysis()
    
    # Exporting results
    analyzer.export_results()