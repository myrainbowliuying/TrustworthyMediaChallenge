import argparse
from moviepy.editor import *
import os
from os.path import join


def main(config):

    f = os.listdir(config.video_directory)
    f = sorted(f)

    for video_file in f:
        video_name = join(config.video_directory,video_file)
        video = VideoFileClip(video_name)

        audio_name=join(config.audio_directory,video_file[:-4]+".wav") #audio type, can change
        audio=AudioFileClip(audio_name)

        output=video.set_audio(audio)
        output_name=join(config.output_directory,video_file)
        output.write_videofile(output_name)



if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--video_directory','-v',type=str)
    parser.add_argument('--audio_directory','-a',type=str)
    parser.add_argument('--output_directory','-o',type=str)

    config = parser.parse_args()
    main(config)