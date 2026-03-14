"""
NyayaSetu — Document Service
Handles document suggestions and PDF checklist generation.
"""

import os
import uuid
from datetime import datetime
from typing import List, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# Document suggestions by legal category
DOCUMENT_SUGGESTIONS = {
    "labour": [
        {"name": "Employment Contract / Appointment Letter", "required": True},
        {"name": "Salary Slips (Last 6 months)", "required": True},
        {"name": "Written Reminders / Emails to Employer", "required": True},
        {"name": "Identity Proof (Aadhaar/PAN)", "required": True},
        {"name": "Bank Statements (Salary Account)", "required": True},
        {"name": "Legal Notice to Employer", "required": False},
        {"name": "Offer Letter / Joining Letter", "required": False},
        {"name": "Employee ID Card", "required": False},
    ],
    "property": [
        {"name": "Sale Deed / Title Deed", "required": True},
        {"name": "Land Ownership Certificate", "required": True},
        {"name": "Property Tax Receipts", "required": True},
        {"name": "Government ID (Aadhaar/PAN)", "required": True},
        {"name": "Encumbrance Certificate", "required": True},
        {"name": "Mutation Records", "required": False},
        {"name": "Survey/Map Documents", "required": False},
        {"name": "Witness Statements", "required": False},
        {"name": "Photographs of Property", "required": False},
    ],
    "criminal": [
        {"name": "FIR Copy", "required": True},
        {"name": "Government ID (Aadhaar/PAN)", "required": True},
        {"name": "Witness Statements", "required": True},
        {"name": "Medical Reports (if applicable)", "required": True},
        {"name": "CCTV Footage / Photographs", "required": False},
        {"name": "Communication Records", "required": False},
        {"name": "Previous Complaints (if any)", "required": False},
    ],
    "family": [
        {"name": "Marriage Certificate", "required": True},
        {"name": "Government ID (Aadhaar/PAN)", "required": True},
        {"name": "Income Proof of Both Parties", "required": True},
        {"name": "Children's Birth Certificates", "required": True},
        {"name": "Domestic Violence Evidence (if applicable)", "required": False},
        {"name": "Communication/Chat Records", "required": False},
        {"name": "Joint Property Documents", "required": False},
        {"name": "Medical/Counseling Records", "required": False},
    ],
    "consumer": [
        {"name": "Purchase Invoice / Bill", "required": True},
        {"name": "Product Warranty Card", "required": True},
        {"name": "Government ID (Aadhaar/PAN)", "required": True},
        {"name": "Communication with Seller/Company", "required": True},
        {"name": "Photographs of Defective Product", "required": False},
        {"name": "Bank/Payment Transaction Proof", "required": False},
        {"name": "E-commerce Order Details", "required": False},
    ],
    "constitutional": [
        {"name": "Government ID (Aadhaar/PAN)", "required": True},
        {"name": "Evidence of Rights Violation", "required": True},
        {"name": "Relevant Government Orders/Notifications", "required": True},
        {"name": "Witness Affidavits", "required": False},
        {"name": "Media Reports (if applicable)", "required": False},
        {"name": "RTI Responses", "required": False},
    ],
    "cyber": [
        {"name": "Screenshot of Cyber Crime", "required": True},
        {"name": "Government ID (Aadhaar/PAN)", "required": True},
        {"name": "Bank Statements showing fraud", "required": True},
        {"name": "Email/Message Records", "required": True},
        {"name": "Cyber Cell Complaint Copy", "required": False},
        {"name": "Device Information", "required": False},
        {"name": "IP Address/URL Records", "required": False},
    ],
}

DEFAULT_DOCUMENTS = [
    {"name": "Government ID (Aadhaar/PAN)", "required": True},
    {"name": "Written Description of Issue", "required": True},
    {"name": "Supporting Documents/Evidence", "required": True},
    {"name": "Witness Contact Information", "required": False},
    {"name": "Communication Records", "required": False},
]

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_pdfs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def suggest_documents(legal_category: str) -> List[Dict]:
    """Get suggested documents for a legal category."""
    return DOCUMENT_SUGGESTIONS.get(legal_category, DEFAULT_DOCUMENTS)


