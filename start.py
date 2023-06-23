#!/usr/bin/env python3
import cv2
import config
import multiprocessing as mp

def process_camera(camera_id):
  camera = config.cameras[camera_id]
  print(camera)
  # # Create a VideoCapture object
  # cap = cv2.VideoCapture(camera['url'])

  # while True:
  #     # Read the video stream frame by frame
  #     ret, frame = cap.read()

  #     # Check if the frame was successfully captured
  #     if not ret:
  #         break

  #     # Display the frame
  #     cv2.imshow('RTSP Stream', frame)

  #     # Check for key press and exit if 'q' is pressed
  #     if cv2.waitKey(1) & 0xFF == ord('q'):
  #         break

  # # Release the VideoCapture object and close any open windows
  # cap.release()
  return

if __name__ == '__main__':
  # Create face process in a dedicated process
  manager = mp.Manager()

  # Create a multiprocessing Pool
  pool = manager.Pool(processes=len(config.camera_urls))

  results = []
  # using pymongo for faster query

  for camera_id in range(len(config.camera_urls)):
    result = pool.apply_async(process_camera, (camera_id,))
    results.append(result)

  final_results = [result.get() for result in results]
  # Close the Pool to release resources
  pool.close()
  pool.join()
