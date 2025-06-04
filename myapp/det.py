from datetime import datetime

import torch
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Load YOLO model
model = YOLO(r'C:\Users\91815\PycharmProjects\detectinghum\myapp\static\yolov9c.pt')


def detect_and_plot_bounding_box(image_path):
    # Load image
    img = cv2.imread(image_path)

    # Perform inference using YOLO model
    results = model(img)
    person_count = 0  # Counter for persons

    # Extract bounding box coordinates, confidence, and class labels
    for result in results:  # Loop through the detected objects
        boxes = result.boxes  # Access boxes from result
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Get bounding box coordinates
            conf = float(box.conf.cpu().numpy())  # Extract confidence as a scalar
            cls = int(box.cls.cpu().numpy().item())  # Extract class index as a scalar

            # Count the "person" class (usually class 0 in YOLO models)
            if cls == 0:  # Replace `0` with the index for the "person" class if it's different in your model
                person_count += 1

            # Draw rectangle around detected object
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f'{model.names[cls]} {conf:.2f}'  # Add label with class name and confidence
            cv2.putText(img, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    date=datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'
    output_image_path = r"C:\Users\91815\PycharmProjects\detectinghum\media\det\\"+date

    # Save the processed image to the specified output path
    cv2.imwrite(output_image_path, img)

    # Convert BGR image to RGB for display using Matplotlib
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Display the image with bounding boxes
    # plt.figure(figsize=(10, 10))
    # plt.imshow(img_rgb)
    # plt.axis('off')
    # plt.show()

    # Print the number of detected persons
    print(f"Number of detected persons: {person_count}")
    return person_count,date


# Usage example
# input_image_path = r"C:\Users\91815\OneDrive\Desktop\collapsed_building_image0150_3.png"
# print(detect_and_plot_bounding_box(input_image_path))
