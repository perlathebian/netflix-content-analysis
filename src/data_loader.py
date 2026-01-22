"""
Data loading module for Netflix dataset analysis.
Handles CSV loading, validation, and metadata extraction.
"""

import pandas as pd
import os
from pathlib import Path


class DataLoader:
    """
    Handles loading and initial validation of Netflix dataset.
    
    Attributes:
        filepath (Path): Path to the CSV file
        df (pd.DataFrame): Loaded dataset
        metadata (dict): Dataset metadata (size, rows, columns, etc.)
    """
    
    def __init__(self, filepath):
        """
        Initialize DataLoader with file path.
        
        Args:
            filepath (str): Path to CSV file
        """
        self.filepath = Path(filepath)
        self.df = None
        self.metadata = {}
    
    def load_data(self):
        """
        Load CSV file with comprehensive error handling.
        
        Returns:
            pd.DataFrame: Loaded dataset
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or invalid
        """
        # Check if file exists
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        # Check file size
        file_size = self.filepath.stat().st_size
        if file_size == 0:
            raise ValueError(f"File is empty: {self.filepath}")
        
        try:
            # Load CSV
            self.df = pd.read_csv(self.filepath)
            
            # Validate dataset is not empty
            if self.df.empty:
                raise ValueError("Dataset loaded but contains no data")
            
            # Store metadata
            self.metadata = {
                'filepath': str(self.filepath),
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'rows': len(self.df),
                'columns': len(self.df.columns),
                'column_names': list(self.df.columns),
                'memory_usage_mb': round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            }
            
            print(f"Data loaded successfully!")
            print(f"   Rows: {self.metadata['rows']:,}")
            print(f"   Columns: {self.metadata['columns']}")
            print(f"   File size: {self.metadata['file_size_mb']} MB")
            print(f"   Memory usage: {self.metadata['memory_usage_mb']} MB")
            
            return self.df
        
        except pd.errors.EmptyDataError:
            raise ValueError(f"File is empty or invalid: {self.filepath}")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error loading data: {e}")
    
    def get_basic_info(self):
        """
        Display basic dataset information.
        """
        if self.df is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*50)
        print("DATASET OVERVIEW")
        print("="*50)
        print(f"\nShape: {self.df.shape}")
        print(f"\nColumn Names:\n{self.df.columns.tolist()}")
        print(f"\nData Types:\n{self.df.dtypes}")
        print(f"\nFirst 3 Rows:\n{self.df.head(3)}")
        print(f"\nLast 3 Rows:\n{self.df.tail(3)}")


if __name__ == "__main__":
    # Testing the DataLoader
    loader = DataLoader("data/raw/netflix.csv")
    df = loader.load_data()
    loader.get_basic_info()