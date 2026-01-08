import time

from Detector.Face.face_landmarks import get_landmark_model, detect_marks
from Detector.Face.face_detector import get_face_detector, find_faces
from Tracker.eye_tracker import eye_tracker

from tkinter import messagebox


class Proctoring:
    def __init__(self):
        self.face_model = get_face_detector()
        self.landmark_model = get_landmark_model()
        self.timestamp = None
        self.detections = 0

    def process(self, image):
        if self.timestamp is None:
            self.timestamp = time.time()
        elif (time.time()-self.timestamp) > 5:
            print(self.detections)
            self.timestamp = time.time()
            faces = find_faces(image, self.face_model)
            for face in faces:
                marks = detect_marks(image, self.landmark_model, face)
                if eye_tracker(image, marks):
                    self.detections += 1
        if self.detections == 5:
            messagebox.showwarning('Warning', 'Possible plagiarism detected')
            self.detections = 0
            return True