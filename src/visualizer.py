"""
Visualization module for Netflix dataset analysis.
Creates professional data visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class Visualizer:
    """
    Creates comprehensive visualizations for Netflix dataset analysis.
    
    Attributes:
        df (pd.DataFrame): Dataset with engineered features
        output_dir (Path): Directory to save visualizations
        figures (dict): Dictionary storing all created figures
    """
    
    def __init__(self, df, output_dir="visualizations"):
        """
        Initialize Visualizer with dataset.
        
        Args:
            df (pd.DataFrame): Dataset with engineered features
            output_dir (str): Directory to save plots
        """
        self.df = df.copy()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.figures = {}
        
        # Set style for all plots
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
    
    def create_distribution_plots(self):
        """
        Create distribution plots for key numeric features.
        """
        print("\n" + "="*60)
        print("CREATING DISTRIBUTION PLOTS")
        print("="*60)
        
        # 1. Movie Duration Distribution
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        movie_durations = self.df[self.df['is_movie'] == 1]['duration_minutes'].dropna()
        axes[0].hist(movie_durations, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        axes[0].set_title('Movie Duration Distribution', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Duration (minutes)', fontsize=11)
        axes[0].set_ylabel('Number of Movies', fontsize=11)
        axes[0].axvline(movie_durations.mean(), color='red', linestyle='--', linewidth=2, 
                       label=f'Mean: {movie_durations.mean():.1f} min')
        axes[0].legend()
        
        # Box plot
        axes[1].boxplot(movie_durations, vert=True, patch_artist=True,
                       boxprops=dict(facecolor='lightblue', color='steelblue'),
                       medianprops=dict(color='red', linewidth=2),
                       whiskerprops=dict(color='steelblue'),
                       capprops=dict(color='steelblue'))
        axes[1].set_title('Movie Duration Box Plot', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Duration (minutes)', fontsize=11)
        axes[1].set_xticklabels(['Movies'])
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'movie_duration_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['movie_duration_distribution'] = fig
        print("Created movie duration distribution plots")
        
        # 2. Content Age Distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        
        content_age = self.df['content_age'].dropna()
        ax.hist(content_age, bins=40, color='coral', edgecolor='black', alpha=0.7)
        ax.set_title('Content Age Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Content Age (years)', fontsize=12)
        ax.set_ylabel('Number of Titles', fontsize=12)
        ax.axvline(content_age.mean(), color='darkred', linestyle='--', linewidth=2, 
                   label=f'Mean: {content_age.mean():.1f} years')
        ax.axvline(content_age.median(), color='blue', linestyle='--', linewidth=2, 
                   label=f'Median: {content_age.median():.1f} years')
        ax.legend()
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'content_age_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['content_age_distribution'] = fig
        print("Created content age distribution plot")
        
        # 3. Genre Count Distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        
        genre_counts = self.df['genre_count'].value_counts().sort_index()
        ax.bar(genre_counts.index, genre_counts.values, color='mediumseagreen', edgecolor='black', alpha=0.8)
        ax.set_title('Distribution of Genre Counts per Title', fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Genres', fontsize=12)
        ax.set_ylabel('Number of Titles', fontsize=12)
        ax.set_xticks(range(1, genre_counts.index.max() + 1))
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'genre_count_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['genre_count_distribution'] = fig
        print("Created genre count distribution plot")
    
    def create_time_series_plots(self):
        """
        Create time series visualizations showing trends over time.
        """
        print("\n" + "="*60)
        print("CREATING TIME SERIES PLOTS")
        print("="*60)
        
        # 1. Content Added Per Year
        yearly_data = self.df.groupby('year_added').agg({
            'show_id': 'count',
            'is_movie': 'sum',
            'is_tv_show': 'sum'
        }).reset_index()
        yearly_data.columns = ['Year', 'Total', 'Movies', 'TV Shows']
        yearly_data = yearly_data.sort_values('Year')
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(yearly_data['Year'], yearly_data['Total'], marker='o', linewidth=2.5, 
                color='darkblue', label='Total Titles', markersize=6)
        ax.plot(yearly_data['Year'], yearly_data['Movies'], marker='s', linewidth=2, 
                color='steelblue', label='Movies', markersize=5)
        ax.plot(yearly_data['Year'], yearly_data['TV Shows'], marker='^', linewidth=2, 
                color='lightcoral', label='TV Shows', markersize=5)
        
        ax.set_title('Netflix Content Added Per Year', fontsize=14, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Number of Titles', fontsize=12)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'yearly_content_additions.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['yearly_additions'] = fig
        print("Created yearly content additions plot")
        
        # 2. Monthly Seasonality
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_data = self.df.groupby('month_name').size().reset_index(name='Count')
        monthly_data['month_name'] = pd.Categorical(monthly_data['month_name'], 
                                                     categories=month_order, ordered=True)
        monthly_data = monthly_data.sort_values('month_name')
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        bars = ax.bar(monthly_data['month_name'], monthly_data['Count'], 
                      color='teal', edgecolor='black', alpha=0.7)
        
        # Highlight max and min months
        max_idx = monthly_data['Count'].idxmax()
        min_idx = monthly_data['Count'].idxmin()
        bars[max_idx].set_color('darkgreen')
        bars[min_idx].set_color('lightcoral')
        
        ax.set_title('Content Added by Month (All Years Combined)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Number of Titles', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'monthly_seasonality.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['monthly_seasonality'] = fig
        print("Created monthly seasonality plot")
    
    def create_categorical_plots(self):
        """
        Create visualizations comparing categorical variables.
        """
        print("\n" + "="*60)
        print("CREATING CATEGORICAL COMPARISON PLOTS")
        print("="*60)
        
        # 1. Top 10 Genres
        top_genres = self.df['primary_genre'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.barh(top_genres.index, top_genres.values, color='skyblue', edgecolor='navy', alpha=0.8)
        # Color the top bar differently
        bars[0].set_color('mediumseagreen')
        
        ax.set_title('Top 10 Genres on Netflix', fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Titles', fontsize=12)
        ax.set_ylabel('Genre', fontsize=12)
        ax.invert_yaxis()
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'top_genres.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['top_genres'] = fig
        print("Created top genres plot")
        
        # 2. Top 10 Countries
        top_countries = self.df['primary_country'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.barh(top_countries.index, top_countries.values, color='lightcoral', edgecolor='darkred', alpha=0.8)
        bars[0].set_color('crimson')
        
        ax.set_title('Top 10 Content Producing Countries', fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Titles', fontsize=12)
        ax.set_ylabel('Country', fontsize=12)
        ax.invert_yaxis()
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'top_countries.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['top_countries'] = fig
        print("Created top countries plot")
        
        # 3. Content Type by Rating
        fig, ax = plt.subplots(figsize=(14, 6))
        
        rating_type = self.df.groupby(['rating', 'type']).size().unstack(fill_value=0)
        rating_type = rating_type.loc[rating_type.sum(axis=1).nlargest(10).index]
        
        rating_type.plot(kind='bar', stacked=True, ax=ax, color=['steelblue', 'lightcoral'], 
                        edgecolor='black', alpha=0.8)
        
        ax.set_title('Content Count by Rating and Type (Top 10 Ratings)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Rating', fontsize=12)
        ax.set_ylabel('Number of Titles', fontsize=12)
        ax.legend(title='Type', fontsize=11)
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'rating_type_breakdown.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['rating_type'] = fig
        print("Created rating-type breakdown plot")
    
    def create_heatmaps(self):
        """
        Create heatmap visualizations.
        """
        print("\n" + "="*60)
        print("CREATING HEATMAPS")
        print("="*60)
        
        # 1. Year-Month Heatmap
        # Filter to last 10 years
        recent_years = sorted(self.df['year_added'].dropna().unique())[-10:]
        recent_df = self.df[self.df['year_added'].isin(recent_years)]
        
        # Create pivot table for heatmap
        year_month_pivot = recent_df.pivot_table(
            values='show_id',
            index='month_name',
            columns='year_added',
            aggfunc='count',
            fill_value=0
        )
        
        # Reorder months
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        year_month_pivot = year_month_pivot.reindex(month_order)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        sns.heatmap(year_month_pivot, annot=True, fmt='d', cmap='YlOrRd', 
                   linewidths=0.5, cbar_kws={'label': 'Number of Titles'}, ax=ax)
        
        ax.set_title('Content Additions: Year vs Month Heatmap (Last 10 Years)', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Month', fontsize=12)
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'year_month_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['year_month_heatmap'] = fig
        print("Created year-month heatmap")
        
        # 2. Genre-Type Heatmap
        top_10_genres = self.df['primary_genre'].value_counts().head(10).index.tolist()
        genre_type_pivot = self.df[self.df['primary_genre'].isin(top_10_genres)].pivot_table(
            values='show_id',
            index='primary_genre',
            columns='type',
            aggfunc='count',
            fill_value=0
        )
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(genre_type_pivot, annot=True, fmt='d', cmap='Blues', 
                   linewidths=0.5, cbar_kws={'label': 'Number of Titles'}, ax=ax)
        
        ax.set_title('Top 10 Genres by Content Type', fontsize=14, fontweight='bold')
        ax.set_xlabel('Content Type', fontsize=12)
        ax.set_ylabel('Genre', fontsize=12)
        
        plt.tight_layout()
        fig.savefig(self.output_dir / 'genre_type_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.figures['genre_type_heatmap'] = fig
        print("Created genre-type heatmap")
    
    def create_all_visualizations(self):
        """
        Create all visualizations and save to output directory.
        
        Returns:
            dict: Dictionary of all created figures
        """
        print("\nStarting Visualization Creation...")
        
        self.create_distribution_plots()
        self.create_time_series_plots()
        self.create_categorical_plots()
        self.create_heatmaps()
        
        print("\nAll visualizations created!")
        print(f"   Total plots created: {len([f for f in self.output_dir.iterdir() if f.suffix == '.png'])}")
        print(f"   Saved to: {self.output_dir}")
        
        return self.figures


if __name__ == "__main__":
    # Testing the Visualizer
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
    
    # Creating visualizations
    visualizer = Visualizer(df_engineered)
    figures = visualizer.create_all_visualizations()