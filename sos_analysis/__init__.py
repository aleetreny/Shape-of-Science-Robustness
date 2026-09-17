"""Read-only access to audited embeddings. No scientific defaults or metrics."""

from .reader import EmbeddingCorpus, IntegrityError

__all__ = ["EmbeddingCorpus", "IntegrityError"]
