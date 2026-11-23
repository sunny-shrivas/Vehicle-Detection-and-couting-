'''Direction-aware virtual-line crossing counter.'''
from dataclasses import dataclass, field

@dataclass
class LineCounter:
    line_y: int
    direction: str = 'down'
    counted_track_ids: set[int] = field(default_factory=set)
    total: int = 0

    def update(self, tracks):
        new_ids = []
        for track in tracks:
            if track.track_id in self.counted_track_ids or len(track.history) < 2:
                continue
            previous_y, current_y = track.history[-2][1], track.history[-1][1]
            down = previous_y < self.line_y <= current_y
            up = previous_y > self.line_y >= current_y
            crossed = (self.direction == 'down' and down) or (self.direction == 'up' and up) or (self.direction == 'both' and (down or up))
            if crossed:
                self.counted_track_ids.add(track.track_id)
                self.total += 1
                new_ids.append(track.track_id)
        return new_ids

def classify_by_width(width, threshold=70):
    '''A size heuristic only; not semantic vehicle classification.'''
    return 'car_or_larger' if width > threshold else 'two_wheeler_or_smaller'
