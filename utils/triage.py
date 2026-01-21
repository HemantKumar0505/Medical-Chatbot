def triage(symptoms: list, severity: str = "moderate", duration_days: int = 1):
    severity = severity.lower()

    # High risk conditions (Red Flags)
    red_flags = [
        "difficulty breathing",
        "severe chest pain",
        "loss of consciousness",
        "one-sided weakness",
        "vomiting blood",
        "bluish lips",
        "bleeding",
        "severe abdominal pain"
    ]

    # Check red flags first
    for flag in red_flags:
        if flag in [s.lower() for s in symptoms]:
            return "HIGH RISK"

    # Duration-based moderate risk
    if duration_days >= 3 and severity in ["moderate", "severe"]:
        return "MODERATE RISK"

    # Severity-based moderate risk
    if severity == "severe":
        return "MODERATE RISK"

    # Otherwise assume low risk
    return "LOW RISK"


if __name__ == "__main__":
    print(triage(["fever", "rash"], "moderate", 2))
    print(triage(["difficulty breathing"], "mild", 1))
    print(triage(["headache"], "mild", 1))
