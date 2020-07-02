import argparse
from moviepy.editor import *
import json
import os
from os.path import join


def main(config):

    f = os.listdir(config.input_directory)
    f = sorted(f)

    for video_file in f:
        video_name = join(config.input_directory,video_file)
        print(video_name + ' start')
        json_name = join(config.json_directory, video_file[:-4] + ".json")

        video = VideoFileClip(video_name)
        with open(json_name, encoding='utf-8') as json_file:
            segments = json.load(json_file)['details']['segments']

        i = 0
        for segment in segments:
            speaker_id=segment['speaker_id']
            if speaker_id != '0':
                name = segment['name']
                if name=='0':
                    output_path=join(config.output_directory,video_file[7:-4]+'_'+str(speaker_id))
                else:
                    output_path = join(config.output_directory,name)
                if not os.path.exists(output_path):os.mkdir(output_path)
                start=segment['start']
                index=start.find('.')
                index2=start.find('.',index+1)
                a=int(start[:index])
                b=int(start[index+1:index2])
                c=int(start[index2+1:])
                print(a,b,c)
                start=a*60+b+c*0.01
                end=segment['end']
                index=end.find('.')
                index2=end.find('.',index+1)
                a = int(end[:index])
                b = int(end[index + 1:index2])
                c = int(end[index2 + 1:])
                print(a, b, c)
                end=a*60+b+c*0.01
                if(end-start)>10:
                    output_name=join(output_path,'%03d.mp4'%(i))
                    i = i + 1
                    if not os.path.exists(output_path): os.mkdir(output_path)
                    video_clip = video.subclip(start, end)
                    video_clip.resize((1920,1080))
                    video_clip.write_videofile(output_name)
        print(video_name + ' end')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input_directory','-i',type=str)
    parser.add_argument('--json_directory','-j',type=str)
    parser.add_argument('--output_directory','-o',type=str)

    config = parser.parse_args()
    main(config)