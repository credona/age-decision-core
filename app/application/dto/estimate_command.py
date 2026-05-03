from dataclasses import dataclass


@dataclass(frozen=True)
class EstimateCommand:
    image_bytes: bytes
    content_type: str | None
    request_id: str
    correlation_id: str
    age_threshold: int | None
    majority_country: str | None
