import cv2
import sys
import os

# Set the path to the OpenPose build directory (you may need to change this to your own path)
sys.path.append('/path/to/openpose/build/python')
from openpose import pyopenpose as op

# Set up OpenPose configuration
params = {
    "model_folder": "/path/to/openpose/models",  # Path to OpenPose models
    "hand": False,  # Enable hand keypoint detection
    "face": False,  # Enable face keypoint detection
    "num_gpu": 1,  # Number of GPUs to use
    "num_gpu_start": 0,  # Start from this GPU
}

# Initialize OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Read input image
image_path = 'input_image.jpg'  # Path to your image
image = cv2.imread(image_path)

# Process image with OpenPose
datum = op.Datum()
datum.cvInputData = image
opWrapper.emplaceAndPop([datum])

# Output the result
output_image = datum.cvOutputData
cv2.imshow("OpenPose Output", output_image)

# Wait for a key press and close the image window
cv2.waitKey(0)
cv2.destroyAllWindows()
