import numpy as np
from keras_facenet import FaceNet
import cv2

facenet = FaceNet()

def extract_embeddings(image, face_box):
    """Extract FaceNet embeddings for a given face box."""
    x, y, w, h = face_box
    face = image[y:y+h, x:x+w]
    face = cv2.resize(face, (160, 160))  # Required input size for FaceNet
    face = np.expand_dims(face, axis=0)

    embeddings = facenet.embeddings(face)
    return embeddings
