import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageEnhance
from skimage.transform import hough_circle, hough_circle_peaks

def Analyze(filename, start=None, end=None):
    video = cv2.VideoCapture(filename)

    with open("./output.csv", 'w+') as f:
        for i in tqdm(range(start, end)):
            success, image = video.read()
            circles = DetectEdgesInfo(image) # Should implement radius calculation in the future.
            
            for circle in circles: f.write(f"{circle[2]}, ")
            f.write("\n")

    video.release()

def DetectEdgesInfo(image):
    image = Image.fromarray(image).convert('L')
    image = PrepareImage(image)
    circles = FindCircles(image)

    return sorted(circles[0], key=lambda x: x[0])

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
    circles = np.round(circles).astype("int")

    for (x, y, r) in circles:
        cv2.circle(output, (x, y), r, (90, 90, 90), 2)
        cv2.circle(output, (x, y), r//2, (255, 255, 255), 2)
    
    return output