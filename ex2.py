import cv2
import tkinter as tk
from tkinter import Label
import torch  # PyTorch for YOLOv5 inference

# Initialize Tkinter GUI
root = tk.Tk()
root.title("People Density Monitor")

# Labels for phone and laptop overall densities
phone_density_label = Label(root, text="Phone Cam: Calculating...", font=("Arial", 16))
phone_density_label.pack()
laptop_density_label = Label(root, text="Laptop Cam: Calculating...", font=("Arial", 16))
laptop_density_label.pack()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.classes = [0]  # Detect only "person" class

# Phone camera URL
phone_cam_url = "http://192.168.161.164:4747/video"  # Replace with your phone camera's URL
phone_cam = cv2.VideoCapture(phone_cam_url)

# Laptop camera
laptop_cam = cv2.VideoCapture(0)

def draw_grid_and_counts(frame, grid_counts, grid_size=(3, 3), color=(0, 255, 0), font_scale=0.6, thickness=2):
    """
    Draw a 3x3 grid on the frame and overlay the person counts in each cell.
    """
    frame_height, frame_width, _ = frame.shape
    cell_width = frame_width // grid_size[1]
    cell_height = frame_height // grid_size[0]

    # Draw grid lines
    for i in range(1, grid_size[1]):
        x = i * cell_width
        cv2.line(frame, (x, 0), (x, frame_height), color, thickness)  # Vertical lines

    for i in range(1, grid_size[0]):
        y = i * cell_height
        cv2.line(frame, (0, y), (frame_width, y), color, thickness)  # Horizontal lines

    # Overlay counts in each cell
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            grid_index = i * grid_size[1] + j
            count_text = f"{grid_counts[grid_index]} person(s)"
            x = j * cell_width + 10
            y = i * cell_height + 30
            cv2.putText(frame, count_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

    return frame

def process_frame():
    global phone_cam, laptop_cam, model

    phone_counts = [0] * 9  # 9 cells for phone cam
    laptop_counts = [0] * 9  # 9 cells for laptop cam

    # Function to map detections to grid cells
    def count_people_in_grid(detections, frame_width, frame_height, grid_size=(3, 3)):
        grid_counts = [0] * (grid_size[0] * grid_size[1])
        cell_width = frame_width // grid_size[1]
        cell_height = frame_height // grid_size[0]

        for det in detections:
            x_min, y_min, x_max, y_max = det[:4]  # Bounding box
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2

            # Determine which grid cell the detection falls into
            grid_x = int(center_x // cell_width)
            grid_y = int(center_y // cell_height)
            grid_index = grid_y * grid_size[1] + grid_x  # Map 2D grid to 1D list
            if 0 <= grid_index < len(grid_counts):  # Ensure index is valid
                grid_counts[grid_index] += 1

        return grid_counts

    # Process phone camera
    ret1, phone_frame = phone_cam.read()
    if ret1:
        phone_frame_resized = cv2.resize(phone_frame, (640, 480))
        phone_results = model(phone_frame_resized)
        phone_detections = phone_results.xyxy[0].cpu().numpy()
        phone_counts = count_people_in_grid(phone_detections, 640, 480)
        # Create a writable copy of the rendered frame
        phone_frame_annotated = phone_results.render()[0].copy()
        phone_frame_annotated = draw_grid_and_counts(phone_frame_annotated, phone_counts)

    # Process laptop camera
    ret2, laptop_frame = laptop_cam.read()
    if ret2:
        laptop_frame_resized = cv2.resize(laptop_frame, (640, 480))
        laptop_results = model(laptop_frame_resized)
        laptop_detections = laptop_results.xyxy[0].cpu().numpy()
        laptop_counts = count_people_in_grid(laptop_detections, 640, 480)
        # Create a writable copy of the rendered frame
        laptop_frame_annotated = laptop_results.render()[0].copy()
        laptop_frame_annotated = draw_grid_and_counts(laptop_frame_annotated, laptop_counts)

    # Update Tkinter GUI for overall densities
    phone_density_label.config(text=f"Phone Cam: {sum(phone_counts)} person(s)")
    laptop_density_label.config(text=f"Laptop Cam: {sum(laptop_counts)} person(s)")

    # Annotate and display combined frame
    combined_frame = None
    if ret1 and ret2:
        combined_frame = cv2.hconcat([phone_frame_annotated, laptop_frame_annotated])
    elif ret1:
        combined_frame = phone_frame_annotated
    elif ret2:
        combined_frame = laptop_frame_annotated

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
