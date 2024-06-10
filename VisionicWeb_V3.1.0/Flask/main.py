from flask import Flask, render_template, Response, jsonify
from visionic_detection import VisionicDetection
from visionic_i2s import ImageToSpeech
import cv2

latest_recognition_output = ""
latest_its_output = ""
should_detect = False
should_its = False
should_cam = False

visionic = VisionicDetection()
image_to_speech = ImageToSpeech()

app = Flask(__name__)


def gen_frames():  
    global should_cam, should_detect, should_its, latest_its_output

    video_capture = cv2.VideoCapture(0)
    while video_capture.isOpened() and should_cam:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        if should_detect:
            processed_frame, _ = visionic.process_frame(frame)
        elif should_its:
            frame, detected_text = image_to_speech.detectText(frame)
            latest_its_output = detected_text
            should_its = False
        else:
            processed_frame = frame

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    video_capture.release()

def reset_detection_flag():
    global should_detect
    should_detect = False

def update_camera(status):
    global should_cam
    should_cam = status

@app.route('/', methods=['GET', 'POST'])
def home():
    reset_detection_flag()
    update_camera(False)
    return render_template('home.html')

@app.route('/option-menu')
def option_menu():
    reset_detection_flag()
    return render_template('option.html')

@app.route('/detection-menu') 
def detection_menu():
    global should_detect
    update_camera(True)
    should_detect = True
    return render_template('detection-menu.html') 

@app.route('/train-menu')
def train_menu():
    reset_detection_flag()
    return render_template('train-menu.html')

@app.route('/text-menu')
def text_menu():
    reset_detection_flag()
    update_camera(True)
    return render_template('text-menu.html')

@app.route('/training-menu')
def training_menu():
    reset_detection_flag()
    return render_template('training-menu.html')

@app.route('/about-us-menu')
def about_us_menu():
    reset_detection_flag()
    return render_template('about-us.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/activate-its')
def activate_its():
    global should_its
    global latest_its_output
    latest_its_output = ""
    should_its = True
    return jsonify({'message': 'ITS activated'})

@app.route('/get-its-text')
def get_its_text():
    global latest_its_output
    return jsonify({'detectedText': latest_its_output})


if __name__ == '__main__':
    app.run(debug=True, threaded=True)

