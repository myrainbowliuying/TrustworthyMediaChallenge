from pydub.silence import split_on_silence
from pydub import AudioSegment
import os
import argparse

def main(config):
    abandon_chunk_len=2*1000
    length_limit=60*1000
    audiotype = 'wav'

    print('load file')
    audio=AudioSegment.from_file(config.input_video_name,'wav')


    chunks = split_on_silence(audio,min_silence_len=900,silence_thresh=-45)
    chunks_path = config.filepath+'/chunks4/'
    if not os.path.exists(chunks_path):os.mkdir(chunks_path)

    #save all segemnts
    print('start save')
    for i in range(len(chunks)):
        new = chunks[i]
        if len(new)<=abandon_chunk_len :
            continue
        else:
            save_name = chunks_path+'%04d.%s'%(i,audiotype)
            new.export(save_name, format=audiotype)
            print('%04d'%i,len(new))
    print('end save')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input_video_name','-i',type=str)
    parser.add_argument('--filepath','-o',type=str)

    config = parser.parse_args()
    main(config)
