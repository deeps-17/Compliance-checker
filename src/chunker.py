import re

def clean_text(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def extract_text_from_upload(uploaded_file) -> str:
    import fitz

    if uploaded_file.name.endswith(".pdf"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return clean_text(text)

    elif uploaded_file.name.endswith(".txt"):
        try:
            return clean_text(uploaded_file.read().decode("utf-8"))
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return clean_text(uploaded_file.read().decode("latin-1", errors="replace"))

    else:
        raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")

def prepare_policy_text(text: str) -> str:
    return clean_text(text)