import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_simple_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Clean Color Palette
    NAVY = RGBColor(15, 43, 72)         # Primary Dark Blue
    ROYAL = RGBColor(37, 99, 235)       # Bright Royal Blue
    CYAN = RGBColor(56, 189, 248)       # Bright Cyan Accent
    DARK = RGBColor(30, 41, 59)         # Dark text
    MUTED = RGBColor(100, 116, 139)     # Subtitle gray
    CARD_BG = RGBColor(255, 255, 255)   # White
    BORDER_COL = RGBColor(226, 232, 240)# Soft border
    GREEN = RGBColor(16, 185, 129)      # Success Green
    RED = RGBColor(225, 29, 72)         # Problem Red

    def add_header(slide, title_text, category="UG PROJECT REVIEW - I"):
        # Top banner
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = NAVY
        top_bar.line.fill.background()

        # Accent bar
        acc_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        acc_bar.fill.solid()
        acc_bar.fill.fore_color.rgb = ROYAL
        acc_bar.line.fill.background()

        # Category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.3))
        cat_tf = cat_box.text_frame
        cat_tf.word_wrap = True
        cat_p = cat_tf.paragraphs[0]
        cat_p.text = category.upper()
        cat_p.font.size = Pt(10)
        cat_p.font.bold = True
        cat_p.font.color.rgb = CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.7), Inches(0.65))
        title_tf = title_box.text_frame
        title_tf.word_wrap = True
        title_p = title_tf.paragraphs[0]
        title_p.text = title_text
        title_p.font.size = Pt(21)
        title_p.font.bold = True
        title_p.font.color.rgb = RGBColor(255, 255, 255)

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.35))
        ft_tf = footer_box.text_frame
        ft_p = ft_tf.paragraphs[0]
        ft_p.text = "Dept of CSE | UG Project Review - 1 | Team: Deva S, Athithi A, Arthi S"
        ft_p.font.size = Pt(9.5)
        ft_p.font.color.rgb = MUTED

    def create_card(slide, left, top, width, height, title, items, badge="", title_color=DARK, bg_color=CARD_BG, border_color=BORDER_COL):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        tp = tf.paragraphs[0]
        if badge:
            tp.text = f"{title}  [{badge}]"
        else:
            tp.text = title
        tp.font.size = Pt(14.5)
        tp.font.bold = True
        tp.font.color.rgb = title_color
        tp.space_after = Pt(10)

        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(11.5)
            p.font.color.rgb = DARK
            p.space_after = Pt(6)

        return card

    # ==================== SLIDE 1: TITLE SLIDE ====================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.2))
    ttf = tbox.text_frame
    ttf.word_wrap = True
    
    tp1 = ttf.paragraphs[0]
    tp1.text = "UG PROJECT - FIRST REVIEW"
    tp1.font.size = Pt(13)
    tp1.font.bold = True
    tp1.font.color.rgb = CYAN
    tp1.space_after = Pt(12)

    tp2 = ttf.add_paragraph()
    tp2.text = "AI-Based Smart Document Autofill for Government Portals"
    tp2.font.size = Pt(28)
    tp2.font.bold = True
    tp2.font.color.rgb = RGBColor(255, 255, 255)
    tp2.space_after = Pt(10)

    tp3 = ttf.add_paragraph()
    tp3.text = "Automatically reading ID cards (Aadhaar / PAN) and filling Voter ID Form 6 using local AI and face detection"
    tp3.font.size = Pt(15)
    tp3.font.color.rgb = RGBColor(203, 213, 225)

    dline = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.333), Inches(0.04))
    dline.fill.solid()
    dline.fill.fore_color.rgb = ROYAL
    dline.line.fill.background()

    # Team Card
    team_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.15), Inches(6.8), Inches(2.5))
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = RGBColor(22, 53, 86)
    team_card.line.color.rgb = ROYAL
    team_card.line.width = Pt(1)

    tctb = s1.shapes.add_textbox(Inches(1.2), Inches(4.25), Inches(6.4), Inches(2.3))
    tctf = tctb.text_frame
    tctf.word_wrap = True
    
    tcp1 = tctf.paragraphs[0]
    tcp1.text = "PROJECT TEAM MEMBERS:"
    tcp1.font.size = Pt(12)
    tcp1.font.bold = True
    tcp1.font.color.rgb = CYAN
    tcp1.space_after = Pt(8)

    members = [
        ("DEVA S", "2117230070025"),
        ("ATHITHI A", "2117230070004"),
        ("ARTHI S", "2117230070016")
    ]
    for name, regno in members:
        mp = tctf.add_paragraph()
        mp.text = f"•  {name}  —  Reg No: {regno}"
        mp.font.size = Pt(13)
        mp.font.bold = True
        mp.font.color.rgb = RGBColor(255, 255, 255)
        mp.space_after = Pt(4)

    # Info card
    acad_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(4.15), Inches(4.233), Inches(2.5))
    acad_card.fill.solid()
    acad_card.fill.fore_color.rgb = RGBColor(22, 53, 86)
    acad_card.line.color.rgb = ROYAL
    acad_card.line.width = Pt(1)

    actb = s1.shapes.add_textbox(Inches(8.3), Inches(4.25), Inches(3.8), Inches(2.3))
    actf = actb.text_frame
    actf.word_wrap = True
    acp = actf.paragraphs[0]
    acp.text = "PROJECT DETAILS"
    acp.font.size = Pt(12)
    acp.font.bold = True
    acp.font.color.rgb = CYAN
    acp.space_after = Pt(8)

    ac_items = [
        "Degree: B.E. Computer Science & Engineering",
        "Target Application: ECI NVSP Voter Registration (Form 6)",
        "Review Stage: First Review (Phase - 1)",
        "System: 100% Local Processing (Zero Cloud Cost)"
    ]
    for it in ac_items:
        p = actf.add_paragraph()
        p.text = it
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(3)

    s1.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Good morning staff. We are Deva, Athithi, and Arthi. Our project is an AI tool that helps people fill government web forms easily. "
        "Today, when applying for a Voter ID card (Form 6), people have to type over 20 details by hand from their Aadhaar card. "
        "In our project, the user simply uploads their Aadhaar card or PAN card, and our AI reads all the details, cuts out their passport photo, "
        "and fills the entire form automatically in just a few seconds.'"
    )

    # ==================== SLIDE 2: TABLE OF CONTENTS ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Table of Contents", "AGENDA")
    
    col1 = [
        "1. Introduction",
        "2. Background of the Project",
        "3. Problem Statement",
        "4. Aim and Objectives",
        "5. Literature Review",
        "6. Existing System",
        "7. Limitations of the Existing System"
    ]
    col2 = [
        "8. Proposed System",
        "9. System Architecture & How it Works",
        "10. Tools & Technologies Used",
        "11. Work Completed So Far (Our Results)",
        "12. What We Have Built (Key Features)",
        "13. Expected Outcomes & Benefits",
        "14. Project Timeline & Next Steps",
        "15. Conclusion & References"
    ]
    create_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "Part 1: The Problem & Study", col1, badge="Slides 3-9", title_color=ROYAL)
    create_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), "Part 2: Our Solution & Results", col2, badge="Slides 10-16", title_color=GREEN)

    s2.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Here is our presentation flow. First, we explain why filling government forms is difficult today, what problems people face, "
        "and what other researchers have done. Then, we explain our system, the technologies we used, the working prototype we have already built, "
        "and our plan for the next review.'"
    )

    # ==================== SLIDE 3: INTRODUCTION ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Introduction: What is this Project About?", "PROJECT OVERVIEW")
    
    intro_1 = [
        "Applying for government IDs (like Voter ID Form 6) requires typing more than 20 details manually.",
        "Applicants have to type Name, Father's Name, DOB, Gender, Mobile No, and break their full address into Door No, Street, Village, and Pincode.",
        "They also have to crop and resize a separate passport photo to match website size rules.",
        "This manual process takes 10 to 15 minutes per person and causes many typing mistakes."
    ]
    intro_2 = [
        "Our Solution: A smart web app that reads the ID card and fills the form automatically.",
        "The user simply uploads their Aadhaar card (PDF or image).",
        "Our AI reads all the text, finds the person's face, cuts out a clean passport photo, and fills all the boxes instantly.",
        "Privacy-Friendly: Everything runs directly on the computer—no data is sent to external cloud servers."
    ]
    create_card(s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "The Real-World Need", intro_1, badge="The Situation", title_color=ROYAL)
    create_card(s3, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), "Our Smart Approach", intro_2, badge="Our Idea", title_color=GREEN)

    s3.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Staff, in simple terms: whenever anyone applies for a Voter ID card, they must sit with their Aadhaar card and type every single box by hand. "
        "They also have to open Paint or Photoshop to crop their passport photo. In our project, the user simply drops their Aadhaar card on the screen. "
        "Our AI automatically reads the text, cuts the photo, and fills all boxes in 20 seconds. It works completely offline on the computer, so personal data is safe.'"
    )

    # ==================== SLIDE 4: BACKGROUND ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Background: The Voter ID (Form 6) Process", "BACKGROUND STUDY")
    
    bg_1 = [
        "Form 6 is the official form used by the Election Commission of India (ECI) for new voter registrations.",
        "Over 2 crore (20 million) new voters apply every single year across India.",
        "Every applicant must provide proof documents—most commonly e-Aadhaar cards, PAN cards, or Birth Certificates.",
        "Applicants must select family relations correctly (Father, Mother, Husband, or Guardian)."
    ]
    bg_2 = [
        "High Rejection Rate: Nearly 1 in 5 applications face delays or rejection due to silly typing mistakes.",
        "Common mistakes include: typing month before day in date of birth, misspelling names, or missing door numbers.",
        "Public Cafe Risks: Rural citizens go to browsing centers and leave copies of their Aadhaar cards on public computers.",
        "Conclusion: We need an easy, automated tool that helps common citizens fill forms without mistakes."
    ]
    create_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "Scale of Voter Registration in India", bg_1, badge="The Scale", title_color=ROYAL)
    create_card(s4, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), "Why Applications Get Rejected", bg_2, badge="Common Mistakes", title_color=RED)

    s4.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Every year, more than 2 crore young citizens turn 18 and apply for Voter ID cards using Form 6. But around 20% of applications "
        "have issues because people type their birth date in the wrong format or make spelling mistakes. Also, people who don't have computers "
        "go to internet cafes, pay money, and leave copies of their Aadhaar cards on shared computers. This is why we wanted to build this solution.'"
    )

    # ==================== SLIDE 5: PROBLEM STATEMENT ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Problem Statement: 4 Major Challenges", "CORE ISSUES")
    
    p_cards = [
        ("1. Too Much Manual Typing", [
            "Users must type over 20 separate boxes by hand.",
            "Long numbers (12-digit Aadhaar UID) are easy to mistype.",
            "Address fields require splitting Door No, Street, and City manually."
        ], Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.55), RED),

        ("2. Personal Data Privacy Risks", [
            "Uploading ID cards to public online servers can leak private information.",
            "Cyber cafes store scanned cards on shared hard drives.",
            "Commercial OCR services cost money and save user data."
        ], Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.55), RED),

        ("3. Confusing ID Card Text", [
            "Aadhaar cards have 14-digit enrolment numbers that look like Aadhaar numbers.",
            "Cards contain long legal disclaimers that confuse normal scanning tools.",
            "Photos taken on mobile phones can be blurry, tilted, or faint."
        ], Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.55), DARK),

        ("4. Photo Cropping Headache", [
            "Websites require a separate passport-size photo under 2MB.",
            "Normal users do not know how to crop images properly.",
            "Users are forced to ask others for help or pay cyber cafes."
        ], Inches(6.8), Inches(4.25), Inches(5.7), Inches(2.55), DARK)
    ]
    for title, items, l, t, w, h, col in p_cards:
        create_card(s5, l, t, w, h, title, items, title_color=col)

    s5.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Staff, there are four main problems: First, too much typing leads to mistakes. Second, uploading private Aadhaar cards to commercial cloud "
        "APIs is dangerous for privacy. Third, Aadhaar cards have messy text like enrolment numbers and disclaimers that fool normal scanners. "
        "And fourth, people find it very hard to crop and resize a passport photo by themselves.'"
    )

    # ==================== SLIDE 6: AIM AND OBJECTIVES ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Aim & Objectives of Our Project", "PROJECT GOALS")
    
    aim_box = [
        "To build a fast, free, and completely private web application that reads Indian ID cards (Aadhaar / PAN), automatically detects and crops the applicant's passport photo, and fills the Voter ID Form 6 in under 30 seconds."
    ]
    create_card(s6, Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.4), "OUR MAIN AIM", aim_box, badge="Primary Goal", title_color=ROYAL)

    obj1 = [
        "Objective 1: Multi-Document Upload",
        "  • Allow users to upload both Front and Back images, or a single PDF.",
        "  • Show clear badges for attached files with an easy remove option.",
        "Objective 2: Accurate Text Reading (OCR)",
        "  • Use EasyOCR to read English and Tamil/regional text clearly.",
        "  • Convert PDFs to high-resolution images so small text is easily read."
    ]
    obj2 = [
        "Objective 3: Smart Field Sorting (Local AI)",
        "  • Use Meta Llama 3.2 AI running on our laptop to sort words into Name, DOB, etc.",
        "  • Automatically identify Father's or Husband's name from 'S/O' or 'W/O'.",
        "Objective 4: Automatic Face Photo Cropping",
        "  • Use OpenCV YuNet face detection to find the person's face on the card.",
        "  • Automatically crop a clean passport-size photo without any text around it."
    ]
    create_card(s6, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7), "Objectives (1 & 2): Reading & Files", obj1, badge="Input & OCR", title_color=DARK)
    create_card(s6, Inches(6.8), Inches(3.1), Inches(5.7), Inches(3.7), "Objectives (3 & 4): AI & Face Cropping", obj2, badge="AI & Vision", title_color=GREEN)

    s6.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Our aim is simple: In under 30 seconds, take an ID card, extract all details, crop the photo, and fill Form 6. "
        "Our four clear objectives are: 1. Let users upload front and back images easily. 2. Read the text accurately with OCR. "
        "3. Use local AI to put names and addresses in the right boxes. 4. Automatically find and crop the face photo for the form.'"
    )

    # ==================== SLIDE 7: LITERATURE REVIEW ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Literature Review: What Existing Tools Do", "PREVIOUS WORK COMPARISON")
    
    lit_cards = [
        ("1. Standard OCR Tools (like Tesseract)", [
            "What they do: Reads words from simple scanned papers.",
            "Drawback: Just gives a big list of words; does not know which word is 'Name' and which is 'City'. Fails on Indian regional languages."
        ], Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.55)),

        ("2. Commercial Cloud APIs (Google Vision / AWS)", [
            "What they do: Very good at reading documents and forms.",
            "Drawback: Charges money for every single scan, needs internet, and sends private citizen data to third-party servers."
        ], Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.55)),

        ("3. Huge AI Models (like ChatGPT / Claude)", [
            "What they do: Can understand forms very well.",
            "Drawback: Too large to run locally on a normal laptop; requires expensive graphic cards or paid internet subscriptions."
        ], Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.55)),

        ("4. Our Approach: Lightweight Local AI", [
            "What we do: We use EasyOCR for reading + Meta Llama 3.2 (small 3B model) for sorting + YuNet for face detection.",
            "Advantage: 100% Free, runs on any laptop, zero internet cost, and zero data leakage."
        ], Inches(6.8), Inches(4.25), Inches(5.7), Inches(2.55))
    ]
    for title, items, l, t, w, h in lit_cards:
        create_card(s7, l, t, w, h, title, items, title_color=ROYAL)

    s7.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'When we looked at previous research: basic tools like Tesseract can read text but don't understand what the text means. "
        "Big cloud tools like Google or AWS work well, but they charge money and upload private Aadhaar cards to their servers. "
        "So we chose a lightweight, open-source approach: running a small AI model called Llama 3.2 and a small face detector called YuNet "
        "directly on the computer for free.'"
    )

    # ==================== SLIDE 8: EXISTING SYSTEM ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Existing System: How People Fill Forms Today", "MANUAL PROCESS")
    
    ex1 = [
        "Step 1: The user opens the government website (NVSP Voter Portal).",
        "Step 2: They look at their Aadhaar card in one hand (or a PDF window on screen).",
        "Step 3: They type each detail manually: Name, Father's Name, Mobile Number, Email, Gender, and Date of Birth.",
        "Step 4: They manually split their address into House No, Street, Village, Post Office, District, and PIN code."
    ]
    ex2 = [
        "Step 5: The user takes a screenshot of their ID card and opens MS Paint or a mobile cropping app.",
        "Step 6: They manually crop around their face and try to resize the file to be under 2MB.",
        "Step 7: They upload the photo and identity documents one-by-one.",
        "Step 8: The entire process takes 10 to 15 minutes of slow, frustrating manual effort."
    ]
    create_card(s8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "Typing Details (Steps 1 to 4)", ex1, badge="Typing Friction", title_color=DARK)
    create_card(s8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), "Photo Cropping (Steps 5 to 8)", ex2, badge="Image Editing", title_color=DARK)

    s8.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Today, the process is completely manual. The user opens the voter portal, reads their card, and types 20 boxes. "
        "When they reach the photo section, the portal doesn't crop photos for them. They have to open Paint, cut their face out, "
        "save the file, and upload it. It takes 10 to 15 minutes per form.'"
    )

    # ==================== SLIDE 9: LIMITATIONS OF EXISTING SYSTEM ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Limitations of the Existing System", "THE DRAWBACKS")
    
    lim_cards = [
        ("1. High Chance of Mistakes", [
            "People often type birth dates in the wrong format (like swapping day and month).",
            "Accidentally typing 'S/O Shankar' into the name box.",
            "Mistyping even one digit of the 12-digit Aadhaar number."
        ], Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.55)),

        ("2. Privacy and Security Risks", [
            "People leave unredacted Aadhaar copies in download folders at cyber cafes.",
            "Normal browser autofills save sensitive personal data unencrypted.",
            "High risk of identity theft for rural and non-technical citizens."
        ], Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.55)),

        ("3. Waste of Time & Money", [
            "Takes 10–15 minutes per person; long queues at registration camps.",
            "Citizens pay Rs. 50 to Rs. 100 at internet centers just for basic form typing.",
            "Many first-time voters give up halfway because of photo size errors."
        ], Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.55)),

        ("4. No Verification", [
            "The website does not verify if the typed name matches the uploaded document.",
            "Government officers have to manually check every typo during physical verification.",
            "Creates a huge backlog of delayed voter identity cards."
        ], Inches(6.8), Inches(4.25), Inches(5.7), Inches(2.55))
    ]
    for title, items, l, t, w, h in lim_cards:
        create_card(s9, l, t, w, h, title, items, title_color=RED)

    s9.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'To summarize the drawbacks: 1. Lots of spelling and date mistakes. 2. Privacy risks at internet cafes. "
        "3. Wasting 15 minutes per form and paying money to cyber cafes. 4. The website doesn't check if what you typed matches the card. "
        "Our project solves all four problems.'"
    )

    # ==================== SLIDE 10: PROPOSED SYSTEM ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Proposed System: How Our Solution Works", "OUR SMART SOLUTION")
    
    prop1 = [
        "1. Easy Multi-File Upload: Drag and drop front and back images, or a PDF. Add files one by one or all together.",
        "2. 100% Private (No Cloud): Everything is processed locally on the laptop. No data is sent over the internet.",
        "3. Smart OCR + AI: EasyOCR reads all text; Meta Llama 3.2 AI arranges the text into Name, DOB, Address, etc.",
        "4. Automatic Face Cropping: Deep learning face detector finds the face on the card and crops a perfect passport photo."
    ]
    prop2 = [
        "5. Accurate Aadhaar Extraction: Custom rules ensure the 12-digit Aadhaar number is picked, ignoring 14-digit enrolment numbers.",
        "6. Clean Address Parsing: Automatically separates Door No (e.g. 78) from Street Name and removes legal disclaimer text.",
        "7. Automatic Dropdown Selection: Automatically selects 'Father' or 'Husband' in the relationship dropdown.",
        "8. Lightning Fast: Entire process completes in under 25 seconds with a single click."
    ]
    create_card(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "Key Features of Our System", prop1, badge="Smart & Private", title_color=ROYAL)
    create_card(s10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), "Accuracy & Speed Improvements", prop2, badge="Accurate & Fast", title_color=GREEN)

    s10.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'In our proposed system, the user just drops their ID card images or PDF on the website. In less than 25 seconds, "
        "our Python backend reads the text, local Llama 3.2 AI sorts the fields, YuNet cuts out the passport photo, our cleaning rules "
        "fix the address and Aadhaar number, and every field in Form 6 is filled automatically. The user just clicks Submit.'"
    )

    # ==================== SLIDE 11: PROPOSED METHODOLOGY ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Proposed Methodology & Step-by-Step Architecture", "WORKFLOW")
    
    flow_steps = [
        ("Step 1: Upload", [
            "• User drops Front & Back card images or PDF.",
            "• Frontend manages attached file chips.",
            "• Sends files to FastAPI backend."
        ], Inches(0.8), Inches(1.5), Inches(2.75), Inches(5.3), NAVY),

        ("Step 2: Read & Detect", [
            "• EasyOCR reads all text from the card.",
            "• YuNet AI finds the face on the card.",
            "• Automatically crops clean passport photo.",
            "• Skin-tone filter rejects text crops."
        ], Inches(3.75), Inches(1.5), Inches(2.75), Inches(5.3), ROYAL),

        ("Step 3: Understand", [
            "• Text is sent to local Llama 3.2 AI.",
            "• AI sorts text into Name, DOB, Father's Name, and Address.",
            "• Runs offline via Ollama (no cloud)."
        ], Inches(6.7), Inches(1.5), Inches(2.75), Inches(5.3), DARK),

        ("Step 4: Clean & Fill", [
            "• Cleans 12-digit Aadhaar UID.",
            "• Splits Door No & Street clearly.",
            "• Converts DOB to YYYY-MM-DD.",
            "• Fills all Form 6 boxes instantly!"
        ], Inches(9.65), Inches(1.5), Inches(2.85), Inches(5.3), GREEN)
    ]
    for title, items, l, t, w, h, col in flow_steps:
        create_card(s11, l, t, w, h, title, items, title_color=col)

    s11.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Here is the 4-step workflow: Step 1: User uploads files. Step 2: EasyOCR reads the text, and YuNet AI finds and crops the face. "
        "Step 3: Local Llama 3.2 AI figures out which word is the name, which is the father's name, and which is the address. "
        "Step 4: Our Python code cleans up the data and fills the Form 6 inputs automatically.'"
    )

    # ==================== SLIDE 12: TOOLS AND TECHNOLOGIES ====================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Tools & Technologies Used (Why We Chose Them)", "TECH STACK")
    
    t_cards = [
        ("1. Backend: Python & FastAPI", [
            "• Python 3.12: Main programming language.",
            "• FastAPI: Very fast and modern web backend framework.",
            "• Uvicorn: Runs the local backend server on port 8000.",
            "• Why chosen: Fast, handles multiple files easily, and connects with AI libraries."
        ], Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.55), ROYAL),

        ("2. Text Reading: EasyOCR", [
            "• EasyOCR (PyTorch): Deep learning library to read text from images.",
            "• Reads English and Indian regional text (Tamil, etc.).",
            "• pypdfium2: Converts PDF pages into high-clarity images.",
            "• Why chosen: Much more accurate than old tools like Tesseract."
        ], Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.55), GREEN),

        ("3. Local AI: Meta Llama 3.2 (3B)", [
            "• Llama 3.2: Small Language Model created by Meta AI.",
            "• Hosted locally using Ollama (free local software).",
            "• Converts messy OCR text into clean JSON data.",
            "• Why chosen: Works offline without internet, keeping personal data 100% private."
        ], Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.55), DARK),

        ("4. Face Cropping: OpenCV YuNet", [
            "• YuNet: Modern AI face detection model built into OpenCV.",
            "• Tiny file size (just 232 KB) but achieves over 92% face accuracy.",
            "• Frontend: Clean HTML5, CSS3, and JavaScript.",
            "• Why chosen: Fast, runs on any laptop, and crops perfect passport photos."
        ], Inches(6.8), Inches(4.25), Inches(5.7), Inches(2.55), NAVY)
    ]
    for title, items, l, t, w, h, col in t_cards:
        create_card(s12, l, t, w, h, title, items, title_color=col)

    s12.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Staff, for our technologies: We used Python with FastAPI for the backend. We used EasyOCR to read text from cards. "
        "We used Meta's Llama 3.2 model running locally via Ollama to sort the words into fields without needing internet. "
        "We used OpenCV's YuNet model to detect the face and crop the passport photo. And our frontend uses simple, clean HTML and JavaScript.'"
    )

    # ==================== SLIDE 13: WORK COMPLETED SO FAR ====================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Work Completed So Far (Our Working Results)", "PHASE 1 DELIVERABLES")
    
    res_cards = [
        ("1. Multi-Document File Manager", [
            "• Built an interactive drag-and-drop file uploader.",
            "• Users can attach Front PNG, Back PNG, and multi-page PDFs.",
            "• Shows file size badges and an 'X' button to remove files.",
            "• Status: 100% Completed & Verified."
        ], Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.55), GREEN),

        ("2. Deep Learning Face Photo Cropping", [
            "• Integrated OpenCV YuNet neural network (232 KB model).",
            "• Finds the applicant's face on the card with over 92% confidence.",
            "• Crops a clean 1:1 passport photo with proper margins around head.",
            "• Skin-tone filter prevents accidentally cropping text boxes."
        ], Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.55), GREEN),

        ("3. Accurate Aadhaar Number & Relative Name", [
            "• Fixed Aadhaar extraction: Picks 12-digit UID (e.g. 6120 9678 1604) and ignores 14-digit enrolment numbers.",
            "• Fixed Relative extraction: Handles 'SJO' or 'S/O' and extracts father's name ('Shankar').",
            "• Automatically sets 'Father' in the relationship dropdown."
        ], Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.55), ROYAL),

        ("4. Clean Address Splitting", [
            "• Filtered out legal warnings ('Documents to support identity...').",
            "• Cleanly splits House/Door No ('78') and Street ('2ND STREET, INDRA GANDHI NAGAR').",
            "• Converts Date of Birth to HTML date format ('21-02-2006').",
            "• Code pushed to GitHub: github.com/deva-2006/govtAutofill."
        ], Inches(6.8), Inches(4.25), Inches(5.7), Inches(2.55), ROYAL)
    ]
    for title, items, l, t, w, h, col in res_cards:
        create_card(s13, l, t, w, h, title, items, title_color=col)

    s13.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'For Phase 1, we have already built a fully working prototype! We tested it on real Aadhaar documents. "
        "We successfully solved four tough problems: 1. Uploading both front and back images together. 2. Cropping the face photo cleanly without "
        "including text. 3. Picking the true 12-digit Aadhaar number instead of the 14-digit enrolment number. And 4. Splitting the door number "
        "and street name cleanly while removing legal disclaimer text. All code is committed on GitHub.'"
    )

    # ==================== SLIDE 14: EXPECTED OUTCOMES ====================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Expected Outcomes: Big Benefits for Citizens", "EXPECTED RESULTS")
    
    out_cards = [
        ("1. 90% Faster Form Filling", [
            "• Manual time today: 10 to 15 minutes per form.",
            "• With our system: Under 25 to 30 seconds.",
            "• Saves huge amounts of time for citizens and registration camps."
        ], Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.55), GREEN),

        ("2. Almost Zero Typing Mistakes", [
            "• Typing error rate drops from ~20% to less than 2%.",
            "• Eliminates wrong date formats and misspelled names.",
            "• Applications get approved faster without administrative queries."
        ], Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.55), GREEN),

        ("3. 100% Data Privacy (Safe for Citizens)", [
            "• All processing runs locally on the user's computer.",
            "• No Aadhaar data is stored or sent to outside servers.",
            "• Safe to use even on personal computers."
        ], Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.55), ROYAL),

        ("4. Reusable for Other Forms", [
            "• Can be easily adapted for PAN card applications, Driving License forms, or College admissions.",
            "• Works on normal 8GB RAM laptops without expensive GPUs."
        ], Inches(6.8), Inches(4.25), Inches(5.7), Inches(2.55), ROYAL)
    ]
    for title, items, l, t, w, h, col in out_cards:
        create_card(s14, l, t, w, h, title, items, title_color=col)

    s14.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'The expected benefits are very clear: 1. 90% time saved—filling a form takes under 30 seconds instead of 15 minutes. "
        "2. Typing mistakes drop to under 2%. 3. Total privacy—no citizen data is sent over the internet. And 4. The same system can be "
        "used for PAN cards, Driving Licenses, and college admission forms in the future.'"
    )

    # ==================== SLIDE 15: PROJECT TIMELINE ====================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Project Timeline & Work Plan", "ROADMAP")
    
    time_cards = [
        ("Phase 1: Working Prototype [COMPLETED]", [
            "• Studied Voter ID Form 6 requirements.",
            "• Integrated EasyOCR for reading text.",
            "• Setup local Meta Llama 3.2 AI via Ollama.",
            "• Integrated OpenCV YuNet deep learning face cropping.",
            "• Tested and verified on sample Aadhaar cards.",
            "• Current Status: Fully working prototype demonstrated in Review 1."
        ], Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.55), GREEN),

        ("Phase 2: More Documents & Security [MID REVIEW]", [
            "• Add support for PAN Card and Driving License uploads.",
            "• Cross-verify name and DOB between Aadhaar and PAN card.",
            "• Add green checkmarks showing confidence for each filled box.",
            "• Automatically wipe uploaded images from memory after form is submitted."
        ], Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.55), ROYAL),

        ("Phase 3: Browser Extension & Final Testing [FINAL REVIEW]", [
            "• Package the system as a Chrome / Firefox Browser Extension.",
            "• The extension will directly fill the real live government website (voters.eci.gov.in) with 1 click.",
            "• Test on 50 different sample cards with different photo qualities.",
            "• Complete final project report and documentation."
        ], Inches(0.8), Inches(4.25), Inches(11.7), Inches(2.55), DARK)
    ]
    for title, items, l, t, w, h, col in time_cards:
        create_card(s15, l, t, w, h, title, items, title_color=col)

    s15.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Here is our 3-phase plan: Phase 1 is completed—we built the core working prototype for Aadhaar and Form 6. "
        "In Phase 2 for the Mid Review, we will add PAN cards and Driving Licenses, and add green confidence checkmarks. "
        "In Phase 3 for the Final Review, we will turn this into a Chrome Extension that directly fills the live government website with one click.'"
    )

    # ==================== SLIDE 16: CONCLUSION & REFERENCES ====================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Conclusion & References", "SUMMARY")
    
    refs = [
        "1. Election Commission of India (ECI), 'Voter Registration Form 6 Guidelines', eci.gov.in, 2023.",
        "2. Meta AI, 'Llama 3.2: Lightweight Multilingual Models for Edge Devices', 2024.",
        "3. OpenCV Zoo, 'YuNet: Compact Deep Neural Network for Real-Time Face Detection', 2023.",
        "4. Jaided AI, 'EasyOCR: Python Package for Optical Character Recognition', 2023.",
        "5. Project GitHub Repository: https://github.com/deva-2006/govtAutofill"
    ]
    conc = [
        "• Solves a Real Problem: Eliminates boring, error-prone typing for citizens applying for government voter cards.",
        "• Privacy First: Uses local AI and on-device face detection so no private data leaves the laptop.",
        "• High Accuracy: Automatically separates door numbers, picks true Aadhaar numbers, and crops passport photos.",
        "• Proven Working System: Already tested and working; strong base ready for Phase 2 expansion."
    ]
    create_card(s16, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "References Used", refs, badge="References", title_color=DARK)
    create_card(s16, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), "Conclusion & Summary", conc, badge="Conclusion", title_color=GREEN)

    s16.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'In conclusion: our project makes filling government forms fast, simple, and completely private. "
        "We have already built a working system that takes an ID card, reads the text, crops the photo, and fills Form 6 in 20 seconds. "
        "We are ready for Phase 2. Thank you staff, we are happy to answer any questions!'"
    )

    output_filename = "First_Review_UG_Project_Presentation.pptx"
    prs.save(output_filename)
    print(f"Simple presentation successfully updated: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_simple_presentation()
