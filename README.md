# SAAI - Student Academic Assistant AI

## Overview
SAAI is a local AI academic assistant developed for COMP2319.

## Features
- Search course documents with citations.
- List assignments and deadlines.
- Draft professional emails.
- Human approval for email actions.
- Local AI language model.

## Technology
- Python 3.14.7
- Ollama and Qwen 2.5 7B
- Nomic Embed Text
- OpenAI Python SDK
- NumPy and Pytest

## Installation
1. Create virtual environment: python -m venv .venv
2. Activate: .venv\Scripts\Activate.ps1
3. Install: pip install -r requirements.txt
4. Download models:
   - ollama pull qwen2.5:7b
   - ollama pull nomic-embed-text:latest

## Run
- Build index: python src\memory.py
- Start assistant: python -m src.agent
- Approval tool: python -m src.approval_cli

Email delivery is simulated. No real email is sent.

## Safety
- Prompt injection detection
- Password and API-key detection
- Input length limits
- Output secret checks
- Human approval
- SOUL.md constitution

## Context Limits
- Maximum turns: 5
- Maximum context messages: 10
- Estimated token budget: 6000
- Temperature: 0

## Tests
- Automated tests: 22 passed
- Red-team cases: 12 passed, 0 failed

## Project Structure
- src: Application code
- data: Fictional academic documents
- tests: Automated and red-team tests
- reports: Evaluation results
- SOUL.md: Assistant constitution

## Privacy
The included academic data is fictional. Do not upload credentials, passwords, API keys, or private student data.

## Submission
- Course: COMP2319
- Project: Student Academic Assistant AI
- Student: Abdullah Arshad
- GitHub: https://github.com/abdullah2000nau-dot/COMP2319-Student-Academic-Assistant
- Demonstration video: To be added
