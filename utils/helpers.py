import re

# ----------------------------------------
# 🔹 Hinglish & Casual → Medical Normalization
# ----------------------------------------

HINGLISH_MAP = {
    "bukhar": "fever",
    "thoda": "mild",
    "zyada": "severe",
    "badan dard": "body ache",
    "chakkar": "dizziness",
    "ulti": "vomiting",
    "khansi": "cough",
    "galey mein dard": "sore throat",
    "saans nahi aa rhi": "difficulty breathing",
    "saans phoolna": "shortness of breath",
    "thand lagna": "chills",
    "thand lag rahi": "chills",
    "pet dard": "abdominal pain",
    "pet mein dard": "abdominal pain",
}

# ----------------------------------------
# 🔹 Semi-Open Symptom Vocabulary
# ----------------------------------------

SYMPTOM_VOCAB = {
    "fever", "rash", "headache", "cough", "sore throat", "fatigue",
    "vomiting", "nausea", "chills", "body ache", "shortness of breath",
    "difficulty breathing", "diarrhea", "dizziness", "abdominal pain"
}

# ----------------------------------------
# 🔹 Severity Lexicon
# ----------------------------------------

SEVERITY_MAP = {
    "mild": "mild",
    "little": "mild",
    "thoda": "mild",
    "moderate": "moderate",
    "normal": "moderate",
    "severe": "severe",
    "zyada": "severe",
    "intense": "severe",
}

# ----------------------------------------
# 🔹 Duration Extraction
# ----------------------------------------

DURATION_PATTERNS = [
    (r"^(\d+)$", lambda x: int(x)),
    (r"(\d+)\s*days?", lambda x: int(x)),
    (r"(\d+)\s*day", lambda x: int(x)),
    (r"(\d+)\s*din", lambda x: int(x)),
    (r"(\d+)\s*d", lambda x: int(x)),
    (r"kal se", lambda x: 1),
    (r"yesterday", lambda x: 1),
    (r"couple of days", lambda x: 2),
]


# ----------------------------------------
# 🔹 Normalization Helpers
# ----------------------------------------

def normalize_text(text: str) -> str:
    text = text.lower()
    for hindi, eng in HINGLISH_MAP.items():
        text = text.replace(hindi, eng)
    return text


# ----------------------------------------
# 🔹 Symptom Extraction
# ----------------------------------------

def extract_symptoms(text: str):
    text = normalize_text(text)
    detected = []
    for symptom in SYMPTOM_VOCAB:
        if symptom in text:
            detected.append(symptom)
    return list(set(detected))


# ----------------------------------------
# 🔹 Severity Extraction
# ----------------------------------------

def extract_severity(text: str):
    text = normalize_text(text)
    for k, v in SEVERITY_MAP.items():
        if k in text:
            return v
    return None


# ----------------------------------------
# 🔹 Duration Extraction
# ----------------------------------------

def extract_duration(text: str):
    text = normalize_text(text)

    for pattern, fn in DURATION_PATTERNS:
        match = re.search(pattern, text)

        if match:
            # If pattern has a capture group (like (\d+))
            if match.groups():
                val = match.group(1)
                return fn(val)
            else:
                # Patterns without capture return directly
                return fn(None)

    return None



# ----------------------------------------
# 🔹 Check if Clarification Needed
# ----------------------------------------

def needs_clarification(struct):
    return (
        struct["severity"] is None or
        struct["duration"] is None
    )


# ----------------------------------------
# 🔹 Build Structured Output
# ----------------------------------------

def build_structured(text: str):
    symptoms = extract_symptoms(text)
    severity = extract_severity(text)
    duration = extract_duration(text)

    return {
        "symptoms": symptoms,
        "severity": severity,
        "duration": duration,
    }


# ----------------------------------------
# 🔹 Question Routing Logic
# ----------------------------------------

def get_next_question(struct):
    if struct["duration"] is None:
        return "For how many days have you had these symptoms?"
    if struct["severity"] is None:
        return "Would you say the symptoms are mild, moderate, or severe?"
    return None


# Test
if __name__ == "__main__":
    sample = "3 din se bukhar and rash, zyada"
    s = build_structured(sample)
    print(s, "needs_clarify:", needs_clarification(s), "next_q:", get_next_question(s))
