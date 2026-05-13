"""Embedding service wrapper."""


class EmbeddingsService:
    def embed(self, text: str) -> list[float]:
        return [float(len(text))]
