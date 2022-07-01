from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from io import BytesIO
from PIL import Image
import numpy as np
import uvicorn
import requests
import json


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLASS_NAMES = ["crewmate", "impostor"]
THRESHOLD = 0.5

SERVER_URL = "http://localhost:8501/v1/models/mobilenetv2:predict"

@app.get("/ping")
async def ping():
    return "This server is alive!"


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)).convert("RGB"))
    return image


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    image_batch = np.expand_dims(image, 0)

    input_json_data = json.dumps({
        "signature_name": "serving_default",
        "instances": image_batch.tolist()
    })

    response = requests.post(SERVER_URL, data=input_json_data)

    raw_prediction = response.json()["predictions"][0][0]
    prediction = 1 if raw_prediction > THRESHOLD else 0
    class_name = CLASS_NAMES[prediction]
    confidence = (1 - raw_prediction) if prediction == 0 else raw_prediction

    return {
        "class": class_name,
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)





