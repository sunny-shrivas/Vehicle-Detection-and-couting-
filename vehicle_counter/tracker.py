'''Lightweight centroid tracker for motion-detection bounding boxes.'''
from __future__ import annotations
from dataclasses import dataclass, field
from math import hypot
from typing import Iterable

@dataclass
class Track:
    track_id: int
    bbox: tuple[int, int, int, int]
    center: tuple[int, int]
    history: list[tuple[int, int]] = field(default_factory=list)
    missed_frames: int = 0

    def update(self, bbox):
        self.bbox = bbox
        x, y, w, h = bbox
        self.center = (x + w // 2, y + h // 2)
        self.history.append(self.center)
        self.history = self.history[-12:]
        self.missed_frames = 0

    def predicted_center(self):
        if len(self.history) < 2:
            return self.center
        x1, y1 = self.history[-2]
        x2, y2 = self.history[-1]
        return (x2 + x2 - x1, y2 + y2 - y1)

class CentroidTracker:
    '''Greedy nearest-centroid tracker for sparse, fixed-camera scenes.'''
    def __init__(self, max_distance=70.0, max_missed=8):
        if max_distance <= 0 or max_missed < 0:
            raise ValueError('Invalid tracker configuration')
        self.max_distance = float(max_distance)
        self.max_missed = int(max_missed)
        self.tracks = {}
        self.next_id = 1

    def update(self, detections: Iterable[tuple[int, int, int, int]]):
        boxes = list(detections)
        unmatched = set(self.tracks)
        assigned = set()
        pairs = []
        for index, bbox in enumerate(boxes):
            x, y, w, h = bbox
            center = (x + w // 2, y + h // 2)
            candidates = []
            for track_id in unmatched:
                px, py = self.tracks[track_id].predicted_center()
                distance = hypot(center[0] - px, center[1] - py)
                if distance <= self.max_distance:
                    candidates.append((distance, track_id))
            if candidates:
                _, track_id = min(candidates)
                pairs.append((index, track_id))
                unmatched.remove(track_id)
                assigned.add(index)
        for index, track_id in pairs:
            self.tracks[track_id].update(boxes[index])
        for track_id in list(unmatched):
            self.tracks[track_id].missed_frames += 1
            if self.tracks[track_id].missed_frames > self.max_missed:
                del self.tracks[track_id]
        for index, bbox in enumerate(boxes):
            if index not in assigned:
                x, y, w, h = bbox
                center = (x + w // 2, y + h // 2)
                self.tracks[self.next_id] = Track(self.next_id, bbox, center, [center])
                self.next_id += 1
        return list(self.tracks.values())
