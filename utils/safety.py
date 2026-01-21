def add_medical_safety(text: str, risk: str) -> dict:
    """
    Convert LLM output into structured dict for UI rendering.
    """

    data = {
        "causes": "",
        "red_flags": "",
        "doctor": "",
        "self_care": "",
        "sources": "",
        "disclaimer": ""
    }

    # Basic splitter pattern (will upgrade later)
    sections = text.split("\n")

    current = None
    for line in sections:
        l = line.lower().strip()

        if "cause" in l:
            current = "causes"
        elif "red flag" in l or "watch" in l:
            current = "red_flags"
        elif "doctor" in l or "seek" in l:
            current = "doctor"
        elif "self" in l or "home" in l:
            current = "self_care"
        elif "source" in l:
            current = "sources"
        elif "disclaimer" in l:
            current = "disclaimer"
        else:
            if current:
                data[current] += line + "\n"

    # add fallback disclaimer if missing
    if not data["disclaimer"]:
        data["disclaimer"] = "This is informational and not a diagnosis."

    return data

if __name__ == "__main__":
    print(add_medical_safety("Possible causes may include viral illness.", "MODERATE RISK"))
