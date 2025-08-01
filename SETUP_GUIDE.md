# Hybrid Search System Setup Guide

## Quick Start

### 1. Environment Setup

Create a `.env` file in the project root with your PostgreSQL credentials:

```env
DB_NAME=hybrid_search
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Dry Run Test

```bash
python dry_run.py
```

This will:
- Check environment variables
- Verify all dependencies are installed
- Set up the database with pgvector extension
- Preprocess the data
- Test the search engine functionality
- Verify the Streamlit app can be imported

### 4. Start the Application

```bash
streamlit run hybrid_search_app.py
```

Then open your browser to: http://localhost:8501

## Manual Testing Steps

### Step 1: Database Setup
```bash
python setup_database.py
```

### Step 2: Data Preprocessing
```bash
python data_preprocessor.py
```

### Step 3: Test Search Engine
```bash
python test_hybrid_search.py
```

### Step 4: Run Performance Evaluation
```bash
python search_evaluation.py
```

## Troubleshooting

### Common Issues:

1. **PostgreSQL Connection Error**
   - Ensure PostgreSQL is running
   - Verify credentials in .env file
   - Check if pgvector extension is installed

2. **Missing Dependencies**
   - Run: `pip install -r requirements.txt`
   - For Windows: Install Visual Studio Build Tools

3. **Memory Issues**
   - Reduce batch size in data_preprocessor.py
   - Use smaller embedding dimensions

4. **Streamlit Issues**
   - Check if port 8501 is available
   - Try: `streamlit run hybrid_search_app.py --server.port 8502`

## System Requirements

- Python 3.8+
- PostgreSQL 15+ with pgvector extension
- 4GB+ RAM (for large datasets)
- Windows: Visual Studio Build Tools

## Expected Output

After running `python dry_run.py`, you should see:

```
============================================================
HYBRID SEARCH SYSTEM - DRY RUN
============================================================
Checking environment...
Environment variables are set correctly.

Checking dependencies...
✓ psycopg2-binary
✓ pandas
✓ numpy
✓ sentence-transformers
✓ scikit-learn
✓ streamlit
✓ python-dotenv
All dependencies are installed.

Setting up database...
Connected to PostgreSQL database successfully!
pgvector extension enabled
documents table created
dense_vectors table created
sparse_vectors table created
dense vectors HNSW index created
sparse vectors HNSW index created
additional indexes created
pgvector extension verified (version: 0.8.0)
Database setup completed successfully.

Preprocessing data...
Data preprocessing completed successfully.

Testing search engine...
Testing Hybrid Search System
==================================================
Loading preprocessed data...
Loaded 2622 documents
Initializing search engine...
Indexing documents...
Indexing completed in 335.34 seconds
==================================================
TESTING SEARCH FUNCTIONALITY
==================================================
Testing query: 'revenue growth and quarterly earnings'
Dense Search (0.094s):
  Results: 5
  Avg Similarity: 0.5196
Sparse Search (0.102s):
  Results: 5
  Avg Similarity: 0.4805
Hybrid Search (0.484s):
  Results: 5
  Avg Similarity: 0.4990
Search engine test completed successfully.

Testing Streamlit app...
Streamlit is available.
Streamlit app can be imported successfully.

============================================================
DRY RUN COMPLETED SUCCESSFULLY!
============================================================

All components are working correctly.

To run the application:
1. Start the Streamlit app: streamlit run hybrid_search_app.py
2. Open your browser to: http://localhost:8501
3. Click 'Index Documents' in the sidebar
4. Enter a search query and test the system
``` 