"""
Model Asset Loader and Offline Cache Contract
Manages local disk cache contracts for NLP models (spaCy, sentence-transformers/MiniLM)
without performing automated internet downloads during phase 1 foundation setup.
"""

import os
from pathlib import Path
from typing import Dict, Any


class ModelRegistry:
    """Registry maintaining metadata and local paths for offline NLP models."""

    def __init__(self, cache_dir: str = "/app/models/cache"):
        self.cache_dir = Path(cache_dir)

    def is_cache_available(self) -> bool:
        """Check if the designated model cache directory exists."""
        return self.cache_dir.exists() and self.cache_dir.is_dir()

    def get_model_status(self) -> Dict[str, Any]:
        """
        Inspect local cache for pre-cached model assets.
        Returns status dictionary without attempting network operations.
        """
        return {
            "cache_directory": str(self.cache_dir),
            "cache_exists": self.is_cache_available(),
            "spacy_available": (self.cache_dir / "spacy").exists() if self.is_cache_available() else False,
            "minilm_available": (self.cache_dir / "minilm").exists() if self.is_cache_available() else False,
            "runtime_mode": "offline-contract",
        }
