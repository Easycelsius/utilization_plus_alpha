# LaTeX Extractor from PDF

This project utilizes a lightweight and fast open-source stack (`marker-pdf`) to extract text and mathematical formulas (LaTeX) from PDF files, designed to run on local machines even without GPU support.

## Features
- **100% Local**: Operates entirely on your local environment without external APIs.
- **Formula Extraction**: Automatically pulls out all LaTeX formulas ($...$ or $$...$$) into a separate `extracted_formulas.txt` file.
- **CPU Friendly**: Runs on CPU-only machines (though processing time may vary as it uses ONNX or PyTorch CPU backends).
- **Environment Isolation**: Uses a project-specific virtual environment (`venv`).

## Installation
1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: On the first run, model weight files may be downloaded from HuggingFace in the background.*

## Usage
1. Place your PDF files into the `input_pdf/` folder.
2. Run the processing script:
   ```bash
   python main.py
   ```
3. The results (Markdown files with LaTeX formulas) will be generated in separate folders within `output_latex_txt/` for each input PDF.

*If no PDF files are found in `input_pdf/`, the script will notify you to upload files.*
