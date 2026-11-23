# Vehicle Detection and Counting with OpenCV

A legacy computer-vision prototype for detecting and tracking moving vehicles in a video stream and counting vehicles as they cross configured virtual lines.

The implementation uses classical image-processing and contour-tracking techniques rather than a trained deep-learning detector.

## How it works

The source code in `Code` follows this processing flow:

1. Read consecutive frames from a video source using OpenCV.
2. Convert frames to grayscale and apply Gaussian blur.
3. Compute the absolute difference between consecutive frames.
4. Apply thresholding and morphological operations to reduce noise.
5. Extract contours and create candidate vehicle blobs using geometric filters.
6. Match current-frame blobs with previously tracked blobs using predicted center positions.
7. Detect when tracked objects cross configured horizontal lines.
8. Update and display vehicle-count overlays and frame information.

The original script also contains width-based logic to separate larger vehicle detections from a second, smaller-vehicle count. These thresholds are tied to the original camera/video setup and may need calibration for other footage.

## Technology

- Python (legacy Python 2-era source syntax)
- OpenCV
- NumPy

## Repository contents

- `Code` — original vehicle detection, blob tracking, and line-crossing implementation.
- `IJRAR_Certificate_IJRAR_288114.pdf` — certificate document included with the project.

## Important compatibility note

This is an older implementation and is **not ready to run unchanged in a modern Python 3 environment**. The source contains Python 2 print syntax and uses an older OpenCV contour-return convention. It also sets the video filename and line coordinates directly in the script.

Before running it in a current environment, the code needs to be ported to Python 3, updated for the installed OpenCV API, and configured with a valid video path and calibrated counting lines. No current Python/OpenCV version or successful modern-environment run is claimed here.

## Known limitations

- Motion detection by frame differencing can be affected by lighting changes, shadows, camera movement, and stationary vehicles.
- Blob matching is a simple position-prediction approach and can lose identity when objects overlap or move close together.
- Vehicle size thresholds and line coordinates are camera-specific.
- The implementation does not use a modern object detector or robust multi-object tracking framework.
- The code is a video-analysis prototype, not a production traffic-monitoring system.

## Potential improvements

- Port the script to Python 3 and current OpenCV APIs.
- Move video paths, line positions, and thresholds into configuration.
- Add sample input video and reproducible setup instructions.
- Evaluate counting accuracy on annotated clips.
- Compare classical motion detection with object-detection and tracking approaches.
- Add tests for line-crossing and counting logic.

## Author

**Sunny Shrivas**
