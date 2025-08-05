#!/usr/bin/env python3

import os
from PIL import Image

def process_images(directory):
    """
    Processes all .TIF images in the given directory.
    Rotates, resizes, and converts them to .jpeg format.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".tiff") or filename.endswith(".TIF"):
            filepath = os.path.join(directory, filename)
            base_name = os.path.splitext(filename)[0]
            with Image.open(filepath) as im:
                # Rotate, resize, and convert to RGB
                new_im = im.rotate(-90).resize((600, 400)).convert("RGB")
                new_im.save(os.path.join(directory, f"{base_name}.jpeg"), "JPEG")

if __name__ == "__main__":
    process_images("supplier-data/images/")
