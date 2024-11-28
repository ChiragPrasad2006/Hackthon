import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import torch
import os
import numpy as np
import pandas as pd

email_origin = "your_email@example.com"  # Replace with your default email
master_pass = "your_master_password"  # Replace with your master password

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App")
        self.geometry("500x500")
        self.frames = {}

        # Initialize all pages (frames)
        for Page in (LogSign, Login, SignUp, HomePage):
            page_name = Page.__name__
            frame = Page(self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)  # Stack all frames but keep them hidden

        self.show_frame("LogSign")  # Start with the LogSign page

        # Handle the close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_frame(self, page_name):
        """Bring the specified frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()  # Bring the frame to the top

    def on_close(self):
        """Handle the application close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


class LogSign(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Store reference to the parent window

        # Load the background image and store it as an instance attribute
        background_image = Image.open("BackG.png")  # Replace with your image path
        resized_image = background_image.resize((500, 500))  # Adjust to your window size
        self.background_photo = ImageTk.PhotoImage(resized_image)

        # Create a label to hold the image
        background_label = tk.Label(self, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        style = ttk.Style(self)
        style.configure(
            "TButton",
            background="#004AAD",  # Set the default background color
            foreground="#004AAD",
            padding=(15, 2),
            font=("Arial", 12)
        )

        style.map(
            "TButton",
            background=[("active", "#004AAD")],  # Background color when button is active (hovered or clicked)
            foreground=[("active", "blue")],  # Text color when hovered or clicked
        )

        # Create the buttons
        self.log_button = ttk.Button(self, text="Log In", style="TButton", padding=(30, 5), command=lambda: parent.show_frame("Login"))
        self.sign_button = ttk.Button(self, text="Sign Up", style="TButton", padding=(27, 5), command=lambda: parent.show_frame("SignUp"))

        # Calculate positions to center the buttons
        button_width = 120  # Approximate width of the button (adjust as needed)
        button_height = 40  # Approximate height of the button (adjust as needed)

        window_width = 500
        window_height = 500

        x_center = (window_width - button_width) // 2
        log_y_center = (window_height // 2) - 30  # Adjust offset for the first button
        sign_y_center = (window_height // 2) + 30  # Adjust offset for the second button

        # Use place() with calculated positions and anchor
        self.log_button.place(x=x_center, y=log_y_center, width=button_width, height=button_height, anchor="nw")
        self.sign_button.place(x=x_center, y=sign_y_center, width=button_width, height=button_height, anchor="nw")


class Login(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Store reference to the parent window

        self.grid_rowconfigure(0, weight=1)  # Allow rows to expand
        self.grid_rowconfigure(6, weight=1)  # Bottom spacer
        self.grid_columnconfigure(0, weight=1)  # Allow columns to expand

        # Load background image and store it as an instance attribute
        background_image1 = Image.open("1.png")  # Replace with your image path
        resized_image = background_image1.resize((500, 500))  # Adjust to your window size
        self.background_photo = ImageTk.PhotoImage(resized_image)

        background_label = tk.Label(self, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        # Email Label and Entry
        ttk.Label(self, text="Email:").grid(row=1, column=0, pady=(20, 5), sticky="n")
        self.email_entry = ttk.Entry(self, width=40)
        self.email_entry.grid(row=2, column=0, pady=(0, 20), sticky="n")

        # Password Label and Entry
        ttk.Label(self, text="Master Password:").grid(row=3, column=0, pady=(0, 5), sticky="n")

        password_frame = ttk.Frame(self)  # Create a frame for password entry and toggle
        password_frame.grid(row=4, column=0, pady=(0, 20), sticky="n")

        self.show_password = False

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*", width=35)
        self.password_entry.grid(row=0, column=0)

        # Password visibility toggle button
        self.eye_open_image = ImageTk.PhotoImage(Image.open("View(2).png").resize((20, 20)))  # Replace with your image path
        self.eye_closed_image = ImageTk.PhotoImage(Image.open("Hide(2).png").resize((20, 20)))  # Replace with your image path

        self.eye_button = ttk.Label(password_frame, image=self.eye_closed_image, cursor="hand2")
        self.eye_button.grid(row=0, column=1, padx=5)
        self.eye_button.bind("<Button-1>", self.toggle_password)

        # Login Button
        self.login_button = ttk.Button(self, text="Login", command=self.add_account)
        self.login_button.grid(row=5, column=0, pady=(0, 30), sticky="n")

    def add_account(self):
        emailp = self.email_entry.get()
        masterpass = self.password_entry.get()

        if not masterpass or not emailp or masterpass != master_pass or emailp != email_origin:
            messagebox.showwarning("Input Error", "Password or Email is incorrect. Please try again.")
            return

        if masterpass == master_pass:
            self.parent.show_frame("HomePage")

    def toggle_password(self, event=None):
        """Toggle password visibility."""
        if self.show_password:
            self.password_entry.config(show="*")
            self.eye_button.config(image=self.eye_closed_image)
            self.show_password = False
        else:
            self.password_entry.config(show="")
            self.eye_button.config(image=self.eye_open_image)
            self.show_password = True


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Camera feeds and other attributes
        self.phone_cam_url = "http://192.168.161.164:4747/video"
        self.phone_cam = cv2.VideoCapture(self.phone_cam_url)
        self.laptop_cam = cv2.VideoCapture(0)
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.classes = [0]  # Detect "person" class

        self.previous_phone_counts = [0] * 9
        self.previous_laptop_counts = [0] * 9

        # UI Components - Instance variables
        self.phone_density_label = tk.Label(self, text="Phone Cam: Calculating...", font=("Arial", 16))
        self.phone_density_label.pack()
        self.laptop_density_label = tk.Label(self, text="Laptop Cam: Calculating...", font=("Arial", 16))
        self.laptop_density_label.pack()

        # Canvas to show camera feed
        self.canvas = tk.Canvas(self, width=640, height=480)
        self.canvas.pack()

        self.process_frame()  # Start processing frames

    def process_frame(self):
        # Process phone camera
        if self.phone_cam.isOpened():
            ret1, phone_frame = self.phone_cam.read()
            if ret1:
                phone_results = self.model(phone_frame)
                phone_detections = phone_results.xyxy[0].cpu().numpy()
                phone_counts = self.count_people_in_grid(phone_detections, phone_frame.shape[1], phone_frame.shape[0])
                phone_frame = self.draw_grid_and_counts(phone_frame, phone_counts)
                self.phone_density_label.config(text=f"Phone Cam: {sum(phone_counts)} person(s)")

                self.display_image(phone_frame)

        # Process laptop camera
        if self.laptop_cam.isOpened():
            ret2, laptop_frame = self.laptop_cam.read()
            if ret2:
                laptop_results = self.model(laptop_frame)
                laptop_detections = laptop_results.xyxy[0].cpu().numpy()
                laptop_counts = self.count_people_in_grid(laptop_detections, laptop_frame.shape[1], laptop_frame.shape[0])
                laptop_frame = self.draw_grid_and_counts(laptop_frame, laptop_counts)
                self.laptop_density_label.config(text=f"Laptop Cam: {sum(laptop_counts)} person(s)")

        self.after(100, self.process_frame)  # Call again after 100ms

    def count_people_in_grid(self, detections, frame_width, frame_height):
        grid_size = 3
        grid_counts = [0] * (grid_size * grid_size)
        grid_width = frame_width // grid_size
        grid_height = frame_height // grid_size

        for detection in detections:
            x1, y1, x2, y2, conf, cls = detection
            if conf > 0.5:  # Filter by confidence threshold
                person_x_center = (x1 + x2) / 2
                person_y_center = (y1 + y2) / 2
                grid_x = int(person_x_center // grid_width)
                grid_y = int(person_y_center // grid_height)
                grid_idx = grid_y * grid_size + grid_x
                grid_counts[grid_idx] += 1

        return grid_counts

    def draw_grid_and_counts(self, frame, grid_counts):
        grid_size = 3
        frame_height, frame_width, _ = frame.shape
        grid_width = frame_width // grid_size
        grid_height = frame_height // grid_size

        for i in range(grid_size):
            for j in range(grid_size):
                x0, y0 = j * grid_width, i * grid_height
                x1, y1 = (j + 1) * grid_width, (i + 1) * grid_height
                cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
                cv2.putText(frame, f"{grid_counts[i * grid_size + j]}", (x0 + 5, y0 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame

    def display_image(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)
        image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=image_tk, anchor="nw")
        self.update_idletasks()


if __name__ == "__main__":
    app = App()
    app.mainloop()
