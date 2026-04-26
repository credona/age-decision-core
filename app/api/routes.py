from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Header
from fastapi.responses import JSONResponse

from app.schemas.error import ErrorResponse
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


@router.post(
    "/estimate",
    response_model=AgeDecisionResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
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
        return _error_response(
            status_code=400,
            request_id=request_id,
            correlation_id=correlation_id,
            code=_map_value_error_code(str(exc)),
            message=str(exc),
        )

    except RuntimeError as exc:
        return _error_response(
            status_code=500,
            request_id=request_id,
            correlation_id=correlation_id,
            code="model_runtime_error",
            message=str(exc),
        )


def _error_response(
    status_code: int,
    request_id: str,
    correlation_id: str,
    code: str,
    message: str,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "request_id": request_id,
            "correlation_id": correlation_id,
            "error": {
                "code": code,
                "message": message,
            },
        },
    )


def _map_value_error_code(message: str) -> str:
    normalized = message.lower()

    if "empty file" in normalized:
        return "empty_file"

    if "unsupported file type" in normalized:
        return "unsupported_file_type"

    return "invalid_request"