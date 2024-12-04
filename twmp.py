import tkinter as tk
from tkinter import ttk, messagebox,Label
from PIL import Image, ImageTk
import cv2
import os
import torch
import numpy as np
import pandas as pd

email_origin = "0"  # Replace with your default email
master_pass = "0"  # Replace with your master password

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
        background_image = Image.open("Back_ground_image/BackG.png")  # Replace with your image path
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
        background_image1 = Image.open("Back_ground_image/1.png")  # Replace with your image path
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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.eye_open_image = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "Back_ground_image/View(2).png")).resize((20, 20)))
        self.eye_closed_image = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "Back_ground_image/Hide(2).png")).resize((20, 20)))

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
            self.destroy()
            HomePage(tk.Frame)

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

    def add_account(self):
        email = self.email_entry.get()
        masterp = self.password_entry.get()

        if not masterp or not email or masterp != master_pass or email != email_origin:
            messagebox.showwarning("Input Error", "Password or Email is incorrect. Please try again.")
            return

        if masterp == master_pass:
            self.parent.show_frame("HomePage")
            home_page = self.parent.frames["HomePage"]
            home_page.initialize_cameras()

class SignUp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Load background image and store it as an instance attribute
        background_image2 = Image.open("Back_ground_image/2.png")  # Replace with your image path
        resized_image = background_image2.resize((500, 500))  # Adjust to your window size
        self.background_photo = ImageTk.PhotoImage(resized_image)

        background_label = tk.Label(self, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        ttk.Label(self, text="Sign Up (Feature not implemented)").pack(pady=20)


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initialized = False  # Flag to ensure camera setup runs only once

        self.phone_density_label = Label(self, text="Phone Cam: Calculating...", font=("Arial", 16))
        self.phone_density_label.pack(pady=10)
        self.laptop_density_label = Label(self, text="Laptop Cam: Calculating...", font=("Arial", 16))
        self.laptop_density_label.pack(pady=10)

        self.error_label = tk.Label(self, text="", font=("Arial", 16), fg="red")
        self.error_label.pack()

    def initialize_cameras(self):
        if self.initialized:
            return  # Avoid re-initialization

        self.initialized = True
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.classes = [0]  # Detect only "person" class

        self.phone_cam_url = "http://192.168.1.10:8080/video"  # Replace with your phone camera URL
        self.phone_cam = cv2.VideoCapture(self.phone_cam_url)
        self.laptop_cam = cv2.VideoCapture(0)

        self.previous_phone_counts = [0] * 9
        self.previous_laptop_counts = [0] * 9

        self.process_frame()  # Start processing frames

    def draw_grid_and_counts(self, frame, grid_counts, grid_size=(3, 3), color=(0, 255, 0), font_scale=0.6, thickness=2):
            """
            Draw a 3x3 grid on the frame and overlay the person counts in each cell.
            """
            frame_height, frame_width, _ = frame.shape
            cell_width = frame_width // grid_size[1]
            cell_height = frame_height // grid_size[0]

            # Draw grid lines
            for i in range(1, grid_size[1]):
                x = i * cell_width
                cv2.line(frame, (x, 0), (x, frame_height), color, thickness)

            for i in range(1, grid_size[0]):
                y = i * cell_height
                cv2.line(frame, (0, y), (frame_width, y), color, thickness)

            # Draw counts
            for i in range(grid_size[0]):
                for j in range(grid_size[1]):
                    grid_index = i * grid_size[1] + j
                    count_text = f"{grid_counts[grid_index]} person(s)"
                    x = j * cell_width + 10
                    y = i * cell_height + 30
                    cv2.putText(frame, count_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

            return frame

    def process_frame(self):
        # Your frame processing logic goes here...
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
        ret1, phone_frame = self.phone_cam.read()
        if ret1:
            phone_frame_resized = cv2.resize(phone_frame, (640, 480))
            phone_results = self.model(phone_frame_resized)
            phone_detections = phone_results.xyxy[0].cpu().numpy()
            phone_counts = count_people_in_grid(phone_detections, 640, 480)

            # Detect abnormal crowd density increase in phone cam
            for i, (current_count, prev_count) in enumerate(zip(phone_counts, self.previous_phone_counts)):
                if current_count - prev_count > 50:
                    error_label.config(text=f"Check Phone Cam: Issue in Grid Cell {i+1}")

            previous_phone_counts = phone_counts.copy()  # Update counts

            # Annotate frame
            phone_frame_annotated = phone_results.render()[0].copy()
            phone_frame_annotated = self.draw_grid_and_counts(phone_frame_annotated, phone_counts)

        # Process laptop camera
        ret2, laptop_frame = self.laptop_cam.read()
        if ret2:
            laptop_frame_resized = cv2.resize(laptop_frame, (640, 480))
            laptop_results = self.model(laptop_frame_resized)
            laptop_detections = laptop_results.xyxy[0].cpu().numpy()
            laptop_counts = count_people_in_grid(laptop_detections, 640, 480)

            # Detect abnormal crowd density increase in laptop cam
            for i, (current_count, prev_count) in enumerate(zip(laptop_counts, self.previous_laptop_counts)):
                if current_count - prev_count > 50:
                    error_label.config(text=f"Check Laptop Cam: Issue in Grid Cell {i+1}")

            previous_laptop_counts = laptop_counts.copy()  # Update counts

    
            laptop_frame_annotated = laptop_results.render()[0].copy()
            laptop_frame_annotated = self.draw_grid_and_counts(laptop_frame_annotated, laptop_counts)



        self.phone_density_label.config(text=f"Phone Cam: {sum(phone_counts)} person(s)")
        self.laptop_density_label.config(text=f"Laptop Cam: {sum(laptop_counts)} person(s)")


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
            self.quit()
            self.phone_cam.release()
            self.laptop_cam.release()
            cv2.destroyAllWindows()


            self.after(10, self.process_frame)

        self.process_frame()

    def release_resources(self):
        """Release camera resources on exit or switching."""
        if hasattr(self, "phone_cam"):
            self.phone_cam.release()
        if hasattr(self, "laptop_cam"):
            self.laptop_cam.release()
        cv2.destroyAllWindows()


if __name__== "__main__":
    app = App()  # No 'root' argument passed
    app.mainloop()