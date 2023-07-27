import os
from PIL import Image
from io import BytesIO


def add_watermark(image_path, watermark_path, output_path):
    # input_buffer.seek(0)  # go to the start of the buffer
    base_image = Image.open(image_path)
    watermark = Image.open(watermark_path)

    # Resize watermark to be 1/4 the width and height of the base image
    watermark = watermark.resize((base_image.size[0] // 4, base_image.size[1] // 4))

    # Calculate the position for pasting the watermark (bottom-right)
    position = ((base_image.size[0] - watermark.size[0]) - 20, (base_image.size[1] - watermark.size[1]) - 20)

    # Make sure the image has an "alpha" (opacity) channel
    if base_image.mode != 'RGBA':
        base_image = base_image.convert('RGBA')

    # Create a new blank image with the same size as the base image
    transparent = Image.new('RGBA', base_image.size)

    # Paste the base image and the watermark onto the new image
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)

    # Save the result
    transparent.save(output_path, format="png")


def remove_background(input_image_path, output_buffer):
    img = Image.open(input_image_path)
    img = img.convert("RGBA")

    data = img.getdata()

    new_data = []
    for item in data:
        # change all green screen like pixels to white
        # In this code, pixels are considered green if the green value (item[1]) is high (> 100) and the red (item[0])
        # and blue (item[2]) values are low (< 100). These values might need to be adjusted depending on the exact shade
        # of green in your green screen. If you notice that the background is not fully removed, or that parts of the
        # image that should not be removed are being removed, you should adjust these thresholds.
        if item[0] < 100 and item[1] > 100 and item[2] < 100:
            new_data.append((255, 255, 255, 255))  # change all matching (green) pixels to white
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_buffer, "PNG")


# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Folder containing images
image_folder = "images"
image_dir = os.path.join(base_dir, image_folder)

# Path to watermark image
watermark_path = os.path.join(base_dir, "kinetic-garage-logo.png")

# Output folder for watermarked images
output_folder = "output"
output_dir = os.path.join(base_dir, output_folder)
os.makedirs(output_dir, exist_ok=True)  # Create output_dir if it does not exist

# Remove background and change to white, also add watermark to all images in the image_dir folder
for filename in os.listdir(image_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_dir, filename)
        output_path = os.path.join(output_dir, filename)

        image_buffer = BytesIO()
        # remove_background(image_path, image_buffer)
        # add_watermark(image_buffer, watermark_path, output_path)
        add_watermark(image_path, watermark_path, output_path)
