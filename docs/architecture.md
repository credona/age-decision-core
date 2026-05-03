# Age Decision Core Architecture

## Scope

This document describes the internal architecture of the Core service.

The public API contract is frozen for v2.4.0. Internal refactoring must not add, remove or rename public response fields.

## Layers

app/
  api/
  application/
  domain/
  infrastructure/
  schemas/

## API layer

app/api contains FastAPI routing, request parsing, error mapping and public response filtering.

app/api/response_filter.py is the public contract barrier. Internal fields returned by application or infrastructure code must be ignored unless declared in the public schema.

## Application layer

app/application contains use cases, DTOs and ports.

It must not depend on FastAPI request objects. Input data must be passed through framework-neutral DTOs.

## Domain layer

app/domain contains pure decision logic:

- decision policy
- score calculation
- privacy metadata
- proof metadata
- country policy rules

Domain code must not import infrastructure, FastAPI, ONNX Runtime or OpenCV.

## Infrastructure layer

app/infrastructure contains technical adapters:

- ONNX age prediction
- OpenCV face detection and preprocessing
- runtime settings
- safe logging

Infrastructure may depend on external libraries, but must not own public API contract decisions.

## Schemas

app/schemas contains public API schemas.

Only fields declared in schemas may be exposed publicly.

## Dependency direction

api -> application -> domain
api -> infrastructure composition
application -> ports
infrastructure -> ports implementation

Domain must remain independent.

## Privacy rule

Internal values such as estimated age, confidence, raw scores and thresholds must never be exposed in public responses.

Public exposure remains limited to the existing contract.
