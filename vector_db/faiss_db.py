'''this file is for the FAISS database'''
# vector_db/faiss_db.py
import faiss
import numpy as np
import os
from ui.models import Chunk
from transformers import AutoTokenizer, AutoModel
from django.conf import settings
from typing import Optional, Tuple, Callable, List
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
        self.chunk_ids = []  # Store chunk IDs

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

    def add_chunk(self, chunk_id: int, vector: np.ndarray):
        if vector.shape[0] != self.dimension:
            raise ValueError(f"Vector dimension mismatch: {vector.shape[0]} != {self.dimension}")
        self.index.add(vector.reshape(1, -1).astype(np.float32))
        self.chunk_ids.append(chunk_id)

    def search_similar_chunks(self, query_vector: np.ndarray, k: int = 5):
        D, I = self.index.search(query_vector.reshape(1, -1).astype(np.float32), k)
        return [(self.chunk_ids[idx], dist) for dist, idx in zip(D[0], I[0])]

    def save(self, path: str):
        faiss.write_index(self.index, f"{path}.index")
        np.save(f"{path}.chunk_ids", self.chunk_ids)

    def load(self, path: str):
        self.index = faiss.read_index(f"{path}.index")
        self.chunk_ids = np.load(f"{path}.chunk_ids.npy").tolist()

class VectorDB:
    def __init__(self, dimension: int = 768):
        self.faiss_index = FAISSIndex(dimension)
        self.index_path = "faiss_index"

    def setUp(self):
        self.dimension = 768
        self.test_index_path = "test_faiss.index"
        self.db = VectorDB(dimension=self.dimension)
        self.test_vectors = np.random.rand(100, self.dimension).astype('float32')
        self.test_chunk_ids = list(range(100))


    def store_chunks(self, chunks: List[Chunk], batch_size: int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            for chunk in batch:
                vector = encode_chunk(chunk.chunk_txt)
                self.faiss_index.add_chunk(chunk.id, vector)
        self.faiss_index.save(self.index_path)

    def search_similar(self, query_text: str, k: int = 5):
        query_vector = encode_chunk(query_text)
        results = self.faiss_index.search_similar_chunks(query_vector, k)
        return [Chunk.objects.get(id=chunk_id) for chunk_id, _ in results]

def encode_chunk(chunk_text):
    '''Encode a chunk of text'''
    inputs = tokenizer(chunk_text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    vector = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return vector

#pylint: enable=E1120 E1101
