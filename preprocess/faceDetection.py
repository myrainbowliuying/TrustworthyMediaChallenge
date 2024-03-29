import face_recognition
from moviepy.editor import *
import os
import argparse
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def main(config):
    f = os.listdir(config.face_directory_name)
    f = sorted(f)

    for picture_name in f:
        target_face = face_recognition.load_image_file(config.face_directory_name + '/' + picture_name)
        target_face_encoding = face_recognition.face_encodings(target_face)
        if len(target_face_encoding)==0:
            print('failed recognize target image'+picture_name)
        # some temporary variables.
        golden_ratio = 0.618
        delete_flag = 0
        size_flag = 0
        before_flag = 0  # 0 means not delete
        real_delete_flag = 0
        output_video_list=[]
        # input video
        video_name = picture_name[:-4] + '.mp4'
        print('begin: '+video_name)

        video = VideoFileClip(config.video_directory_name + '/' + video_name)

        #begin detect
        width,height=video.size
        duration = video.duration  # == audio.duration, presented in seconds, float
        step = 0.5

        suffix=1
        for t in range(1,int(duration / step)):  # runs through audio/video frames obtaining them by timestamp with step 100 msec
            t = t * step
            if t > video.duration: break
            video_frame = video.get_frame(t)  # numpy array representing RGB/gray frame
            unknown_face_encodings = face_recognition.face_encodings(video_frame)
            unknown_face_encodings = face_recognition.face_encodings(video_frame)
            face_locations = face_recognition.face_locations(video_frame)

            if len(unknown_face_encodings) == 0:
                size_flag = 1
                delete_flag = 1
            else:
                i = -1
                for unknown_face_encoding in unknown_face_encodings:
                    i = i + 1
                    result = face_recognition.compare_faces([target_face_encoding], unknown_face_encoding)
                    if result == False:
                        delete_flag = 1
                    else:
                        delete_flag = 0
                        break

                face_location = face_locations[i]
                top, right, bottom, left = face_location
                center = ((bottom + top) / 2, (right + left) / 2)
                print(face_location)
                if ((bottom - top) * (right - left) / width / height > 0.25) or center[0] < height * (
                        0.5 - golden_ratio / 2) or \
                        center[0] > height * (0.5 + golden_ratio / 2) or center[1] > width * (0.5 + golden_ratio / 2) or \
                        center[
                            1] < width * (0.5 - golden_ratio / 2):
                    size_flag = 1
                else:
                    size_flag = 0

            if before_flag == 1 and size_flag == 0 and delete_flag == 0:
                print("before flag = 0")
                before_flag = 0
            elif size_flag == 1 or delete_flag == 1:
                print("before flag = 1")
                before_flag = 1

                # output video
                output_video_name = picture_name[:-4] +'_'+str(suffix)+ '_1080.mp4'
                output_video = concatenate_videoclips(output_video_list)
                if(len(output_video)>1.5):
                    output_video.write_videofile(config.output_directory_name + '/' + output_video_name)
                    suffix +=1
                output_video_list.clear()
            else:
                before_flag = 0
                print("add")
                output_video_list.append(video.subclip(t-step,t))

        print(video_name + ' finished')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--face_directory_name','-i',type=str)
    parser.add_argument('--video_directory_name','-o',type=str)
    parser.add_argument('--output_directory_name','-o',type=str)

    config = parser.parse_args()
    main(config)