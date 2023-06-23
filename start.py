#!/usr/bin/env python3
import cv2
import config
import multiprocessing as mp
from core.image_capture import image_capture
from core.image_processor import image_processor

def process_camera(camera_id):
  camera = config.cameras[camera_id]
  image_capture(camera=camera, callback=image_processor)
  return

if __name__ == '__main__':
  # Create face process in a dedicated process
  manager = mp.Manager()

  # Create a multiprocessing Pool
  pool = manager.Pool(processes=len(config.cameras))

  results = []
  # using pymongo for faster query

  for camera_id in range(len(config.cameras)):
    result = pool.apply_async(process_camera, (camera_id,))
    results.append(result)

  final_results = [result.get() for result in results]
  # Close the Pool to release resources
  pool.close()
  pool.join()
