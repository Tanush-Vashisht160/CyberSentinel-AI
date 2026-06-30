def detect_rules(prompt: str):
    prompt = prompt.lower()

    threats = []

    if "ignore previous instructions" in prompt:
        threats.append("Prompt Injection")

    if "system prompt" in prompt:
        threats.append("Prompt Leakage")

    if "pretend you are" in prompt:
        threats.append("Possible Jailbreak")

    return threats