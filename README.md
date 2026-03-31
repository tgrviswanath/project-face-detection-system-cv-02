# Project 02 - Face Detection System (CV)

Detect faces in images using OpenCV DNN (SSD ResNet-10). Returns bounding boxes, confidence scores, and annotated image.

## Architecture

```
Frontend :3000  →  Backend :8000  →  CV Service :8001
  React/MUI        FastAPI/httpx      FastAPI/OpenCV DNN
```

## How It Works

```
Image uploaded
    ↓
OpenCV DNN blobFromImage (300×300, mean subtraction)
    ↓
SSD ResNet-10 forward pass
    ↓
Filter detections by confidence threshold (0.5)
    ↓
Draw bounding boxes on annotated image
    ↓
Return: face_count + faces[] + annotated_image (base64)
```

## What's Different from Project 01

| | Project 01 (Classification) | Project 02 (Face Detection) |
|---|---|---|
| Task | Classify whole image | Locate faces in image |
| Model | SVM (trained) | OpenCV DNN SSD (pretrained) |
| Output | Single label + confidence | Bounding boxes + annotated image |
| Training | Required (train.py) | Not required (pretrained weights) |

## Local Run

```bash
# Terminal 1 - CV Service (models auto-downloaded on first request)
cd cv-service && python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

# Terminal 2 - Backend
cd backend && python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 3 - Frontend
cd frontend && npm install && npm start
```

- CV Service docs: http://localhost:8001/docs
- Backend docs:   http://localhost:8000/docs
- UI:             http://localhost:3000

## Docker

```bash
docker-compose up --build
```

## Dataset
Use any photo with faces — try LFW (Labeled Faces in the Wild) from Kaggle.
Model weights auto-downloaded from OpenCV GitHub on first run (~10MB).
