from os import system
import cv2
import pytesseract
import numpy as np

class Image2Text():
    # Define necessary variables
    def __init__(self, file_name, image_name):
        self.file_name = file_name
        self.image_name = image_name
        self.image = cv2.imread(self.image_name)
        self.image_text()

    # convert image to np array & resize it appropriately
    def manipulate_image(self):
        self.image = cv2.resize(self.image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        kernel = np.ones((1, 1), np.uint8)
        self.image = cv2.dilate(self.image, kernel, iterations=1)
        self.image = cv2.erode(self.image, kernel, iterations=1)

    # remove blur from image & make it more readable
    def perform_preprocessing(self):
        cv2.threshold(cv2.GaussianBlur(self.image, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.threshold(cv2.bilateralFilter(self.image, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.threshold(cv2.medianBlur(self.image, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        cv2.adaptiveThreshold(cv2.GaussianBlur(self.image, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        cv2.adaptiveThreshold(cv2.bilateralFilter(self.image, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        cv2.adaptiveThreshold(cv2.medianBlur(self.image, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # convert image to text via pytesseract
    def image_text(self):
        self.manipulate_image()
        self.perform_preprocessing()
        #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        result = pytesseract.image_to_string(self.image, lang="eng")
        self.write_file(result)

    # Writing contents of response to file
    def write_file(self, content):
        with open(self.file_name, 'w+') as file:
            file.write(content)
        print(content)

a = Image2Text("text.txt", "image.jpg")