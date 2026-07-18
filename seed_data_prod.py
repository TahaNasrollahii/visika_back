import os
import django
from django.core.files import File
from pathlib import Path

# Set up Django environment
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visika.settings.prod')
django.setup()

from products.models import Category, Product

def run():
    print("--- Uploading Category Images ---")
    for cat in Category.objects.all():
        if cat.image and cat.image.name:
            # We explicitly read from the local 'media' folder
            local_path = os.path.join(BASE_DIR, 'media', cat.image.name)
            
            # Skip if it's already a Cloudinary URL
            if "cloudinary" in cat.image.name or "http" in cat.image.name:
                print(f"Skipping {cat.title} - already a Cloudinary link")
                continue
                
            if os.path.exists(local_path):
                print(f"Uploading {local_path} to Cloudinary for Category: {cat.title}...")
                with open(local_path, 'rb') as f:
                    # This will automatically upload to Cloudinary and update the DB
                    cat.image.save(os.path.basename(cat.image.name), File(f), save=True)
            else:
                print(f"File not found locally: {local_path}")

    print("\n--- Uploading Product Images ---")
    for prod in Product.objects.all():
        if prod.image and prod.image.name:
            local_path = os.path.join(BASE_DIR, 'media', prod.image.name)
            
            if "cloudinary" in prod.image.name or "http" in prod.image.name:
                print(f"Skipping {prod.title} - already a Cloudinary link")
                continue
                
            if os.path.exists(local_path):
                print(f"Uploading {local_path} to Cloudinary for Product: {prod.title}...")
                with open(local_path, 'rb') as f:
                    prod.image.save(os.path.basename(prod.image.name), File(f), save=True)
            else:
                print(f"File not found locally: {local_path}")

if __name__ == "__main__":
    run()
    print("\nFinished uploading all local images to Cloudinary!")