def generate_checklist_pdf(
    documents: List[Dict],
    legal_category: str,
    case_summary: str = ""
) -> str:
    """
    Generate a professional PDF checklist of required documents.
    Returns the filename of the generated PDF.
    """
    filename = f"Required_Documents_Checklist_{uuid.uuid4().hex[:8]}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    pdf_doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=25 * mm,
        leftMargin=25 * mm,
        topMargin=25 * mm,
        bottomMargin=20 * mm,
    )

    # Colors
    primary_color = HexColor("#D97706")
    dark_color = HexColor("#0A1128")
    text_color = HexColor("#475569")
    green_color = HexColor("#059669")
    red_color = HexColor("#C2410C")
    light_bg = HexColor("#FAF9F6")
    border_color = HexColor("#E2E8F0")

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=dark_color,
        spaceAfter=6 * mm,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=text_color,
        spaceAfter=8 * mm,
        alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=primary_color,
        spaceBefore=6 * mm,
        spaceAfter=4 * mm,
        fontName='Helvetica-Bold',
    )
    item_style = ParagraphStyle(
        'ItemStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=dark_color,
        leading=16,
    )
    note_style = ParagraphStyle(
        'NoteStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=text_color,
        spaceBefore=4 * mm,
    )
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=text_color,
        alignment=TA_CENTER,
        spaceBefore=10 * mm,
    )

    # Build content
    elements = []

    # Title
    elements.append(Paragraph("⚖ NyayaSetu", title_style))
    elements.append(Paragraph("Required Documents Checklist", subtitle_style))
    elements.append(HRFlowable(
        width="100%", thickness=1, color=border_color,
        spaceBefore=2 * mm, spaceAfter=4 * mm
    ))

    # Case info
    elements.append(Paragraph(
        f"Legal Category: <b>{legal_category.title()}</b>",
        ParagraphStyle('Info', parent=styles['Normal'], fontSize=10, textColor=text_color)
    ))
    elements.append(Paragraph(
        f"Generated: <b>{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</b>",
        ParagraphStyle('Info2', parent=styles['Normal'], fontSize=10, textColor=text_color,
                       spaceAfter=4 * mm)
    ))

    if case_summary:
        elements.append(Paragraph(f"Case Summary: {case_summary[:200]}...", note_style))

    # Required documents section
    required_docs = [d for d in documents if d.get("required", False)]
    optional_docs = [d for d in documents if not d.get("required", False)]

    if required_docs:
        elements.append(Paragraph("Required Documents", section_style))
        for i, doc_item in enumerate(required_docs, 1):
            elements.append(Paragraph(
                f"☐  {i}. {doc_item['name']}  —  <font color='#C2410C'><b>REQUIRED</b></font>",
                item_style
            ))
            elements.append(Spacer(1, 2 * mm))

    if optional_docs:
        elements.append(Spacer(1, 3 * mm))
        elements.append(Paragraph("Recommended Documents", section_style))
        for i, doc_item in enumerate(optional_docs, 1):
            elements.append(Paragraph(
                f"☐  {i}. {doc_item['name']}  —  <font color='#059669'>RECOMMENDED</font>",
                item_style
            ))
            elements.append(Spacer(1, 2 * mm))

    # Notes
    elements.append(Spacer(1, 6 * mm))
    elements.append(HRFlowable(
        width="100%", thickness=0.5, color=border_color,
        spaceBefore=2 * mm, spaceAfter=4 * mm
    ))
    elements.append(Paragraph(
        "📌 <b>Important Notes:</b>", note_style
    ))
    elements.append(Paragraph(
        "• Ensure all documents are originals or certified copies",
        note_style
    ))
    elements.append(Paragraph(
        "• Keep multiple photocopies of each document",
        note_style
    ))
    elements.append(Paragraph(
        "• Documents in regional languages should have notarized English translations",
        note_style
    ))
    elements.append(Paragraph(
        "• Consult a qualified advocate before submitting documents to court",
        note_style
    ))

    # Footer
    elements.append(Paragraph(
        "Generated by NyayaSetu — AI-Powered Legal Guidance Platform<br/>"
        "This is an AI-generated checklist. For legal advice, consult a qualified advocate.",
        footer_style
    ))

    pdf_doc.build(elements)
    return filename
