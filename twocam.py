import cv2

# Phone camera URL
phone_cam_url = "http://192.168.225.169:4747/video"
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
