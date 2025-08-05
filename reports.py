#!/usr/bin/env python3

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(attachment, title, paragraph):
    """
    Generates a PDF report.
    """
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(attachment)
    report_title = Paragraph(title, styles["h1"])
    report_info = Paragraph(paragraph, styles["BodyText"])
    empty_line = Spacer(1, 20)

    report.build([
        report_title,
        empty_line,
        report_info,
        empty_line,
    ])
