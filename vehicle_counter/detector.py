'''OpenCV frame-difference detector for fixed-camera videos.'''
import cv2

class MotionDetector:
    def __init__(self, min_area=650, threshold=25, blur_size=5):
        if min_area < 1 or threshold < 0 or blur_size < 3 or blur_size % 2 == 0:
            raise ValueError('Invalid detector configuration')
        self.min_area, self.threshold, self.blur_size = min_area, threshold, blur_size
        self.previous_gray = None
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (self.blur_size, self.blur_size), 0)
        if self.previous_gray is None:
            self.previous_gray = gray
            return [], gray * 0
        diff = cv2.absdiff(self.previous_gray, gray)
        self.previous_gray = gray
        _, mask = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel, iterations=1)
        mask = cv2.dilate(mask, self.kernel, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for contour in contours:
            if cv2.contourArea(contour) >= self.min_area:
                x, y, w, h = cv2.boundingRect(contour)
                if w >= 18 and h >= 18:
                    boxes.append((x, y, w, h))
        return boxes, mask
