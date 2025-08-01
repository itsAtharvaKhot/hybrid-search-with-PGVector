-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500),
    content TEXT,
    source VARCHAR(200),
    document_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dense vectors table (using sentence-transformers embeddings)
CREATE TABLE IF NOT EXISTS dense_vectors (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    vector vector(384),  -- all-MiniLM-L6-v2 embeddings dimension
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sparse vectors table (using TF-IDF)
CREATE TABLE IF NOT EXISTS sparse_vectors (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    vector vector(1000),  -- TF-IDF dimension
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create HNSW indexes for fast similarity search
CREATE INDEX IF NOT EXISTS idx_dense_vectors_vector 
ON dense_vectors 
USING hnsw (vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_sparse_vectors_vector 
ON sparse_vectors 
USING hnsw (vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_documents_title 
ON documents(title);

CREATE INDEX IF NOT EXISTS idx_documents_type 
ON documents(document_type);

CREATE INDEX IF NOT EXISTS idx_dense_vectors_document_id 
ON dense_vectors(document_id);

CREATE INDEX IF NOT EXISTS idx_sparse_vectors_document_id 
ON sparse_vectors(document_id);