import numpy as np
import pandas as pd
from database import Database

class VectorStore:
    def __init__(self, vector_models=None):
        self.db = Database()
        self.vector_models = vector_models
    
    def store_document(self, title, content, source, document_type):
        return self.db.store_document(title, content, source, document_type)
    
    def store_dense_vector(self, document_id, vector):
        self.db.store_dense_vector(document_id, vector)
    
    def store_sparse_vector(self, document_id, vector):
        self.db.store_sparse_vector(document_id, vector)
    
    def dense_search(self, query, limit=10):
        query_vector = self._get_dense_embedding(query)
        results = self.db.dense_search(query_vector, limit)
        return self._format_results(results)
    
    def sparse_search(self, query, limit=10):
        query_vector = self._get_sparse_embedding(query)
        results = self.db.sparse_search(query_vector, limit)
        return self._format_results(results)
    
    def hybrid_search(self, query, limit=10, dense_weight=0.5):
        dense_vector = self._get_dense_embedding(query)
        sparse_vector = self._get_sparse_embedding(query)
        results = self.db.hybrid_search(dense_vector, sparse_vector, limit, dense_weight)
        return self._format_results(results)
    
    def _get_dense_embedding(self, text):
        if self.vector_models is None:
            from vector_models import VectorModels
            self.vector_models = VectorModels()
        return self.vector_models.get_dense_embedding(text)
    
    def _get_sparse_embedding(self, text):
        if self.vector_models is None:
            from vector_models import VectorModels
            self.vector_models = VectorModels()
        return self.vector_models.get_sparse_embedding(text)
    
    def _format_results(self, results):
        if not results:
            return pd.DataFrame()
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                'id': result[0],
                'title': result[1],
                'content': result[2],
                'source': result[3],
                'document_type': result[4] if len(result) > 4 else 'unknown',
                'similarity': result[5] if len(result) > 5 else 0.0
            })
        
        return pd.DataFrame(formatted_results)
    
    def close(self):
        self.db.close()