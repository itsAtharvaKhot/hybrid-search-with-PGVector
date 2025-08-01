import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
from search_engine import SearchEngine
from data_preprocessor import main as preprocess_data
import os

st.set_page_config(
    page_title="Hybrid Search System",
    page_icon="🔍",
    layout="wide"
)

@st.cache_resource
def load_search_engine():
    return SearchEngine()

@st.cache_data
def load_preprocessed_data():
    if not os.path.exists('data/preprocessed_data.csv'):
        preprocess_data()
    return pd.read_csv('data/preprocessed_data.csv')

def index_documents(search_engine, documents_df):
    with st.spinner("Indexing documents..."):
        search_engine.index_documents(documents_df)

def display_search_results(results_df, search_type):
    if results_df.empty:
        st.warning("No results found.")
        return
    
    st.subheader(f"{search_type} Search Results")
    
    for idx, row in results_df.head(5).iterrows():
        with st.expander(f"{row['title'][:80]}..."):
            st.write(f"**Source:** {row['source']}")
            st.write(f"**Type:** {row['document_type']}")
            st.write(f"**Similarity:** {row['similarity']:.4f}")
            st.write(f"**Content:** {row['content'][:200]}...")

def create_performance_comparison(dense_results, sparse_results, hybrid_results):
    methods = ['Dense', 'Sparse', 'Hybrid']
    avg_similarities = [
        dense_results['similarity'].mean() if not dense_results.empty else 0,
        sparse_results['similarity'].mean() if not sparse_results.empty else 0,
        hybrid_results['similarity'].mean() if not hybrid_results.empty else 0
    ]
    
    fig = go.Figure(data=[
        go.Bar(x=methods, y=avg_similarities, text=[f'{x:.4f}' for x in avg_similarities], textposition='auto')
    ])
    
    fig.update_layout(
        title="Average Similarity Scores by Search Method",
        xaxis_title="Search Method",
        yaxis_title="Average Similarity",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("Hybrid Search System")
    
    search_engine = load_search_engine()
    documents_df = load_preprocessed_data()
    
    with st.sidebar:
        st.header("Configuration")
        
        if st.button("Index Documents"):
            index_documents(search_engine, documents_df)
            st.success("Documents indexed successfully!")
        
        st.subheader("Search Settings")
        search_type = st.selectbox(
            "Search Type",
            ["Dense", "Sparse", "Hybrid"],
            help="Dense: Semantic similarity, Sparse: Keyword matching, Hybrid: Combined approach"
        )
        
        limit = st.slider("Number of Results", 1, 20, 5)
        
        if search_type == "Hybrid":
            dense_weight = st.slider("Dense Weight", 0.0, 1.0, 0.5, 0.1)
        else:
            dense_weight = 0.5
    
    st.header("Search Interface")
    
    query = st.text_input("Enter your search query:", placeholder="e.g., revenue growth and quarterly earnings")
    
    if st.button("Search"):
        if not query:
            st.error("Please enter a search query.")
            return
        
        with st.spinner("Searching..."):
            start_time = time.time()
            
            if search_type == "Hybrid":
                results = search_engine.search(
                    query, 
                    search_type='hybrid', 
                    limit=limit, 
                    dense_weight=dense_weight
                )
            else:
                results = search_engine.search(
                    query, 
                    search_type=search_type.lower(), 
                    limit=limit
                )
            
            search_time = time.time() - start_time
        
        st.success(f"Search completed in {search_time:.3f} seconds")
        display_search_results(results, search_type)
        
        with st.expander("Detailed Results"):
            st.dataframe(results, use_container_width=True)
    
    st.subheader("Performance Comparison")
    
    if st.button("Compare All Search Methods"):
        with st.spinner("Running comparison..."):
            dense_results = search_engine.search(query, 'dense', limit) if query else pd.DataFrame()
            sparse_results = search_engine.search(query, 'sparse', limit) if query else pd.DataFrame()
            hybrid_results = search_engine.search(query, 'hybrid', limit, 0.5) if query else pd.DataFrame()
            
            create_performance_comparison(dense_results, sparse_results, hybrid_results)
            
            st.subheader("Detailed Comparison")
            
            comparison_data = []
            for method, results in [('Dense', dense_results), ('Sparse', sparse_results), ('Hybrid', hybrid_results)]:
                if not results.empty:
                    comparison_data.append({
                        'Method': method,
                        'Avg Similarity': results['similarity'].mean(),
                        'Max Similarity': results['similarity'].max(),
                        'Min Similarity': results['similarity'].min(),
                        'Result Count': len(results)
                    })
            
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True)
    
    st.subheader("Experimental Setup")
    
    with st.expander("Test Queries for Evaluation"):
        st.markdown("""
        **Suggested test queries for comprehensive evaluation:**
        
        **Financial Performance:**
        - "revenue growth and quarterly earnings"
        - "net income and profit margins"
        - "stock price performance and market trends"
        
        **Strategic Initiatives:**
        - "digital transformation and innovation"
        - "market expansion and partnerships"
        - "sustainability initiatives and ESG"
        
        **Risk and Outlook:**
        - "risk factors and market volatility"
        - "future guidance and projections"
        - "competitive pressures and market share"
        
        **Operational Metrics:**
        - "R&D investment and product development"
        - "operational efficiency and cost control"
        - "customer adoption and market penetration"
        """)
    
    st.subheader("Insights and Recommendations")
    
    with st.expander("Analysis Framework"):
        st.markdown("""
        **Evaluation Metrics:**
        1. **Recall**: How many relevant documents are retrieved
        2. **Precision**: How many retrieved documents are relevant
        3. **Speed**: Query response time
        4. **Similarity Score Distribution**: Quality of matches
        
        **Expected Findings:**
        - **Dense Search**: Better for semantic similarity and conceptual matches
        - **Sparse Search**: Better for exact keyword matches and specific terms
        - **Hybrid Search**: Combines benefits of both approaches for optimal results
        """)

if __name__ == "__main__":
    main()