import subprocess
import os
import re
import glob

def extract_formulas_from_markdown(md_path: str) -> list[str]:
    """
    Parses a Markdown file and extracts all LaTeX formulas.
    Handles both display math ($$...$$) and inline math ($...$).
    Returns a list of formula strings.
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    formulas = []

    # Step 1: Extract display math blocks ($$...$$) and replace them with
    # placeholders so they don't get caught by the inline regex.
    display_pattern = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
    display_matches = display_pattern.findall(content)
    for match in display_matches:
        stripped = match.strip()
        if stripped:
            formulas.append(f"[Display] {stripped}")

    # Remove display math from content before searching for inline
    content_no_display = display_pattern.sub('', content)

    # Step 2: Extract inline math ($...$)
    # Avoids matching empty content or pure whitespace
    inline_pattern = re.compile(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)')
    inline_matches = inline_pattern.findall(content_no_display)
    for match in inline_matches:
        stripped = match.strip()
        if stripped:
            formulas.append(f"[Inline]  {stripped}")

    return formulas


def extract_latex_from_pdf(pdf_path: str, output_dir: str):
    """
    Calls the marker-pdf CLI to parse the PDF into Markdown (including LaTeX for formulas).
    Then post-processes the output to extract all LaTeX formulas into a separate file.
    Runs on CPU environments; model weights may be downloaded on the first execution.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Input PDF file not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Run marker-pdf to convert PDF to Markdown
    print(f"[INFO] Starting extraction for '{pdf_path}'. (This may take a while)")
    try:
        # Force PyTorch CPU usage via environment variable
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

    # Step 2: Find generated .md files and extract formulas
    md_files = glob.glob(os.path.join(output_dir, "**", "*.md"), recursive=True)

    if not md_files:
        print("[WARN] No Markdown files found in the output. Formula extraction skipped.")
        return

    all_formulas = []
    for md_file in md_files:
        print(f"[INFO] Extracting formulas from: {md_file}")
        formulas = extract_formulas_from_markdown(md_file)
        all_formulas.extend(formulas)

    if not all_formulas:
        print("[NOTE] No LaTeX formulas found in the generated Markdown.")
        return

    # Step 3: Save extracted formulas to a dedicated file
    formulas_path = os.path.join(output_dir, "extracted_formulas.txt")
    with open(formulas_path, 'w', encoding='utf-8') as f:
        for formula in all_formulas:
            f.write(formula + "\n\n")

    print(f"[SUCCESS] Extracted {len(all_formulas)} formulas -> '{formulas_path}'")
