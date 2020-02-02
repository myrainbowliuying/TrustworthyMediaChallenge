import face_recognition
import imageio
import cv2
import os

# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

face_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\face_pictures'
video_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\Video-frame-rate_24'
output_directory_name = 'C:\\Users\\research\\rainbow\\fake media\\face_only_videos'
f = os.listdir(face_directory_name)
f = sorted(f)

for picture_name in f:
    target_face = face_recognition.load_image_file(face_directory_name + '/' + picture_name)
    target_face_encoding = face_recognition.face_encodings(target_face)[0]

    # input video
    video_name = picture_name[:-4] + '.mp4'
    reader = imageio.get_reader(video_directory_name + '/' + video_name, 'ffmpeg')
    fps = reader.get_meta_data()['fps']

    read_size = cv2.VideoCapture(video_directory_name + '/' + video_name)
    width = int(read_size.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(read_size.get(cv2.CAP_PROP_FRAME_HEIGHT))
    read_size.release()
    print(width, height)

    output_name = picture_name[:-4] + '_1080.mp4'
    writer = imageio.get_writer(output_directory_name + '/' + output_name, fps=fps)

    golden_ratio = 0.618
    frames = []
    delete_flag = 0
    size_flag = 0

    before_flag = 0  # 0 means not delete
    real_delete_flag = 0

    for num, im in enumerate(reader):

        frames.append(im)

        if (num % 17) == 0:
            unknown_face_encodings = face_recognition.face_encodings(im)
            face_locations = face_recognition.face_locations(im)

            if len(unknown_face_encodings) == 0:
                size_flag = 1
                delete_flag = 1
            else:
                i = -1
                for unknown_face_encoding in unknown_face_encodings:
                    i = i + 1
                    results = face_recognition.compare_faces([target_face_encoding], unknown_face_encoding)
                    if results[0] == False:
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
                before_flag=0
                frames.clear()
            elif size_flag == 1 or delete_flag == 1:
                print("before flag = 1")
                before_flag = 1
                frames.clear()
            else:
                before_flag = 0
                print("add")
                for frame in frames:
                    writer.append_data(frame)
                frames.clear()

    print(video_name + 'finish')
    writer.close()
