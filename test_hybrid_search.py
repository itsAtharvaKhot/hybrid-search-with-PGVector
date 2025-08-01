#!/usr/bin/env python3
import pandas as pd
import time
from search_engine import SearchEngine
from data_preprocessor import main as preprocess_data
import os

def test_hybrid_search():
    if not os.path.exists('data/preprocessed_data.csv'):
        preprocess_data()
    
    documents_df = pd.read_csv('data/preprocessed_data.csv')
    search_engine = SearchEngine()
    
    start_time = time.time()
    search_engine.index_documents(documents_df)
    indexing_time = time.time() - start_time
    
    test_queries = [
        "revenue growth and quarterly earnings",
        "digital transformation and innovation",
        "risk factors and market volatility",
        "R&D investment and product development"
    ]
    
    for query in test_queries:
        dense_results = search_engine.search(query, 'dense', limit=5)
        sparse_results = search_engine.search(query, 'sparse', limit=5)
        hybrid_results = search_engine.search(query, 'hybrid', limit=5, dense_weight=0.5)
    
    search_engine.close()

if __name__ == "__main__":
    test_hybrid_search()