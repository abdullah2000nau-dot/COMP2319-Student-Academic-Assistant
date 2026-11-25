# SAAI - Student Academic Assistant AI

## Overview
SAAI is a local AI academic assistant developed for COMP2319.

Features:
- Search course documents with citations.
- List assignments and deadlines.
- Draft professional emails.
- Require human approval for email actions.
- Answer academic questions using a local language model.

## Technology
- Python 3.14.7
- Ollama
- Qwen 2.5 7B
- Nomic Embed Text
- OpenAI Python SDK
- NumPy
- Pytest

## Install Models
ollama pull qwen2.5:7b
ollama pull nomic-embed-text:latest

## Installation
Create and activate a virtual environment:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## Build Document Index
python src\memory.py

## Run Assistant
python -m src.agent

Type exit to stop.

## Human Approval
python -m src.approval_cli

The user reviews pending email requests and types APPROVE or REJECT.
The AI cannot approve its own requests.
Email delivery is simulated; no real email is sent.

## Safety
- Prompt injection detection
- Password and API-key detection
- Input length limits
- Output secret checks
- Human approval
- Project constitution in SOUL.md

## Context Limits
- Maximum agent turns: 5
- Maximum context messages: 10
- Estimated token budget: 6000
- Temperature: 0

## Tests
Run automated tests:

pytest -v

Run security tests:

python run_red_team.py

Latest verified results:
- Automated tests: 22 passed
- Red-team cases: 12 passed, 0 failed

## Project Structure
src/       Application source code
data/      Fictional academic documents and local data
tests/     Automated and red-team tests
reports/   Evaluation results
SOUL.md    Assistant constitution

## Privacy
The included academic data is fictional.
Do not upload credentials, passwords, API keys, or private student data.

## Submission
Course: COMP2319
Project: Student Academic Assistant AI
Student: Abdullah Arshad

GitHub repository: To be added
Demonstration video: To be added
