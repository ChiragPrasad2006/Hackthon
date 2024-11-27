import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import os

email_origin = "0"  # Replace with your default email
master_pass = "0"  # Replace with your master password


class LogSign(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Store reference to the parent window
        self.title("Login or Sign Up")
        self.geometry("500x500")  # Set the window size

        style = ttk.Style(self)
        style.configure(
            "TButton",
            background="#004AAD",  # Set the default background color
            foreground="#004AAD",
            padding = (15, 2),
            font = ("Arial", 12)
        )

        style.map(
            "TButton",
            background=[("active", "#004AAD")],  # Background color when button is active (hovered or clicked)
            foreground=[("active", "blue")],  # Text color when hovered or clicked
        )

        # Create the buttons
        self.log_button = ttk.Button(self, text="Log In",style="TButton",padding=(30, 5), command=self.login_in)
        self.sign_button = ttk.Button(self, text="Sign Up",style="TButton", padding=(27, 5), command=self.signup_in)

        # Calculate positions to center the buttons
        button_width = 120  # Approximate width of the button (adjust as needed)
        button_height = 50  # Approximate height of the button (adjust as needed)

        window_width = 500
        window_height = 500

        x_center = (window_width - button_width) // 2
        log_y_center = (window_height // 2) - 30  # Adjust offset for the first button
        sign_y_center = (window_height // 2) + 30  # Adjust offset for the second button

        # Use place() with calculated positions and anchor
        self.log_button.place(x=x_center, y=log_y_center, width=button_width, height=button_height, anchor="nw")
        self.sign_button.place(x=x_center, y=sign_y_center, width=button_width, height=button_height, anchor="nw")

    def login_in(self):
        self.destroy()  # Close this window
        Login(self.parent)  # Open the Login window

    def signup_in(self):
        self.destroy()  # Close this window
        SignUp(self.parent)  # Open the Sign Up window


class Login(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Store reference to the parent window
        self.title("Login")
        self.geometry("500x500")

        ttk.Label(self, text="Email:").pack(pady=14)
        self.email_entry = ttk.Entry(self, width=40)
        self.email_entry.pack(pady=5)

        ttk.Label(self, text="Master Password:").pack(pady=10)

        # Password Entry Frame
        password_frame = ttk.Frame(self)
        password_frame.pack(pady=5)

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*", width=35)
        self.password_entry.grid(row=0, column=1)

        self.show_password = False

        # Image handling
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.eye_open_image = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "View(1).png")).resize((20, 20)))
        self.eye_closed_image = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "Hide(1).png")).resize((20, 20)))

        self.eye_button = ttk.Label(password_frame, image=self.eye_closed_image, cursor="hand2")
        self.eye_button.grid(row=0, column=2, padx=5)
        self.eye_button.bind("<Button-1>", self.toggle_password)

        self.login_button = ttk.Button(self, text="Login", command=self.add_account)
        self.login_button.pack(pady=20)

    def toggle_password(self, event=None):
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
            self.destroy()
            HomePage(self.parent)



class SignUp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Sign Up")
        self.geometry("500x500")
        ttk.Label(self, text="Sign Up (Feature not implemented)").pack(pady=20)


class HomePage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Home Page")
        self.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

        # Webcam setup
        phone_cam_url = "http://192.168.161.244:4747/video"
phone_cam = cv2.VideoCapture(phone_cam_url)

# Laptop camera (default webcam, usually device index 0)
laptop_cam = cv2.VideoCapture(0)

while True:
    # Read frame from phone camera
    ret1, phone_frame = phone_cam.read()
    if not ret1:
        print("Failed to grab frame from phone camera")
        break

    # Read frame from laptop camera
    ret2, laptop_frame = laptop_cam.read()
    if not ret2:
        print("Failed to grab frame from laptop camera")
        break

    # Resize frames to the same height
    phone_frame = cv2.resize(phone_frame, (640, 480))
    laptop_frame = cv2.resize(laptop_frame, (640, 480))

    # Combine frames horizontally (side-by-side)
    combined_frame = cv2.hconcat([phone_frame, laptop_frame])

    # Display the combined frame
    cv2.imshow("Combined Camera Feeds", combined_frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
phone_cam.release()
laptop_cam.release()
cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    log_sign = LogSign(root)
    log_sign.protocol("WM_DELETE_WINDOW", root.quit)
    log_sign.mainloop()
