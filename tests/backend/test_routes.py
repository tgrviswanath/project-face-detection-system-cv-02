from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

MOCK_RESULT = {
    "face_count": 2,
    "faces": [
        {"x": 50, "y": 30, "width": 120, "height": 140, "confidence": 92.5},
        {"x": 200, "y": 40, "width": 110, "height": 130, "confidence": 78.3},
    ],
    "image_width": 640,
    "image_height": 480,
    "annotated_image": "base64encodedstring",
}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200


@patch("app.core.service.detect_faces", new_callable=AsyncMock, return_value=MOCK_RESULT)
def test_detect_endpoint(mock_detect):
    r = client.post(
        "/api/v1/detect",
        files={"file": ("test.jpg", b"fake", "image/jpeg")},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["face_count"] == 2
    assert len(data["faces"]) == 2
    assert data["faces"][0]["confidence"] == 92.5
