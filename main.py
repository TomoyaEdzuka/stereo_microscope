import glob
import os
import shutil
import sys

import termcolor

import ffmpeg_util
import path_util
import resize_image

if not os.path.exists('temp'):
    os.makedirs('temp')
if not os.path.exists('ffmpeg_out'):
    os.makedirs('ffmpeg_out')

target_dir, n = path_util.get_target_dir('sample.txt')
path_list = path_util.get_sorted_paths(target_dir, 'JPG')

filtered_paths = [p for i, p in enumerate(path_list) if i % n == 0]


def make_mp4_movie(image_paths=filtered_paths, save_dir='temp',
                   image_scale=0.5, frame_rate=30,
                   out_dir='ffmpeg_out', rm_resized=True, over_write=False):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if os.path.exists(image_paths[0]):
        out_title = os.path.split(os.path.dirname(image_paths[0]))[1] + '.mp4'
    else:
        print('image path is None')
        sys.exit(-1)

    resized_paths = glob.glob(save_dir + os.sep + '*.jpg')

    if not resized_paths:
        resized_paths = glob.glob(save_dir + os.sep + '*.jpg')
        if over_write:
            shutil.rmtree(save_dir)
            os.mkdir(save_dir)
    else:
        for p in image_paths:
            resize_image.resize_img(p, save_dir, image_scale)
        resized_paths = path_util.get_sorted_paths(save_dir, 'jpg')

        for i, fp in enumerate(resized_paths):
            os.rename(fp, os.path.join(save_dir, f'{i + 1:0=5}.jpg'))

    out_name = os.path.join(out_dir, out_title)
    ffmpeg_util.render_jpg_to_mp4(jpg_pattern=os.path.join(save_dir, '%05d.jpg'),
                                  frame_rate=frame_rate,
                                  out_name=out_name)

    if os.path.exists(out_name):
        if rm_resized:

            message = f'The movie was saved as {out_name}'
            colored_output = termcolor.colored(message, color="blue", attrs=["bold"])
            print(colored_output)

            shutil.rmtree(save_dir)
            os.mkdir(save_dir)
            print('The all resized image has been deleted.')
        else:
            message = f'The movie was saved as {out_name}'
            colored_output = termcolor.colored(message, color="blue", attrs=["bold"])
            print(colored_output)
    else:
        print('The movie rendering failed')
        sys.exit(-1)


if __name__ == '__main__':
    make_mp4_movie(image_paths=filtered_paths, save_dir='temp',
                   image_scale=0.5, frame_rate=30,
                   out_dir='ffmpeg_out')
# save_dir = resize_image.validate_save_dir(path_list[0])
# if save_dir:
#     for p in filtered_paths:
#         img = resize_image.resize_img(p, save_dir, 0.5)
#         del img
#
#     resized_paths = path_util.get_sorted_paths(save_dir, 'jpg')
#
#     # 連番をふるためrename
#     for i, path in enumerate(resized_paths):
#         dir_name = os.path.dirname(path)
#         # file_name = os.path.basename(path)
#         path2 = os.path.join(dir_name, '{:0=5}'.format(i))
#         os.rename(path, path2)
#
#     # ffmpegをsubprocessで呼び出す
#     parent_folder = os.path.split(resized_paths)[0]
#     dir_title = os.path.basename(parent_folder)
#     out_path = os.path.join(parent_folder, dir_title + '.mp4')
#     input_pattern = os.path.join(parent_folder, "%05d.jpg")
#     ffmpeg_util.render_jpg_to_mp4(jpg_pattern=input_pattern, frame_rate=30, out_name=out_path)
#
#     for i, path in resized_paths:
#         dir_name = os.path.dirname(path)
#         # file_name = os.path.basename(path)
#         path2 = os.path.join(dir_name, '{:0=5}'.format(i))
#         os.rename(path2, path)
# else:
#     print(f'{save_dir} does not exists.')
