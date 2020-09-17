import glob
import os
import sys

import PySimpleGUI as sg

if not os.path.exists('sample.txt'):
    f = open('sample.txt', 'w')
    f.close()


def get_target_dir(ref_file='sample.txt'):  # return Tuple:(str, int)
    with open(ref_file, 'r') as f:
        data = [s.strip() for s in f.readlines()]

    if data:
        for d in reversed(data):
            if os.path.exists(d):
                parent_dir = d
                break
            else:
                parent_dir = ''
    else:
        parent_dir = ''

    if len(sys.argv) == 1:
        event, values = sg.Window('Choose',
                                  [[sg.Text('Choose a image folder to process')],
                                   [sg.In(), sg.FolderBrowse('Choose your folder', initial_folder=parent_dir)],
                                   [sg.Text('Pick every n image'), sg.InputText(default_text='1')],
                                   [sg.Open(), sg.Cancel()]]).read(close=True)
        folder_name = values[0]

        try:
            n = int(values[1])
        except ValueError:
            n = 1
    else:
        folder_name = sys.argv[1]

    if not folder_name:
        sg.popup("Cancel", "No filename supplied")
        raise SystemExit("Cancelling: no filename supplied")

    else:
        if folder_name not in data:
            with open(ref_file, 'a') as f:
                f.write(folder_name + '\n')

        try:
            n
        except NameError:
            n = 1

        return folder_name, n


def apply_func(path_list, func, *args):
    for p in path_list:
        func(p, *args)


def get_sorted_paths(dir_name, ext='jpg'):
    jpgs = glob.glob(dir_name + os.sep + '*.' + ext)
    sorted_jpgs = sorted(jpgs)
    return sorted_jpgs
