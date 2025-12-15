from PIL import Image


def create_thumbnail(input_path, output_path, size=(150, 150)):
    try:
        with Image.open(input_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            img.save(output_path, 'JPEG', quality=85)
    except Exception as e:
        print(f"Error creating thumbnail: {e}")