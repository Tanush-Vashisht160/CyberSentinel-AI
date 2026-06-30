"""
Explanation Engine
Returns an explanation for detected threats.
"""

def get_explanations(threats):

    explanations = {
        "Prompt Injection":
            "Attempts to override or ignore the AI's original instructions.",

        "Prompt Leakage":
            "Attempts to reveal hidden system prompts or confidential instructions.",

        "Possible Jailbreak":
            "Attempts to bypass the AI's safety rules or change its intended behavior."
    }

    result = []

    for threat in threats:
        result.append({
            "threat": threat,
            "explanation": explanations.get(
                threat,
                "No explanation available."
            )
        })

    return result