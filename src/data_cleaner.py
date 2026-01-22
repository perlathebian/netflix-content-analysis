"""
Data cleaning module for Netflix dataset analysis.
Handles missing values, duplicates, and data type validation.
"""

import pandas as pd
import numpy as np
from pathlib import Path


class DataCleaner:
    """
    Handles data cleaning operations for Netflix dataset.
    
    Attributes:
        df_original (pd.DataFrame): Original dataset (unchanged)
        df (pd.DataFrame): Working dataset (gets cleaned)
        cleaning_report (dict): Cleaning metrics and summary
    """
    
    def __init__(self, df):
        """
        Initialize DataCleaner with DataFrame.
        
        Args:
            df (pd.DataFrame): Raw dataset to clean
        """
        self.df_original = df.copy()  # Keep original for comparison
        self.df = df.copy()           # Working copy
        self.cleaning_report = {}
    
    def analyze_missing_values(self):
        """
        Analyze missing values in dataset.
        
        Returns:
            pd.DataFrame: Missing value summary
        """
        missing_data = pd.DataFrame({
            'Column': self.df.columns,
            'Missing_Count': self.df.isnull().sum().values,
            'Missing_Percentage': (self.df.isnull().sum().values / len(self.df) * 100).round(2)
        })
        
        # Filter to only columns with missing values
        missing_data = missing_data[missing_data['Missing_Count'] > 0]
        missing_data = missing_data.sort_values('Missing_Count', ascending=False).reset_index(drop=True)
        
        print("\n" + "="*60)
        print("MISSING VALUE ANALYSIS")
        print("="*60)
        print(missing_data.to_string(index=False))
        
        return missing_data
    
    def handle_missing_values(self):
        """
        Handle missing values with domain-specific logic.
        """
        print("\n" + "="*60)
        print("HANDLING MISSING VALUES")
        print("="*60)
        
        initial_missing = self.df.isnull().sum().sum()
        
        # 1. Director: Fill with 'Unknown Director'
        if 'director' in self.df.columns:
            missing_directors = self.df['director'].isnull().sum()
            self.df['director'] = self.df['director'].fillna('Unknown Director')
            print(f"✓ Filled {missing_directors:,} missing directors with 'Unknown Director'")
        
        # 2. Cast: Fill with 'No Cast Information'
        if 'cast' in self.df.columns:
            missing_cast = self.df['cast'].isnull().sum()
            self.df['cast'] = self.df['cast'].fillna('No Cast Information')
            print(f"✓ Filled {missing_cast:,} missing cast with 'No Cast Information'")
        
        # 3. Country: Fill with 'Unknown Country'
        if 'country' in self.df.columns:
            missing_country = self.df['country'].isnull().sum()
            self.df['country'] = self.df['country'].fillna('Unknown Country')
            print(f"✓ Filled {missing_country:,} missing countries with 'Unknown Country'")
        
        # 4. Date Added: Drop rows (if date is missing, data quality is questionable)
        if 'date_added' in self.df.columns:
            rows_before = len(self.df)
            self.df = self.df.dropna(subset=['date_added'])
            rows_dropped = rows_before - len(self.df)
            print(f"✓ Dropped {rows_dropped:,} rows with missing date_added")
        
        # 5. Rating: Fill with 'Not Rated'
        if 'rating' in self.df.columns:
            missing_rating = self.df['rating'].isnull().sum()
            self.df['rating'] = self.df['rating'].fillna('Not Rated')
            print(f"✓ Filled {missing_rating:,} missing ratings with 'Not Rated'")
        
        # 6. Duration: Cannot be missing - drop these rows
        if 'duration' in self.df.columns:
            rows_before = len(self.df)
            self.df = self.df.dropna(subset=['duration'])
            rows_dropped = rows_before - len(self.df)
            print(f"✓ Dropped {rows_dropped:,} rows with missing duration")
        
        final_missing = self.df.isnull().sum().sum()
        self.cleaning_report['missing_values_handled'] = {
            'initial_missing': initial_missing,
            'final_missing': final_missing,
            'missing_removed': initial_missing - final_missing
        }
    
    def remove_duplicates(self):
        """
        Remove duplicate rows from dataset.
        """
        print("\n" + "="*60)
        print("REMOVING DUPLICATES")
        print("="*60)
        
        initial_rows = len(self.df)
        
        # Remove exact duplicates
        self.df = self.df.drop_duplicates()
        
        duplicates_removed = initial_rows - len(self.df)
        print(f"✓ Removed {duplicates_removed:,} duplicate rows")
        
        self.cleaning_report['duplicates_removed'] = duplicates_removed
    
    def validate_data_types(self):
        """
        Validate and convert data types where necessary.
        """
        print("\n" + "="*60)
        print("VALIDATING DATA TYPES")
        print("="*60)
        
        conversions = []
        
        # 1. Convert date_added to datetime
        if 'date_added' in self.df.columns:
            try:
                self.df['date_added'] = pd.to_datetime(self.df['date_added'], errors='coerce')
                conversions.append("date_added → datetime")
                print("Converted 'date_added' to datetime")
            except Exception as e:
                print(f"Could not convert date_added: {e}")
        
        # 2. Convert release_year to integer
        if 'release_year' in self.df.columns:
            try:
                self.df['release_year'] = pd.to_numeric(self.df['release_year'], errors='coerce').astype('Int64')
                conversions.append("release_year → Int64")
                print("Converted 'release_year' to Int64")
            except Exception as e:
                print(f"Could not convert release_year: {e}")
        
        # 3. Ensure categorical columns are strings
        categorical_cols = ['type', 'title', 'director', 'cast', 'country', 'rating', 'duration', 'listed_in', 'description']
        for col in categorical_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str)
                conversions.append(f"{col} → string")
        
        print(f"Ensured {len(categorical_cols)} categorical columns are strings")
        
        self.cleaning_report['type_conversions'] = conversions
        
        # Display final data types
        print("\nFinal Data Types:")
        print(self.df.dtypes)
    
    def generate_cleaning_report(self):
        """
        Generate comprehensive cleaning report.
        """
        print("\n" + "="*60)
        print("CLEANING REPORT SUMMARY")
        print("="*60)
        
        print(f"\nOriginal Dataset:")
        print(f"   Rows: {len(self.df_original):,}")
        print(f"   Columns: {len(self.df_original.columns)}")
        
        print(f"\nCleaned Dataset:")
        print(f"   Rows: {len(self.df):,}")
        print(f"   Columns: {len(self.df.columns)}")
        
        rows_removed = len(self.df_original) - len(self.df)
        print(f"\nRows Removed: {rows_removed:,} ({(rows_removed/len(self.df_original)*100):.2f}%)")
        
        print(f"\nMissing Values Handled:")
        if 'missing_values_handled' in self.cleaning_report:
            mvh = self.cleaning_report['missing_values_handled']
            print(f"   Initial: {mvh['initial_missing']:,}")
            print(f"   Final: {mvh['final_missing']:,}")
            print(f"   Removed: {mvh['missing_removed']:,}")
        
        print(f"\nDuplicates Removed: {self.cleaning_report.get('duplicates_removed', 0):,}")
        
        print(f"\nType Conversions: {len(self.cleaning_report.get('type_conversions', []))}")
    
    def clean(self):
        """
        Execute full cleaning pipeline.
        
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        print("\nStarting Data Cleaning Pipeline...")
        
        self.analyze_missing_values()
        self.handle_missing_values()
        self.remove_duplicates()
        self.validate_data_types()
        self.generate_cleaning_report()
        
        print("\nData cleaning complete!")
        
        return self.df
    
    def export_cleaned_data(self, output_path):
        """
        Export cleaned dataset to CSV.
        
        Args:
            output_path (str): Path to save cleaned data
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.df.to_csv(output_path, index=False)
        print(f"\nCleaned data exported to: {output_path}")


if __name__ == "__main__":
    # Testing the DataCleaner
    from data_loader import DataLoader
    
    # Loading data
    loader = DataLoader("data/raw/netflix.csv")
    df = loader.load_data()
    
    # Cleaning data
    cleaner = DataCleaner(df)
    df_cleaned = cleaner.clean()
    
    # Exporting cleaned data
    cleaner.export_cleaned_data("data/processed/netflix_cleaned.csv")