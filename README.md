# VehicleFlow — Vehicle Detection & Counting with OpenCV

A modern Python 3 rebuild of the original project. It uses classical computer vision to detect moving regions in fixed-camera traffic footage, track them across frames, and count unique tracks crossing a configurable virtual line.

> **Scope:** this is a motion-detection prototype, not a YOLO detector or production traffic surveillance system. Vehicle-size grouping uses bounding-box width as a heuristic, not semantic vehicle classification.

## Features
- Frame differencing, Gaussian blur, thresholding, and morphological cleanup.
- Contour-based moving-object proposals with configurable minimum area.
- Lightweight centroid association with predicted positions and missed-frame handling.
- Configurable horizontal counting line with up/down/both directions.
- Per-track de-duplication and optional width-based grouping.
- Streamlit upload interface, annotated preview, live metrics, count timeline, and CSV export.
- Unit tests and GitHub Actions workflow.

## Architecture
```text
Video upload → OpenCV → MotionDetector → CentroidTracker → LineCounter
                                              ↓
                              Streamlit preview, metrics, CSV report
```

## Quick start
Python 3.10 or 3.11 is recommended.
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Windows PowerShell:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Upload an MP4, AVI, MOV, or MKV clip, configure the line and thresholds, then start analysis.

## Tests
```bash
pytest -q
```
Tests cover track association, new-track creation, direction-aware line crossing, de-duplication, and width grouping.

## How it works
Consecutive frames are converted to grayscale and blurred. Their absolute difference is thresholded; morphology reduces isolated noise and joins nearby motion. Contours become bounding-box detections. A centroid tracker associates detections using predicted positions and a maximum distance. The line counter detects a direction-specific crossing and records each track once.

## Tuning
- Use a stationary camera with vehicles moving consistently through the frame.
- Place the line where vehicles are clearly separated.
- Increase minimum area to suppress noise; decrease it for distant objects.
- Tune tracker distance based on speed, frame rate, and frame stride.
- Processing every frame gives the best continuity.
- Width threshold depends on camera perspective and resolution; it is not a general vehicle classifier.

## Limitations
Frame differencing detects motion, not vehicles. Shadows, rain, camera shake, lighting changes, pedestrians, and overlapping objects can cause errors. Stationary vehicles disappear from motion detections. Greedy centroid association can swap identities in crowded scenes. This repository has not been evaluated against a labeled benchmark; no accuracy percentage is claimed.

A future version could add a pretrained object detector, class-aware tracking, perspective calibration, and evaluation on annotated traffic clips.

## Original assets
The original `Code` source and `IJRAR_Certificate_IJRAR_288114.pdf` are retained. The modern implementation lives in `vehicle_counter/` and `app.py`.

## Author
**Sunny Shrivas**
