#!/usr/bin/env python3
"""
Search Performance Evaluation Script
Compares dense, sparse, and hybrid search strategies
"""

import pandas as pd
import numpy as np
import time
from search_engine import SearchEngine
from data_preprocessor import main as preprocess_data
import os

class SearchEvaluator:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.test_queries = self._create_test_queries()
        
        # Initialize the search engine with data
        self._initialize_search_engine()
    
    def _initialize_search_engine(self):
        """Initialize the search engine with preprocessed data."""
        import pandas as pd
        import os
        
        if not os.path.exists('data/preprocessed_data.csv'):
            from data_preprocessor import main as preprocess_data
            preprocess_data()
        
        documents_df = pd.read_csv('data/preprocessed_data.csv')
        print(f"Initializing search engine with {len(documents_df)} documents...")
        self.search_engine.index_documents(documents_df)
        print("Search engine initialized successfully!")
        
    def _create_test_queries(self):
        """Create a comprehensive set of test queries for evaluation."""
        return {
            'financial_performance': [
                "revenue growth and quarterly earnings",
                "net income and profit margins",
                "stock price performance and market trends",
                "financial results and earnings per share",
                "revenue increase and profitability"
            ],
            'strategic_initiatives': [
                "digital transformation and innovation",
                "market expansion and partnerships",
                "sustainability initiatives and ESG",
                "product development and R&D",
                "strategic partnerships and acquisitions"
            ],
            'risk_and_outlook': [
                "risk factors and market volatility",
                "future guidance and projections",
                "competitive pressures and market share",
                "regulatory changes and compliance",
                "economic uncertainty and challenges"
            ],
            'operational_metrics': [
                "R&D investment and product development",
                "operational efficiency and cost control",
                "customer adoption and market penetration",
                "supply chain and logistics",
                "employee productivity and workforce"
            ]
        }
    
    def evaluate_search_method(self, query, search_type, limit=10, dense_weight=0.5):
        """Evaluate a single search method."""
        start_time = time.time()
        
        try:
            results = self.search_engine.search(
                query, 
                search_type=search_type, 
                limit=limit, 
                dense_weight=dense_weight
            )
            
            search_time = time.time() - start_time
            
            return {
                'query': query,
                'search_type': search_type,
                'results_count': len(results),
                'search_time': search_time,
                'avg_similarity': results['similarity'].mean() if not results.empty else 0,
                'max_similarity': results['similarity'].max() if not results.empty else 0,
                'min_similarity': results['similarity'].min() if not results.empty else 0,
                'std_similarity': results['similarity'].std() if not results.empty else 0,
                'results': results
            }
        except Exception as e:
            print(f"Error evaluating {search_type} search for query '{query}': {e}")
            return {
                'query': query,
                'search_type': search_type,
                'results_count': 0,
                'search_time': time.time() - start_time,
                'avg_similarity': 0,
                'max_similarity': 0,
                'min_similarity': 0,
                'std_similarity': 0,
                'results': pd.DataFrame(),
                'error': str(e)
            }
    
    def run_comprehensive_evaluation(self, limit=10):
        """Run comprehensive evaluation of all search methods."""
        print("Starting comprehensive search evaluation...")
        
        evaluation_results = []
        
        for category, queries in self.test_queries.items():
            print(f"\nEvaluating category: {category}")
            
            for query in queries:
                print(f"  Testing query: '{query}'")
                
                # Test dense search
                dense_result = self.evaluate_search_method(query, 'dense', limit)
                evaluation_results.append(dense_result)
                
                # Test sparse search
                sparse_result = self.evaluate_search_method(query, 'sparse', limit)
                evaluation_results.append(sparse_result)
                
                # Test hybrid search with different weights
                for weight in [0.3, 0.5, 0.7]:
                    hybrid_result = self.evaluate_search_method(
                        query, 'hybrid', limit, dense_weight=weight
                    )
                    hybrid_result['dense_weight'] = weight
                    evaluation_results.append(hybrid_result)
        
        return pd.DataFrame(evaluation_results)
    
    def analyze_results(self, results_df):
        """Analyze evaluation results and generate insights."""
        print("\n" + "="*80)
        print("SEARCH EVALUATION RESULTS")
        print("="*80)
        
        # Overall statistics by search type
        print("\n1. OVERALL PERFORMANCE BY SEARCH TYPE")
        print("-" * 50)
        
        search_types = results_df['search_type'].unique()
        for search_type in search_types:
            type_data = results_df[results_df['search_type'] == search_type]
            
            print(f"\n{search_type.upper()} SEARCH:")
            print(f"  Average Search Time: {type_data['search_time'].mean():.4f} seconds")
            print(f"  Average Similarity Score: {type_data['avg_similarity'].mean():.4f}")
            print(f"  Max Similarity Score: {type_data['max_similarity'].max():.4f}")
            print(f"  Min Similarity Score: {type_data['min_similarity'].min():.4f}")
            print(f"  Average Results Count: {type_data['results_count'].mean():.1f}")
        
        # Hybrid search weight analysis
        print("\n2. HYBRID SEARCH WEIGHT ANALYSIS")
        print("-" * 50)
        
        hybrid_data = results_df[results_df['search_type'] == 'hybrid']
        for weight in [0.3, 0.5, 0.7]:
            weight_data = hybrid_data[hybrid_data['dense_weight'] == weight]
            if not weight_data.empty:
                print(f"\nDense Weight {weight}:")
                print(f"  Average Similarity: {weight_data['avg_similarity'].mean():.4f}")
                print(f"  Average Search Time: {weight_data['search_time'].mean():.4f} seconds")
        
        # Query category analysis
        print("\n3. PERFORMANCE BY QUERY CATEGORY")
        print("-" * 50)
        
        for category in self.test_queries.keys():
            print(f"\n{category.replace('_', ' ').upper()}:")
            category_queries = self.test_queries[category]
            
            for search_type in ['dense', 'sparse', 'hybrid']:
                category_data = results_df[
                    (results_df['search_type'] == search_type) & 
                    (results_df['query'].isin(category_queries))
                ]
                
                if not category_data.empty:
                    print(f"  {search_type.title()}: Avg Similarity = {category_data['avg_similarity'].mean():.4f}")
        
        # Generate recommendations
        print("\n4. RECOMMENDATIONS")
        print("-" * 50)
        
        # Find best performing method overall
        best_method = results_df.groupby('search_type')['avg_similarity'].mean().idxmax()
        print(f"  Best overall method: {best_method.upper()}")
        
        # Find fastest method
        fastest_method = results_df.groupby('search_type')['search_time'].mean().idxmin()
        print(f"  Fastest method: {fastest_method.upper()}")
        
        # Best hybrid weight
        hybrid_data = results_df[results_df['search_type'] == 'hybrid']
        if not hybrid_data.empty:
            best_weight = hybrid_data.groupby('dense_weight')['avg_similarity'].mean().idxmax()
            print(f"  Optimal hybrid dense weight: {best_weight}")
        
        return results_df
    
    def save_results(self, results_df, filename='search_evaluation_results.csv'):
        """Save evaluation results to CSV."""
        # Remove the 'results' column as it contains DataFrames
        save_df = results_df.drop('results', axis=1, errors='ignore')
        save_df.to_csv(filename, index=False)
        print(f"\nResults saved to {filename}")
    
    def create_performance_report(self, results_df):
        """Create a detailed performance report."""
        report = []
        report.append("HYBRID SEARCH EVALUATION REPORT")
        report.append("=" * 50)
        report.append("")
        
        # Summary statistics
        report.append("SUMMARY STATISTICS")
        report.append("-" * 30)
        
        for search_type in ['dense', 'sparse', 'hybrid']:
            type_data = results_df[results_df['search_type'] == search_type]
            if not type_data.empty:
                report.append(f"{search_type.upper()} SEARCH:")
                report.append(f"  Total Queries: {len(type_data)}")
                report.append(f"  Avg Search Time: {type_data['search_time'].mean():.4f}s")
                report.append(f"  Avg Similarity: {type_data['avg_similarity'].mean():.4f}")
                report.append(f"  Avg Results: {type_data['results_count'].mean():.1f}")
                report.append("")
        
        # Detailed results by query
        report.append("DETAILED RESULTS BY QUERY")
        report.append("-" * 30)
        
        for category, queries in self.test_queries.items():
            report.append(f"\n{category.upper()}:")
            for query in queries:
                query_data = results_df[results_df['query'] == query]
                if not query_data.empty:
                    report.append(f"  Query: '{query}'")
                    for _, row in query_data.iterrows():
                        report.append(f"    {row['search_type']}: {row['avg_similarity']:.4f} "
                                   f"({row['search_time']:.4f}s)")
                    report.append("")
        
        # Save report
        with open('performance_report.txt', 'w') as f:
            f.write('\n'.join(report))
        
        print("Performance report saved to performance_report.txt")
        return report

def main():
    """Main function to run the search evaluation."""
    print("HYBRID SEARCH EVALUATION")
    print("=" * 50)
    
    # Check if preprocessed data exists
    if not os.path.exists('data/preprocessed_data.csv'):
        print("Preprocessed data not found. Creating it now...")
        preprocess_data()
    
    # Initialize evaluator
    evaluator = SearchEvaluator()
    
    # Run comprehensive evaluation
    print("Running comprehensive evaluation...")
    results = evaluator.run_comprehensive_evaluation(limit=10)
    
    # Analyze results
    evaluator.analyze_results(results)
    
    # Save results
    evaluator.save_results(results)
    
    # Create performance report
    evaluator.create_performance_report(results)
    
    print("\nEvaluation completed successfully!")
    print("Check the generated files for detailed results.")

if __name__ == "__main__":
    main() 