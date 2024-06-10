import cv2
from visionic_detection import VisionicDetection
from visionic_i2s import ImageToSpeech 

#CHANGE THIS CONFIG FOR SAVING VIDEO
SAVE_CONFIG = True

def main():
    PATH_TO_TEST = './test/IMG_6755.MOV'

    visionic = VisionicDetection()
    speech = ImageToSpeech()
    video_capture = cv2.VideoCapture(0)

    if SAVE_CONFIG:
        #START OPTION TO SAVE VIDEO
        OUTPUT_PATH = './output/text_output.mp4'
        frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video_capture.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        video_writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (frame_width, frame_height))
        #END OPTION TO SAVE VIDEO

    while True:
        choice = input("\n1. Train New Person\n2. Run Detection\n3. Exit\nChoose an option: ")
        if choice == '1':
            visionic.train_new_person(video_capture)
        elif choice == '2':
            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break

                processed_frame, _ = visionic.process_frame(frame)
                cv2.imshow('Visionic', processed_frame)
                
                #START OPTION TO SAVE TO VIDEO
                if SAVE_CONFIG:
                    video_writer.write(processed_frame)
                #END OPTION TO SAVE TO VIDEO

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
                elif key == ord('t'):
                    _, text = speech.detectText(frame)
                    print("Recognized Text:", text)

        elif choice == '3':
            break


    video_capture.release()
    if SAVE_CONFIG:
        video_writer.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
