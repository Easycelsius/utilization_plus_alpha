# Utilization Plus Alpha

A collection of various miscellaneous functions and utilities.

## Feature List

### 1. LaTeX Extractor from PDF
Extracts mathematical formulas and Markdown text from PDF files using a local, open-source stack (`marker-pdf`).
- **Location**: `/LaTeX_Extractor_from_PDF`
- **Setup**: Follow the instructions in [LaTeX_Extractor_from_PDF/README.md](file:///Users/easycelsius/git_repo/utilization_plus_alpha/LaTeX_Extractor_from_PDF/README.md) to set up the virtual environment.
- **Workflow**:
  - Place PDFs in `input_pdf/`.
  - Results (Markdown and extracted LaTeX formulas) are generated in `output_latex_txt/`.
  - Mathematical formulas are saved separately in `extracted_formulas.txt` for each PDF.

## Directory Structure
- `LaTeX_Extractor_from_PDF/`: Source code and environment for the PDF extractor.
  - `input_pdf/`: Folder for input PDF files (ignored by Git).
  - `output_latex_txt/`: Folder for generated LaTeX/Markdown output (ignored by Git).
- `AGENTS.md`: Agent configuration and roles.
- `SKILLS.md`: Skills and guidelines for project maintenance.
