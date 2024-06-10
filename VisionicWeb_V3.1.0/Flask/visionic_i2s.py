import cv2
import pytesseract
from gtts import gTTS
import io
import pygame
import re


class ImageToSpeech:
    def __init__(self):
        pygame.mixer.init()

    def preprocess_text(self, text):
        text = re.sub(r'[^A-Za-z0-9.,;!?\'\s]', '', text)
        words = text.split()
        text = ' '.join(words)
        return text
    
    def generate_audio(self, read):
        if not read.strip():
            print("invalid")
            return
        with io.BytesIO() as f:
            tts = gTTS(text=read, lang='en')
            tts.write_to_fp(f)
            f.seek(0)
            pygame.mixer.music.load(f)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    def detectText(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur = cv2.medianBlur(gray, 3)
        # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        read = pytesseract.image_to_string(gray)
        formatted_read = self.preprocess_text(read)
        print(read)
        self.generate_audio(read)

        return frame, read