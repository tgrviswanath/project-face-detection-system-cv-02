# Project CV-02 - Face Detection System

Microservice CV system that detects faces in images using OpenCV DNN (SSD ResNet-10). Returns bounding boxes, confidence scores, and annotated image.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND  (React - Port 3000)                              │
│  axios POST /api/v1/detect                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP JSON
┌──────────────────────▼──────────────────────────────────────┐
│  BACKEND  (FastAPI - Port 8000)                             │
│  httpx POST /api/v1/cv/detect  →  calls cv-service          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP JSON
┌──────────────────────▼──────────────────────────────────────┐
│  CV SERVICE  (FastAPI - Port 8001)                          │
│  OpenCV DNN blobFromImage → SSD ResNet-10 forward pass      │
│  Returns { face_count, faces[], annotated_image (base64) }  │
└─────────────────────────────────────────────────────────────┘
```

---

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

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Frontend | React, MUI |
| Backend | FastAPI, httpx |
| CV | OpenCV DNN (SSD ResNet-10), Pillow |
| Model | Pretrained weights — auto-downloaded (~10MB) |
| Deployment | Docker, docker-compose |

---

## Prerequisites

- Python 3.12+
- Node.js — run `nvs use 20.14.0` before starting the frontend

---

## Local Run

### Step 1 — Start CV Service (Terminal 1)

```bash
cd cv-service
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
# Model weights auto-downloaded on first request (~10MB)
```

Verify: http://localhost:8001/health → `{"status":"ok"}`

### Step 2 — Start Backend (Terminal 2)

```bash
cd backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Verify: http://localhost:8000/health → `{"status":"ok"}`

### Step 3 — Start Frontend (Terminal 3)

```bash
cd frontend
npm install && npm start
```

Opens at: http://localhost:3000

---

## Environment Files

### `backend/.env`

```
APP_NAME=Face Detection API
APP_VERSION=1.0.0
ALLOWED_ORIGINS=["http://localhost:3000"]
CV_SERVICE_URL=http://localhost:8001
```

### `frontend/.env`

```
REACT_APP_API_URL=http://localhost:8000
```

---

## Docker Run

```bash
docker-compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API docs | http://localhost:8000/docs |
| CV Service docs | http://localhost:8001/docs |

---

## Run Tests

```bash
cd cv-service && venv\Scripts\activate
pytest ../tests/cv-service/ -v

cd backend && venv\Scripts\activate
pytest ../tests/backend/ -v
```

---

## Project Structure

```
project-face-detection-system-cv-02/
├── frontend/                    ← React (Port 3000)
├── backend/                     ← FastAPI (Port 8000)
│   └── app/
│       ├── api/routes.py
│       ├── core/service.py      ← httpx → cv-service
│       └── main.py
├── cv-service/                  ← FastAPI CV (Port 8001)
│   └── app/
│       ├── api/routes.py
│       ├── core/detector.py     ← OpenCV DNN SSD
│       └── main.py
├── samples/
├── tests/
├── docker/
└── docker-compose.yml
```

---

## API Reference

```
POST /api/v1/detect
Body:     { "image": "<base64>" }
Response: { "face_count": 2, "faces": [{ "confidence": 98.5, "bounding_box": {...} }], "annotated_image": "<base64>" }
```

---

## Dataset

Use any photo with faces — try LFW (Labeled Faces in the Wild) from Kaggle.
Model weights auto-downloaded from OpenCV GitHub on first run (~10MB).
