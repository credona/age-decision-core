from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from app.domain.models.metadata import ModelMetadata
from app.infrastructure.models.registry import (
    StaticModelRegistry,
    build_default_model_registry,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for chunk in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def build_private_scientific_model_identity(
    *,
    registry: StaticModelRegistry | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """
    Build the private scientific identity of the configured Core models.

    Model paths are used only to hash the exact runtime artifacts and are
    deliberately excluded from the returned identity.
    """
    resolved_registry = (
        registry
        if registry is not None
        else build_default_model_registry()
    )
    resolved_root = (
        root
        if root is not None
        else Path.cwd()
    )

    models = []

    for model in resolved_registry.models.values():
        models.append(
            _build_model_identity(
                model=model,
                root=resolved_root,
            )
        )

    models.sort(
        key=lambda model: (
            model["model_id"],
            model["model_version"],
            model["sha256"],
        )
    )

    return {
        "models": models,
    }


def _build_model_identity(
    *,
    model: ModelMetadata,
    root: Path,
) -> dict[str, str]:
    model_path = Path(model.path)

    if not model_path.is_absolute():
        model_path = root / model_path

    if not model_path.is_file():
        raise FileNotFoundError(
            f"configured model artifact does not exist: {model.model_id}"
        )

    return {
        "model_id": model.model_id,
        "model_version": model.model_version,
        "task": model.task,
        "sha256": sha256_file(model_path),
    }
