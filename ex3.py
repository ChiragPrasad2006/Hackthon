import cv2
import tkinter as tk
from tkinter import Label
import torch  # PyTorch for YOLOv5 inference

# Initialize Tkinter GUI
root = tk.Tk()
root.title("People Density Monitor")
phone_density_label = Label(root, text="Phone Cam: Calculating...", font=("Arial", 18))
phone_density_label.pack()
laptop_density_label = Label(root, text="Laptop Cam: Calculating...", font=("Arial", 18))
laptop_density_label.pack()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # YOLOv5 small model
model.classes = [0] 

# Phone camera URL
phone_cam_url = "http://192.168.161.164:4747/video"
phone_cam = cv2.VideoCapture(phone_cam_url)

# Laptop camera
laptop_cam = cv2.VideoCapture(0)

def process_frame():
    global phone_cam, laptop_cam, model

    phone_count = 0
    laptop_count = 0

    # Read frame from phone camera
    ret1, phone_frame = phone_cam.read()
    if ret1:
        # Resize frame for consistent processing
        phone_frame_resized = cv2.resize(phone_frame, (640, 480))
        # Run YOLO inference
        phone_results = model(phone_frame_resized)

        # Count "person" detections (model is restricted to "person" class only)
        phone_count = len(phone_results.xyxy[0])

    # Read frame from laptop camera
    ret2, laptop_frame = laptop_cam.read()
    if ret2:
        # Resize frame for consistent processing
        laptop_frame_resized = cv2.resize(laptop_frame, (640, 480))
        # Run YOLO inference
        laptop_results = model(laptop_frame_resized)

        # Count "person" detections (model is restricted to "person" class only)
        laptop_count = len(laptop_results.xyxy[0])

    # Update the density in the Tkinter GUI
    phone_density_label.config(text=f"Phone Cam: {phone_count} person(s)")
    laptop_density_label.config(text=f"Laptop Cam: {laptop_count} person(s)")

    # Annotate and display frames
    combined_frame = None
    if ret1 and ret2:
        phone_annotated = phone_results.render()[0]
        laptop_annotated = laptop_results.render()[0]
        combined_frame = cv2.hconcat([phone_annotated, laptop_annotated])
    elif ret1:
        combined_frame = phone_results.render()[0]
    elif ret2:
        combined_frame = laptop_results.render()[0]

    if combined_frame is not None:
        cv2.imshow("Combined Camera Feeds", combined_frame)

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