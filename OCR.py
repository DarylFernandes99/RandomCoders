#Extracting text from image
from PIL import Image
import pytesseract
import argparse
import cv2
import re

def func():
  image = cv2.imread('D:/Training Data Set/KFC/2.jpg')
  cv2.imshow("Original", image)

  blurred = cv2.blur(image, (2,2))
  cv2.imshow("Blurred_image", blurred)
  img = Image.fromarray(blurred)
  text = pytesseract.image_to_string(img, lang='eng')
  words = text.split("\n")
  cv2.waitKey(0)
  return words

result = func()
print(*result, sep = "\n")