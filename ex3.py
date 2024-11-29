import cv2
import tkinter as tk
from tkinter import Label
import torch  # PyTorch for YOLOv5 inference
import numpy as np


root = tk.Tk()
root.title("People Density Monitor")


phone_density_label = Label(root, text="Phone Cam: Calculating...", font=("Arial", 16))
phone_density_label.pack()
laptop_density_label = Label(root, text="Laptop Cam: Calculating...", font=("Arial", 16))
laptop_density_label.pack()


error_label = Label(root, text="", font=("Arial", 16), fg="red")
error_label.pack()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.classes = [0]  # Detect only "person" class

# Phone camera URL
phone_cam_url = "http://192.168.137.190:4747/video"#make sure your are connected to same network
phone_cam = cv2.VideoCapture(phone_cam_url)

# Laptop camera
laptop_cam = cv2.VideoCapture(0)

# Initialize  grid cells for the feed
previous_phone_counts = [0] * 9 
previous_laptop_counts = [0] * 9 

def draw_grid_and_counts(frame, grid_counts, grid_size=(3, 3), color=(0, 255, 0), font_scale=0.6, thickness=2):
    """
    Draw a 3x3 grid on the frame and overlay the person counts in each cell.
    """
    frame_height, frame_width, _ = frame.shape
    cell_width = frame_width // grid_size[1]
    cell_height = frame_height // grid_size[0]


    for i in range(1, grid_size[1]):
        x = i * cell_width
        cv2.line(frame, (x, 0), (x, frame_height), color, thickness) 

    for i in range(1, grid_size[0]):
        y = i * cell_height
        cv2.line(frame, (0, y), (frame_width, y), color, thickness)

 
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            grid_index = i * grid_size[1] + j
            count_text = f"{grid_counts[grid_index]} person(s)"
            x = j * cell_width + 10
            y = i * cell_height + 30
            cv2.putText(frame, count_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

    return frame

def process_frame():
    global phone_cam, laptop_cam, model, previous_phone_counts, previous_laptop_counts

    phone_counts = [0] * 9
    laptop_counts = [0] * 9

    def count_people_in_grid(detections, frame_width, frame_height, grid_size=(3, 3)):
        grid_counts = [0] * (grid_size[0] * grid_size[1])
        cell_width = frame_width // grid_size[1]
        cell_height = frame_height // grid_size[0]

        for det in detections:
            x_min, y_min, x_max, y_max = det[:4]
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2

            
            grid_x = int(center_x // cell_width)
            grid_y = int(center_y // cell_height)
            grid_index = grid_y * grid_size[1] + grid_x
            if 0 <= grid_index < len(grid_counts):
                grid_counts[grid_index] += 1

        return grid_counts

    # Process phone camera
    ret1, phone_frame = phone_cam.read()
    if ret1:
        phone_frame_resized = cv2.resize(phone_frame, (640, 480))
        phone_results = model(phone_frame_resized)
        phone_detections = phone_results.xyxy[0].cpu().numpy()
        phone_counts = count_people_in_grid(phone_detections, 640, 480)

        # Detect abnormal crowd density increase in phone cam
        for i, (current_count, prev_count) in enumerate(zip(phone_counts, previous_phone_counts)):
            if current_count - prev_count > 50:
                error_label.config(text=f"Check Phone Cam: Issue in Grid Cell {i+1}")

        previous_phone_counts = phone_counts.copy()  # Update counts

        # Annotate frame
        phone_frame_annotated = phone_results.render()[0].copy()
        phone_frame_annotated = draw_grid_and_counts(phone_frame_annotated, phone_counts)

    # Process laptop camera
    ret2, laptop_frame = laptop_cam.read()
    if ret2:
        laptop_frame_resized = cv2.resize(laptop_frame, (640, 480))
        laptop_results = model(laptop_frame_resized)
        laptop_detections = laptop_results.xyxy[0].cpu().numpy()
        laptop_counts = count_people_in_grid(laptop_detections, 640, 480)

        # Detect abnormal crowd density increase in laptop cam
        for i, (current_count, prev_count) in enumerate(zip(laptop_counts, previous_laptop_counts)):
            if current_count - prev_count > 50:
                error_label.config(text=f"Check Laptop Cam: Issue in Grid Cell {i+1}")

        previous_laptop_counts = laptop_counts.copy()  # Update counts

        
        laptop_frame_annotated = laptop_results.render()[0].copy()
        laptop_frame_annotated = draw_grid_and_counts(laptop_frame_annotated, laptop_counts)


    phone_density_label.config(text=f"Phone Cam: {sum(phone_counts)} person(s)")
    laptop_density_label.config(text=f"Laptop Cam: {sum(laptop_counts)} person(s)")


    if ret1 or ret2:

        separator = np.zeros((480, 10, 3), dtype=np.uint8)

        if ret1 and ret2:
            combined_frame = cv2.hconcat([phone_frame_annotated, separator, laptop_frame_annotated])
        elif ret1:
            combined_frame = phone_frame_annotated
        elif ret2:
            combined_frame = laptop_frame_annotated

        cv2.imshow("Combined Camera Feeds", combined_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        root.quit()
        phone_cam.release()
        laptop_cam.release()
        cv2.destroyAllWindows()


    root.after(10, process_frame)


process_frame()


root.mainloop()