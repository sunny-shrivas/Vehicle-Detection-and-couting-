from vehicle_counter.counting import LineCounter, classify_by_width
from vehicle_counter.tracker import CentroidTracker

def test_tracker_keeps_identity():
    tracker = CentroidTracker(max_distance=50)
    first = tracker.update([(10, 10, 20, 20)])
    second = tracker.update([(12, 18, 20, 20)])
    assert first[0].track_id == second[0].track_id
    assert len(tracker.tracks) == 1

def test_far_detection_creates_new_track():
    tracker = CentroidTracker(max_distance=20)
    tracker.update([(0, 0, 10, 10)])
    tracker.update([(100, 100, 10, 10)])
    assert len(tracker.tracks) == 2

def test_counts_downward_crossing_once():
    tracker = CentroidTracker(max_distance=50)
    counter = LineCounter(50, 'down')
    tracks = tracker.update([(10, 20, 20, 20)])
    assert counter.update(tracks) == []
    tracks = tracker.update([(10, 42, 20, 20)])
    assert counter.update(tracks) == [1]
    tracks = tracker.update([(10, 48, 20, 20)])
    assert counter.update(tracks) == []
    assert counter.total == 1

def test_direction_is_respected():
    tracker = CentroidTracker(max_distance=80)
    counter = LineCounter(50, 'down')
    tracker.update([(10, 60, 20, 20)])
    tracks = tracker.update([(10, 20, 20, 20)])
    assert counter.update(tracks) == []

def test_width_grouping_is_a_heuristic():
    assert classify_by_width(71, 70) == 'car_or_larger'
    assert classify_by_width(70, 70) == 'two_wheeler_or_smaller'
