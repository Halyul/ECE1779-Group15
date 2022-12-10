import io
from PIL import Image

def make_thumbnail(byte_data):
    # create the thumbnail
    data = io.BytesIO(byte_data)
    image = Image.open(data)
    image.thumbnail((128, 128))
    if image.mode == 'P' or image.mode == 'RGB':
        if image.mode == 'P':
            image = image.convert('RGB')
        # save the thumbnail to memory, then return it
        file = io.BytesIO()
        image.save(file, "JPEG")
        file.seek(0) # move the pointer to the beginning of the buffer 'file'
        return file
    else:
        # save the thumbnail to memory, then return it
        file = io.BytesIO()
        image.save(file, "PNG")
        file.seek(0) # move the pointer to the beginning of the buffer 'file'
        return file
