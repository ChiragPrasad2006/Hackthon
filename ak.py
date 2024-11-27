import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Function to update the frame in the Tkinter window
def update_frame():
    global cap
    ret, frame = cap.read()  # Capture a frame from the webcam
    if ret:
        # Convert the frame to RGB (from BGR used by OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to a format suitable for Tkinter
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        # Update the label with the new image
        camera_label.imgtk = img
        camera_label.configure(image=img)
    # Call this function again after a short delay
    camera_label.after(10, update_frame)

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Tkinter Camera Feed")
root.geometry("800x600")

# Open the camera (0 is the default camera)
cap = cv2.VideoCapture(0)

# Add a label to display the video feed
camera_label = tk.Label(root)
camera_label.pack()

# Add a quit button
def quit_app():
    global cap
    cap.release()  # Release the camera resource
    root.destroy()  # Close the Tkinter window

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack()

# Start the video feed update loop
update_frame()

# Start the Tkinter main loop
root.mainloop()
