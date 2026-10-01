"""
test_deepface.py
Standalone test — run this BEFORE touching the Streamlit app.
Goal: confirm DeepFace gives sensible similarity scores on your own test photos,
so we know whether to build it into the dashboard or fall back to text-only matching.

Usage:
    python test_deepface.py

Put 3-4 test image pairs in a folder called test_photos/ next to this script:
    test_photos/person1_a.jpg   (same person, photo A)
    test_photos/person1_b.jpg   (same person, photo B — should score HIGH)
    test_photos/person2_a.jpg   (different person)
    test_photos/person2_b.jpg   (should score LOW against person1 photos)
"""
from deepface import DeepFace
import os
import traceback
import cv2

TEST_DIR = "test_photos"


def sanity_check_images():
    """
    Before touching DeepFace at all, confirm OpenCV can even read each file.
    This isolates whether the problem is the image files themselves or DeepFace.
    """
    print("=== Sanity check: can OpenCV read each image? ===")
    for f in sorted(os.listdir(TEST_DIR)):
        path = os.path.join(TEST_DIR, f)
        img = cv2.imread(path)
        if img is None:
            print(f"  XX {f} -> cv2.imread() returned None (file unreadable or corrupted)")
        else:
            print(f"  OK {f} -> shape={img.shape}")
    print()


def compare(img1_path, img2_path):
    try:
        result = DeepFace.verify(
            img1_path=img1_path,
            img2_path=img2_path,
            model_name="VGG-Face",
            enforce_detection=False,
        )
        distance = result["distance"]
        threshold = result["threshold"]
        similarity_pct = max(0, round((1 - (distance / (threshold * 2))) * 100, 2))

        return {
            "verified": result["verified"],
            "distance": round(distance, 4),
            "threshold": round(threshold, 4),
            "similarity_pct": similarity_pct,
        }
    except Exception as e:
        print("---- FULL ERROR TRACEBACK ----")
        traceback.print_exc()
        print("-------------------------------")
        return {"error": str(e)}


if __name__ == "__main__":
    if not os.path.isdir(TEST_DIR):
        print(f"Create a '{TEST_DIR}' folder with test images first. See docstring at top of this file.")
        exit()

    sanity_check_images()

    files = sorted(os.listdir(TEST_DIR))
    print(f"Found {len(files)} files in {TEST_DIR}: {files}\n")

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            path1 = os.path.join(TEST_DIR, files[i])
            path2 = os.path.join(TEST_DIR, files[j])
            print(f"Comparing {files[i]}  vs  {files[j]}")
            result = compare(path1, path2)
            print(f"  -> {result}\n")