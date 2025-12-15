from PIL import Image
import io
from flask import url_for

def convert_to_image(bytes_array):
    # img = Image.open(io.BytesIO(bytes_array))
    # img.save(url_for('static', filename=f'img/avatars/image{current_user.id}.png')[1:])
    # return f"{url_for('static', filename=f'img/avatars/image{current_user.id}.png')}"
    return 0