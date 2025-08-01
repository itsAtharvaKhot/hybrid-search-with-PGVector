<<<<<<< HEAD
# Hybrid Search with PGVector

A comprehensive hybrid search application that combines dense (semantic) and sparse (keyword-based) search using PostgreSQL with the pgvector extension.

## Features

- **Dense Search**: Semantic similarity using sentence-transformers
- **Sparse Search**: Keyword-based matching using TF-IDF
- **Hybrid Search**: Combined approach with tunable weights
- **PGVector Integration**: PostgreSQL with pgvector extension
- **HNSW Indexing**: Fast similarity search with optimized indexes
- **Streamlit Interface**: User-friendly web application

## Prerequisites

- **Python 3.8+**
- **PostgreSQL 15+** with pgvector extension
- **Windows**: Visual Studio Build Tools (for some dependencies)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd hybrid-search
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```env
DB_NAME=hybrid_search
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

### 4. Set Up PostgreSQL Database

Make sure PostgreSQL is running and create the database:

```sql
CREATE DATABASE hybrid_search;
```

### 5. Install PGVector Extension

Follow the [pgvector installation guide](https://github.com/pgvector/pgvector) for your system.

## Quick Start

### Option 1: Simple One-Command Run

```bash
python run.py
```

This will:
- Start the Streamlit application
- Automatically open your browser to `http://localhost:8501`

### Option 2: Manual Setup

1. **Set up the database schema:**
   ```bash
   python setup_database.py
   ```

2. **Preprocess the data:**
   ```bash
   python data_preprocessor.py
   ```

3. **Start the Streamlit application:**
   ```bash
   streamlit run hybrid_search_app.py
   ```

4. **Open your browser to:** `http://localhost:8501`

## Usage

### Web Interface

1. **Index Documents**: Click "Index Documents" in the sidebar
2. **Enter a Query**: Type your search query
3. **Select Search Type**: Choose Dense, Sparse, or Hybrid
4. **View Results**: See search results with similarity scores

### Example Queries

- "revenue growth and quarterly earnings"
- "digital transformation and innovation"
- "risk factors and market volatility"
- "R&D investment and product development"

### Search Types

- **Dense Search**: Best for semantic similarity and conceptual queries
- **Sparse Search**: Best for exact keyword matching
- **Hybrid Search**: Combines both approaches with configurable weights

## Testing

### Run Basic Tests

```bash
python test_hybrid_search.py
```

### Run Performance Evaluation

```bash
python search_evaluation.py
```

## Project Structure

```
hybrid-search/
├── data/
│   ├── financial_reports/     # Raw financial data
│   └── preprocessed_data.csv  # Processed documents
├── hybrid_search_app.py       # Streamlit web application
├── search_engine.py           # Main search engine
├── vector_models.py           # Dense and sparse embedding models
├── vector_store.py            # Vector storage and retrieval
├── database.py                # Database connection and operations
├── setup_database.py          # Database setup script
├── data_preprocessor.py       # Data preprocessing pipeline
├── test_hybrid_search.py      # Basic functionality tests
├── search_evaluation.py       # Performance evaluation
├── run.py                     # Simple startup script
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Configuration

### Database Schema

- **documents**: Document metadata and content
- **dense_vectors**: 384-dimensional semantic embeddings
- **sparse_vectors**: 1000-dimensional TF-IDF vectors

### Model Configuration

- **Dense Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **Sparse Model**: TF-IDF with 1000 features
- **Hybrid Weights**: Configurable dense/sparse weight ratio

## Troubleshooting

### Common Issues

1. **PostgreSQL Connection Error**
   - Ensure PostgreSQL is running
   - Verify credentials in `.env` file
   - Check if pgvector extension is installed

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **TF-IDF Model Error**
   - Make sure to click "Index Documents" before searching
   - The model needs to be fitted on document content first

4. **Port Already in Use**
   ```bash
   streamlit run hybrid_search_app.py --server.port 8502
   ```

### Debug Mode

Enable debug logging:
```bash
export DEBUG=1
streamlit run hybrid_search_app.py
```

## Performance

- **Indexing Speed**: ~80 seconds for 2,600+ documents
- **Query Response**: <0.5 seconds average
- **Memory Usage**: Optimized for large datasets
- **Scalability**: Designed for production deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- [pgvector](https://github.com/pgvector/pgvector) for PostgreSQL vector extension
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers) for semantic embeddings
- [Streamlit](https://streamlit.io/) for the web interface
- [PostgreSQL](https://www.postgresql.org/) for the database backend 
=======
# hybrid-search-with-PGVector
>>>>>>> 5517a3b69bdb304067ec66035a9b6dbd97b7400f
