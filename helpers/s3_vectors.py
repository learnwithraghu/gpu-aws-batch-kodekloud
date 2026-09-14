"""Shared S3 Vectors operations for the video semantic-search lessons."""

from collections.abc import Iterable

CLIP_DIMENSION = 512
PUT_VECTORS_BATCH_SIZE = 500


def validate_embedding(vector) -> list[float]:
    """Return one finite, non-zero CLIP embedding as float32 values."""
    import numpy as np

    values = np.asarray(vector, dtype=np.float32).reshape(-1)
    if values.size != CLIP_DIMENSION:
        raise ValueError(f"Expected {CLIP_DIMENSION} dimensions, got {values.size}")
    if not np.isfinite(values).all():
        raise ValueError("Embeddings must contain only finite values")
    if not np.any(values):
        raise ValueError("Cosine-distance embeddings cannot be all zero")
    return values.tolist()


def frame_vector_record(
    video_stem: str,
    frame_key: str,
    frame_index: int,
    timestamp_ms: int,
    embedding,
) -> dict:
    """Build the S3 Vectors record and metadata used by Lesson 05."""
    return {
        "key": f"{video_stem}/frame_{frame_index:05d}",
        "data": {"float32": validate_embedding(embedding)},
        "metadata": {
            "video_stem": video_stem,
            "frame_key": frame_key,
            "frame_index": frame_index,
            "timestamp_ms": timestamp_ms,
        },
    }


def put_frame_vectors(client, vector_bucket: str, index_name: str, records: Iterable[dict]) -> int:
    """Upsert frame vectors in S3 Vectors' maximum supported request size."""
    records = list(records)
    for start in range(0, len(records), PUT_VECTORS_BATCH_SIZE):
        client.put_vectors(
            vectorBucketName=vector_bucket,
            indexName=index_name,
            vectors=records[start : start + PUT_VECTORS_BATCH_SIZE],
        )
    return len(records)