import os

import path_util
import resize_image

import ffmpeg_util

target_dir, n = path_util.get_target_dir('sample.txt')
path_list = path_util.get_sorted_paths(target_dir, 'JPG')

filtered_paths = [p for i, p in enumerate(path_list) if i % n == 0]

save_dir = resize_image.validate_save_dir(path_list[0])

if save_dir:
    for p in filtered_paths:
        img = resize_image.resize_img(p, save_dir, 0.5)
        del img

    resized_paths = path_util.get_sorted_paths(save_dir, 'jpg')

    # 連番をふるためrename
    for i, path in enumerate(resized_paths):
        dir_name = os.path.dirname(path)
        # file_name = os.path.basename(path)
        path2 = os.path.join(dir_name, '{:0=5}'.format(i))
        os.rename(path, path2)

    # ffmpegをsubprocessで呼び出す
    parent_folder = os.path.split(resized_paths)[0]
    dir_title = os.path.basename(parent_folder)
    out_path = os.path.join(parent_folder, dir_title + '.mp4')
    input_pattern = os.path.join(parent_folder, "%05d.jpg")
    ffmpeg_util.render_jpg_to_mp4(jpg_pattern=input_pattern, frame_rate=30, out_name=out_path)

    for i, path in resized_paths:
        dir_name = os.path.dirname(path)
        # file_name = os.path.basename(path)
        path2 = os.path.join(dir_name, '{:0=5}'.format(i))
        os.rename(path2, path)
else:
    print(f'{save_dir} does not exists.')