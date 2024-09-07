
# Visionic

Visionic is designed to assist the elderly by integrating advanced computer vision and audio processing technologies. By employing facial recognition, Visionic facilitates the identification of people and objects. Additionally, it utilizes Optical Character Recognition (OCR) to detect text and converts it into speech using Text-to-Speech (TTS) systems. This dual functionality provides significant support for individuals with vision impairments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [CLI Version](#cli-version)
  - [WebApp Version](#webapp-version)
- [Camera Configuration](#camera-configuration)
- [Features](#features)
  - [Training - Train New Face](#training---train-new-face)
  - [Face Recognition](#face-recognition)
  - [Text Detection](#text-detection)
- [Saving Video Output](#saving-video-output)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Ensure you have all the necessary libraries and dependencies installed. These are listed in `./requirements.txt`.

```bash
pip install -r requirements.txt
```

## Getting Started

### CLI Version

1. Open the `Visionic_V3.0.0` directory.
2. Run the CLI:
   ```bash
   python main.py
   ```
3. Wait for the process to complete.

### WebApp Version

1. Open the `Visionic_V3.1.0` directory.
2. Navigate to the Flask directory:
   ```bash
   cd Flask
   ```
3. Run the web application:
   ```bash
   python main.py
   ```
4. Open the application in your designated port.

## Camera Configuration

**IMPORTANT!!**

Visionic will automatically use your webcam for detection. If you have an external camera, connect it to your system via WIFI or BLUETOOTH.

If your external camera is not detected, configure the webcam using `videoCapture(x)` where `x` is an integer value (0-x), corresponding to your camera device.

To process a video, replace `videoCapture(0)` with the video path. `main.py` provides a placeholder for video file input called `PATH_TO_TEST`. Place your video in the test folder and modify `PATH_TO_TEST` to match your filename.

## Features

### Training - Train New Face

Visionic allows for easy training:
1. Press the training menu then input a name.
2. Scan a 180° view of the face from left to right. This works similarly to Apple FaceID, where a live video feed is shown, and the user rotates their face while Visionic automatically captures and processes the face.

**IMPORTANT:**
- Ensure you are the only face in the frame during training to avoid misleading detection.
- The dataset must be in a readable format (`.png`, `.jpg`, `.jpeg`).

### Face Recognition

Visionic automatically detects and recognizes faces. To quit the video interface, press 'q'. It might take a few moments to fully process, so please **DO NOT SPAM**.

### Text Detection

For detecting text, press 't' and wait for the frame to be processed. It might take a few moments before the audio starts playing, so please **DO NOT SPAM**.

## Saving Video Output

To save a video:
1. Alter the `SAVE_CONFIG` located in `main.py` to `True` or `False` based on preference. 
2. Note that the video output will be saved in the `./output` directory.

**IMPORTANT:** Please modify the output name to avoid overwriting existing files.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
