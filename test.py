#!/usr/bin/env python3
import cv2
import config
import os, sys
import time
import numpy as np

camera = config.cameras[0]
cap = cv2.VideoCapture(camera['url'])

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
output_root = f"{project_root}/output"
camera['output_folder'] = f"{output_root}/{camera['folder']}"

output_folder = camera['output_folder']
if not os.path.exists(output_folder):
  os.makedirs(output_folder)

if not cap.isOpened():
    print("Failed to open the RTSP stream.")
    exit()

count = 0
prev_frame = None
while True:
    # Read a frame from the stream
    ret, frame = cap.read()

    # Check if a frame is successfully read
    if not ret:
        print("Failed to read a frame from the stream.")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    should_save = False
    if prev_frame is not None:
      diff = cv2.absdiff(gray_frame, prev_frame)
      changed_pixels = np.sum(diff > 0)
      total_pixels = diff.shape[0] * diff.shape[1]
      changed_percent = (changed_pixels / total_pixels) * 100
      count += 1
      # print(changed_percent)
      if changed_percent > 15: should_save = True
    else:
      should_save = True

    if should_save:
      # Save the frame as a JPG image
      image_path = os.path.join(output_folder, f"frame_{count}.jpg")
      cv2.imwrite(image_path, frame)
      print(f"Frame {count} saved as {image_path}")

    time.sleep(0.5)
    prev_frame = gray_frame

# Release the stream and close windows
cap.release()
cv2.destroyAllWindows()