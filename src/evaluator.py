import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set. Please add it to your .env file.")

genai.configure(api_key=api_key)

def load_dpdp_act():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "dpdp-act.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def evaluate_policy(policy_text: str) -> dict:
    if not policy_text.strip():
        raise ValueError("Policy text is empty. Please provide a valid privacy policy.")

    dpdp_act = load_dpdp_act()

    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "overall_score": {"type": "STRING"},
                "overall_summary": {"type": "STRING"},
                "pillars": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "pillar_name": {"type": "STRING"},
                            "status": {"type": "STRING", "enum": ["Pass", "Partial", "Fail"]},
                            "reasoning": {"type": "STRING"},
                            "evidence": {"type": "STRING"},
                            "relevant_sections_act": {"type": "STRING"}
                        },
                        "required": ["pillar_name", "status", "reasoning", "evidence", "relevant_sections_act"]
                    }
                }
            },
            "required": ["overall_score", "overall_summary", "pillars"]
        }
    }

    prompt = f"""
You are a legal compliance expert specializing in India's Digital Personal Data Protection (DPDP) Act 2023.

Below is the full text of the DPDP Act, followed by an organization's privacy policy.
Evaluate the privacy policy strictly against the DPDP Act across exactly these 7 pillars.

The 7 pillars to evaluate:
1. Consent - Is consent free, specific, informed, unconditional and obtained via clear affirmative action? (Section 6)
2. Notice - Does the policy clearly state what data is collected, the purpose, and how rights can be exercised? (Section 5)
3. Data Principal Rights - Are rights to access, correction, erasure, grievance redressal and nomination acknowledged? (Sections 11-14)
4. Data Fiduciary Obligations - Are accuracy, security safeguards, breach notification and data deletion on purpose completion mentioned? (Section 8)
5. Children's Data - Is parental/guardian consent required for minors and is processing that harms children prohibited? (Section 9)
6. Grievance Officer - Are the contact details of a Grievance Officer published? (Section 13)
7. Cross-border Data Transfer - Is the location of data storage or transfer mentioned? (Section 16)

---

DPDP ACT 2023 (Full Text):
{dpdp_act}

---

PRIVACY POLICY TO EVALUATE:
{policy_text}
"""

    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash",
        generation_config=generation_config
    )

    response = model.generate_content(prompt)
    return json.loads(response.text)