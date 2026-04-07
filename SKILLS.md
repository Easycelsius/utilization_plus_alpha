---
name: utilization-plus-alpha-skills
description: Guidelines and skills for maintaining the Utilization Plus Alpha project.
---

# Skills

This document defines the common guidelines and skills for developing and maintaining the project.

## Maintenance Rules
- **Keep Documentation Updated**: Whenever a feature is added or modified, update the root `README.md`, `SKILLS.md`, and `AGENTS.md`.
- **Local & Open Source**: Prioritize open-source tools and local execution (no-API) to maintain privacy and reduce costs.
- **Environment Isolation**: Each subdirectory should manage its own virtual environment (`venv`) to prevent dependency conflicts.
- **Data Privacy**: Input/Output directories like `input_pdf/` should always be included in `.gitignore`.
