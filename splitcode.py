import os
import shutil
import random

# Paths
SOURCE_DIR = "/home/surya/AgroScan~/data/AgroScan_Balanced"
DEST_DIR = "/home/surya/AgroScan~/data/AgroScan_Split"

shutil.rmtree(DEST_DIR, ignore_errors=True)

# Split ratio
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

# Create folders
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(DEST_DIR, split), exist_ok=True)

# Process each class
for cls in os.listdir(SOURCE_DIR):
    class_path = os.path.join(SOURCE_DIR, cls)

    if not os.path.isdir(class_path):
        continue

    images = [f for f in os.listdir(class_path)
        if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    random.shuffle(images)

    total = len(images)

    train_end = int(total * train_ratio)
    val_end = int(total * (train_ratio + val_ratio))

    train_imgs = images[:train_end]
    val_imgs = images[train_end:val_end]
    test_imgs = images[val_end:]

    # Create class folders
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(DEST_DIR, split, cls), exist_ok=True)

    # Copy files
    for img in train_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(DEST_DIR, "train", cls, img))

    for img in val_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(DEST_DIR, "val", cls, img))

    for img in test_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(DEST_DIR, "test", cls, img))

print("✅ Dataset Split Completed")