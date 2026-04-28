from fastapi import FastAPI

from app.api.routes import router
from app.project import project_metadata

app = FastAPI(
    title=project_metadata.app_name,
    version=project_metadata.version,
)

app.include_router(router)
