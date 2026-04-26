from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Header

from app.schemas.estimate import AgeDecisionResponse
from app.services.age_estimation_service import AgeEstimationService

router = APIRouter()

age_estimation_service = AgeEstimationService()

@router.get("/health")
def health():
    return {"status": "ok", "service": "age-decision-core"}


@router.get("/model/status")
def model_status():
    return age_estimation_service.get_model_status()


@router.post("/estimate", response_model=AgeDecisionResponse)
async def estimate_age(
    file: UploadFile = File(...),
    age_threshold: int | None = Query(default=None),
    age_margin: int | None = Query(default=None),
    confidence_threshold: float | None = Query(default=None),
    country: str | None = Query(default=None),
    x_request_id: str | None = Header(default=None),
    x_correlation_id: str | None = Header(default=None),
):
    request_id = x_request_id or str(uuid4())
    correlation_id = x_correlation_id or request_id

    try:
        result = await age_estimation_service.estimate(
            file=file,
            request_id=request_id,
            correlation_id=correlation_id,
            age_threshold=age_threshold,
            age_margin=age_margin,
            confidence_threshold=confidence_threshold,
            country=country,
        )

        return AgeDecisionResponse(**result)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))