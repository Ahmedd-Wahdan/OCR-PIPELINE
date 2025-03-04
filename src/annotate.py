import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import os
import pandas as pd

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Text Annotator")
        
        self.canvas = tk.Canvas(root, width=640, height=640)
        self.canvas.pack()
        
        # Label for image name and remaining count
        self.image_info_label = tk.Label(root, text="No image loaded", font=("Arial", 12))
        self.image_info_label.pack(pady=5)
        
        # Text box for prescription (mixed Arabic/English, normal state, read-only via bindings)
        self.prescription_text_box = tk.Text(root, height=4, width=50, font=("Arial Unicode MS", 12))
        self.prescription_text_box.pack(pady=5)
        
        # Bindings for copying and preventing edits
        self.prescription_text_box.bind("<Control-a>", lambda e: self.prescription_text_box.tag_add("sel", "1.0", "end"))
        self.prescription_text_box.bind("<Control-c>", self.copy_text)
        self.prescription_text_box.bind("<Button-3>", self.copy_text)  # Right-click to copy
        self.prescription_text_box.bind("<Key>", self.prevent_edit)
        
        # Text box for annotation (editable for user input)
        self.annotation_text_box = tk.Text(root, height=4, width=50, font=("Arial Unicode MS", 12))
        self.annotation_text_box.pack()
        
        self.save_btn = tk.Button(root, text="Save Box", command=self.save_box)
        self.save_btn.pack(side=tk.LEFT)
        
        self.undo_btn = tk.Button(root, text="Undo Last Box", command=self.undo_box)
        self.undo_btn.pack(side=tk.LEFT)
        
        self.next_btn = tk.Button(root, text="Next Image", command=self.next_image)
        self.next_btn.pack(side=tk.LEFT)
        
        self.images = []  # List of image paths
        self.current_image = 0
        self.start_x = self.start_y = 0
        self.current_rect = None
        self.rectangles = []  # Store (coords, text) for current image
        self.image_to_text = {}  # Mapping of image names to prescription text (mixed Arabic/English)
        
        self.load_image_folder()
        
        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<B1-Motion>", self.draw_rect)
        self.canvas.bind("<ButtonRelease-1>", self.end_rect)
        
    def prevent_edit(self, event):
        if event.keysym not in ('Control_L', 'Control_R', 'a', 'c'):  # Allow Ctrl+A, Ctrl+C
            return "break"  # Block other keys
    
    def copy_text(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.prescription_text_box.get("1.0", tk.END).strip())
        self.root.update()
    
    def load_image_folder(self):
        # Select Excel file first
        excel_file = filedialog.askopenfilename(
            title="Select Excel File with Prescriptions",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not excel_file:
            messagebox.showerror("Error", "No Excel file selected!")
            self.root.quit()
            return
            
        # Read Excel file (try .xlsx first, then .xls)
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read Excel file: {e}")
            self.root.quit()
            return
            
        # Ensure required columns exist (adjust column names if needed)
        if 'Image' not in df.columns or 'Prescription' not in df.columns:
            messagebox.showerror("Error", "Excel file must have 'Image' and 'Prescription' columns!")
            self.root.quit()
            return
            
        # Create mapping of image names to mixed Arabic/English prescription text
        self.image_to_text = dict(zip(df['Image'].str.strip(), df['Prescription'].astype(str)))
        
        # Select image folder
        folder = filedialog.askdirectory(title="Select Folder Containing Images")
        if not folder:
            self.root.quit()
            return
            
        self.images = [os.path.join(folder, f) for f in os.listdir(folder) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not self.images:
            messagebox.showerror("Error", "No images found in selected folder!")
            self.root.quit()
            return
            
        self.output_base_dir = r"C:\Users\ahmed\Desktop\STP\prescription-data"
        self.resized_image_dir = os.path.join(self.output_base_dir, "images")
        self.label_dir = os.path.join(self.output_base_dir, "labels")
        self.annotation_dir = os.path.join(self.output_base_dir, "annotations")
        
        if not (os.path.exists(self.resized_image_dir) and 
                os.path.exists(self.label_dir) and 
                os.path.exists(self.annotation_dir)):
            messagebox.showerror("Error", "Required folders (images, labels, annotations) not found!")
            self.root.quit()
            return
        
        processed_images = {os.path.splitext(f)[0].split('_resized')[0] 
                           for f in os.listdir(self.resized_image_dir) 
                           if f.endswith('_resized.jpg')}
        self.images = [img for img in self.images 
                      if os.path.splitext(os.path.basename(img))[0] not in processed_images]
        
        if not self.images:
            messagebox.showinfo("Done", "All images in the folder have been annotated!")
            self.root.quit()
            return
        
        self.show_image()
        self.annotation_text_box.focus_set()  # Focus on annotation box for input
            
    def show_image(self):
        while self.current_image < len(self.images):
            # Load and resize the current image
            img = Image.open(self.images[self.current_image])
            aspect_ratio = img.width / img.height
            if aspect_ratio > 1:
                new_width = 640
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = 640
                new_width = int(new_height * aspect_ratio)
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.current_resized_img = ImageOps.pad(img_resized, (640, 640), color=(114, 114, 114))
            
            # Display on canvas
            self.photo = ImageTk.PhotoImage(self.current_resized_img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            # Redraw existing rectangles
            for coords, _ in self.rectangles:
                self.canvas.create_rectangle(coords, outline="red")
            
            # Update label with image name and remaining count
            current_image_name = os.path.basename(self.images[self.current_image])
            base_name = os.path.splitext(current_image_name)[0]  # e.g., "image1" from "image1.jpg"
            remaining_images = len(self.images) - self.current_image - 1  # Exclude current image
           
            # Look up mixed Arabic/English prescription text from Excel mapping
            prescription_text = self.image_to_text.get(base_name, "No prescription text found")
           
            self.image_info_label.config(
                text=f"Current Image: {current_image_name} | {remaining_images} images left"
            )
           
            # Update prescription text box
            self.prescription_text_box.delete("1.0", tk.END)
            self.prescription_text_box.insert("1.0", prescription_text)
           
            # Clear and focus on annotation text box
            self.annotation_text_box.delete("1.0", tk.END)
           
            break
        else:
            self.image_info_label.config(text="No more images to annotate")
            messagebox.showinfo("Done", "All images have been annotated!")
            self.root.quit()
            
    def start_rect(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(self.start_x, self.start_y, 
                                                       self.start_x, self.start_y, 
                                                       outline="red")
        
    def draw_rect(self, event):
        self.canvas.coords(self.current_rect, self.start_x, self.start_y, event.x, event.y)
        
    def end_rect(self, event):
        pass
        
    def save_box(self):
        if not self.current_rect:
            messagebox.showwarning("Warning", "Please draw a bounding box first!")
            return
        
        text = self.annotation_text_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text for the bounding box!")
            return
            
        coords = self.canvas.coords(self.current_rect)
        self.rectangles.append((coords, text))
        self.annotation_text_box.delete("1.0", tk.END)
        self.canvas.delete(self.current_rect)
        self.current_rect = None
        self.show_image()
        
    def undo_box(self):
        if self.rectangles:
            self.rectangles.pop()
            self.show_image()
        else:
            messagebox.showinfo("Info", "No boxes to undo!")
            
    def next_image(self):
        if self.current_image < len(self.images):
            if self.current_rect:
                messagebox.showwarning("Warning", "Please save or remove the current box first!")
                return
                
            if self.rectangles:
                base_name = os.path.splitext(os.path.basename(self.images[self.current_image]))[0]
                resized_img_path = os.path.join(self.resized_image_dir, f"{base_name}_resized.jpg")
                label_path = os.path.join(self.label_dir, f"{base_name}_resized.txt")
                
                self.current_resized_img.save(resized_img_path)
                
                yolo_lines = []
                for i, (coords, text) in enumerate(self.rectangles):
                    x1, y1, x2, y2 = map(int, coords)
                    box_width = x2 - x1
                    box_height = y2 - y1
                    x_center = x1 + (box_width / 2)
                    y_center = y1 + (box_height / 2)
                    
                    x_center /= 640
                    y_center /= 640
                    box_width /= 640
                    box_height /= 640
                    
                    yolo_lines.append(f"0 {x_center} {y_center} {box_width} {box_height}")
                    
                    crop_area = (x1, y1, x2, y2)
                    cropped_img = self.current_resized_img.crop(crop_area)
                    crop_img_path = os.path.join(self.annotation_dir, f"{base_name}_resized_box{i}.png")
                    crop_text_path = os.path.join(self.annotation_dir, f"{base_name}_resized_box{i}.txt")
                    cropped_img.save(crop_img_path)
                    with open(crop_text_path, "w", encoding="utf-8") as f:
                        f.write(text)
                
                with open(label_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(yolo_lines) + "\n")
                
                print(f"Saved: {resized_img_path}, {label_path}, and annotations in {self.annotation_dir}")
            
            self.current_image += 1
            self.rectangles = []
            self.annotation_text_box.delete("1.0", tk.END)
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()