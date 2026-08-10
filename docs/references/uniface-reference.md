# UniFace — Reference Study

**Repo:** https://github.com/yakhyo/uniface
**Stars:** 1.2k | **Forks:** 156 | **License:** MIT

## What It Is
A unified face analysis library for Python: detection, alignment, landmarks, recognition, parsing, gaze, attributes, and anti-spoofing under one API.

## Capabilities
| Module | Models/Notes |
|---|---|
| Detection | SCRFD, RetinaFace, CenterFace, BlazeFace |
| Alignment | Based on 5-point landmarks |
| Landmarks | MediaPipe Face Mesh (468 3D points) |
| Recognition | ArcFace / insightface-based |
| Parsing | Face parsing / segmentation |
| Gaze | Gaze estimation |
| Attributes | FairFace, FaceAttribNet (age/gender/emotion/eyeglasses/mask/sunglasses) |
| Anti-Spoofing | MiniFASNet |
| Quality | eDifFIQA |
| Matting | MODNet |

## Architecture Pattern
- ONNX Runtime backend
- Unified `FaceAnalyzer` pipeline: detectors + predictors under one call
- Model registry + weight management
- Breaking change in v4.0.0: factory methods removed, direct class instantiation required

## Relevance to Our Ecosystem
- **Input layer diversity**: if we ever build local/desktop input, face analysis = hands-free gesture or presence detection
- **Pattern**: unified API over heterogeneous backends = same pattern as Agent Reach ordered routing
- **ONNX deployment**: lightweight, CPU-friendly, no GPU required for inference
- **Privacy**: on-device face analysis, no cloud upload

## Status
Reference only. Not directly applicable to current Personal AI OS stack unless we expand into local vision/desktop presence features.
