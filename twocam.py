import cv2


phone_cam_url = "http://192.168.225.169:4747/video"
phone_cam = cv2.VideoCapture(phone_cam_url)


laptop_cam = cv2.VideoCapture(0)

while True:

    ret1, phone_frame = phone_cam.read()
    if not ret1:
        print("Failed to connect to phone camera")
        break

    # Read frame from laptop camera
    ret2, laptop_frame = laptop_cam.read()
    if not ret2:
        print("Failed to connect to laptop camera")
        break

    
    phone_frame = cv2.resize(phone_frame, (640, 480))
    laptop_frame = cv2.resize(laptop_frame, (640, 480))

    
    combined_frame = cv2.hconcat([phone_frame, laptop_frame])

    
    cv2.imshow("Combined Camera Feeds", combined_frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


phone_cam.release()
laptop_cam.release()
cv2.destroyAllWindows()
