import subprocess


def render_jpg_to_mp4(jpg_pattern="%05d.jpg", frame_rate=30, out_name='out.mp4'):
    # command_list = ["ffmpeg", "-framerate", str(frame_rate),
    #                 "-i", jpg_pattern,
    #                 "-vcodec", "libx264" "-pix_fmt", "yuv420p",
    #                 "-r", str(frame_rate), out_name]
    command_list1 = ["ffmpeg", "-framerate", str(frame_rate),
                    "-i", jpg_pattern,
                    "-r", str(frame_rate), out_name]
    subprocess.run(command_list)
