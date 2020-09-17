import os

import PIL.ImageOps
import termcolor
from PIL import Image

"""
Example from command line
Transform to 1/4 size
python3 resize_image.py input.jpeg 0.25
"""


def validate_save_dir(file_path):
    if not os.path.exists(file_path):
        return False
    parent_dir, file_name_ext = os.path.split(file_path)
    folder_title = os.path.basename(os.path.split(file_path)[0])
    save_dir = os.path.join(parent_dir, folder_title + '_resized')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return save_dir


def resize_img(file_path: str, save_dir: str, scale: float = 0.5) -> PIL.Image.Image:
    img = Image.open(file_path)  # img: PIL.Image.Image object
    resized_width = int(scale * img.width)
    resized_height = int(scale * img.height)

    if resized_width % 2 == 1:
        resized_width = resized_width + 1
    if resized_height % 2 == 1:
        resized_height = resized_height + 1
    resized_img = img.resize((resized_width, resized_height), Image.LANCZOS)
    # img = img.convert("YCbCr")
    # yy, cb, cr = img.split()
    # yy = ImageOps.equalize(yy)
    # img = Image.merge("YCbCr", (yy, cb, cr))
    # img = img.convert("RGB")

    base_file_name = os.path.basename(file_path)
    name, ext = base_file_name.split('.')

    scale = str(scale)
    if scale.find("."):
        replaced_dot_scale = scale.replace(".", ",")
        save_path = f'{save_dir + os.sep + name}_x{replaced_dot_scale}.jpg'
    else:
        save_path = f'{save_dir + os.sep + name}_x{scale}.jpg'

    resized_img.save(save_path)
    colored_output = termcolor.colored(save_path, color="blue", attrs=["bold"])
    print(colored_output)
    return resized_img


def change_contrast(image: PIL.Image.Image,
                    brightness: float,
                    save_image: bool = True):
    result_image = image.point(lambda x: x * brightness)
    if save_image:
        file_path = image.filename
        file_name, ext = file_path.split(".")
        brightness = str(brightness)
        if brightness.find('.'):
            comma_name = brightness.replace('.', ',')
            save_path = f'{file_name}_contrast-{comma_name}.{ext}'
        else:
            save_path = f'{file_name}_contrast-{brightness}.{ext}'
        result_image.save(save_path)

        colored_output = termcolor.colored(save_path, color="blue", attrs=["bold"])
        print(f'The image was saved as {colored_output}')

    return result_image


def exif_transpose(img):
    if not img:
        return img
    exif_orientation_tag = 274
    # Check for EXIF data (only present on some files)
    if hasattr(img, "_getexif") and isinstance(img._getexif(), dict) and exif_orientation_tag in img._getexif():
        exif_data = img._getexif()
        orientation = exif_data[exif_orientation_tag]
        # Handle EXIF Orientation
        if orientation == 1:
            # Normal image - nothing to do!
            pass
        elif orientation == 2:
            # Mirrored left to right
            img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # Rotated 180 degrees
            img = img.rotate(180)
        elif orientation == 4:
            # Mirrored top to bottom
            img = img.rotate(180).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            # Mirrored along top-left diagonal
            img = img.rotate(-90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            # Rotated 90 degrees
            img = img.rotate(-90, expand=True)
        elif orientation == 7:
            # Mirrored along top-right diagonal
            img = img.rotate(90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            # Rotated 270 degrees
            img = img.rotate(90, expand=True)
    return img


def transpose_image(file, mode='RGB'):
    # Load the image with PIL
    img = PIL.Image.open(file)
    if hasattr(PIL.ImageOps, 'exif_transpose'):
        # Very recent versions of PIL can do exit transpose internally
        img = PIL.ImageOps.exif_transpose(img)
    else:
        # Otherwise, do the exif transpose ourselves
        img = exif_transpose(img)
    img = img.convert(mode)
    return img


# if __name__ == "__main__":
#     args_count = len(sys.argv)
#     if args_count == 2:
#         input_path = sys.argv[1]  # file_path
#         resize_img(input_path)
#     if args_count == 3:
#         input_path = sys.argv[1]  # file_path
#         sc = float(sys.argv[2]) # scale
#         resize_img(input_path, scale=sc)

# if __name__ == "__main__":
#     import glob
#
#     BASE_DIR = "/Users/Edzuka/PycharmProjects/py_util/heic_to_jpeg/"
#     path_list = glob.glob(BASE_DIR + "*" + ".jpeg")
#     for path in path_list:
#         resize_img(path, 0.5)

# file_list = ["/Volumes/microSD256/move/2020-01-22_1",
#              "/Volumes/microSD256/move/2020-01-22_4",
#              "/Volumes/microSD256/move/2020-01-22_2",
#              "/Volumes/microSD256/move/2020-01-22_3"]
