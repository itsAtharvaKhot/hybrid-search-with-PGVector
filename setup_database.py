import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    db_params = {
        'dbname': os.getenv('DB_NAME', 'hybrid_search'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                title VARCHAR(500),
                content TEXT,
                source VARCHAR(200),
                document_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS dense_vectors (
                id SERIAL PRIMARY KEY,
                document_id INTEGER REFERENCES documents(id),
                vector vector(384),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sparse_vectors (
                id SERIAL PRIMARY KEY,
                document_id INTEGER REFERENCES documents(id),
                vector vector(1000),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_dense_vectors_vector 
            ON dense_vectors 
            USING hnsw (vector vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """)
        conn.commit()
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_sparse_vectors_vector 
            ON sparse_vectors 
            USING hnsw (vector vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """)
        conn.commit()
        
        cur.execute("CREATE INDEX IF NOT EXISTS idx_documents_title ON documents(title);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(document_type);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_dense_vectors_document_id ON dense_vectors(document_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sparse_vectors_document_id ON sparse_vectors(document_id);")
        conn.commit()
        
        cur.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        return False
    except Exception as e:
        return False

if __name__ == "__main__":
    setup_database() 