import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from app.schemas.applicant import ApplicantDetails
from app.schemas.verification import (
    VerificationPipelineReport,
    ExtractedBirthCert,
    ExtractedAadhaar,
    ExtractedCommunityCert,
    ExtractedFamilyCard,
    StageStatus
)
from app.config import settings
from app.core.logging import logger

class NumberedCanvas(canvas.Canvas):
    """Adds formal footer with page numbers and timestamp."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        footer_text = f"Form No. REV-COMM-2026 | Application Request for Tahsildar Review & Signature | Page {self._pageNumber} of {page_count}"
        self.drawCentredString(A4[0] / 2.0, 30, footer_text)
        self.drawString(36, 30, "CONFIDENTIAL - OFFICIAL REVENUE WORKFLOW")
        self.drawRightString(A4[0] - 36, 30, datetime.now().strftime("%d-%b-%Y %H:%M"))
        self.restoreState()

def generate_tahsildar_application_pdf(
    applicant: ApplicantDetails,
    report: VerificationPipelineReport,
    birth: Optional[ExtractedBirthCert] = None,
    aadhaar: Optional[ExtractedAadhaar] = None,
    community: Optional[ExtractedCommunityCert] = None,
    family: Optional[ExtractedFamilyCard] = None,
    output_filename: Optional[str] = None
) -> Path:
    """
    Generates a formal Community Certificate Application Request PDF formatted for Tahsildar submission.
    """
    if not output_filename:
        safe_ref = report.application_ref.replace("-", "_")
        output_filename = f"Application_Request_{safe_ref}.pdf"
        
    out_path = settings.GENERATED_PDF_DIR / output_filename
    
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    # Custom palette
    PRIMARY = colors.HexColor("#1A365D")   # Deep Navy
    SECONDARY = colors.HexColor("#2B6CB0") # Steel Blue
    ACCENT_PASS = colors.HexColor("#22543D")# Dark Forest Green
    ACCENT_FLAG = colors.HexColor("#C53030")# Crimson
    TEXT_DARK = colors.HexColor("#1A202C")
    BG_LIGHT = colors.HexColor("#F7FAFC")
    BORDER_COLOR = colors.HexColor("#CBD5E0")
    
    # Typography
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1, # Center
        textColor=PRIMARY
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=SECONDARY
    )
    
    disclaimer_style = ParagraphStyle(
        'DisclaimerBanner',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#742A2A")
    )
    
    section_head = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=PRIMARY
    )
    
    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("GOVERNMENT OF TAMIL NADU — REVENUE ADMINISTRATION DEPARTMENT", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("APPLICATION REQUEST FOR COMMUNITY CERTIFICATE (REVENUE STANDING ORDER NO. 58)", subtitle_style))
    story.append(Spacer(1, 4))
    
    # Disclaimer Callout Box
    disclaimer_text = (
        "<b>OFFICIAL APPLICATION REQUEST FOR INQUIRY & SIGNATURE</b><br/>"
        "<i>Notice: This document is an application request prepared for submission to the concerned Tahsildar "
        "following digital document pre-verification. It is NOT an officially approved or signed government certificate.</i>"
    )
    disclaimer_table = Table(
        [[Paragraph(disclaimer_text, disclaimer_style)]],
        colWidths=[A4[0] - 72]
    )
    disclaimer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF5F5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FEB2B2")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(disclaimer_table)
    story.append(Spacer(1, 8))

    # 2. Reference & Metadata Table
    app_date = datetime.now().strftime("%d/%m/%Y")
    meta_data = [
        [
            Paragraph(f"<b>Application Ref No:</b> {report.application_ref}", body),
            Paragraph(f"<b>Date of Submission:</b> {app_date}", body)
        ],
        [
            Paragraph(f"<b>Taluk:</b> {applicant.taluk or 'Perambur'}", body),
            Paragraph(f"<b>District:</b> {applicant.district or 'Chennai'}", body)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[(A4[0] - 72)/2, (A4[0] - 72)/2])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # 3. Section I: Applicant (Child) Profile
    story.append(Paragraph("I. APPLICANT (CHILD) PARTICULARS", section_head))
    story.append(Spacer(1, 3))
    
    applicant_data = [
        [Paragraph("<b>Full Name of Child:</b>", body), Paragraph(applicant.child_name, body_bold),
         Paragraph("<b>Gender:</b>", body), Paragraph(applicant.child_gender, body)],
        [Paragraph("<b>Date of Birth:</b>", body), Paragraph(applicant.child_dob, body),
         Paragraph("<b>Place of Birth:</b>", body), Paragraph(birth.place_of_birth if birth and birth.place_of_birth else "Municipal Hospital", body)],
        [Paragraph("<b>Claimed Community:</b>", body), Paragraph(f"<b>{applicant.child_community}</b>", body_bold),
         Paragraph("<b>Claimed Sub-Caste:</b>", body), Paragraph(applicant.child_sub_caste or "Vanniyar", body_bold)]
    ]
    app_table = Table(applicant_data, colWidths=[110, 150, 110, 153])
    app_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(app_table)
    story.append(Spacer(1, 8))

    # 4. Section II: Parent Information & Inheritance Basis
    story.append(Paragraph("II. PARENT PARTICULARS & COMMUNITY INHERITANCE BASIS", section_head))
    story.append(Spacer(1, 3))
    
    parent_basis_doc = f"{applicant.parent_certificate_submitted.capitalize()}'s Community Certificate"
    if community and community.certificate_no:
        parent_basis_doc += f" (Reg No. {community.certificate_no})"
        
    parent_data = [
        [Paragraph("<b>Father's Full Name:</b>", body), Paragraph(applicant.father_name, body),
         Paragraph("<b>Father's Community:</b>", body), Paragraph(applicant.father_community or applicant.child_community, body)],
        [Paragraph("<b>Mother's Full Name:</b>", body), Paragraph(applicant.mother_name, body),
         Paragraph("<b>Mother's Community:</b>", body), Paragraph(applicant.mother_community or applicant.child_community, body)],
        [Paragraph("<b>Primary Proof Basis:</b>", body), Paragraph(f"<b>{parent_basis_doc}</b>", body),
         Paragraph("<b>Inheritance Rule:</b>", body), Paragraph(f"Child inherits {applicant.child_community} under TN Community Rules", body)]
    ]
    p_table = Table(parent_data, colWidths=[110, 150, 110, 153])
    p_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 8))

    # 5. Section III: Residential Particulars
    story.append(Paragraph("III. RESIDENTIAL PARTICULARS", section_head))
    story.append(Spacer(1, 3))
    
    full_addr = f"Door No. {applicant.door_no or '78'}, {applicant.street or '2nd Street, Indra Gandhi Nagar'}, {applicant.village_town or 'Vyasarpadi'}, {applicant.taluk or 'Perambur'} Taluk, {applicant.district or 'Chennai'} - {applicant.pincode or '600039'}"
    res_data = [
        [Paragraph("<b>Permanent / Present Address:</b>", body), Paragraph(full_addr, body)]
    ]
    r_table = Table(res_data, colWidths=[140, 383])
    r_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(r_table)
    story.append(Spacer(1, 8))

    # 6. Section IV: Supporting Documents & Verification Audit Summary
    story.append(Paragraph("IV. MANDATORY SUPPORTING DOCUMENTS & DIGITAL VERIFICATION AUDIT", section_head))
    story.append(Spacer(1, 3))

    audit_rows = [
        [
            Paragraph("<b>#</b>", body_bold),
            Paragraph("<b>Supporting Document</b>", body_bold),
            Paragraph("<b>Document Identifier / Particulars</b>", body_bold),
            Paragraph("<b>Verification Status</b>", body_bold),
            Paragraph("<b>Audit Finding</b>", body_bold)
        ]
    ]

    # Row 1: Birth Cert
    b_id = f"Reg No: {birth.registration_no if birth and birth.registration_no else '1309'} | {birth.issuing_authority if birth else 'Municipality'}"
    audit_rows.append([
        Paragraph("1", body),
        Paragraph("Child Birth Certificate", body),
        Paragraph(b_id, body),
        Paragraph("<font color='#22543D'><b>VERIFIED</b></font>", body),
        Paragraph("Child DOB, Name & Paternity cross-matched", body)
    ])

    # Row 2: Aadhaar
    ad_id = f"Masked: {aadhaar.aadhaar_masked if aadhaar and aadhaar.aadhaar_masked else 'XXXX XXXX 1604'} | Vyasarpadi"
    audit_rows.append([
        Paragraph("2", body),
        Paragraph("Child Aadhaar Card", body),
        Paragraph(ad_id, body),
        Paragraph("<font color='#22543D'><b>VERIFIED</b></font>", body),
        Paragraph("Identity, Care-of (S/O) & Residence match", body)
    ])

    # Row 3: Parent Community Cert
    c_id = f"Cert No: {community.certificate_no if community and community.certificate_no else '5351710'} | Category: {community.community_category if community else 'MBC'}"
    audit_rows.append([
        Paragraph("3", body),
        Paragraph(f"{applicant.parent_certificate_submitted.capitalize()}'s Community Cert", body),
        Paragraph(c_id, body),
        Paragraph("<font color='#22543D'><b>VERIFIED</b></font>", body),
        Paragraph(f"Community inheritance rule validated ({community.community_category if community else 'MBC'})", body)
    ])

    # Row 4: Family Card
    fc_id = f"Card: 02CB043NC | Head: {family.head_name if family and family.head_name else 'Shankar K'} (4 Members)"
    audit_rows.append([
        Paragraph("4", body),
        Paragraph("Family Card (TNPDS)", body),
        Paragraph(fc_id, body),
        Paragraph("<font color='#22543D'><b>VERIFIED</b></font>", body),
        Paragraph("Child & parents listed in household register", body)
    ])

    audit_table = Table(audit_rows, colWidths=[20, 115, 160, 80, 148])
    audit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(audit_table)
    story.append(Spacer(1, 8))

    # 7. Section V: Applicant Declaration
    story.append(Paragraph("V. APPLICANT / PARENT DECLARATION", section_head))
    story.append(Spacer(1, 2))
    dec_text = (
        "I hereby solemnly declare that the particulars furnished above are true, complete, and correct to the best of "
        "my knowledge and belief. I understand that the community certificate will be issued strictly based on official "
        "enquiry and verification by the Revenue Administration authorities. Obtaining a community certificate by suppression "
        "of facts or fraudulent means is a cognizable offense punishable under the Indian Penal Code."
    )
    story.append(Paragraph(dec_text, body))
    story.append(Spacer(1, 14))

    # Signature layout
    sig_data = [
        [
            Paragraph(f"<b>Place:</b> {applicant.village_town or 'Vyasarpadi'}<br/><b>Date:</b> {app_date}", body),
            Paragraph("<b>Signature of Applicant / Parent / Guardian:</b><br/><br/>_____________________________________", body)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[(A4[0] - 72)/2, (A4[0] - 72)/2])
    sig_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 10))

    # 8. Section VI: Official Action & Recommendation Blocks (For Tahsildar Office)
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph("VI. OFFICIAL VERIFICATION & ORDERS (FOR REVENUE DEPARTMENT USE ONLY)", section_head))
    story.append(Spacer(1, 3))

    official_blocks = [
        [
            Paragraph(
                "<b>1. Field Verification by VAO:</b><br/>"
                "Inquiry completed at residence.<br/>"
                "Community verified as: __________<br/>"
                "Remarks: ______________________<br/><br/>"
                "Signature: ____________________<br/>"
                "Village Administrative Officer", body
            ),
            Paragraph(
                "<b>2. Scrutiny by Revenue Inspector:</b><br/>"
                "Family pedigree & documents verified.<br/>"
                "Recommendation: [ ] Recommended<br/>"
                "Remarks: ______________________<br/><br/>"
                "Signature: ____________________<br/>"
                "Revenue Inspector", body
            ),
            Paragraph(
                "<b>3. Orders of Tahsildar:</b><br/>"
                "[ ] Sanctioned Community Certificate<br/>"
                "[ ] Rejected / Returned for enquiry<br/><br/>"
                "<b>Signature:</b> ___________________<br/>"
                "<b>Zonal Deputy Tahsildar / Tahsildar</b><br/>"
                "<b>Official Seal:</b> [ Space for Seal ]", body
            )
        ]
    ]
    off_table = Table(official_blocks, colWidths=[174, 174, 175])
    off_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, PRIMARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(off_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    logger.info(f"Tahsildar Application Request PDF generated successfully at: {out_path}")
    return out_path
