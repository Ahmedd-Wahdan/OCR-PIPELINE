import cv2
import numpy as np
import os
import shutil

input_dir = "prescription-data"
output_dir = "prescription-data-enhanced"
os.makedirs(output_dir, exist_ok=True)

for img_file in os.listdir(input_dir):
    if img_file.endswith(".jpg"): 
        img = cv2.imread(os.path.join(input_dir, img_file))
        if img is None:
            print(f"Failed to load {img_file}")
            continue
        

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
       
        lower_blue = np.array([90, 50, 50])  
        upper_blue = np.array([130, 255, 255])
        
        
        lower_black = np.array([0, 0, 0])    
        upper_black = np.array([180, 50, 50]) 
        
        # Create masks
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)  # Blue ink
        black_mask = cv2.inRange(hsv, lower_black, upper_black)  # Black text
        
        
        img_with_black_suppressed = img.copy()
        img_with_black_suppressed[black_mask > 0] = [255, 255, 255] 
        
        # Enhance blue: Increase brightness of blue areas
        blue_enhanced = img_with_black_suppressed.copy()
        # Convert the boost value to a NumPy array with correct dtype
        boost = np.array([50, 50, 50], dtype=np.uint8)
        blue_region = blue_enhanced[blue_mask > 0]
        blue_enhanced[blue_mask > 0] = cv2.add(blue_region, boost)
        
       
        cv2.imwrite(os.path.join(output_dir, img_file), blue_enhanced)
        
        
        shutil.copy(f"{input_dir}/{img_file[:-4]}.gt.txt", output_dir)

print("Filtering and enhancement complete!")