import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def build_inspired_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Inspiration Color Theme
    TOP_BLUE = RGBColor(26, 86, 219)     # Top thin stripe #1A56DB
    NAVY_DARK = RGBColor(15, 23, 42)     # Main Title #0F172A
    BLUE_PILL_TXT = RGBColor(30, 64, 175)# #1E40AF
    BLUE_PILL_BG = RGBColor(239, 246, 255)# #EFF6FF
    BLUE_PILL_BD = RGBColor(191, 219, 254)# #BFDBFE
    
    TEXT_DARK = RGBColor(30, 41, 59)     # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    
    CARD_BLUE_BG = RGBColor(240, 247, 255)# Soft light blue
    CARD_BLUE_BD = RGBColor(191, 219, 254)
    
    CARD_RED_BG = RGBColor(255, 241, 242) # Soft light pink/red
    CARD_RED_BD = RGBColor(254, 205, 211)
    
    CARD_GREEN_BG = RGBColor(240, 253, 244)# Soft light green
    CARD_GREEN_BD = RGBColor(187, 247, 208)
    
    CARD_WHITE_BG = RGBColor(255, 255, 255)
    CARD_WHITE_BD = RGBColor(226, 232, 240)

    def add_top_template(slide, slide_num, total_slides=16, category="B.E. COMPUTER SCIENCE & ENGINEERING | FIRST REVIEW"):
        # Top blue stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = TOP_BLUE
        stripe.line.fill.background()

        # Category pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.25), Inches(5.2), Inches(0.38))
        pill.fill.solid()
        pill.fill.fore_color.rgb = BLUE_PILL_BG
        pill.line.color.rgb = BLUE_PILL_BD
        pill.line.width = Pt(1)

        ptb = slide.shapes.add_textbox(Inches(0.9), Inches(0.26), Inches(5.0), Inches(0.35))
        ptf = ptb.text_frame
        ptf.word_wrap = True
        pp = ptf.paragraphs[0]
        pp.text = category
        pp.font.size = Pt(10.5)
        pp.font.bold = True
        pp.font.color.rgb = BLUE_PILL_TXT

        # Slide Number
        snum_box = slide.shapes.add_textbox(Inches(10.8), Inches(0.25), Inches(1.8), Inches(0.35))
        stf = snum_box.text_frame
        sp = stf.paragraphs[0]
        sp.alignment = PP_ALIGN.RIGHT
        sp.text = f"Slide {slide_num} of {total_slides}"
        sp.font.size = Pt(11)
        sp.font.bold = True
        sp.font.color.rgb = TEXT_MUTED

    def add_slide_title(slide, title_text, subtitle_text=""):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(11.5)
            p2.font.color.rgb = TEXT_MUTED

    def create_card(slide, left, top, width, height, title, items, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, title_col=NAVY_DARK, icon_text=""):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = bd_col
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        tp = tf.paragraphs[0]
        if icon_text:
            tp.text = f"{icon_text}  {title}"
        else:
            tp.text = title
        tp.font.size = Pt(14)
        tp.font.bold = True
        tp.font.color.rgb = title_col
        tp.space_after = Pt(8)

        for item in items:
            p = tf.add_paragraph()
            p.text = "•  " + item
            p.font.size = Pt(11.5)
            p.font.color.rgb = TEXT_DARK
            p.space_after = Pt(6)

        return card

    # ==================== SLIDE 1: TITLE SLIDE (INSPIRATION STYLE) ====================
    s1 = prs.slides.add_slide(blank_layout)
    add_top_template(s1, 1, 16, "B.E. COMPUTER SCIENCE & ENGINEERING | FIRST REVIEW")

    # Title & Subtitle
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.733), Inches(2.3))
    t_tf = t_box.text_frame
    t_tf.word_wrap = True
    
    tp1 = t_tf.paragraphs[0]
    tp1.text = "GovtAutofill AI: Smart Document Auto-Filling Assistant"
    tp1.font.size = Pt(28)
    tp1.font.bold = True
    tp1.font.color.rgb = NAVY_DARK
    tp1.space_after = Pt(8)

    tp2 = t_tf.add_paragraph()
    tp2.text = "Automatically reading Indian ID cards (Aadhaar / PAN) and filling Voter ID Form 6 using Local AI, OCR, and Deep Learning Face Detection."
    tp2.font.size = Pt(14.5)
    tp2.font.color.rgb = TEXT_MUTED

    # Bottom Two Inspiration Cards
    # Left Card: Team Name
    c_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.8), Inches(5.6), Inches(2.8))
    c_team.fill.solid()
    c_team.fill.fore_color.rgb = CARD_BLUE_BG
    c_team.line.color.rgb = CARD_BLUE_BD
    c_team.line.width = Pt(1.2)

    ctb = s1.shapes.add_textbox(Inches(1.05), Inches(4.0), Inches(5.1), Inches(2.4))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    
    cp1 = ctf.paragraphs[0]
    cp1.text = "🎓  PROJECT DETAILS"
    cp1.font.size = Pt(13)
    cp1.font.bold = True
    cp1.font.color.rgb = BLUE_PILL_TXT
    cp1.space_after = Pt(8)

    cp2 = ctf.add_paragraph()
    cp2.text = "GovtAutofill Engine"
    cp2.font.size = Pt(18)
    cp2.font.bold = True
    cp2.font.color.rgb = NAVY_DARK
    cp2.space_after = Pt(6)

    details = [
        "Department of Computer Science & Engineering",
        "Target Portal: ECI NVSP Voter Registration (Form 6)",
        "Zero Cloud Processing (100% On-Device & Private)"
    ]
    for d in details:
        p = ctf.add_paragraph()
        p.text = "• " + d
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(3)

    # Right Card: Project Members (with roll numbers as shown in user inspiration)
    c_mem = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.8), Inches(5.733), Inches(2.8))
    c_mem.fill.solid()
    c_mem.fill.fore_color.rgb = CARD_BLUE_BG
    c_mem.line.color.rgb = CARD_BLUE_BD
    c_mem.line.width = Pt(1.2)

    mtb = s1.shapes.add_textbox(Inches(7.05), Inches(4.0), Inches(5.2), Inches(2.4))
    mtf = mtb.text_frame
    mtf.word_wrap = True
    
    mp1 = mtf.paragraphs[0]
    mp1.text = "👥  PROJECT MEMBERS"
    mp1.font.size = Pt(13)
    mp1.font.bold = True
    mp1.font.color.rgb = BLUE_PILL_TXT
    mp1.space_after = Pt(8)

    members_list = [
        ("Deva S", "2117230070025"),
        ("Athithi A", "2117230070004"),
        ("Arthi S", "2117230070016")
    ]
    for name, regno in members_list:
        p = mtf.add_paragraph()
        p.text = f"{name}   ({regno})"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p.space_after = Pt(6)

    s1.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Good morning staff. We are Deva, Athithi, and Arthi. Our project is 'GovtAutofill AI'. "
        "It is a smart web tool that helps citizens fill government registration forms automatically. "
        "Instead of typing 25 boxes by hand, the user uploads their Aadhaar card, and our AI reads the details, "
        "cuts the passport photo, and fills Voter ID Form 6 in 20 seconds. Everything runs 100% on the laptop with zero cloud cost.'"
    )

    # ==================== SLIDE 2: TABLE OF CONTENTS ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_top_template(s2, 2, 16)
    add_slide_title(s2, "Table of Contents", "Overview of today's presentation")

    toc1 = [
        "1. Introduction",
        "2. Background of the Project",
        "3. Problem Statement",
        "4. Aim and Objectives",
        "5. Literature Review",
        "6. Existing System",
        "7. Limitations of the Existing System"
    ]
    toc2 = [
        "8. Proposed System",
        "9. Proposed Methodology & Architecture",
        "10. Tools & Technologies Used",
        "11. Work Completed So Far (Our Results)",
        "12. What We Have Built (Key Features)",
        "13. Expected Outcomes & Benefits",
        "14. Project Timeline & Next Steps",
        "15. References & Conclusion"
    ]
    create_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Part 1: Problem & Literature", toc1, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📋")
    create_card(s2, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Part 2: Solution, Prototype & Plan", toc2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🚀")

    s2.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Here is our presentation outline: First, we cover the real-world problem and background of Voter ID Form 6. "
        "Next, we explain our system architecture, the tools we used, the working prototype we built, and our plan for the next review.'"
    )

    # ==================== SLIDE 3: INTRODUCTION ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_top_template(s3, 3, 16)
    add_slide_title(s3, "Introduction: What is this Project About?", "Real-world context and our core idea")

    intro_left = [
        "Citizens frequently fill statutory government web forms like Voter ID Form 6, PAN, and Ration Card applications.",
        "Form 6 requires typing more than 20 separate boxes by hand from an Aadhaar card.",
        "Applicants must enter Name, Father's Name, DOB, Gender, Mobile, and manually break their address into Door No, Street, City, and PIN code.",
        "They also have to crop and resize a separate passport photo to match website rules."
    ]
    intro_right = [
        "Our Solution: An automatic web assistant that reads the ID card and fills Form 6 instantly.",
        "User simply uploads their Aadhaar card (PDF or images).",
        "Our AI reads the words, cuts out the passport photo, and fills all boxes in 20 seconds.",
        "100% Private: Everything runs on the user's laptop. No data is sent to external cloud servers, keeping Aadhaar details safe."
    ]
    create_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "The Citizen Experience Today", intro_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📝")
    create_card(s3, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Our Smart Auto-Filling Approach", intro_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="💡")

    s3.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Staff, in simple words: Applying for government forms today means typing 20 boxes by hand and struggling to crop passport photos. "
        "In our project, the citizen just uploads their Aadhaar card. Our AI reads the text, cuts the photo, and fills Form 6 in 20 seconds. "
        "Everything runs locally on the computer so citizen privacy is fully protected.'"
    )

    # ==================== SLIDE 4: BACKGROUND ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_top_template(s4, 4, 16)
    add_slide_title(s4, "Background: The Voter Registration Process", "Understanding ECI Form 6 and user difficulties")

    bg_left = [
        "Form 6 is the official form of the Election Commission of India (ECI) for enrolling new voters.",
        "Over 2 Crore (20 Million) citizens apply for Voter ID cards every single year across India.",
        "Every applicant must upload valid proof documents—most commonly e-Aadhaar cards, PAN cards, or Birth Certificates.",
        "Applicants must also select family relationships correctly (Father, Mother, Husband, or Legal Guardian)."
    ]
    bg_right = [
        "High Rejection Rate: Nearly 18% to 24% of applications get delayed or rejected due to simple typing errors.",
        "Common mistakes: swapping day and month in birth date, misspelling names, or missing door numbers in addresses.",
        "Cyber Cafe Risk: People without home computers visit internet cafes, pay Rs. 50-100, and leave private Aadhaar cards on public desktops.",
        "Conclusion: We need an easy, automated tool that helps common citizens fill forms without mistakes."
    ]
    create_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Scale of Voter Registration", bg_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📊")
    create_card(s4, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Why Applications Face Rejections", bg_right, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⚠️")

    s4.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Every year, more than 2 crore young citizens apply for Voter ID cards. But roughly 1 in 5 applications face delays because people "
        "make simple typing mistakes, like writing the wrong date format. Also, rural citizens go to browsing centers and leave copies of their "
        "Aadhaar cards on public computers. This is why automated, private form filling is necessary.'"
    )

    # ==================== SLIDE 5: PROBLEM STATEMENT (4 CARDS LIKE INSPIRATION) ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_top_template(s5, 5, 16)
    add_slide_title(s5, "Problem Statement: 4 Major Challenges", "Key friction points in manual form submission")

    p1 = [
        "Typing 20+ fields by hand takes 10 to 15 minutes.",
        "Long 12-digit Aadhaar numbers are easy to mistype.",
        "Manually splitting door number, street, and district is confusing."
    ]
    p2 = [
        "Sending ID cards to commercial cloud APIs risks data leaks.",
        "Cyber cafes keep unencrypted Aadhaar scans on shared computers.",
        "Commercial cloud OCR charges recurring fees per scan."
    ]
    p3 = [
        "Aadhaar cards print 14-digit enrolment numbers that look like Aadhaar numbers.",
        "Cards have long legal disclaimers that confuse generic scanning tools.",
        "Scanned photos can be faint or low-contrast."
    ]
    p4 = [
        "Government websites require a separate passport-size photo under 2MB.",
        "Normal citizens do not know how to crop images properly in Paint.",
        "Forces users to pay money at internet cafes for simple cropping."
    ]

    create_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Repetitive Manual Typing", p1, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⏱️")
    create_card(s5, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Citizen Data Privacy Risks", p2, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="🔒")
    create_card(s5, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Messy Text on Indian ID Cards", p3, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📄")
    create_card(s5, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Photo Cropping Frustration", p4, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="🖼️")

    s5.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Staff, there are four clear problems: 1. Too much typing takes 15 minutes and causes typos. 2. Sending Aadhaar to cloud websites leaks private data. "
        "3. Aadhaar cards have messy text like enrolment numbers that confuse normal scanners. 4. People struggle to crop their passport photo properly.'"
    )

    # ==================== SLIDE 6: AIM AND OBJECTIVES ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_top_template(s6, 6, 16)
    add_slide_title(s6, "Aim & Specific Objectives", "What we set out to achieve")

    aim_items = [
        "To build a fast, free, and completely private web application that reads Indian ID cards (Aadhaar / PAN), automatically detects and crops the applicant's passport photo, and fills Voter ID Form 6 in under 30 seconds with zero cloud dependency."
    ]
    create_card(s6, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.35), "PROJECT AIM", aim_items, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🎯")

    obj_left = [
        "Objective 1: Multi-Document Upload",
        "  • Allow users to upload Front and Back card images, or a PDF.",
        "  • Show file chips with size info and an easy remove button.",
        "Objective 2: Accurate Text Reading (OCR)",
        "  • Use EasyOCR to read English and Indian regional text.",
        "  • Convert PDFs to high-clarity 300 DPI images for easy reading."
    ]
    obj_right = [
        "Objective 3: Smart Field Sorting (Local AI)",
        "  • Use Meta Llama 3.2 AI running on the laptop to sort text into Name, DOB, etc.",
        "  • Automatically identify Father's or Husband's name from 'S/O' or 'W/O'.",
        "Objective 4: Automatic Face Photo Cropping",
        "  • Use OpenCV YuNet face detector to locate the face on the card.",
        "  • Automatically crop a clean passport-size photo without any text."
    ]
    create_card(s6, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7), "Objectives (1 & 2): Ingestion & OCR", obj_left, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📥")
    create_card(s6, Inches(6.8), Inches(3.1), Inches(5.733), Inches(3.7), "Objectives (3 & 4): AI & Biometrics", obj_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🤖")

    s6.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Our aim is simple: In under 30 seconds, take an ID card, extract all details, crop the photo, and fill Form 6. "
        "Our four objectives are: 1. Let users upload front and back images easily. 2. Read the text accurately with OCR. "
        "3. Use local AI to put names and addresses in the right boxes. 4. Automatically find and crop the face photo for the form.'"
    )

    # ==================== SLIDE 7: LITERATURE REVIEW ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_top_template(s7, 7, 16)
    add_slide_title(s7, "Literature Review: What Existing Tools Do", "Comparison of existing technologies and our approach")

    lit1 = [
        "What it does: Reads words from simple scanned papers.",
        "Drawback: Just outputs a raw list of words; does not know which word is 'Name' or 'Address'. Fails on Indian regional scripts."
    ]
    lit2 = [
        "What they do: Very accurate at reading documents and forms.",
        "Drawback: Charges money for every single scan, needs internet, and uploads private citizen data to third-party servers."
    ]
    lit3 = [
        "What they do: Can understand forms and text very well.",
        "Drawback: Too large to run locally on a normal laptop; requires expensive graphic cards (GPUs) or paid internet subscriptions."
    ]
    lit4 = [
        "What we do: We use EasyOCR for reading + Meta Llama 3.2 (small 3B model) for sorting + YuNet for face detection.",
        "Advantage: 100% Free, runs on any normal laptop, zero internet cost, and zero data leakage."
    ]

    create_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Standard OCR (Tesseract)", lit1, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📖")
    create_card(s7, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Paid Cloud APIs (Google / AWS)", lit2, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="☁️")
    create_card(s7, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Big AI Models (ChatGPT / Claude)", lit3, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="💻")
    create_card(s7, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Our Choice: Lightweight Local AI", lit4, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="⭐")

    s7.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'When looking at previous work: basic tools like Tesseract can read words but don't understand what they mean. "
        "Big cloud tools like Google or AWS work well, but they charge money and upload private Aadhaar cards to their servers. "
        "So we chose a lightweight approach: running a small AI model called Llama 3.2 and a small face detector called YuNet directly on the computer for free.'"
    )

    # ==================== SLIDE 8: EXISTING SYSTEM ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_top_template(s8, 8, 16)
    add_slide_title(s8, "Existing System: How People Fill Forms Today", "The manual multi-step process")

    e_left = [
        "Step 1: The user opens the government website (NVSP Voter Portal).",
        "Step 2: They look at their Aadhaar card in one hand (or a PDF window on screen).",
        "Step 3: They type each detail manually: Name, Father's Name, Mobile Number, Email, Gender, and Date of Birth.",
        "Step 4: They manually split their address into House No, Street, Village, Post Office, District, and PIN code."
    ]
    e_right = [
        "Step 5: The user takes a screenshot of their ID card and opens MS Paint or a mobile cropping app.",
        "Step 6: They manually crop around their face and try to resize the file to be under 2MB.",
        "Step 7: They upload the photo and identity documents one-by-one.",
        "Step 8: The entire process takes 10 to 15 minutes of slow, frustrating manual effort."
    ]
    create_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Typing Details (Steps 1 to 4)", e_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="⌨️")
    create_card(s8, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Cropping Photo & Upload (Steps 5 to 8)", e_right, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✂️")

    s8.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Today, the process is completely manual. The user opens the voter portal, reads their card, and types 20 boxes. "
        "When they reach the photo section, the portal doesn't crop photos for them. They have to open Paint, cut their face out, "
        "save the file, and upload it. It takes 10 to 15 minutes per form.'"
    )

    # ==================== SLIDE 9: LIMITATIONS OF EXISTING SYSTEM ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_top_template(s9, 9, 16)
    add_slide_title(s9, "Limitations of the Existing System", "Why the current manual system fails")

    lim1 = [
        "People often type birth dates in the wrong format (swapping day and month).",
        "Accidentally typing 'S/O Shankar' into the applicant name box.",
        "Mistyping digits in the 12-digit Aadhaar UID leading to rejection."
    ]
    lim2 = [
        "Citizens leave Aadhaar copies in download folders at cyber cafes.",
        "Normal browser autofill saves sensitive identity data unencrypted.",
        "High risk of identity theft for rural and non-technical citizens."
    ]
    lim3 = [
        "Takes 10–15 minutes per person; long queues at registration camps.",
        "Citizens pay Rs. 50 to Rs. 100 at internet centers just for basic typing.",
        "Many first-time voters give up halfway because of photo size errors."
    ]
    lim4 = [
        "The website does not verify if the typed name matches the uploaded document.",
        "Government officers have to manually check every typo during field verification.",
        "Creates a huge backlog of delayed voter identity cards."
    ]

    create_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. High Chance of Mistakes", lim1, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="❌")
    create_card(s9, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Privacy & Security Risks", lim2, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⚠️")
    create_card(s9, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Waste of Time & Money", lim3, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⏳")
    create_card(s9, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Zero Document Checking", lim4, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="🔍")

    s9.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'To summarize the drawbacks: 1. Lots of spelling and date mistakes. 2. Privacy risks at internet cafes. "
        "3. Wasting 15 minutes per form and paying money to cyber cafes. 4. The website doesn't check if what you typed matches the card. "
        "Our project solves all four problems.'"
    )

    # ==================== SLIDE 10: PROPOSED SYSTEM ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_top_template(s10, 10, 16)
    add_slide_title(s10, "Proposed System: How Our Solution Works", "Overview of what we built")

    prop_left = [
        "1. Easy Multi-File Upload: Drag and drop front and back images, or a PDF. Add files one by one or all together.",
        "2. 100% Private (No Cloud): Everything is processed locally on the laptop. No data is sent over the internet.",
        "3. Smart OCR + AI: EasyOCR reads all text; Meta Llama 3.2 AI arranges the text into Name, DOB, Address, etc.",
        "4. Automatic Face Cropping: Deep learning face detector finds the face on the card and crops a perfect passport photo."
    ]
    prop_right = [
        "5. Accurate Aadhaar Extraction: Custom rules ensure the 12-digit Aadhaar number is picked, ignoring 14-digit enrolment numbers.",
        "6. Clean Address Parsing: Automatically separates Door No (e.g. 78) from Street Name and removes legal disclaimer text.",
        "7. Automatic Dropdown Selection: Automatically selects 'Father' or 'Husband' in the relationship dropdown.",
        "8. Lightning Fast: Entire process completes in under 25 seconds with a single click."
    ]
    create_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Key Features of Our System", prop_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✨")
    create_card(s10, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Accuracy & Speed Improvements", prop_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="⚡")

    s10.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'In our proposed system, the user just drops their ID card images or PDF on the website. In less than 25 seconds, "
        "our Python backend reads the text, local Llama 3.2 AI sorts the fields, YuNet cuts out the passport photo, our cleaning rules "
        "fix the address and Aadhaar number, and every field in Form 6 is filled automatically. The user just clicks Submit.'"
    )

    # ==================== SLIDE 11: PROPOSED METHODOLOGY / ARCHITECTURE (STEP PIPELINE) ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_top_template(s11, 11, 16)
    add_slide_title(s11, "Proposed Methodology & System Architecture", "Step-by-step pipeline of our engine")

    # Step Boxes like user's Slide 5 inspiration
    step_data = [
        ("STEP 01", "Upload Document", "User drops Front/Back card images or PDF file on website.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 02", "300 DPI Rendering", "pypdfium2 converts PDF pages to sharp images for clear OCR.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 03", "Text Reading (OCR)", "EasyOCR extracts all text lines across English & Indian scripts.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 04", "Face Cropping", "OpenCV YuNet AI finds the face and cuts out a 1:1 passport photo.", CARD_GREEN_BG, CARD_GREEN_BD),
        ("STEP 05", "Local AI Sorting", "Meta Llama 3.2 AI sorts text into Name, DOB, Father Name & Address.", CARD_GREEN_BG, CARD_GREEN_BD),
        ("STEP 06", "Rules & Autofill", "Python cleans Aadhaar UID and fills Form 6 inputs automatically!", CARD_GREEN_BG, CARD_GREEN_BD),
    ]

    # Row 1: Steps 1 to 3
    col_w = Inches(3.64)
    for i in range(3):
        s_num, s_title, s_desc, bg_c, bd_c = step_data[i]
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 4.04), Inches(1.6), col_w, Inches(2.45))
        c.fill.solid()
        c.fill.fore_color.rgb = bg_c
        c.line.color.rgb = bd_c
        c.line.width = Pt(1.2)

        tb = s11.shapes.add_textbox(Inches(0.95 + i * 4.04), Inches(1.75), col_w - Inches(0.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = s_num
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = TOP_BLUE
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = s_title
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = NAVY_DARK
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = s_desc
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_DARK

    # Row 2: Steps 4 to 6
    for i in range(3):
        s_num, s_title, s_desc, bg_c, bd_c = step_data[i + 3]
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 4.04), Inches(4.35), col_w, Inches(2.45))
        c.fill.solid()
        c.fill.fore_color.rgb = bg_c
        c.line.color.rgb = bd_c
        c.line.width = Pt(1.2)

        tb = s11.shapes.add_textbox(Inches(0.95 + i * 4.04), Inches(4.5), col_w - Inches(0.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = s_num
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(16, 185, 129)
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = s_title
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = NAVY_DARK
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = s_desc
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_DARK

    s11.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Here is the 6-step flow of our engine: 1. User uploads the card. 2. PDF is converted into sharp 300 DPI images. "
        "3. EasyOCR reads all text. 4. YuNet AI finds and crops the face. 5. Local Llama 3.2 AI arranges the text into Name, DOB, etc. "
        "6. Our Python rules clean up the data and fill Form 6 on the screen.'"
    )

    # ==================== SLIDE 12: TOOLS AND TECHNOLOGIES USED ====================
    s12 = prs.slides.add_slide(blank_layout)
    add_top_template(s12, 12, 16)
    add_slide_title(s12, "Tools & Technologies Used", "Components chosen and why we chose them")

    t1 = [
        "Python 3.12: Main programming language.",
        "FastAPI: Asynchronous, high-speed backend API.",
        "Uvicorn: Runs the local web server on port 8000.",
        "Why chosen: Fast, lightweight, and connects directly with AI libraries."
    ]
    t2 = [
        "EasyOCR (PyTorch): Deep learning optical character reader.",
        "Reads English and Indian regional text (Tamil, Hindi, etc.).",
        "pypdfium2: Renders PDF documents into 300 DPI images.",
        "Why chosen: Highly accurate on complex Indian ID layouts."
    ]
    t3 = [
        "Meta Llama 3.2 (3B): Small Language Model created by Meta AI.",
        "Ollama: Software that runs Llama 3.2 locally on the laptop.",
        "Converts messy OCR text into clean, structured fields.",
        "Why chosen: Works offline without internet, keeping personal data 100% safe."
    ]
    t4 = [
        "OpenCV YuNet: Modern deep learning face detector.",
        "Small 232 KB model that achieves over 92% face accuracy.",
        "Frontend: Clean Semantic HTML5, CSS3, and JavaScript.",
        "Why chosen: Crops 1:1 passport photos automatically on any normal laptop."
    ]

    create_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Backend: Python & FastAPI", t1, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="⚙️")
    create_card(s12, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Text Reading: EasyOCR", t2, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📖")
    create_card(s12, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Local AI: Meta Llama 3.2", t3, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🧠")
    create_card(s12, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Face Cropping: OpenCV YuNet", t4, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="👁️")

    s12.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Staff, for our technologies: We used Python with FastAPI for the backend. We used EasyOCR to read text from cards. "
        "We used Meta's Llama 3.2 model running locally via Ollama to sort the words into fields without needing internet. "
        "We used OpenCV's YuNet model to detect the face and crop the passport photo. And our frontend uses simple, clean HTML and JavaScript.'"
    )

    # ==================== SLIDE 13: WORK COMPLETED SO FAR ====================
    s13 = prs.slides.add_slide(blank_layout)
    add_top_template(s13, 13, 16)
    add_slide_title(s13, "Work Completed So Far (Our Working Results)", "Fully working prototype already built and tested")

    r1 = [
        "Built an interactive drag-and-drop file uploader.",
        "Users can attach Front PNG, Back PNG, and multi-page PDFs.",
        "Shows file size badges and an 'X' button to remove files.",
        "Status: 100% Completed & Verified."
    ]
    r2 = [
        "Integrated OpenCV YuNet neural network (232 KB model).",
        "Finds the applicant's face on the card with over 92% confidence.",
        "Crops a clean 1:1 passport photo with proper margins around head.",
        "Skin-tone filter prevents accidentally cropping text boxes."
    ]
    r3 = [
        "Fixed Aadhaar extraction: Picks 12-digit UID (e.g. 6120 9678 1604) and ignores 14-digit enrolment numbers.",
        "Fixed Relative extraction: Handles 'SJO' or 'S/O' and extracts father's name ('Shankar').",
        "Automatically sets 'Father' in the relationship dropdown."
    ]
    r4 = [
        "Filtered out legal warnings ('Documents to support identity...').",
        "Cleanly splits House/Door No ('78') and Street ('2ND STREET, INDRA GANDHI NAGAR').",
        "Converts Date of Birth to HTML date format ('21-02-2006').",
        "Code pushed to GitHub: github.com/deva-2006/govtAutofill."
    ]

    create_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Multi-Document File Manager", r1, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="✅")
    create_card(s13, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Deep Learning Face Cropping", r2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="✅")
    create_card(s13, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Accurate Aadhaar & Relation", r3, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✅")
    create_card(s13, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Clean Address Splitting", r4, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✅")

    s13.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'For Phase 1, we have already built a fully working prototype! We tested it on real Aadhaar documents. "
        "We successfully solved four tough problems: 1. Uploading both front and back images together. 2. Cropping the face photo cleanly without "
        "including text. 3. Picking the true 12-digit Aadhaar number instead of the 14-digit enrolment number. And 4. Splitting the door number "
        "and street name cleanly while removing legal disclaimer text. All code is committed on GitHub.'"
    )

    # ==================== SLIDE 14: EXPECTED OUTCOMES ====================
    s14 = prs.slides.add_slide(blank_layout)
    add_top_template(s14, 14, 16)
    add_slide_title(s14, "Expected Outcomes: Big Benefits for Citizens", "Measurable improvements delivered by our system")

    o1 = [
        "Manual time today: 10 to 15 minutes per form.",
        "With our system: Under 25 to 30 seconds.",
        "Saves huge amounts of time for citizens and registration camps."
    ]
    o2 = [
        "Typing error rate drops from ~20% to less than 2%.",
        "Eliminates wrong date formats and misspelled names.",
        "Applications get approved faster without administrative queries."
    ]
    o3 = [
        "All processing runs locally on the user's computer.",
        "No Aadhaar data is stored or sent to outside servers.",
        "Safe to use even on personal computers."
    ]
    o4 = [
        "Can be easily adapted for PAN card applications, Driving License forms, or College admissions.",
        "Works on normal 8GB RAM laptops without expensive GPUs."
    ]

    create_card(s14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. 90% Faster Form Filling", o1, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="⚡")
    create_card(s14, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Almost Zero Typing Mistakes", o2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🎯")
    create_card(s14, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. 100% Data Privacy (Safe)", o3, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🔒")
    create_card(s14, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Reusable for Other Forms", o4, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="🔄")

    s14.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'The expected benefits are very clear: 1. 90% time saved—filling a form takes under 30 seconds instead of 15 minutes. "
        "2. Typing mistakes drop to under 2%. 3. Total privacy—no citizen data is sent over the internet. And 4. The same system can be "
        "used for PAN cards, Driving Licenses, and college admission forms in the future.'"
    )

    # ==================== SLIDE 15: PROJECT TIMELINE ====================
    s15 = prs.slides.add_slide(blank_layout)
    add_top_template(s15, 15, 16)
    add_slide_title(s15, "Project Timeline & Work Plan", "Roadmap across the three review stages")

    tm1 = [
        "Studied Voter ID Form 6 requirements.",
        "Integrated EasyOCR for reading text.",
        "Setup local Meta Llama 3.2 AI via Ollama.",
        "Integrated OpenCV YuNet deep learning face cropping.",
        "Tested and verified on sample Aadhaar cards.",
        "Current Status: Fully working prototype demonstrated in Review 1."
    ]
    tm2 = [
        "Add support for PAN Card and Driving License uploads.",
        "Cross-verify name and DOB between Aadhaar and PAN card.",
        "Add green checkmarks showing confidence for each filled box.",
        "Automatically wipe uploaded images from memory after form is submitted."
    ]
    tm3 = [
        "Package the system as a Chrome / Firefox Browser Extension.",
        "The extension will directly fill the real live government website (voters.eci.gov.in) with 1 click.",
        "Test on 50 different sample cards with different photo qualities.",
        "Complete final project report and documentation."
    ]

    create_card(s15, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "Phase 1: Working Prototype [DONE]", tm1, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🏁")
    create_card(s15, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "Phase 2: More Documents [MID REVIEW]", tm2, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🚀")
    create_card(s15, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.55), "Phase 3: Browser Extension & Live Testing [FINAL REVIEW]", tm3, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="🌐")

    s15.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Here is our 3-phase plan: Phase 1 is completed—we built the core working prototype for Aadhaar and Form 6. "
        "In Phase 2 for the Mid Review, we will add PAN cards and Driving Licenses, and add green confidence checkmarks. "
        "In Phase 3 for the Final Review, we will turn this into a Chrome Extension that directly fills the live government website with one click.'"
    )

    # ==================== SLIDE 16: CONCLUSION & REFERENCES ====================
    s16 = prs.slides.add_slide(blank_layout)
    add_top_template(s16, 16, 16)
    add_slide_title(s16, "Conclusion & References", "Summary of our work")

    ref_items = [
        "1. Election Commission of India (ECI), 'Voter Registration Form 6 Guidelines', eci.gov.in, 2023.",
        "2. Meta AI, 'Llama 3.2: Lightweight Multilingual Models for Edge Devices', 2024.",
        "3. OpenCV Zoo, 'YuNet: Compact Deep Neural Network for Real-Time Face Detection', 2023.",
        "4. Jaided AI, 'EasyOCR: Python Package for Optical Character Recognition', 2023.",
        "5. Project GitHub Repository: https://github.com/deva-2006/govtAutofill"
    ]
    conc_items = [
        "Solves a Real Problem: Eliminates boring, error-prone typing for citizens applying for government voter cards.",
        "Privacy First: Uses local AI and on-device face detection so no private data leaves the laptop.",
        "High Accuracy: Automatically separates door numbers, picks true Aadhaar numbers, and crops passport photos.",
        "Proven Working System: Already tested and working; strong base ready for Phase 2 expansion."
    ]

    create_card(s16, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Key References", ref_items, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📚")
    create_card(s16, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Concluding Summary", conc_items, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🏆")

    s16.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'In conclusion: our project makes filling government forms fast, simple, and completely private. "
        "We have already built a working system that takes an ID card, reads the text, crops the photo, and fills Form 6 in 20 seconds. "
        "We are ready for Phase 2. Thank you staff, we are happy to answer any questions!'"
    )

    # Save presentation
    output_filename = "First_Review_UG_Project_Presentation.pptx"
    prs.save(output_filename)
    print(f"Inspired presentation successfully created: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    build_inspired_presentation()
