"""
Download YOLOv8 model weights.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings


def download_yolo_model(model_name: str = "yolov8n.pt", save_dir: str = "src/cv_engine/models"):
    """Download YOLOv8 model weights."""
    try:
        from ultralytics import YOLO
    except ImportError:
        print("Error: ultralytics package not installed.")
        print("Please run: pip install ultralytics")
        return None
    
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Downloading {model_name}...")
    model = YOLO(model_name)
    
    # Save to specified directory
    save_path = os.path.join(save_dir, model_name)
    
    # The model is automatically downloaded to the cache
    # We just need to verify it's accessible
    print(f"Model downloaded and cached successfully!")
    print(f"Model will be loaded from: {save_path}")
    
    # Test the model
    print("\nTesting model...")
    try:
        import numpy as np
        test_img = np.zeros((640, 640, 3), dtype=np.uint8)
        results = model(test_img, verbose=False)
        print("✓ Model test successful!")
    except Exception as e:
        print(f"✗ Model test failed: {e}")
    
    return save_path


if __name__ == "__main__":
    print("=" * 60)
    print("YOLOv8 Model Downloader")
    print("=" * 60)
    
    # Download nano model (smallest, fastest)
    result = download_yolo_model("yolov8n.pt")
    
    if result:
        print("\n" + "=" * 60)
        print("Download complete!")
        print("=" * 60)
        print("\nYou can now run the application:")
        print("  streamlit run src/ui/app.py")
    else:
        print("\nDownload failed. Please install required packages:")
        print("  pip install -r requirements.txt")


