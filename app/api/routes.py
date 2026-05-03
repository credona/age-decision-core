from uuid import uuid4

from fastapi import APIRouter, File, Header, Query, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.constants import (
    API_STATUS_OK,
    ERROR_EMPTY_FILE,
    ERROR_INVALID_REQUEST,
    ERROR_MISSING_FILE,
    ERROR_UNSUPPORTED_FILE_TYPE,
    LOG_EVENT_AGE_DECISION_FAILED,
    LOG_LEVEL_WARNING,
)
from app.api.input_validator import UnsupportedInputTypeError, validate_input_type
from app.api.response_filter import filter_decision_response
from app.application.dto.estimate_command import EstimateCommand
from app.application.use_cases.decision_pipeline import DecisionPipeline
from app.application.use_cases.get_model_status import GetEngineStatusUseCase
from app.application.use_cases.run_decision import RunDecisionUseCase
from app.infrastructure.logging.safe_logger import get_logger, log_event
from app.infrastructure.models.onnx_inference_engine import OnnxInferenceEngine
from app.infrastructure.vision.opencv_input_analyzer import OpenCvInputAnalyzer
from app.project import project_metadata
from app.schemas.decision import DecisionResponse
from app.schemas.error import ErrorResponse

router = APIRouter()

decision_pipeline = DecisionPipeline(
    inference_engine=OnnxInferenceEngine(),
    input_analyzer=OpenCvInputAnalyzer(),
)
run_decision_use_case = RunDecisionUseCase(decision_pipeline)
get_engine_status_use_case = GetEngineStatusUseCase(decision_pipeline)
logger = get_logger("age_decision_api")


@router.get("/health")
def health():
    return {
        "status": API_STATUS_OK,
        "service": project_metadata.service_name,
        "version": project_metadata.version,
        "contract_version": project_metadata.contract_version,
    }


@router.get("/version")
def version():
    return project_metadata.model_dump()


@router.get("/engine/status")
def model_status():
    return get_engine_status_use_case.execute()


@router.post(
    "/estimate",
    response_model=DecisionResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def estimate_age(
    file: UploadFile = File(...),
    age_threshold: int | None = Query(default=None),
    input_type: str = Query(default="image"),
    majority_country: str | None = Query(default=None),
    x_request_id: str | None = Header(default=None),
    x_correlation_id: str | None = Header(default=None),
):
    request_id, correlation_id = _resolve_request_identifiers(
        x_request_id=x_request_id,
        x_correlation_id=x_correlation_id,
    )

    try:
        validate_input_type(input_type)

        image_bytes = await file.read()

        result = await run_decision_use_case.execute(
            EstimateCommand(
                image_bytes=image_bytes,
                content_type=file.content_type,
                request_id=request_id,
                correlation_id=correlation_id,
                age_threshold=age_threshold,
                majority_country=majority_country,
            )
        )

        return filter_decision_response(result)

    except UnsupportedInputTypeError as exc:
        _log_error(
            request_id=request_id,
            correlation_id=correlation_id,
            error_type="validation_error",
            error_code="UNSUPPORTED_INPUT_TYPE",
        )

        return _error_response(
            status_code=400,
            request_id=request_id,
            correlation_id=correlation_id,
            code="UNSUPPORTED_INPUT_TYPE",
            message=str(exc),
        )

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


async def handle_request_validation_error(request: Request, exc: RequestValidationError):
    request_id, correlation_id = _resolve_request_identifiers(
        x_request_id=request.headers.get("x-request-id"),
        x_correlation_id=request.headers.get("x-correlation-id"),
    )
    error_code = _map_validation_error_code(exc.errors())

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


def _resolve_request_identifiers(
    x_request_id: str | None,
    x_correlation_id: str | None,
) -> tuple[str, str]:
    request_id = x_request_id or str(uuid4())
    correlation_id = x_correlation_id or request_id
    return request_id, correlation_id


def _map_value_error_code(message: str) -> str:
    normalized = message.lower()

    if "empty file" in normalized:
        return ERROR_EMPTY_FILE

    if "unsupported file type" in normalized:
        return ERROR_UNSUPPORTED_FILE_TYPE

    return ERROR_INVALID_REQUEST


def _map_validation_error_code(errors: list[dict]) -> str:
    for error in errors:
        loc = error.get("loc", ())
        error_type = error.get("type", "")

        if "file" in loc and error_type in {"missing", "value_error.missing"}:
            return ERROR_MISSING_FILE

    return ERROR_INVALID_REQUEST


def _log_error(
    request_id: str,
    correlation_id: str,
    error_type: str,
    error_code: str,
) -> None:
    log_event(
        logger,
        {
            "level": LOG_LEVEL_WARNING,
            "event": LOG_EVENT_AGE_DECISION_FAILED,
            "request_id": request_id,
            "correlation_id": correlation_id,
            "error_type": error_type,
            "error_code": error_code,
        },
    )
