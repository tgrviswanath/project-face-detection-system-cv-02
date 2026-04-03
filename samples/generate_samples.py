"""
Generate sample images for cv-02 Face Detection System.
Run: pip install Pillow && python generate_samples.py
Output: 4 images — single face, multiple faces, side face, group photo.
"""
from PIL import Image, ImageDraw
import os

OUT = os.path.dirname(__file__)


def draw_face(d, cx, cy, r, skin, hair=(60, 40, 20)):
    # hair
    d.ellipse([cx - r, cy - r - 10, cx + r, cy + int(r * 0.3)], fill=hair)
    # head
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin)
    # eyes
    ey = cy - int(r * 0.2)
    ex_l, ex_r = cx - int(r * 0.35), cx + int(r * 0.35)
    er = max(4, int(r * 0.12))
    d.ellipse([ex_l - er, ey - er, ex_l + er, ey + er], fill=(255, 255, 255))
    d.ellipse([ex_r - er, ey - er, ex_r + er, ey + er], fill=(255, 255, 255))
    d.ellipse([ex_l - er // 2, ey - er // 2, ex_l + er // 2, ey + er // 2], fill=(30, 20, 10))
    d.ellipse([ex_r - er // 2, ey - er // 2, ex_r + er // 2, ey + er // 2], fill=(30, 20, 10))
    # nose
    ny = cy + int(r * 0.1)
    d.polygon([(cx, ny - int(r * 0.15)), (cx - int(r * 0.1), ny + int(r * 0.15)),
               (cx + int(r * 0.1), ny + int(r * 0.15))], fill=(int(skin[0] * 0.85), int(skin[1] * 0.85), int(skin[2] * 0.85)))
    # mouth
    my = cy + int(r * 0.4)
    d.arc([cx - int(r * 0.3), my - int(r * 0.15), cx + int(r * 0.3), my + int(r * 0.15)],
          start=0, end=180, fill=(180, 80, 80), width=max(2, r // 10))


def save(img, name):
    img.save(os.path.join(OUT, name))
    print(f"  created: {name}")


def single_face():
    img = Image.new("RGB", (400, 400), (230, 230, 230))
    d = ImageDraw.Draw(img)
    draw_face(d, 200, 200, 90, (220, 180, 140))
    return img


def two_faces():
    img = Image.new("RGB", (600, 400), (200, 220, 200))
    d = ImageDraw.Draw(img)
    draw_face(d, 170, 200, 80, (220, 180, 140))
    draw_face(d, 430, 200, 80, (160, 110, 80), hair=(20, 20, 20))
    return img


def three_faces():
    img = Image.new("RGB", (700, 400), (210, 210, 230))
    d = ImageDraw.Draw(img)
    draw_face(d, 130, 200, 70, (240, 200, 160))
    draw_face(d, 350, 200, 70, (180, 130, 90), hair=(80, 50, 20))
    draw_face(d, 570, 200, 70, (200, 160, 120), hair=(30, 20, 10))
    return img


def face_with_background():
    img = Image.new("RGB", (500, 400), (100, 150, 200))
    d = ImageDraw.Draw(img)
    # background elements
    d.rectangle([0, 280, 500, 400], fill=(80, 120, 60))
    d.rectangle([50, 100, 150, 280], fill=(180, 140, 100))
    d.rectangle([350, 80, 450, 280], fill=(180, 140, 100))
    draw_face(d, 250, 190, 85, (220, 175, 135))
    return img


if __name__ == "__main__":
    print("Generating cv-02 samples...")
    save(single_face(), "sample_single_face.jpg")
    save(two_faces(), "sample_two_faces.jpg")
    save(three_faces(), "sample_three_faces.jpg")
    save(face_with_background(), "sample_face_background.jpg")
    print("Done — 4 images in samples/")
