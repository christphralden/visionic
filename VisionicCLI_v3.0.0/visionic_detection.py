import face_recognition
import os
import cv2
import numpy as np
import math
import time
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

TRAINING_PATH = 'faces'
CAPTURE_INTERVAL = 0.3
CAPTURE_DURATION = 20
MATCH_THRESHOLD = 0.4

# yolo_model = YOLO('yolov8n.pt')
def face_confidence(face_distance, face_match_thresh=MATCH_THRESHOLD):
    range = (1.0 - face_match_thresh)
    linear_value = (1.0-face_distance)/(range*2.0)

    if face_distance > face_match_thresh:
        return str(round(linear_value*100,2)) + '%'
    else:
        value = (linear_value + ((1.0-linear_value)*math.pow((linear_value-0.5)*2,0.2)))*100
        return str(round(value,2))+'%'
    
class VisionicDetection:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.encode_faces()
        self.process_current_frame = True

    def train_new_person(self, video_capture):
        person_name = input("Enter the name of the new person: ")
        person_path = os.path.join(TRAINING_PATH, person_name)
        os.makedirs(person_path, exist_ok=True)

        start_time = time.time()
        while time.time() - start_time < CAPTURE_DURATION:
            ret, frame = video_capture.read()
            if not ret:
                break

            cv2.imshow('Visionic', frame)

            if int((time.time() - start_time) / CAPTURE_INTERVAL) != int((time.time() - start_time - 0.1) / CAPTURE_INTERVAL):
                img_name = os.path.join(person_path, f"{int(time.time() - start_time)}.jpg")
                cv2.imwrite(img_name, frame)

            if cv2.waitKey(1) == ord('q'):
                break

        self.encode_faces(person_name)
        
    def encode_faces(self, new_person=None):
        persons_to_encode = [new_person] if new_person else os.listdir(TRAINING_PATH)

        for person in persons_to_encode:
            person_path = os.path.join(TRAINING_PATH, person)
            if not os.path.isdir(person_path):
                continue

            for image in os.listdir(person_path):
                if not image.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                face_image_path = os.path.join(person_path, image)
                face_image = face_recognition.load_image_file(face_image_path)
                face_encodings = face_recognition.face_encodings(face_image)
                if face_encodings:
                    self.known_face_encodings.extend(face_encodings)
                    self.known_face_names.extend([person] * len(face_encodings))

        if not new_person:
            print(self.known_face_names)
    
    def process_frame(self,frame):
        try:
            # results = yolo_model(frame, conf=MATCH_THRESHOLD)
            recognition_info = ""

            # for r in results:
            annotator = Annotator(frame)

            #     boxes = r.boxes
            #     for box in boxes:
            #         b = box.xyxy[0]
            #         c = box.cls
            #         annotator.box_label(b, yolo_model.names[int(c)])

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            best_matches = {}
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            for face_encoding, (top, right, bottom, left) in zip(self.face_encodings, self.face_locations):
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if face_distances[best_match_index] < MATCH_THRESHOLD: 
                    name = self.known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

                    if name not in best_matches or best_matches[name]['confidence'] < confidence:
                        best_matches[name] = {'confidence': confidence, 'face_rect': (top, right, bottom, left)}

            for name, info in best_matches.items():
                top, right, bottom, left = info['face_rect']
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                label = f"{name}: {info['confidence']}"
                annotator.box_label([left, top, right, bottom], label, color=(0, 255, 0))

                recognition_info += f"{label}\n"

            processed_frame = annotator.result()
            return processed_frame, recognition_info
        except Exception as e:
            print(f"Error during frame processing: {e}")
            return frame, f"Error: {e}" 

