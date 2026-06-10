# DPDP Act Compliance Checker

A web-based tool that evaluates an organization's privacy policy against India's Digital Personal Data Protection (DPDP) Act 2023 and generates a structured, pillar-by-pillar compliance report.

Live app: https://compliance-checker00.streamlit.app

---

## What It Does

The tool takes any privacy policy as input — either pasted as text or uploaded as a PDF or TXT file — and evaluates it against the 7 key compliance pillars of the DPDP Act 2023. It returns a pillar-by-pillar scorecard with quoted evidence from the policy, a Pass / Partial / Fail status for each pillar, an overall compliance score, and a downloadable Markdown report.

This is a readiness assessment tool, not a legal audit. Results indicate where an organization stands ahead of the May 2027 full enforcement deadline under the DPDP Rules 2025, not whether they are currently in violation.

---

## Compliance Pillars Evaluated

| Pillar | DPDP Act Reference |
|---|---|
| Consent | Section 6 |
| Notice | Section 5 |
| Data Principal Rights | Sections 11-14 |
| Data Fiduciary Obligations | Section 8 |
| Children's Data | Section 9 |
| Grievance Officer | Section 13 |
| Cross-border Data Transfer | Section 16 |

---

## Tech Stack

- Python
- Streamlit — frontend UI
- Gemini 2.0 Flash API — evaluation engine
- PyMuPDF — PDF text extraction
- python-dotenv — local environment variable management
- Docker — containerization
- GitHub Actions — CI pipeline

---

## Project Structure

```
compliance-checker/
|
|-- .github/
|   |-- workflows/
|       |-- ci.yml              # GitHub Actions CI pipeline
|
|-- data/
|   |-- dpdp-act.txt            # Full text of the DPDP Act 2023
|
|-- src/
|   |-- chunker.py              # Text extraction and cleaning
|   |-- evaluator.py            # Core Gemini API evaluation logic
|   |-- report.py               # JSON response parsing for UI display
|
|-- app.py                      # Streamlit application
|-- Dockerfile                  # Container definition
|-- .dockerignore
|-- requirements.txt
|-- .env                        # API key (not committed)
|-- .gitignore
|-- README.md
```

---

## How It Works

The tool sends the full privacy policy and the full DPDP Act text in a single structured prompt to Gemini 2.0 Flash, using the model's large context window rather than chunking. This gives the model global visibility over both documents, avoiding false negatives that occur when evaluating isolated sections.

Gemini returns a guaranteed JSON response via a strict response schema, which is parsed and rendered as a scorecard in the Streamlit UI.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/deeps-17/Compliance-checker.git
cd Compliance-checker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a Gemini API key

Go to [aistudio.google.com](https://aistudio.google.com), sign in, and create a free API key.

### 4. Configure environment variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

### 5. Add the DPDP Act text

Place the full text of the DPDP Act 2023 as `dpdp-act.txt` inside the `data/` folder. The official PDF is available on the [MeitY website](https://www.meity.gov.in).

### 6. Run the app

```bash
streamlit run app.py
```

---

## Running with Docker

### Build the image

```bash
docker build -t compliance-checker .
```

### Run the container

```bash
docker run -p 8501:8501 -e GEMINI_API_KEY=your_api_key_here compliance-checker
```

Then open `http://localhost:8501` in your browser.

---

## CI Pipeline

Every push to `main` triggers a GitHub Actions workflow that:

- Installs all dependencies
- Checks for syntax errors across all Python files
- Builds the Docker image to confirm it compiles correctly

---

## Deployment

The app is deployed on Streamlit Community Cloud and is publicly accessible at:

https://compliance-checker00.streamlit.app

API keys are managed via Streamlit Secrets and are never stored in the codebase or Docker image.

---

## Usage

1. Open the app
2. Paste the privacy policy text directly, or upload a PDF or TXT file
3. Click "Analyse Policy"
4. Review the pillar-by-pillar breakdown with evidence and status badges
5. Download the compliance report as a Markdown file

---

## Limitations

- Evaluates the policy document only — does not assess actual technical implementation
- Results depend on what the privacy policy discloses, not what the organization does in practice
- Not a substitute for legal advice or a formal compliance audit
- Accuracy may vary for ambiguous or poorly written policies

---

## Context

The DPDP Rules 2025 were notified by MeitY on November 13, 2025. Full enforcement of all substantive obligations is expected by May 2027. This tool was built to audit how prepared Indian organizations are ahead of that deadline.

---

## License

MIT
