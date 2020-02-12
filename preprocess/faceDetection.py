import face_recognition
from moviepy.editor import *

# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"




face_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\face_pictures'
video_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\Video-frame-rate_24'
output_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\face_only_videos'

# face_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\testpicture'
# video_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\test'
# output_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\testresult'
f = os.listdir(face_directory_name)
f = sorted(f)

for picture_name in f:
    target_face = face_recognition.load_image_file(face_directory_name + '/' + picture_name)
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

    video = VideoFileClip(video_directory_name + '/' + video_name)

    #begin detect
    width,height=video.size
    duration = video.duration  # == audio.duration, presented in seconds, float
    step = 1
    spf=8/video.fps

    suffix=1

    for t in range(1,int(duration / step)):  # runs through audio/video frames obtaining them by timestamp with step 100 msec
        t = t * step
        if t > video.duration: break
        video_frame = video.get_frame(t)  # numpy array representing RGB/gray frame
        video_frame_previous=video.get_frame(t-spf)
        video_frame_previous2=video.get_frame(t-2*spf)
        unknown_face_encodings_now = face_recognition.face_encodings(video_frame)
        unknown_face_encodings_previous = face_recognition.face_encodings(video_frame_previous)
        unknown_face_encodings_previous2 = face_recognition.face_encodings(video_frame_previous2)
        face_locations_now = face_recognition.face_locations(video_frame)
        face_locations_previous = face_recognition.face_locations(video_frame_previous)
        face_locations_next = face_recognition.face_locations(video_frame_previous2)
        face_locations=face_locations_now+face_locations_previous+face_locations_next
        if len(unknown_face_encodings_now) ==0 and len(unknown_face_encodings_previous)== 0 and len(unknown_face_encodings_previous2)== 0 :
            size_flag = 1
            delete_flag = 1
        else:
            i = -1
            for unknown_face_encoding in unknown_face_encodings_now+unknown_face_encodings_previous+unknown_face_encodings_previous2 :
                i += 1
                result = face_recognition.compare_faces([target_face_encoding], unknown_face_encoding,tolerance=0.8)
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
            if (len(output_video_list) > 4):
                output_video_name = picture_name[:-4] +'_'+str(suffix)+ '.mp4'
                output_video = concatenate_videoclips(output_video_list)
                output_video.write_videofile(output_directory_name + '/' + output_video_name)
                suffix +=1
            output_video_list.clear()
        else:
            before_flag = 0
            print("add")
            output_video_list.append(video.subclip(t-step,t))

    print(video_name + ' finished')