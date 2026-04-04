# Azure Deployment Guide — Project CV-02 Face Detection System

---

## Azure Services for Face Detection

### 1. Ready-to-Use AI (No Model Needed)

| Service                              | What it does                                                                 | When to use                                        |
|--------------------------------------|------------------------------------------------------------------------------|----------------------------------------------------|
| **Azure AI Face API**                | Detect faces, return bounding boxes, landmarks, age, emotions, attributes    | Replace your OpenCV DNN SSD pipeline               |
| **Azure AI Vision**                  | Detect faces as part of general image analysis                               | When you need face detection alongside other CV    |
| **Azure OpenAI Vision**              | GPT-4V for custom face analysis via prompt                                   | When you need custom face analysis logic           |

> **Azure AI Face API** is the direct replacement for your OpenCV DNN SSD pipeline. One API call returns bounding boxes + confidence + face attributes — no model weights needed.

### 2. Host Your Own Model (Keep Current Stack)

| Service                        | What it does                                                        | When to use                                           |
|--------------------------------|---------------------------------------------------------------------|-------------------------------------------------------|
| **Azure Container Apps**       | Run your 3 Docker containers (frontend, backend, cv-service)        | Best match for your current microservice architecture |
| **Azure Container Registry**   | Store your Docker images                                            | Used with Container Apps or AKS                       |

### 3. Frontend Hosting

| Service                   | What it does                                                               |
|---------------------------|----------------------------------------------------------------------------|
| **Azure Static Web Apps** | Host your React frontend — free tier available, auto CI/CD from GitHub     |

### 4. Supporting Services

| Service                       | Purpose                                                                  |
|-------------------------------|--------------------------------------------------------------------------|
| **Azure Blob Storage**        | Store uploaded images and annotated results                              |
| **Azure Key Vault**           | Store API keys and connection strings instead of .env files              |
| **Azure Monitor + App Insights** | Track detection latency, face counts, request volume                 |

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Azure Static Web Apps — React Frontend                     │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│  Azure Container Apps — Backend (FastAPI :8000)             │
└──────────────────────┬──────────────────────────────────────┘
                       │ Internal
        ┌──────────────┴──────────────┐
        │ Option A                    │ Option B
        ▼                             ▼
┌───────────────────┐    ┌────────────────────────────────────┐
│ Container Apps    │    │ Azure AI Face API                  │
│ CV Service :8001  │    │ Bounding boxes + attributes        │
│ OpenCV DNN SSD    │    │ No model weights needed            │
└───────────────────┘    └────────────────────────────────────┘
```

---

## Prerequisites

```bash
az login
az group create --name rg-face-detection --location uksouth
az extension add --name containerapp --upgrade
```

---

## Step 1 — Create Container Registry and Push Images

```bash
az acr create --resource-group rg-face-detection --name facedetectacr --sku Basic --admin-enabled true
az acr login --name facedetectacr
ACR=facedetectacr.azurecr.io
docker build -f docker/Dockerfile.cv-service -t $ACR/cv-service:latest ./cv-service
docker push $ACR/cv-service:latest
docker build -f docker/Dockerfile.backend -t $ACR/backend:latest ./backend
docker push $ACR/backend:latest
```

---

## Step 2 — Deploy Container Apps

```bash
az containerapp env create --name facedetect-env --resource-group rg-face-detection --location uksouth

az containerapp create \
  --name cv-service --resource-group rg-face-detection \
  --environment facedetect-env --image $ACR/cv-service:latest \
  --registry-server $ACR --target-port 8001 --ingress internal \
  --min-replicas 1 --max-replicas 3 --cpu 1 --memory 2.0Gi

az containerapp create \
  --name backend --resource-group rg-face-detection \
  --environment facedetect-env --image $ACR/backend:latest \
  --registry-server $ACR --target-port 8000 --ingress external \
  --min-replicas 1 --max-replicas 5 --cpu 0.5 --memory 1.0Gi \
  --env-vars CV_SERVICE_URL=http://cv-service:8001
```

---

## Option B — Use Azure AI Face API

```python
from azure.ai.vision.face import FaceClient
from azure.core.credentials import AzureKeyCredential

face_client = FaceClient(
    endpoint=os.getenv("AZURE_FACE_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_FACE_KEY"))
)

def detect_faces(image_bytes: bytes) -> dict:
    result = face_client.detect(
        image_content=image_bytes,
        detection_model="detection_03",
        return_face_attributes=["age", "emotion", "gender"]
    )
    faces = []
    for face in result:
        rect = face.face_rectangle
        faces.append({
            "confidence": 99.0,
            "bounding_box": {"left": rect.left, "top": rect.top, "width": rect.width, "height": rect.height},
            "age": face.face_attributes.age if face.face_attributes else None,
            "emotions": vars(face.face_attributes.emotion) if face.face_attributes else {}
        })
    return {"face_count": len(faces), "faces": faces}
```

Add to requirements.txt: `azure-ai-vision-face>=1.0.0b1`

---

## Estimated Monthly Cost

| Service                  | Tier      | Est. Cost         |
|--------------------------|-----------|-------------------|
| Container Apps (backend) | 0.5 vCPU  | ~$10–15/month     |
| Container Apps (cv-svc)  | 1 vCPU    | ~$15–20/month     |
| Container Registry       | Basic     | ~$5/month         |
| Static Web Apps          | Free      | $0                |
| Azure AI Face API        | F0 free   | $0 (30k calls)    |
| **Total (Option A)**     |           | **~$30–40/month** |
| **Total (Option B)**     |           | **~$15–20/month** |

For exact estimates → https://calculator.azure.com

---

## Teardown

```bash
az group delete --name rg-face-detection --yes --no-wait
```
