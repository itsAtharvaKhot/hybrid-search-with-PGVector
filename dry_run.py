#!/usr/bin/env python3
"""
Dry run script for the hybrid search system.
This script tests the entire system step by step.
"""

import os
import sys
import time
import pandas as pd
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set."""
    print("Checking environment...")
    load_dotenv()
    
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing environment variables: {missing_vars}")
        print("Please create a .env file with the following variables:")
        print("DB_NAME=hybrid_search")
        print("DB_USER=postgres")
        print("DB_PASSWORD=your_password")
        print("DB_HOST=localhost")
        print("DB_PORT=5432")
        return False
    
    print("Environment variables are set correctly.")
    return True

def check_dependencies():
    """Check if all required Python packages are installed."""
    print("\nChecking dependencies...")
    
    # Map package names to their import names
    package_imports = {
        'psycopg2-binary': 'psycopg2',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sentence-transformers': 'sentence_transformers',
        'scikit-learn': 'sklearn',
        'streamlit': 'streamlit',
        'python-dotenv': 'dotenv'
    }
    
    missing_packages = []
    
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - MISSING")
    
    if missing_packages:
        print(f"\nMissing packages: {missing_packages}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    print("All dependencies are installed.")
    return True

def setup_database():
    """Set up the database."""
    print("\nSetting up database...")
    
    try:
        from setup_database import setup_database
        success = setup_database()
        if success:
            print("Database setup completed successfully.")
            return True
        else:
            print("Database setup failed.")
            return False
    except Exception as e:
        print(f"Database setup error: {e}")
        return False

def preprocess_data():
    """Preprocess the data."""
    print("\nPreprocessing data...")
    
    try:
        from data_preprocessor import main as preprocess_data
        preprocess_data()
        print("Data preprocessing completed successfully.")
        return True
    except Exception as e:
        print(f"Data preprocessing error: {e}")
        return False

def test_search_engine():
    """Test the search engine functionality."""
    print("\nTesting search engine...")
    
    try:
        from test_hybrid_search import test_hybrid_search
        test_hybrid_search()
        print("Search engine test completed successfully.")
        return True
    except Exception as e:
        print(f"Search engine test error: {e}")
        return False

def test_streamlit_app():
    """Test if the Streamlit app can be imported."""
    print("\nTesting Streamlit app...")
    
    try:
        import streamlit as st
        print("Streamlit is available.")
        
        # Test if our app can be imported
        import hybrid_search_app
        print("Streamlit app can be imported successfully.")
        return True
    except Exception as e:
        print(f"Streamlit app test error: {e}")
        return False

def main():
    """Main dry run function."""
    print("=" * 60)
    print("HYBRID SEARCH SYSTEM - DRY RUN")
    print("=" * 60)
    
    # Step 1: Check environment
    if not check_environment():
        print("\nEnvironment check failed. Please fix the issues above.")
        return False
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print("\nDependency check failed. Please install missing packages.")
        return False
    
    # Step 3: Setup database
    if not setup_database():
        print("\nDatabase setup failed. Please check your PostgreSQL connection.")
        return False
    
    # Step 4: Preprocess data
    if not preprocess_data():
        print("\nData preprocessing failed.")
        return False
    
    # Step 5: Test search engine
    if not test_search_engine():
        print("\nSearch engine test failed.")
        return False
    
    # Step 6: Test Streamlit app
    if not test_streamlit_app():
        print("\nStreamlit app test failed.")
        return False
    
    print("\n" + "=" * 60)
    print("DRY RUN COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nAll components are working correctly.")
    print("\nTo run the application:")
    print("1. Start the Streamlit app: streamlit run hybrid_search_app.py")
    print("2. Open your browser to: http://localhost:8501")
    print("3. Click 'Index Documents' in the sidebar")
    print("4. Enter a search query and test the system")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 