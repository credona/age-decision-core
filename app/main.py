from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routes import activate_runtime_calibration, handle_request_validation_error, router
from app.domain.calibration import RuntimeCalibrationPolicy
from app.infrastructure.calibration.runtime_activation import load_core_runtime_calibration
from app.project import project_metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    runtime_calibration = load_core_runtime_calibration()
    app.state.runtime_calibration = runtime_calibration
    activate_runtime_calibration(runtime_calibration)
    yield


app = FastAPI(
    title=project_metadata.app_name,
    version=project_metadata.version,
    lifespan=lifespan,
)

app.add_exception_handler(RequestValidationError, handle_request_validation_error)
app.include_router(router)


def get_runtime_calibration_state() -> RuntimeCalibrationPolicy | None:
    return app.state.runtime_calibration
