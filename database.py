import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'hybrid_search'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        self.cur = self.conn.cursor()
    
    def execute(self, query, params=None):
        self.cur.execute(query, params)
        self.conn.commit()
    
    def fetch_one(self, query, params=None):
        self.cur.execute(query, params)
        return self.cur.fetchone()
    
    def fetch_all(self, query, params=None):
        self.cur.execute(query, params)
        return self.cur.fetchall()
    
    def store_document(self, title, content, source, document_type):
        query = """
            INSERT INTO documents (title, content, source, document_type)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        result = self.fetch_one(query, (title, content, source, document_type))
        return result[0]
    
    def store_dense_vector(self, document_id, vector):
        query = """
            INSERT INTO dense_vectors (document_id, vector)
            VALUES (%s, %s::vector)
        """
        self.execute(query, (document_id, vector.tolist()))
    
    def store_sparse_vector(self, document_id, vector):
        query = """
            INSERT INTO sparse_vectors (document_id, vector)
            VALUES (%s, %s::vector)
        """
        self.execute(query, (document_id, vector.tolist()))
    
    def dense_search(self, query_vector, limit=10):
        query = """
            SELECT d.id, d.title, d.content, d.source, d.document_type,
                   1 - (dv.vector <=> %s::vector) as similarity
            FROM documents d
            JOIN dense_vectors dv ON d.id = dv.document_id
            ORDER BY dv.vector <=> %s::vector
            LIMIT %s
        """
        return self.fetch_all(query, (query_vector.tolist(), query_vector.tolist(), limit))
    
    def sparse_search(self, query_vector, limit=10):
        query = """
            SELECT d.id, d.title, d.content, d.source, d.document_type,
                   1 - (sv.vector <=> %s::vector) as similarity
            FROM documents d
            JOIN sparse_vectors sv ON d.id = sv.document_id
            ORDER BY sv.vector <=> %s::vector
            LIMIT %s
        """
        return self.fetch_all(query, (query_vector.tolist(), query_vector.tolist(), limit))
    
    def hybrid_search(self, dense_vector, sparse_vector, limit=10, dense_weight=0.5):
        query = """
            WITH dense_scores AS (
                SELECT d.id, d.title, d.content, d.source, d.document_type,
                       1 - (dv.vector <=> %s::vector) as dense_similarity
                FROM documents d
                JOIN dense_vectors dv ON d.id = dv.document_id
            ),
            sparse_scores AS (
                SELECT d.id, 1 - (sv.vector <=> %s::vector) as sparse_similarity
                FROM documents d
                JOIN sparse_vectors sv ON d.id = sv.document_id
            )
            SELECT 
                ds.id, ds.title, ds.content, ds.source, ds.document_type,
                (ds.dense_similarity * %s + ss.sparse_similarity * %s) as similarity
            FROM dense_scores ds
            JOIN sparse_scores ss ON ds.id = ss.id
            ORDER BY similarity DESC
            LIMIT %s
        """
        sparse_weight = 1 - dense_weight
        return self.fetch_all(query, (
            dense_vector.tolist(),
            sparse_vector.tolist(),
            dense_weight,
            sparse_weight,
            limit
        ))
    
    def close(self):
        self.cur.close()
        self.conn.close()