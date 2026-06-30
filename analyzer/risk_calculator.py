"""
Risk Calculator
Calculates the overall risk score and severity.
"""

def calculate_risk(threats):
    """
    Calculate the risk score based on detected threats.
    """

    score = 0

    # Score each threat
    for threat in threats:

        if threat == "Prompt Injection":
            score += 40

        elif threat == "Prompt Leakage":
            score += 30

        elif threat == "Possible Jailbreak":
            score += 35

    # Bonus if multiple threats are detected
    if len(threats) > 1:
        score += 15

    # Maximum score is 100
    if score > 100:
        score = 100

    # Determine severity
    if score >= 80:
        severity = "HIGH"

    elif score >= 50:
        severity = "MEDIUM"

    elif score > 0:
        severity = "LOW"

    else:
        severity = "SAFE"

    return score, severity