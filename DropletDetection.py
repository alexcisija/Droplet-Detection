from PIL import Image, ImageEnhance
from skimage.transform import hough_circle, hough_circle_peaks
from tqdm import tqdm
import numpy as np
import sys, os
import cv2

def main():
    video = cv2.VideoCapture("./video1.mp4")
    width, height = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    fourcc = cv2.VideoWriter_fourcc(*'H264')
    detectedVideo = cv2.VideoWriter("./video1out.mp4", fourcc, 60, (width, height))

    for i in tqdm(range(300)):
        success, image = video.read()
        try: im = DrawContours( DetectEdgesInfo(image), image)
        except: print("Failed!")
        detectedVideo.write(im)

    detectedVideo.release()
    video.release()

def DrawContours(circles, output):
    circles = np.round(circles[0, :]).astype("int")

    for (x, y, r) in circles:
        cv2.circle(output, (x, y), r, (90, 90, 90), 2)
        cv2.circle(output, (x, y), r//2, (255, 255, 255), 2)
    

    return output

def PreProcessImage(im):
    im = ImageEnhance.Brightness(im).enhance(5)
    im = ImageEnhance.Contrast(im).enhance(1.5)
    im = np.array( im )
    im = cv2.GaussianBlur(im, (135, 135), cv2.BORDER_DEFAULT)

    return im

def FindCircles(im):
    circles = cv2.HoughCircles(im, method=cv2.HOUGH_GRADIENT, dp=1, minDist=80, param1=70, param2=70)
    if circles is None: raise ValueError("No Circles Detected!")

    return circles

def DetectEdgesInfo(image):
    image = Image.fromarray(image).convert('L')
    image = PreProcessImage(image)
    circles = FindCircles(image)

    return circles

main()