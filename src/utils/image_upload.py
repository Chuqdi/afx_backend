from PIL import Image
from io import BytesIO

def resize_image(image_bytes, size=(100, 100), format="JPEG"):
    image = Image.open(BytesIO(image_bytes))
    image.thumbnail(size)
    with BytesIO() as output:
        image.save(output, format=format)
        return BytesIO(output.getvalue())
