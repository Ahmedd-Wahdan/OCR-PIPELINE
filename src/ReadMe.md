# OCR Pipeline for Handwritten Medical Prescriptions

This repository contains an **OCR pipeline** designed to extract text from handwritten medical prescriptions using a combination of **YOLO11n** (for text detection) and **TrOCR** (for text recognition). The pipeline is tailored for processing medical prescriptions, supporting both English and Arabic text, and is optimized for deployment on local machines or cloud environments like Google Colab.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Local Environment](#local-environment)
  - [Google Colab](#google-colab)
- [Model Training](#model-training)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview
The OCR pipeline combines object detection and optical character recognition to digitize handwritten medical prescriptions. It performs the following steps:
1. **Text Detection**: Uses a fine-tuned YOLO11n model to detect text regions in prescription images.
2. **Text Recognition**: Employs a fine-tuned TrOCR model to transcribe the detected text regions into readable text.
3. **Output**: Returns the extracted text, sorted by vertical position, as a comma-separated string.

The pipeline is designed to handle real-world prescription images, with models trained on custom datasets for improved accuracy in medical contexts.

## Features
- **Dual Model Approach**: Combines YOLO11n for detection and TrOCR for recognition.
- **Multilingual Support**: Recognizes handwritten text in English and Arabic.
- **Custom Trained Models**: Fine-tuned on medical prescription datasets.
- **Flexible Deployment**: Works on local setups (Windows/Linux) and cloud platforms (Google Colab).
- **Preprocessing**: Includes image resizing and padding for consistent input sizes.

## Requirements
- Python 3.8+
- GPU (recommended for faster inference and training)
- Libraries:
  - `ultralytics`
  - `transformers`
  - `huggingface_hub`
  - `torch`
  - `pillow`
  - `pandas` (optional, for data handling)
  - `datasets` (for TrOCR training)
  - `evaluate` (for TrOCR evaluation)

## Installation

### Local Environment
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ahmedd-Wahdan/OCR-PIPELINE.git
   cd OCR-PIPELINE
