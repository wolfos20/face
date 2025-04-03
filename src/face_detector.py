import cv2
from mtcnn import MTCNN

detector = MTCNN()

def detect_faces(image):
    """Detect faces in an image using MTCNN."""
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb_img)
    
    face_boxes = [face['box'] for face in faces]
    return face_boxes
