from abc import ABC, abstractmethod
import numpy as np
from typing import List, Union

class BaseEncoder(ABC):
    """Base class for text encoding implementations"""

    @abstractmethod
    def encode_text(self, text: str) -> np.ndarray:
        """Encode a single text string into a vector representation
        
        Args:
            text (str): Text to encode
            
        Returns:
            np.ndarray: Vector representation of the text
        """

    @abstractmethod
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Encode multiple texts into vector representations
        
        Args:
            texts (List[str]): List of texts to encode
            
        Returns:
            np.ndarray: Matrix of vector representations
        """

    @abstractmethod
    def dimension(self) -> int:
        """Get the dimension of the encoded vectors
        
        Returns:
            int: Dimension of encoded vectors
        """
