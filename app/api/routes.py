from uuid import uuid4

from fastapi import APIRouter, File, Header, Query, UploadFile
from fastapi.responses import JSONResponse

from app.project import project_metadata
from app.schemas.error import ErrorResponse
from app.schemas.estimate import AgeDecisionResponse
from app.services.age_estimation_service import AgeEstimationService
from app.utils.logger import get_logger, log_event

router = APIRouter()

age_estimation_service = AgeEstimationService()
logger = get_logger("age_decision_api")


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": project_metadata.service_name,
        "version": project_metadata.version,
        "contract_version": project_metadata.contract_version,
    }


@router.get("/version")
def version():
    return project_metadata.model_dump()


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
    majority_country: str | None = Query(default=None),
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
            majority_country=majority_country,
        )

        return AgeDecisionResponse(**result)

    except ValueError as exc:
        error_code = _map_value_error_code(str(exc))

        _log_error(
            request_id=request_id,
            correlation_id=correlation_id,
            error_type="validation_error",
            error_code=error_code,
        )

        return _error_response(
            status_code=400,
            request_id=request_id,
            correlation_id=correlation_id,
            code=error_code,
            message="Invalid request.",
        )

    except RuntimeError:
        _log_error(
            request_id=request_id,
            correlation_id=correlation_id,
            error_type="runtime_error",
            error_code="model_runtime_error",
        )

        return _error_response(
            status_code=500,
            request_id=request_id,
            correlation_id=correlation_id,
            code="model_runtime_error",
            message="An internal error has occurred.",
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


def _log_error(
    request_id: str,
    correlation_id: str,
    error_type: str,
    error_code: str,
) -> None:
    log_event(
        logger,
        {
            "level": "warning",
            "event": "age_decision_failed",
            "request_id": request_id,
            "correlation_id": correlation_id,
            "error_type": error_type,
            "error_code": error_code,
        },
    )
