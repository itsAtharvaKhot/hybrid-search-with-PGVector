import pandas as pd
import time
from vector_models import VectorModels
from vector_store import VectorStore

class SearchEngine:
    def __init__(self):
        self.vector_models = VectorModels()
        self.vector_store = VectorStore(self.vector_models)
        self.documents_indexed = False
    
    def index_documents(self, documents_df):
        start_time = time.time()
        
        self.vector_models.fit_sparse_model(documents_df['content'].tolist())
        
        for _, row in documents_df.iterrows():
            document_id = self.vector_store.store_document(
                title=row['title'],
                content=row['content'],
                source=row['source'],
                document_type=row['document_type']
            )
            
            dense_embedding = self.vector_models.get_dense_embedding(row['content'])
            sparse_embedding = self.vector_models.get_sparse_embedding(row['content'])
            
            self.vector_store.store_dense_vector(document_id, dense_embedding)
            self.vector_store.store_sparse_vector(document_id, sparse_embedding)
        
        self.documents_indexed = True
    
    def search(self, query, search_type='hybrid', limit=10, dense_weight=0.5):
        if not self.documents_indexed:
            raise ValueError("Documents must be indexed before searching")
        
        if search_type == 'dense':
            return self.vector_store.dense_search(query, limit)
        elif search_type == 'sparse':
            return self.vector_store.sparse_search(query, limit)
        elif search_type == 'hybrid':
            return self.vector_store.hybrid_search(query, limit, dense_weight)
        else:
            raise ValueError(f"Unknown search type: {search_type}")
    
    def close(self):
        self.vector_store.close()