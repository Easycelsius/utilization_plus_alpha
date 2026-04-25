# Agents

This repository contains a stateless FastAPI backend for AI-powered resume workflows.

## Core Workflows

The current resume creation pipeline follows this flow:

1. **Input Phase**: Target JD (1) + Previous JDs (up to 3) + Multiple Resume PDFs.
   - *Tip for LinkedIn*: You can easily obtain a PDF by navigating to your LinkedIn profile -> Click "More" (or "Resources") -> Select "Save to PDF".
2. **Career History Extraction**: Generate a deduplicated, detailed career history based on the uploaded PDFs.
3. **Career History Refinement**: Review the extracted career history and regenerate it based on section-by-section comments and missing information.
4. **Tailoring Survey**: Generate a tailoring survey based on the Target JD, Previous JDs, and the refined Career History.
5. **Resume Generation**: Generate the tailored resume in a single shot (no streaming) using the survey answers and all prior context.
6. **Preview & Analysis**: Display the generated resume alongside ATS score, strengths, weaknesses, and hiring manager concerns.
7. **Resume Refinement**: Iterate on the generated resume in the preview step using section-by-section comments and missing information.
8. **Export**: Download the final resume and cover letter.

## Working Guidelines

- Keep the backend stateless: no database, auth, sessions, or file persistence.
- Treat the browser as the system of record for user state.
- Keep LLM behavior modular through `backend/services/` and prompt files in `backend/prompts/`.
- Prefer deterministic scoring and validation over extra LLM calls where possible.
- Validate every structured LLM response with Pydantic before returning it to clients.
- Add or update tests in `backend/tests/` for any behavior change.
