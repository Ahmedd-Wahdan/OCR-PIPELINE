# OCR and Object Detection with Fine-tuned TR-OCR and YOLO

## Project Overview
This project focuses on Arabic handwriting recognition using a fine-tuned TR-OCR model on the Khatt dataset and text detection using a fine-tuned YOLO model. The integration of these models enables accurate text detection and recognition in images containing Arabic script. A complete pipeline has been developed that first detects text regions using YOLO and then extracts the text using TR-OCR.

## Features
- Fine-tuned TR-OCR model on the Khatt dataset to enhance Arabic handwriting OCR performance.
- Fine-tuned YOLO model for precise text region detection.
- End-to-end pipeline combining YOLO and TR-OCR for improved recognition accuracy.
- Dataset preprocessing, augmentation, and custom training scripts.
- Implementation in Jupyter notebooks for easy reproducibility.
- Performance evaluation and inference pipelines for real-world application.

## Prerequisites
Ensure you have the following dependencies installed before running the project:
- Python 3.x
- PyTorch
- Transformers (Hugging Face)
- OpenCV
- YOLOv5/YOLOv8 (Ultralytics)
- Jupyter Notebook
- NVIDIA GPU (recommended for training)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dataset Preparation
1. **Download Khatt Dataset:** The dataset must be acquired from the official source.
2. **Preprocess Data:** Convert images into a format compatible with TR-OCR and YOLO.
3. **Augment Data:** Apply transformations such as resizing, normalization, and contrast enhancement.
4. **Split Dataset:** Separate into training, validation, and test sets.

## Fine-Tuning TR-OCR
The fine-tuning process leverages the TR-OCR model from Hugging Face with modifications for Arabic handwriting.

1. **Preprocessing:**
   - Resize and normalize images.
   - Convert labels into tokenized sequences.
2. **Fine-tuning:**
   - Use a VisionEncoderDecoderModel with a pre-trained transformer backbone.
   - Optimize using AdamW and a learning rate scheduler.
3. **Run the Training Notebook:**
   ```bash
   jupyter notebook tr-ocr-yolo.ipynb
   ```

## Fine-Tuning YOLO for Text Detection
The YOLO model is fine-tuned to detect text regions before OCR processing.

1. **Data Annotation:**
   - Label text regions in images.
   - Convert annotations into YOLO-compatible format.
2. **Fine-tuning:**
   - Use pre-trained YOLO weights for transfer learning.
   - Train on annotated images for text detection.
3. **Run the Training Notebook:**
   ```bash
   jupyter notebook YOLO.ipynb
   ```

## Inference Pipeline
A complete pipeline is developed to first detect text regions using YOLO and then recognize the text using TR-OCR.

1. **Detect Text with Fine-tuned YOLO:**
   ```bash
   python detect.py --weights path-to-finetuned-yolo --source test_image.jpg
   ```
2. **Crop Detected Regions and Apply Fine-tuned TR-OCR:**
   ```python
   from transformers import TrOCRProcessor, VisionEncoderDecoderModel
   import torch
   from PIL import Image

   processor = TrOCRProcessor.from_pretrained("path-to-finetuned-trocr")
   model = VisionEncoderDecoderModel.from_pretrained("path-to-finetuned-trocr")

   image = Image.open("cropped_text_region.jpg").convert("RGB")
   inputs = processor(images=image, return_tensors="pt")
   outputs = model.generate(**inputs)
   predicted_text = processor.batch_decode(outputs, skip_special_tokens=True)[0]
   print("Predicted Text:", predicted_text)
   ```

## Evaluation and Performance
- **OCR Performance:** Measured using CER (Character Error Rate) and WER (Word Error Rate).
- **YOLO Accuracy:** Evaluated using mAP (Mean Average Precision).
- **Pipeline Efficiency:** Benchmarked by end-to-end accuracy and processing speed.
- **Comparison:** Evaluated against baseline OCR models to demonstrate improvements.

## Future Work
- Improve generalization by training on larger Arabic datasets.
- Enhance YOLO’s ability to detect small, unclear text regions.
- Optimize inference speed for real-time applications.
- Develop a GUI-based tool integrating the full pipeline.

## Acknowledgments
- [Khatt Dataset](https://example.com)
- [Microsoft TR-OCR](https://huggingface.co/microsoft/trocr)
- [YOLO by Ultralytics](https://github.com/ultralytics/yolov5)****
