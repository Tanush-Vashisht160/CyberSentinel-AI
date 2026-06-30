from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_report(prompt, threats, score, severity, ai_analysis):

    file_name = "CyberSentinel_Report.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "CyberSentinel AI Security Report")

    c.setFont("Helvetica", 10)
    c.drawString(50, 720, f"Timestamp: {datetime.now()}")

    c.drawString(50, 700, f"Prompt: {prompt}")

    c.drawString(50, 680, f"Threats: {', '.join(threats) if threats else 'None'}")

    c.drawString(50, 660, f"Risk Score: {score}/100")

    c.drawString(50, 640, f"Severity: {severity}")

    text = c.beginText(50, 600)
    text.textLines("AI Analysis:\n" + str(ai_analysis))
    c.drawText(text)

    c.save()

    return file_name