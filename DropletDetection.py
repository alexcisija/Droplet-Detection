import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageEnhance
from skimage.transform import hough_circle, hough_circle_peaks

def Analyze(filename, start=None, end=None):
    video = cv2.VideoCapture(filename)

    for i in tqdm(range(300)):
        success, image = video.read()
        DetectEdgesInfo(image) # Should implement radius calculation in the future.

    video.release()

def DetectEdgesInfo(image):
    image = Image.fromarray(image).convert('L')
    image = PrepareImage(image)
    circles = FindCircles(image)

    return sorted(circles[0], key=lambda x: x[0])

    return circles[0][0]

def PrepareImage(im):
    im = ImageEnhance.Brightness(im).enhance(5)
    im = ImageEnhance.Contrast(im).enhance(1.5)
    im = np.array( im )
    im = cv2.GaussianBlur(im, (135, 135), cv2.BORDER_DEFAULT)

    return im

def FindCircles(im):
    circles = cv2.HoughCircles(im, method=cv2.HOUGH_GRADIENT, dp=1, minDist=80, param1=70, param2=70)
    if circles is None: raise ValueError("No Circles Detected!")

    return circles

def DrawContours(circles, output):
    circles = np.round(circles[0, :]).astype("int")

    for (x, y, r) in circles:
        cv2.circle(output, (x, y), r, (90, 90, 90), 2)
        cv2.circle(output, (x, y), r//2, (255, 255, 255), 2)
    
    return output