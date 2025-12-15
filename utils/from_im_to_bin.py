from PIL import Image
import io


def convert_to_binary(img):
    image = Image.open(img)
    byte_stream = io.BytesIO()
    image.save(byte_stream, format=F'PNG')
    byte_image = byte_stream.getvalue()
    return byte_image