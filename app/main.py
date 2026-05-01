from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routes import handle_request_validation_error, router
from app.project import project_metadata

app = FastAPI(
    title=project_metadata.app_name,
    version=project_metadata.version,
)

app.add_exception_handler(RequestValidationError, handle_request_validation_error)
app.include_router(router)
