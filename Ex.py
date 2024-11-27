import torch
import cv2

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # YOLOv5 small model
model.classes = [0]  # Class 0 corresponds to 'person' in the COCO dataset

def detect_people_live():
    # Access the webcam (use 0 for default webcam, or change to another index for external cameras)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return
    
    print("Press 'q' to exit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break
        
        # Perform detection
        # YOLOv5 expects the frame in RGB format
        results = model(frame, size=640)  # YOLOv5 handles the RGB conversion internally
        
        # Render detections on the frame
        results.render()  # Annotates the frame in-place
        
        # Ensure the annotated frame remains in BGR for OpenCV display
        annotated_frame = results.ims[0]
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
        
        # Display the frame
        cv2.imshow("Person Detection - Live Feed", annotated_frame)
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

# Run the live feed detection
detect_people_live()
