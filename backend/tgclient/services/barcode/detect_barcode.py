from cv2 import data
import numpy as np
import cv2
from PIL import Image
from pyzbar.pyzbar import decode
from urllib.request import Request, urlopen
import numpy as np
import ssl
from bs4 import BeautifulSoup

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required = True, help = "path to the image file")
#args = vars(ap.parse_args())
#

def detect_barcode(url):
    print(url)
    req = Request(url)
    print(req)
    context = ssl._create_unverified_context()
    with urlopen(req, context=context) as response:
        image = np.asarray(bytearray(response.read()), dtype="uint8")
        
    print(image)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR) # 'load it as it is'    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # compute the Scharr gradient magnitude representation of the images
    # in both the x and y direction
    gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
    gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)
    
    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    # blur and threshold the image
    blurred = cv2.blur(gradient, (2, 9))
    (_, thresh) = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)
    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations = 4)
    closed = cv2.dilate(closed, None, iterations = 4)
    # find the contours in the thresholded image, then sort the contours
    # by their area, keeping only the largest one
    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
#    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.cv2.boxPoints(rect))
    
    # draw a bounding box arounded the detected barcode and display the
    # image
    try:
        result = decode(image)
        print(result)
        data = result[0].data.decode('utf-8')
    except:
        data = ' не найден'
    return data
    ##print (data)
    ##print(type(result))
    ##print(result)
    ##cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
    ##cv2.imshow("Image", image)
    ##cv2.waitKey(0)