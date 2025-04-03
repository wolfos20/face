from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import logging
from src.predict import recognize_faces

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.post("/predict/")  # ✅ Ensure this matches your Postman URL
async def predict_face(file: UploadFile = File(...)):  # ✅ Correct syntax
    logging.info(f"Received file: {file.filename}, size: {file.size} bytes, type: {file.content_type}")

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)

    if nparr.size == 0:
        return {"error": "Uploaded file is empty or invalid."}

    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "Could not decode the image. Ensure it's a valid format (JPG, PNG)."}

    result = recognize_faces(image)
    return {"message": "Image received successfully", "result": result}

