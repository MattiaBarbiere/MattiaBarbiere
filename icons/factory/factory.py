"""
Python script to convert an image to an SVG icon with a rounded rectangle background and transparent corners.
The output SVG will have a specified background color and the image will be centered and scaled to fit
"""

# Imports
from PIL import Image, ImageOps
import io
import base64
import os

# Paths
ABS_PATH = os.path.abspath(os.path.dirname(__file__))
ICON_SAVE_PATH = os.path.abspath(os.path.join(ABS_PATH, ".."))
IMAGES_TO_CONVERT_PATH = os.path.join(ABS_PATH, "images_to_convert")

def convert_image_to_svg(image_name, output_name, size=256, corner_radius=60, bg_color="#0A66C2"):
    """
    Converts an input image to an SVG icon with a rounded rectangle background and transparent corners.

    Parameters:
        image_name (str): Name of the input image file (must be in the IMAGES_TO_CONVERT_PATH directory).
        output_name (str): Name of the output SVG file (will be saved in the ICON_SAVE_PATH directory).
        size (int, optional): Size (width and height) of the output SVG/icon in pixels. Default is 256.
        corner_radius (int, optional): Radius of the rounded rectangle corners. Default is 60.
        bg_color (str, optional): Background color of the icon in hex format (e.g., "#0A66C2"). Default is LinkedIn blue.

    The output SVG will have a transparent background outside the rounded rectangle.
    The image is centered and scaled to fit within the square icon.
    """
    # Load and convert image to RGBA for transparency support
    img = Image.open(os.path.join(IMAGES_TO_CONVERT_PATH, image_name)).convert("RGBA")

    # Resize the image to fit within the square, maintaining aspect ratio
    img = ImageOps.contain(img, (size, size), method=Image.Resampling.LANCZOS)

    # Create a transparent square canvas
    square_img = Image.new("RGBA", (size, size), (255, 255, 255, 0))

    # Paste the resized image onto the center of the canvas
    square_img.paste(img, ((size - img.width) // 2, (size - img.height) // 2), img)

    # Encode the image as base64 PNG for embedding in SVG
    buffered = io.BytesIO()
    square_img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Compose the SVG content with a colored rounded rectangle and the clipped image
    svg_content = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="{size}" height="{size}" rx="{corner_radius}" fill="{bg_color}"/>
                        <clipPath id="clip">
                        <rect width="{size}" height="{size}" rx="{corner_radius}" />
                        </clipPath>
                        <image href="data:image/png;base64,{img_base64}" width="{size}" height="{size}" clip-path="url(#clip)" />
                        </svg>'''

    # Write the SVG content to the output file
    output_path = os.path.join(ICON_SAVE_PATH, output_name)
    with open(output_path, "w") as f:
        f.write(svg_content)
    print(f"SVG saved to: {output_path}")

if __name__ == "__main__":
    # Call the conversion function with a custom background color
    convert_image_to_svg("EPFL_logo.jpg", "EPFL.svg", bg_color="#FF0000")
    convert_image_to_svg("badge-nvidia-cuda-cpp.png", "CUDA2.svg", bg_color="#F3F2ED")