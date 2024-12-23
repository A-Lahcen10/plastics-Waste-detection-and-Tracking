import cv2
from ultralytics import YOLO
# Load the YOLO model
model = YOLO('model.pt')

class_list = model.names

# Open the video file
cap = cv2.VideoCapture('video4.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    results = model.track(frame, persist=True) 

    # Ensure results are not empty
    if results[0].boxes.data is not None:
        # Get the detected boxes, their class indices, and track IDs
        boxes = results[0].boxes.xyxy
        track_ids = results[0].boxes.id.int()
        class_indices = results[0].boxes.cls.int()
        confidences = results[0].boxes.conf

        # Loop through each detected object
        for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidences):
            x1, y1, x2, y2 = map(int, box)
                
            class_name = class_list[int(class_idx)]
            
            cv2.putText(frame, f"ID: {track_id} {class_name}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) 


    
    
    # Show the frame
    cv2.imshow(" Object Tracking", frame)    
    
    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()