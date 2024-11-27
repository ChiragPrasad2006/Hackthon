import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose Detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
phone_cam_url = "http://192.168.225.169:4747/video"
cap = cv2.VideoCapture(0)  # Using webcam for live feed
prev_density = 0
threshold_density_increase = 0.2  # Threshold for density change (e.g., 20% increase)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        
        # Count the number of people (based on detected pose landmarks)
        detected_people = 0
        if results.pose_landmarks:
            detected_people += 1  # Count detected person (one person per frame if detected)
        
        frame_area = frame.shape[0] * frame.shape[1]
        
        # Density = number of detected people / area of the frame
        density = detected_people / frame_area
        
        # Compare with previous density for sudden change detection
        if prev_density > 0 and (density - prev_density) / prev_density > threshold_density_increase:
            print("Sudden density increase detected!")
        
        prev_density = density
        
        # Draw pose landmarks on the frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Show the output frame
        cv2.imshow("Pose Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
