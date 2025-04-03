import os
from PIL import Image

def compress_image(image_path, target_size_kb=250, step=5):
    """Compress an image to be ≤ target_size_kb (default: 150 KB)"""
    img = Image.open(image_path)
    
    # Convert PNG to JPEG for better compression
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    output_path = image_path  # Overwrite the original image
    quality = 99  # Start with high quality

    while quality > 10:
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        file_size_kb = os.path.getsize(output_path) / 1024  # Convert bytes to KB

        if file_size_kb <= target_size_kb:
            print(f"✔ {os.path.basename(image_path)} compressed to {file_size_kb:.2f} KB at quality {quality}")
            return
        quality -= step  # Reduce quality step by step

    print(f"⚠ {os.path.basename(image_path)} could not be reduced below {file_size_kb:.2f} KB")

def compress_all_images(folder_path, target_size_kb=150):
    """Compress all images in a folder to ≤150 KB"""
    if not os.path.exists(folder_path):
        print("❌ Folder does not exist!")
        return

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                compress_image(image_path, target_size_kb)

    print("\n✅ All images compressed successfully!")

# Example usage
compress_all_images(r"C:\Users\uk961\Downloads\Upload Image\Upload Image(passport size) (File responses)")  # Ch
