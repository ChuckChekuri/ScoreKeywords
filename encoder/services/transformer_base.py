from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModel, RobertaModel, BertModel, AlbertModel
from ..interfaces.base_encoder import BaseEncoder
from .pooling import MeanPooling
import numpy as np
from django.conf import settings

class TransformerEncoderBase(BaseEncoder):
    """Encodes text using transformer models."""
    def __init__(self, model_name: str = 'albert-base-v2'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        """Initialize the transformer encoder."""
        # Error messages
        self.EMPTY_INPUT_ERROR = "Input text cannot be empty or whitespace only"
        config = settings.TRANSFORMER_SETTINGS['models'][model_name]
        cache_dir = settings.TRANSFORMER_SETTINGS['cache_dir']
        self.cache_dir = Path(cache_dir+'/'+ model_name)


        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=self.cache_dir
        )
        self.model = AutoModel.from_pretrained(
            model_name,
            cache_dir=self.cache_dir
        ).to(self.device)

        self.pooling = MeanPooling()
        self.dimension = config['dimension']
        self.batch_size = config['batch_size']

    def encode_text(self, text: str) -> np.ndarray:
        """
        Encode a single text string.
        
        Args:
            text: Input text to encode
            
        Returns:
            np.ndarray: Encoded text vector
            
        Raises:
            ValueError: If input text is empty or whitespace only
        """
        if not text or not text.strip():
            raise ValueError(self.EMPTY_INPUT_ERROR)

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).cpu().numpy()[0]

    def encode_batch(self, texts: list[str]) -> np.ndarray:
        if not texts:
            raise ValueError(self.EMPTY_INPUT_ERROR)
        inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        #inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).cpu().numpy()

    def dimension(self) -> int:
        return self._dimension

class BertEncoder(TransformerEncoderBase):
    def __init__(self, model_name: str = 'bert-base-uncased'):
        super().__init__(model_name)
        self.model = BertModel.from_pretrained(
            model_name,
            output_hidden_states=True,
            cache_dir=self.cache_dir
        )
        if hasattr(self.model, 'pooler'):
            self.model.pooler.dense.weight.data.normal_(mean=0.0, std=0.02)
            self.model.pooler.dense.bias.data.zero_()
        self.model.to(self.device)

class AlbertEncoder(TransformerEncoderBase):
    def __init__(self, model_name: str = 'albert-base-v2'):
        super().__init__(model_name)
        self.model = AlbertModel.from_pretrained(
            model_name,
            output_hidden_states=True,
            cache_dir=self.cache_dir
        )
        # Albert uses a simple Linear layer as pooler
        if hasattr(self.model, 'pooler'):
            self.model.pooler.weight.data.normal_(mean=0.0, std=0.02)
            self.model.pooler.bias.data.zero_()
        self.model.to(self.device)

class RobertaEncoder(TransformerEncoderBase):
    def __init__(self, model_name: str = 'roberta-base'):
        super().__init__(model_name)
        self.model = RobertaModel.from_pretrained(
            model_name,
            output_hidden_states=True,
            cache_dir=self.cache_dir
        )
        # Move model to correct device without custom initialization
        self.model.to(self.device)
        
        # Validate model loaded correctly
        if not hasattr(self.model, 'pooler'):
            raise ValueError(f"Model {model_name} does not have expected pooler layer")
