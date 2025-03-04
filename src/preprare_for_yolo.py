import os
import shutil
from sklearn.model_selection import train_test_split

def setup_train_val_split(source_dir, output_base_dir, train_ratio=0.9):
    """
    Shuffle and split images and their YOLO labels into train and val folders without deleting originals.
    
    Args:
        source_dir (str): Path to the folder containing images and labels (e.g., prescription-data).
        output_base_dir (str): Path where train and val folders will be created (e.g., prescription-data).
        train_ratio (float): Proportion of data for training (default 0.9 for 90%).
    """
    
    image_dir = os.path.join(source_dir, "images")
    label_dir = os.path.join(source_dir, "labels")
    
    
    if not (os.path.exists(image_dir) and os.path.exists(label_dir)):
        print(f"Error: Source directories {image_dir} and/or {label_dir} not found!")
        return
    
    
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not image_files:
        print(f"Error: No images found in {image_dir}!")
        return
    
   
    image_base_names = [os.path.splitext(f)[0] for f in image_files]
    missing_labels = [name for name in image_base_names if not os.path.exists(os.path.join(label_dir, f"{name}.txt"))]
    if missing_labels:
        print(f"Warning: Missing label files for: {missing_labels}")
    
    
    train_images, val_images = train_test_split(image_files, train_size=train_ratio, random_state=42, shuffle=True)
    
    
    train_dir = os.path.join(output_base_dir, "train")
    val_dir = os.path.join(output_base_dir, "val")
    
    train_images_dir = os.path.join(train_dir, "images")
    train_labels_dir = os.path.join(train_dir, "labels")
    val_images_dir = os.path.join(val_dir, "images")
    val_labels_dir = os.path.join(val_dir, "labels")
    
    
    for dir_path in [train_images_dir, train_labels_dir, val_images_dir, val_labels_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
   
    for img_file in train_images:
        base_name = os.path.splitext(img_file)[0]  # e.g., "image1" from "image1.jpg"
        label_file = f"{base_name}.txt"  # e.g., "image1.txt"
        
        src_img = os.path.join(image_dir, img_file)
        src_label = os.path.join(label_dir, label_file)
        dst_img = os.path.join(train_images_dir, img_file)
        dst_label = os.path.join(train_labels_dir, label_file)
        
        shutil.copy2(src_img, dst_img)  
        if os.path.exists(src_label):
            shutil.copy2(src_label, dst_label) 
        else:
            print(f"Warning: Label file {src_label} not found for {img_file}")
    
   
    for img_file in val_images:
        base_name = os.path.splitext(img_file)[0]
        label_file = f"{base_name}.txt"
        
        src_img = os.path.join(image_dir, img_file)
        src_label = os.path.join(label_dir, label_file)
        dst_img = os.path.join(val_images_dir, img_file)
        dst_label = os.path.join(val_labels_dir, label_file)
        
        shutil.copy2(src_img, dst_img)
        if os.path.exists(src_label):
            shutil.copy2(src_label, dst_label)
        else:
            print(f"Warning: Label file {src_label} not found for {img_file}")
    
    # Report results
    print(f"Train split: {len(train_images)} images in {train_images_dir}")
    print(f"Validation split: {len(val_images)} images in {val_images_dir}")
    print(f"Labels copied to {train_labels_dir} and {val_labels_dir}")
    print(f"Original files remain intact in {image_dir} and {label_dir}")

if __name__ == "__main__":

    source_dir = r"C:\Users\ahmed\Desktop\STP\prescription-data"
    output_base_dir = r"C:\Users\ahmed\Desktop\STP\YOLO_DATA"
    
 
    setup_train_val_split(source_dir, output_base_dir)