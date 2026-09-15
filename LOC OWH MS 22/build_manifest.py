import json
import os
from PIL import Image

# GitHub Pages base path & current directory settings
BASE_URL = "https://lmorreale3.github.io/iiif-manifests"
IMAGE_FOLDER = "."
OUTPUT_MANIFEST = "manifest.json"

manifest = {
    "@context": "http://iiif.io/api/presentation/3/context.json",
    "id": f"{BASE_URL}/LOC%20OWH%20MS%2022/{OUTPUT_MANIFEST}",
    "type": "Manifest",
    "label": {"en": ["LOC OWH MS 22"]},
    "behavior": ["paged"],
    "items": [],
}

# Process images 1 through 153
for i in range(1, 154):
    img_filename = f"image{i:05d}.jpg"
    img_path = os.path.join(IMAGE_FOLDER, img_filename)

    width, height = 1000, 1500
    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            width, height = img.size

    canvas_id = f"{BASE_URL}/LOC%20OWH%20MS%2022/canvas/p{i}"
    image_url = f"{BASE_URL}/LOC%20OWH%20MS%2022/{img_filename}"

    canvas = {
        "id": canvas_id,
        "type": "Canvas",
        "label": {"en": [f"Folio {i}r" if i % 2 != 0 else f"Folio {i//2}v"]},
        "height": height,
        "width": width,
        "items": [
            {
                "id": f"{canvas_id}/page",
                "type": "AnnotationPage",
                "items": [
                    {
                        "id": f"{canvas_id}/annotation",
                        "type": "Annotation",
                        "motivation": "painting",
                        "body": {
                            "id": image_url,
                            "type": "Image",
                            "format": "image/jpeg",
                            "height": height,
                            "width": width,
                        },
                        "target": canvas_id,
                    }
                ],
            }
        ],
    }
    manifest["items"].append(canvas)

with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(
    f"Successfully generated {OUTPUT_MANIFEST} with {len(manifest['items'])} canvases."
)
