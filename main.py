from analyzer.risk_calculator import calculate_risk
from analyzer.rule_engine import detect_rules
from analyzer.explanation_engine import get_explanations
from ai.gemini_client import analyze_prompt

def main():

    print("=" * 50)
    print("🛡️ CyberSentinel AI")
    print("=" * 50)

    prompt = input("\nEnter a prompt:\n> ")

    threats = detect_rules(prompt)
    score, severity = calculate_risk(threats)
    details = get_explanations(threats)
    ai_analysis = None

    if score > 0:
        ai_analysis = analyze_prompt(prompt, threats, score, severity)
    else:
        ai_analysis = "No AI analysis needed — system is safe."


    print("\n" + "=" * 50)
    print("Threat Analysis Report")
    print("=" * 50)


    if not details:
        print("Threats Detected : None")
    else:
        print("Threats Detected:\n")

        for item in details:
            print(f"Threat      : {item['threat']}")
            print(f"Explanation : {item['explanation']}")
            print("-" * 50)

    print(f"Risk Score : {score}/100")
    print(f"Severity   : {severity}")
    
    print("\n" + "=" * 50)
    print("🤖 Gemini AI Analysis")
    print("=" * 50)
    print(ai_analysis)

    
if __name__ == "__main__":
    main()


