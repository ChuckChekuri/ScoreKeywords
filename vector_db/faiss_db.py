'''this file is for the FAISS database'''
# vector_db/faiss_db.py
import faiss
import numpy as np
import os
from ui.models import Chunk
from transformers import AutoTokenizer, AutoModel
from django.conf import settings
from typing import Optional, Tuple, Callable
from numpy.typing import NDArray

# Initialize the tokenizer and model
default_model  = settings.TRANSFORMER_SETTINGS['models']['default']
tokenizer = AutoTokenizer.from_pretrained(default_model)
model = AutoModel.from_pretrained(default_model)

#pylint: disable=E1120 E1101
class FAISSIndex:
    """FAISS vector index wrapper for similarity search"""
    
    def __init__(self, dimension: int):
        """Initialize FAISS index
        
        Args:
            dimension: Vector dimension size
        """
        if dimension <= 0:
            raise ValueError("Dimension must be positive")
            
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self._total_vectors = 0

    def add_vectors(self, 
                   vectors: NDArray, 
                   batch_size: int = 1000,
                   progress_callback: Optional[Callable[[float], None]] = None) -> None:
        """Add vectors to index in batches
        
        Args:
            vectors: Numpy array of vectors to add
            batch_size: Number of vectors per batch
            progress_callback: Optional callback for progress updates
        """
        if not isinstance(vectors, np.ndarray):
            raise TypeError("Vectors must be numpy array")
            
        if vectors.shape[1] != self.dimension:
            raise ValueError(f"Vectors must have dimension {self.dimension}")

        total_vectors = len(vectors)
        for i in range(0, total_vectors, batch_size):
            batch = vectors[i:min(i + batch_size, total_vectors)]
            self.index.add(batch.astype(np.float32))
            self._total_vectors += len(batch)
            
            if progress_callback:
                progress = min((i + batch_size) / total_vectors, 1.0)
                progress_callback(progress)

    def search_vectors(self, 
                      query_vector: NDArray, 
                      k: int = 5) -> Tuple[NDArray, NDArray]:
        """Search for similar vectors
        
        Args:
            query_vector: Vector to search for
            k: Number of results to return
            
        Returns:
            Tuple of (distances, indices)
        """
        if len(query_vector.shape) == 1:
            query_vector = query_vector.reshape(1, -1)
            
        if query_vector.shape[1] != self.dimension:
            raise ValueError(f"Query vector must have dimension {self.dimension}")

        return self.index.search(query_vector.astype(np.float32), k)

    @property
    def ntotal(self) -> int:
        """Get total number of vectors in index"""
        return self._total_vectors

class VectorDB:
    def __init__(self, dimension=768):
        self.dimension = dimension
        self.faiss_index = FAISSIndex(dimension=self.dimension)
        self.index_path = "faiss_index.bin"
        if os.path.exists(self.index_path):
            self.load_index()

    def store_chunk_vectors(self, chunks):
        '''Store chunk vectors in the FAISS index'''
        vectors = []
        for chunk in chunks:
            vector = encode_chunk(chunk.chunk_txt)
            vectors.append(vector)
        vectors = np.vstack(vectors)
        self.faiss_index.add_vectors(vectors)
        self.save_index()

    def search_similar_chunks(self, query_text):
        '''Search for similar chunks to a query text'''
        query_vector = encode_chunk(query_text)
        distances, indices = self.faiss_index.search_vectors(query_vector)
        return distances, indices

    def save_index(self):
        '''Save FAISS index to disk'''
        faiss.write_index(self.faiss_index.index, self.index_path)

    def load_index(self):
        '''Load FAISS index from disk'''
        self.faiss_index.index = faiss.read_index(self.index_path)

def encode_chunk(chunk_text):
    '''Encode a chunk of text'''
    inputs = tokenizer(chunk_text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    vector = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return vector

#pylint: enable=E1120 E1101
