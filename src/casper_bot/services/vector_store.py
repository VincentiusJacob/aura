"""Vector store wrapper."""


class VectorStore:
    def upsert(self, key: str, vector: list[float]) -> dict[str, object]:
        return {"key": key, "dimensions": len(vector)}
