<h1>Age Decision Core Models</h1>

This document lists the models currently used by Age Decision Core.

It is intentionally separated from the main README to keep model transparency visible without overloading the repository entry page.

<hr>

<h2>Model binary policy</h2>

Model binaries are not intended to be committed to Git.

Model binaries are not intended to be embedded in the public Docker image by default.

Models should be downloaded explicitly when needed:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
```

Expected local structure:

```text
models/
  age_estimation/
    age-gender-prediction-ONNX.onnx
  face_detection/
    face_detection_yunet_2023mar.onnx
```

<hr>

<h2>Face detection</h2>

<h3>Model</h3>

```text
YuNet face detection model
```

Expected path:

```text
models/face_detection/face_detection_yunet_2023mar.onnx
```

<h3>Source</h3>

```text
OpenCV Zoo - YuNet face detection
https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet
```

<h3>License note</h3>

The model is distributed by the OpenCV Zoo project.

Before redistribution or commercial use, verify the current upstream license and model card.

<h3>Usage in this project</h3>

YuNet is used to detect face bounding boxes before age estimation.

The service does not use YuNet for identity recognition.

<hr>

<h2>Age estimation</h2>

<h3>Model</h3>

```text
age-gender-prediction-ONNX.onnx
```

Expected path:

```text
models/age_estimation/age-gender-prediction-ONNX.onnx
```

<h3>Source</h3>

```text
ONNX Community - age-gender-prediction-ONNX
https://huggingface.co/onnx-community/age-gender-prediction-ONNX
```

<h3>License note</h3>

The model page currently indicates an Apache 2.0 license.

Before redistribution or commercial use, verify the current upstream license, model source, and dataset provenance.

<h3>Supported output formats</h3>

The service supports several ONNX output shapes:

```text
[batch, 2]    age-gender style output
[batch, 1]    direct regression output
[batch, >=80] age distribution output
```

<h3>Related architecture reference</h3>

```text
MobileNetV2: Inverted Residuals and Linear Bottlenecks
https://arxiv.org/abs/1801.04381
```

<hr>

<h2>Model limitations</h2>

Age estimation is probabilistic.

The estimated age should not be interpreted as:

- real age proof
- identity proof
- legal verification
- document verification
- certified compliance result

Model behavior may vary depending on:

- image quality
- lighting
- face pose
- occlusion
- camera sensor
- compression
- demographic distribution
- domain shift

<hr>

<h2>Operational transparency</h2>

The `/model/status` endpoint exposes model runtime metadata.

It allows integrators to inspect:

- configured model paths
- loaded status
- model mode
- input metadata
- output metadata

<hr>

<h2>Redistribution checklist</h2>

Before redistributing model binaries, verify:

- upstream license
- model source
- dataset provenance
- intended use
- redistribution terms
- attribution requirements
- commercial usage terms
- model card updates

<hr>

<h2>Current project stance</h2>

Age Decision Core documents supported model paths and provides a download script.

The repository should not rely on committed model binaries.

The public Docker image should remain application-focused and should not include ONNX model binaries by default.

This keeps the repository lighter, improves transparency, and avoids silently redistributing third-party model files.
