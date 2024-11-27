import cv2
import tkinter as tk
from tkinter import Label
import torch  # PyTorch for YOLOv5 inference

# Initialize Tkinter GUI
root = tk.Tk()
root.title("People Density Monitor")
density_label = Label(root, text="Density: Calculating...", font=("Arial", 18))
density_label.pack()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # YOLOv5 small model

# Phone camera URL
phone_cam_url = "http://192.168.161.164:4747/video"
phone_cam = cv2.VideoCapture(phone_cam_url)

# Laptop camera
laptop_cam = cv2.VideoCapture(0)

def process_frame():
    global phone_cam, laptop_cam, model

    # Read frame from phone camera
    ret1, phone_frame = phone_cam.read()
    if not ret1:
        phone_frame = None

    # Read frame from laptop camera
    ret2, laptop_frame = laptop_cam.read()
    if not ret2:
        laptop_frame = None

    # Combine frames horizontally
    if phone_frame is not None and laptop_frame is not None:
        phone_frame = cv2.resize(phone_frame, (640, 480))
        laptop_frame = cv2.resize(laptop_frame, (640, 480))
        combined_frame = cv2.hconcat([phone_frame, laptop_frame])
    elif phone_frame is not None:
        combined_frame = phone_frame
    elif laptop_frame is not None:
        combined_frame = laptop_frame
    else:
        combined_frame = None

    if combined_frame is not None:
        # Run YOLO inference
        results = model(combined_frame)

        # Filter out detections labeled as "person"
        people_count = sum(1 for detection in results.xyxy[0] if int(detection[5]) == 0)  # Class 0 = Person

        # Update the density in the Tkinter GUI
        density_label.config(text=f"Density: {people_count} person(s)")

        # Show combined frame in OpenCV window
        annotated_frame = results.render()[0]  # Render detections
        cv2.imshow("Combined Camera Feeds", annotated_frame)

    # Check if 'q' is pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        root.quit()
        phone_cam.release()
        laptop_cam.release()
        cv2.destroyAllWindows()

    # Call this function again
    root.after(10, process_frame)

# Start processing frames
process_frame()

# Start Tkinter main loop
root.mainloop()
