import cv2
import numpy as np
import requests
from io import BytesIO


picture_url = "http://192.168.1.185/capture"

''' 
#For 640x480
K = np.array([[574.85, 0, 298.35], [0, 559.21, 275.61], [0, 0, 1]])  # Intrinsic matrix
D = np.array([-0.8, 1.2, -0.02, 0.036, -1.678])  # Distortion coefficients

#For 240x240
'''
K = np.array([[254.85, 0, 119.60], [0, 247.14, 155.82], [0, 0, 1]])  # Intrinsic matrix
D = np.array([-0.63, 0.57, -0.046, -0.0058, -0.483])  # Distortion coefficients

# For 96x96
#K = np.array([[111.73, 0, 48.25], [0, 109.6, 54.15], [0, 0, 1]])  # Intrinsic matrix
#D = np.array([-0.8, 1.56, -0.0015, 0.0008, -2.72])  # Distortion coefficients


def undistort_image(img, K, D):
    # Get the dimensions of the image
    h, w = img.shape[:2]
    # Perform lens distortion correction
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(K, D, (w, h), 1, (w, h))
    undistorted_img = cv2.undistort(img, K, D, None, new_camera_matrix)[30:130,109:209]
    return undistorted_img


response = requests.get(picture_url)
if response.status_code == 200:
        # Specify the file path to save the image
        image_data = np.frombuffer(BytesIO(response.content).read(), dtype=np.uint8)
        # Decode the image data using OpenCV
        orig = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

undistorted_image = undistort_image(orig, K, D)
    
cv2.imshow("Original Image", orig)
cv2.imshow("Undistorted Image", undistorted_image)
cv2.imwrite("capture.jpg", undistorted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
