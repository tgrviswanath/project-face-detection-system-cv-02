"""
Face detection using OpenCV DNN (SSD ResNet-10).
- Detects faces in uploaded images
- Returns bounding boxes, confidence scores
- Returns annotated image as base64 PNG
"""
import cv2
import numpy as np
from PIL import Image
import io
import base64
from app.core.config import settings
from app.core.downloader import download_models

_net = None


def _get_net():
    global _net
    if _net is None:
        try:
            download_models(settings.PROTOTXT_PATH, settings.CAFFEMODEL_PATH)
            _net = cv2.dnn.readNetFromCaffe(settings.PROTOTXT_PATH, settings.CAFFEMODEL_PATH)
        except Exception as e:
            raise FileNotFoundError(f"Face detection model unavailable: {e}")
    return _net


def _load_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Resize if too large
    w, h = img.size
    if max(w, h) > settings.MAX_IMAGE_SIZE:
        scale = settings.MAX_IMAGE_SIZE / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)))
    return np.array(img)


def _image_to_base64(img_rgb: np.ndarray) -> str:
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    _, buf = cv2.imencode(".jpg", img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf).decode("utf-8")


def detect(image_bytes: bytes) -> dict:
    net = _get_net()
    img = _load_image(image_bytes)
    h, w = img.shape[:2]

    # Prepare blob
    blob = cv2.dnn.blobFromImage(
        cv2.cvtColor(img, cv2.COLOR_RGB2BGR),
        scalefactor=1.0,
        size=(300, 300),
        mean=(104.0, 177.0, 123.0),
    )
    net.setInput(blob)
    detections = net.forward()

    faces = []
    annotated = img.copy()

    for i in range(detections.shape[2]):
        confidence = float(detections[0, 0, i, 2])
        if confidence < settings.CONFIDENCE_THRESHOLD:
            continue
        x1 = max(0, int(detections[0, 0, i, 3] * w))
        y1 = max(0, int(detections[0, 0, i, 4] * h))
        x2 = min(w, int(detections[0, 0, i, 5] * w))
        y2 = min(h, int(detections[0, 0, i, 6] * h))

        faces.append({
            "x": x1, "y": y1,
            "width": x2 - x1, "height": y2 - y1,
            "confidence": round(confidence * 100, 2),
        })

        # Draw bounding box on annotated image
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{round(confidence * 100, 1)}%"
        cv2.putText(annotated, label, (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    # Sort by confidence
    faces.sort(key=lambda x: x["confidence"], reverse=True)

    return {
        "face_count": len(faces),
        "faces": faces,
        "image_width": w,
        "image_height": h,
        "annotated_image": _image_to_base64(annotated),
    }
