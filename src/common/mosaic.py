import os
import math
from PIL import Image

def create_mosaic(image_folder, output_path):
    # Load all images from the folder
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('gif'))]
    num_images = len(image_files)

    # Ensure we have at least one image
    if num_images == 0:
        raise ValueError("The folder must contain at least one image.")

    grid_width = math.ceil(math.sqrt(num_images))
    grid_height = math.ceil(num_images / grid_width)

    # Open images in order and determine the maximum width and height
    images = [(Image.open(img).resize((164, 180)), img) for img in image_files]
    # Sort by filename
    images.sort(key=lambda x: int(os.path.basename(x[1]).split('.')[0]))

    img_widths = [img[0].size[0] for img in images]
    img_heights = [img[0].size[1] for img in images]

    # Use the largest image dimensions for consistent spacing
    max_width = max(img_widths)
    max_height = max(img_heights)

    # Create a blank canvas for the mosaic
    mosaic_width = grid_width * max_width
    mosaic_height = grid_height * max_height
    mosaic = Image.new('RGB', (mosaic_width, mosaic_height), (255, 255, 255))  # White background

    # Paste images onto the mosaic
    for index, (img, _) in enumerate(images):
        x = (index % grid_width) * max_width
        y = (index // grid_width) * max_height
        mosaic.paste(img, (x, y))

    # Save the mosaic
    mosaic.save(output_path)