import cv2
import torch
import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict

# CentroidTracker class (as previously provided)
class CentroidTracker:
    def __init__(self, maxDisappeared=40, maxDistance=50):
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.maxDisappeared = maxDisappeared
        self.maxDistance = maxDistance

    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        if len(rects) == 0:
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            return self.objects

        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        if len(self.objects) == 0:
            for i in range(len(inputCentroids)):
                self.register(inputCentroids[i])
        else:
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())
            D = dist.cdist(np.array(objectCentroids), inputCentroids)

            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            usedRows, usedCols = set(), set()

            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue
                if D[row, col] > self.maxDistance:
                    continue

                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0
                usedRows.add(row)
                usedCols.add(col)

            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            for row in unusedRows:
                objectID = objectIDs[row]
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)

            for col in unusedCols:
                self.register(inputCentroids[col])

        return self.objects


# Load YOLOv5 model (ensure you have the latest YOLOv5 model loaded)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.classes = [0]  # Only detect "person" class (class 0)

# Initialize video capture (replace with your video path)
video_file = "C:/Users/akash/Downloads/3105196-uhd_3840_2160_30fps.mp4"  # Replace with your video path
cap = cv2.VideoCapture(video_file)

if not cap.isOpened():
    print("Error: Cannot open video file.")
else:
    print("Video file opened successfully.")

# Create a CentroidTracker instance
tracker = CentroidTracker(maxDisappeared=40, maxDistance=50)

# Process video
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot read frame or video ended.")
        break

    print("Processing frame...")  # Debugging: Processing frame

    # Resize frame for consistency
    frame_resized = cv2.resize(frame, (640, 480))

    # Perform detection with YOLOv5
    results = model(frame_resized)
    detections = results.xyxy[0].cpu().numpy()  # Extract detections

    # Prepare bounding boxes for tracking (rectangles)
    rects = []
    for det in detections:
        x_min, y_min, x_max, y_max, confidence, cls = det
        if confidence > 0.5:  # Only consider detections with confidence > 0.5
            rects.append((int(x_min), int(y_min), int(x_max), int(y_max)))

    # Update CentroidTracker with current detections
    objects = tracker.update(rects)

    # Draw bounding boxes and IDs on the frame
    for objectID, centroid in objects.items():
        cX, cY = centroid  # Get centroid coordinates

        # Draw a circle at the centroid of each tracked object
        cv2.circle(frame_resized, (cX, cY), 5, (0, 255, 0), -1)
        text = f"ID {objectID}"
        cv2.putText(frame_resized, text, (cX, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with tracking info
    cv2.imshow("Video Tracking", frame_resized)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
