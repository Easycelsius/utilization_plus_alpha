import subprocess
import os
import re
import glob

def extract_formulas_from_text(content: str) -> list[dict]:
    """
    Extracts all LaTeX formulas from a given Markdown text content.
    Handles both display math ($$...$$) and inline math ($...$).
    Returns a list of dicts: {'type': 'Display'|'Inline', 'content': str}
    """
    formulas = []

    # Step 1: Extract display math blocks ($$...$$)
    display_pattern = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
    display_matches = display_pattern.findall(content)
    for match in display_matches:
        stripped = match.strip()
        if stripped:
            formulas.append({'type': 'Display', 'content': stripped})

    # Remove display math from content before searching for inline
    content_no_display = display_pattern.sub('', content)

    # Step 2: Extract inline math ($...$)
    inline_pattern = re.compile(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)')
    inline_matches = inline_pattern.findall(content_no_display)
    for match in inline_matches:
        stripped = match.strip()
        if stripped:
            formulas.append({'type': 'Inline', 'content': stripped})

    return formulas

def extract_formulas_from_markdown(md_path: str) -> list[dict]:
    """
    Parses a Markdown file and extracts all LaTeX formulas.
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return extract_formulas_from_text(content)

def run_marker_pdf(pdf_path: str, output_dir: str):
    """
    Runs the marker_single CLI tool to convert PDF to Markdown.
    """
    print(f"[INFO] Starting extraction for '{pdf_path}'. (This may take a while)")
    try:
        env = os.environ.copy()
        env["CUDA_VISIBLE_DEVICES"] = ""
        result = subprocess.run(
            ["marker_single", pdf_path, "--output_dir", output_dir],
            check=True,
            capture_output=True,
            text=True,
            env=env
        )
        print("[SUCCESS] PDF parsing completed.")
        if result.stdout.strip():
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("[ERROR] An error occurred during extraction.")
        print(f"Error Code: {e.returncode}")
        print(f"Error Output: {e.stderr}")
        raise

def find_md_files(directory: str) -> list[str]:
    """
    Finds all Markdown files in the given directory recursively.
    """
    return glob.glob(os.path.join(directory, "**", "*.md"), recursive=True)

def process_md_files_for_formulas(md_files: list[str]) -> list[dict]:
    """
    Extracts formulas from a list of Markdown files.
    """
    all_formulas = []
    for md_file in md_files:
        print(f"[INFO] Extracting formulas from: {md_file}")
        formulas = extract_formulas_from_markdown(md_file)
        all_formulas.extend(formulas)
    return all_formulas

def save_formulas_to_files(formulas: list[dict], output_dir: str):
    """
    Saves the extracted formulas to dedicated text files in the output directory.
    """
    if not formulas:
        print("[NOTE] No LaTeX formulas found in the generated Markdown.")
        return

    # Step 3: Save extracted formulas to dedicated files (two versions)
    # Version 1: Labeled for reference
    labeled_path = os.path.join(output_dir, "extracted_formulas.txt")
    with open(labeled_path, 'w', encoding='utf-8') as f:
        for item in formulas:
            f.write(f"[{item['type']}] {item['content']}\n\n")

    # Version 2: Wrapped for direct LaTeX usage (preserve Inline/Display)
    wrapped_path = os.path.join(output_dir, "extracted_formulas_wrapped.txt")
    with open(wrapped_path, 'w', encoding='utf-8') as f:
        for item in formulas:
            if item['type'] == 'Display':
                f.write(f"$$\n{item['content']}\n$$\n\n")
            else:
                f.write(f"${item['content']}$\n\n")

    print(f"[SUCCESS] Extracted {len(formulas)} formulas.")
    print(f"[INFO] Reference: {labeled_path}")
    print(f"[INFO] Wrapped: {wrapped_path}")

def extract_latex_from_pdf(pdf_path: str, output_dir: str):
    """
    Calls the marker-pdf CLI to parse the PDF into Markdown (including LaTeX for formulas).
    Then post-processes the output to extract all LaTeX formulas into separate files.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Input PDF file not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Run marker-pdf to convert PDF to Markdown
    run_marker_pdf(pdf_path, output_dir)

    # Step 2: Find generated .md files and extract formulas
    md_files = find_md_files(output_dir)

    if not md_files:
        print("[WARN] No Markdown files found in the output. Formula extraction skipped.")
        return

    all_formulas = process_md_files_for_formulas(md_files)

    # Step 3: Save extracted formulas to dedicated files
    save_formulas_to_files(all_formulas, output_dir)

if __name__ == "__main__":
    output_dir = "LaTeX_Extractor_from_PDF/output_latex_txt/SQM-w2 (1)"
    md_files = find_md_files(output_dir)
    all_formulas = process_md_files_for_formulas(md_files)
    save_formulas_to_files(all_formulas, output_dir)