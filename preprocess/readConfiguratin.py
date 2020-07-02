# -*- coding: utf-8 -*-
from os.path import join
from string import digits
import os
from videoprops import get_video_properties, get_audio_properties
import xlsxwriter
import argparse

def main(config):
    wb = xlsxwriter.Workbook(config.excel_directory)
    sheet=wb.add_worksheet('sheet1')
    sheet.write_row(0,0,['name','person','file_size /M','video_bitrate /bps','video_duration /s','video_codec','video_resolution','video_frame_rate','audio_codec','audio_bitrate /bps','audio_channels','audio_sample_rate /Hz'])

    video_path=os.listdir(config.video_directory)
    video_path=sorted(video_path)
    number=0
    for each_video in video_path:
        number += 1
        video_name = join(config.video_directory, each_video)
        print(video_name)

        # get properties
        # video
        fsize = os.path.getsize(video_name)
        fsize = fsize / float(1024 * 1024)
        file_size = round(fsize, 2)
        try:
            video_props = get_video_properties(video_name)
            if 'duration' in video_props.keys():
                video_duration = round(float(video_props['duration']), 2)
            else:
                video_duration = ''
            if 'bit_rate' in video_props.keys():
                video_bitrate = int(video_props['bit_rate'])
            else:
                video_bitrate = ''
            if 'codec_name' in video_props.keys():
                video_codec = video_props['codec_name']
            else:
                video_codec = ''
            if 'width' in video_props.keys():
                video_width = video_props['width']
            else:
                video_width = ''
            if 'height' in video_props.keys():
                video_height = video_props['height']
            else:
                video_height = ''
            video_resolution = '[' + str(video_width) + ',' + str(video_height) + ']'
            if 'avg_frame_rate' in video_props.keys():
                video_frame_rate = video_props['avg_frame_rate']
            else:
                video_frame_rate = ''
        except:
            video_duration = ''
            video_bitrate = ''
            video_codec = ''
            video_width = ''
            video_height = ''
            video_resolution = '[' + str(video_width) + ',' + str(video_height) + ']'
            video_frame_rate = ''
        # audio
        try:
            audio_props = get_audio_properties(video_name)
            if 'bit_rate' in audio_props.keys():
                audio_bitrate = audio_props['bit_rate']
            else:
                audio_bitrate = ''
            if 'codec_name' in audio_props.keys():
                audio_codec = audio_props['codec_name']
            else:
                audio_codec = ''
            if 'channels' in audio_props.keys():
                audio_channels = audio_props['channels']
            else:
                audio_channels = ''
            if 'sample_rate' in audio_props.keys():
                audio_sample_rate = audio_props['sample_rate']
            else:
                audio_sample_rate = ''
        except:
            audio_bitrate=''
            audio_codec = ''
            audio_channels = ''
            audio_sample_rate = ''
        person=each_video[7:-4]
        remove_digits = str.maketrans('', '', digits)
        person=person.translate(remove_digits)
        print(person)
        data = [each_video, person, file_size, video_bitrate, video_duration, video_codec, video_resolution,
                video_frame_rate, audio_codec, audio_bitrate, audio_channels, audio_sample_rate]
        sheet.write_row(number, 0, data)
    wb.close()

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--video_directory','-v',type=str)
    parser.add_argument('--excel_directory','-e',type=str)

    config = parser.parse_args()
    main(config)