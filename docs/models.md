<h1>Age Decision Core Models</h1>

This document lists the models currently used by Age Decision Core.

It is intentionally separated from the main README to keep model transparency visible without overloading the repository entry page.

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

<h3>Reference</h3>

```text
OpenCV Zoo - YuNet face detection
https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet
```

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

<h2>Model files</h2>

Model files may be large and may have independent upstream licenses.

Before redistribution or commercial use, verify:

- upstream license
- model source
- dataset provenance
- intended use
- redistribution terms
