import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

class VectorModels:
    def __init__(self):
        self.dense_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sparse_model = TfidfVectorizer(max_features=1000, stop_words='english')
        self.sparse_fitted = False
    
    def fit_sparse_model(self, documents):
        self.sparse_model.fit(documents)
        self.sparse_fitted = True
    
    def get_dense_embedding(self, text):
        embedding = self.dense_model.encode(text)
        return normalize(embedding.reshape(1, -1))[0]
    
    def get_sparse_embedding(self, text):
        if not self.sparse_fitted:
            raise ValueError("TF-IDF model must be fitted before generating embeddings")
        
        embedding = self.sparse_model.transform([text]).toarray()[0]
        return normalize(embedding.reshape(1, -1))[0]
    
    def normalize_vector(self, vector):
        return normalize(vector.reshape(1, -1))[0]