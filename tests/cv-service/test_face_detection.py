from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np
from PIL import Image
import io
from app.main import app

client = TestClient(app)


def _sample_image() -> bytes:
    img = Image.new("RGB", (300, 300), color=(200, 180, 160))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def _mock_net():
    net = MagicMock()
    # Simulate one face detection at 85% confidence
    detections = np.zeros((1, 1, 1, 7), dtype=np.float32)
    detections[0, 0, 0] = [0, 0, 0.85, 0.1, 0.1, 0.4, 0.5]
    net.forward.return_value = detections
    return net


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@patch("app.core.detector._get_net", return_value=_mock_net())
def test_detect_single_face(mock_net):
    r = client.post(
        "/api/v1/cv/detect",
        files={"file": ("test.jpg", _sample_image(), "image/jpeg")},
    )
    assert r.status_code == 200
    data = r.json()
    assert "face_count" in data
    assert "faces" in data
    assert "annotated_image" in data
    assert data["face_count"] >= 0


def test_detect_unsupported_format():
    r = client.post(
        "/api/v1/cv/detect",
        files={"file": ("test.gif", b"GIF89a", "image/gif")},
    )
    assert r.status_code == 400


def test_detect_empty_file():
    r = client.post(
        "/api/v1/cv/detect",
        files={"file": ("test.jpg", b"", "image/jpeg")},
    )
    assert r.status_code == 400
