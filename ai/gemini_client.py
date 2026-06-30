import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env
load_dotenv()

# Get API key safely
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the modern Gemini Client
client = genai.Client(api_key=API_KEY)


def analyze_prompt(prompt, threats, score, severity):
    """
    Sends cybersecurity analysis request to Gemini
    and returns AI-generated explanation using the modern google-genai SDK.
    """

    # Keep your excellent, structured analysis prompt!
    analysis_input = f"""
You are a Cybersecurity AI Analyst.

Analyze the following user prompt and system results.

USER PROMPT:
{prompt}

DETECTED THREATS:
{threats}

RISK SCORE:
{score}/100

SEVERITY:
{severity}

Give:
1. Security analysis
2. Why this is dangerous or safe
3. Recommendation (ALLOW / BLOCK / REVIEW)
"""

    # Call the new unified API interface
    # Using 'gemini-2.5-flash' for fast, efficient security triage
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=analysis_input
    )

    return response.text