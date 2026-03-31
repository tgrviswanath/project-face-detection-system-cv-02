"""
Downloads OpenCV DNN face detector model files on first run.
Files: deploy.prototxt + res10_300x300_ssd_iter_140000.caffemodel
"""
import os
import requests

PROTOTXT_URL = (
    "https://raw.githubusercontent.com/opencv/opencv/master/"
    "samples/dnn/face_detector/deploy.prototxt"
)
CAFFEMODEL_URL = (
    "https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/"
    "res10_300x300_ssd_iter_140000.caffemodel"
)


def download_models(prototxt_path: str, caffemodel_path: str):
    os.makedirs(os.path.dirname(prototxt_path), exist_ok=True)

    if not os.path.exists(prototxt_path):
        print("Downloading deploy.prototxt...")
        r = requests.get(PROTOTXT_URL, timeout=30)
        r.raise_for_status()
        with open(prototxt_path, "wb") as f:
            f.write(r.content)

    if not os.path.exists(caffemodel_path):
        print("Downloading caffemodel (~10MB)...")
        r = requests.get(CAFFEMODEL_URL, timeout=60, stream=True)
        r.raise_for_status()
        with open(caffemodel_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("Models ready.")
