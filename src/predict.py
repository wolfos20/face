import pickle
import numpy as np
from scipy.spatial.distance import euclidean
from src.feature_extractor import extract_embeddings
from sklearn.preprocessing import LabelEncoder
import cv2 as cv
from mtcnn import MTCNN
from keras_facenet import FaceNet

facenet = FaceNet()
detector = MTCNN()
# Load trained SVM model & embeddings
model = pickle.load(open("models/svm2025.pkl", "rb"))
data = np.load("models/emb2025.npz")
X_known, Y_known = data["EMBEDDED_X"], data["Y"]

encoder = LabelEncoder()
encoder.fit(Y_known)

def recognize_faces(image):
    """Recognize faces in an OpenCV image."""
    print("Running face recognition...")
    recognized_names = []

    # Convert image to RGB (OpenCV loads in BGR format)
    rgb_img = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    # Detect faces using MTCNN
    faces = detector.detect_faces(rgb_img)

    if not faces:
        print("No faces detected.")
        return {"message": "No faces detected.", "recognized_faces": []}

    i = 0
    for face in faces:
        x, y, w, h = face['box']
        x, y = max(0, x), max(0, y)  # Ensure values are positive

        img = rgb_img[y:y+h, x:x+w]
        img = cv.resize(img, (160, 160))  # Resize for FaceNet
        img = np.expand_dims(img, axis=0)

        # Extract face embeddings
        ypred = facenet.embeddings(img)

        if np.all(ypred == 0):
            print(f"Invalid embeddings for face at ({x}, {y}). Skipping.")
            continue

        # Predict face identity
        face_name = model.predict(ypred)
        final_name = encoder.inverse_transform(face_name)[0]

        # Compute distance from known embeddings
        distances = [euclidean(ypred.flatten(), known_emb) for known_emb in X_known]
        min_distance = min(distances)

        # Define threshold
        threshold = 0.78

        if min_distance < threshold:
            recognized_names.append(final_name)
            print(f"✔ Recognized: {final_name} (Distance: {min_distance:.2f})")
        else:
            recognized_names.append(f"Unknown_{i}")
            print(f"❌ Unknown face rejected (Distance: {min_distance:.2f})")
            i += 1

    return recognized_names

