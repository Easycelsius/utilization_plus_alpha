import sys
import os
import glob
from extractor import extract_latex_from_pdf

def main():
    # Define default input and output directories
    input_dir = "input_pdf"
    output_base_dir = "output_latex_txt"

    # Create directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_base_dir, exist_ok=True)

    # Find all PDF files in the input folder
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

    if not pdf_files:
        print(f"[NOTE] The '{input_dir}' folder is empty. Please upload your PDF files there.")
        return

    print(f"[INFO] Found {len(pdf_files)} PDF file(s) in '{input_dir}'.")

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        # Create a specific output folder for each file to keep results organized
        file_output_dir = os.path.join(output_base_dir, os.path.splitext(filename)[0])
        formulas_file = os.path.join(file_output_dir, "extracted_formulas.txt")

        # Skip if already processed (check for specifically the final formulas file)
        if os.path.exists(formulas_file):
            print(f"\n--- Skipping: {filename} ---")
            print(f"[INFO] '{formulas_file}' already exists. Use --force if we wanted to re-run (not implemented yet).")
            continue

        try:
            print(f"\n--- Processing: {filename} ---")
            extract_latex_from_pdf(pdf_path, file_output_dir)
            print(f"[Done] Result saved to '{file_output_dir}'.")
        except Exception as e:
            print(f"[Error] Failed to process '{filename}': {e}", file=sys.stderr)

    print("\n[Finished] All tasks completed.")

if __name__ == "__main__":
    main()
