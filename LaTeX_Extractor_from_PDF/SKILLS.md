---
name: latex-extractor-skills
description: Skills and context for the LaTeX Extractor from PDF sub-project.
---

# SKILLS

This document outlines the considerations for agents when performing maintenance or related tasks for the `LaTeX_Extractor_from_PDF` project.

## Architecture Context
- **Tooling**: Uses the `marker-pdf` package for open-source/offline file extraction.
- **Environment**: It is highly recommended to use the virtual environment (`venv`) within this directory to avoid dependency conflicts with the global Python environment.
- **Implementation Rules**: 
  - **No External Paid APIs**: Do not introduce paid APIs; all features must be open-source.
  - **CPU Compatibility**: Ensure features are compatible with CPU environments and avoid GPU-exclusive dependencies or verify their Fallback behavior.
