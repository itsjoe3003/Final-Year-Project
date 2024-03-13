import os
import numpy as np
import cv2

def resize_images_in_folder(folder_path, x, y, w, h):

  for filename in os.listdir(folder_path):
      # Check if the file is an image
      if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
          # Construct the full file path
          file_path = folder_path + filename
          # Open the image file
          img = cv2.imread(file_path)
          # Resize the image
          img_resized = img[y:y+h, x:x+w]
          # Save the resized image back to the file
          cv2.imwrite(file_path, img_resized)
          # print(f"Resized {filename}")

  # with Image.open(folder_path) as img:
  #   img_resized = img.resize((new_width, new_height))
  #   img_resized.save(folder_path)

# Example usage
file_path = r'map/t/51/'
y=230
x=230
h=300
w=400
resize_images_in_folder(file_path, x, y, w, h)
