'''Composable vehicle-counting pipeline.'''
from .counting import LineCounter, classify_by_width
from .detector import MotionDetector
from .tracker import CentroidTracker

class VehicleCountingPipeline:
    def __init__(self, line_y, min_area=650, max_distance=75, direction='down', width_threshold=70):
        self.detector = MotionDetector(min_area=min_area)
        self.tracker = CentroidTracker(max_distance=max_distance)
        self.counter = LineCounter(line_y=line_y, direction=direction)
        self.width_threshold = width_threshold
        self.large_count = 0
        self.small_count = 0

    def process(self, frame):
        detections, mask = self.detector.detect(frame)
        tracks = self.tracker.update(detections)
        crossed_ids = self.counter.update(tracks)
        for track_id in crossed_ids:
            width = self.tracker.tracks[track_id].bbox[2]
            if classify_by_width(width, self.width_threshold) == 'car_or_larger':
                self.large_count += 1
            else:
                self.small_count += 1
        return tracks, mask, crossed_ids
