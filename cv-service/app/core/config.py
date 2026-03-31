from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "Face Detection CV Service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8001
    # OpenCV DNN face detector model files (auto-downloaded by setup.py)
    PROTOTXT_PATH: str = "models/deploy.prototxt"
    CAFFEMODEL_PATH: str = "models/res10_300x300_ssd_iter_140000.caffemodel"
    CONFIDENCE_THRESHOLD: float = 0.5
    MAX_IMAGE_SIZE: int = 1280   # resize if larger

    class Config:
        env_file = ".env"


settings = Settings()
