import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_smart_attendance_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Modern Palette (matching the user's inspiration)
    TOP_BLUE = RGBColor(26, 86, 219)      # #1A56DB
    NAVY_DARK = RGBColor(15, 23, 42)      # #0F172A
    BLUE_PILL_TXT = RGBColor(30, 64, 175) # #1E40AF
    BLUE_PILL_BG = RGBColor(239, 246, 255)# #EFF6FF
    BLUE_PILL_BD = RGBColor(191, 219, 254)# #BFDBFE
    
    TEXT_DARK = RGBColor(30, 41, 59)      # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
    
    CARD_BLUE_BG = RGBColor(240, 247, 255) # Light blue
    CARD_BLUE_BD = RGBColor(191, 219, 254)
    
    CARD_RED_BG = RGBColor(255, 241, 242)  # Light pink/red
    CARD_RED_BD = RGBColor(254, 205, 211)
    
    CARD_GREEN_BG = RGBColor(240, 253, 244)# Light green
    CARD_GREEN_BD = RGBColor(187, 247, 208)
    
    CARD_WHITE_BG = RGBColor(255, 255, 255)
    CARD_WHITE_BD = RGBColor(226, 232, 240)

    def add_top_template(slide, slide_num, total_slides=16, category="B.TECH AI & DATA SCIENCE | FIRST PROJECT REVIEW"):
        # Top blue stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = TOP_BLUE
        stripe.line.fill.background()

        # Category pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.25), Inches(5.4), Inches(0.38))
        pill.fill.solid()
        pill.fill.fore_color.rgb = BLUE_PILL_BG
        pill.line.color.rgb = BLUE_PILL_BD
        pill.line.width = Pt(1)

        ptb = slide.shapes.add_textbox(Inches(0.9), Inches(0.26), Inches(5.2), Inches(0.35))
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

    # ==================== SLIDE 1: TITLE SLIDE ====================
    s1 = prs.slides.add_slide(blank_layout)
    add_top_template(s1, 1, 16, "B.TECH AI & DATA SCIENCE | FIRST PROJECT REVIEW")

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.733), Inches(2.3))
    t_tf = t_box.text_frame
    t_tf.word_wrap = True
    
    tp1 = t_tf.paragraphs[0]
    tp1.text = "SMART ATTENDANCE MONITORING SYSTEM"
    tp1.font.size = Pt(28)
    tp1.font.bold = True
    tp1.font.color.rgb = NAVY_DARK
    tp1.space_after = Pt(8)

    tp2 = t_tf.add_paragraph()
    tp2.text = "An Automated Contactless Face Recognition Attendance Engine using Deep Learning, Real-Time Video Analytics, and Cloud Database Integration"
    tp2.font.size = Pt(14.5)
    tp2.font.color.rgb = TEXT_MUTED

    # Left Card: Project Details
    c_proj = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.8), Inches(5.6), Inches(2.8))
    c_proj.fill.solid()
    c_proj.fill.fore_color.rgb = CARD_BLUE_BG
    c_proj.line.color.rgb = CARD_BLUE_BD
    c_proj.line.width = Pt(1.2)

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
    cp2.text = "Smart Attendance Engine"
    cp2.font.size = Pt(18)
    cp2.font.bold = True
    cp2.font.color.rgb = NAVY_DARK
    cp2.space_after = Pt(6)

    details = [
        "Department of Artificial Intelligence & Data Science",
        "Institution: Rajalakshmi Institute of Technology",
        "Academic Year: 2026–2027",
        "Focus: Zero Proxy, Contactless, High-Speed Classroom Logging"
    ]
    for d in details:
        p = ctf.add_paragraph()
        p.text = "• " + d
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(3)

    # Right Card: Project Member
    c_mem = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.8), Inches(5.733), Inches(2.8))
    c_mem.fill.solid()
    c_mem.fill.fore_color.rgb = CARD_BLUE_BG
    c_mem.line.color.rgb = CARD_BLUE_BD
    c_mem.line.width = Pt(1.2)

    mtb = s1.shapes.add_textbox(Inches(7.05), Inches(4.0), Inches(5.2), Inches(2.4))
    mtf = mtb.text_frame
    mtf.word_wrap = True
    
    mp1 = mtf.paragraphs[0]
    mp1.text = "👤  PROJECT SUBMITTED BY"
    mp1.font.size = Pt(13)
    mp1.font.bold = True
    mp1.font.color.rgb = BLUE_PILL_TXT
    mp1.space_after = Pt(12)

    mp2 = mtf.add_paragraph()
    mp2.text = "DHANUSH M N"
    mp2.font.size = Pt(20)
    mp2.font.bold = True
    mp2.font.color.rgb = NAVY_DARK
    mp2.space_after = Pt(4)

    mp3 = mtf.add_paragraph()
    mp3.text = "Register Number: 2117230070028"
    mp3.font.size = Pt(14)
    mp3.font.bold = True
    mp3.font.color.rgb = TOP_BLUE
    mp3.space_after = Pt(10)

    mp4 = mtf.add_paragraph()
    mp4.text = "B.Tech Artificial Intelligence and Data Science\nFirst Project Review Presentation"
    mp4.font.size = Pt(11.5)
    mp4.font.color.rgb = TEXT_DARK

    s1.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Good morning respected staff and panel members. I am Dhanush M N, Register Number 2117230070028, "
        "from the Department of Artificial Intelligence and Data Science. Today, I am presenting my First Project Review on "
        "'SMART ATTENDANCE MONITORING SYSTEM'. This project automates daily classroom and office attendance using "
        "AI face recognition, eliminating manual roll calls, saving classroom time, and completely preventing proxy attendance.'"
    )

    # ==================== SLIDE 2: TABLE OF CONTENTS ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_top_template(s2, 2, 16)
    add_slide_title(s2, "Table of Contents", "Overview of today's review presentation")

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
        "12. Technical Highlights & Features",
        "13. Expected Outcomes & Impact",
        "14. Project Timeline & Work Plan",
        "15. Conclusion & References"
    ]
    create_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Part 1: The Problem & Background", toc1, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📋")
    create_card(s2, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Part 2: Proposed AI Solution & Results", toc2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🚀")

    s2.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Here is the presentation structure: In Part 1, I explain why traditional attendance methods fail, the background of manual roll calls, "
        "and previous research work. In Part 2, I present my proposed AI face recognition architecture, the tech stack, the prototype results "
        "already achieved, and the next milestones.'"
    )

    # ==================== SLIDE 3: INTRODUCTION ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_top_template(s3, 3, 16)
    add_slide_title(s3, "Introduction: Why Smart Attendance Matters", "Context and motivation behind the project")

    intro_left = [
        "Attendance tracking is mandatory in colleges, universities, schools, and corporate workplaces.",
        "Traditional attendance still depends on manual paper roll calls or queuing up before biometric fingerprint scanners.",
        "In a classroom of 60 students, manual roll call takes 10 to 15 minutes of lecture time every single hour.",
        "Over a semester, hundreds of teaching hours are lost merely marking presence and absence."
    ]
    intro_right = [
        "Our Solution: A Smart AI Attendance system powered by Computer Vision & Deep Learning.",
        "A classroom camera scans students as they enter or sit in class.",
        "The system detects human faces, recognizes enrolled students, and logs attendance automatically into a secure database.",
        "Key Benefits: 100% Contactless, works in seconds, eliminates proxy, and sends instant absent notifications."
    ]
    create_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "The Current Situation in Colleges", intro_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🏫")
    create_card(s3, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Our AI-Powered Vision", intro_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="💡")

    s3.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Staff, in simple terms: Today, teachers spend 10 to 15 minutes in every period calling out roll numbers from an attendance register. "
        "This wastes valuable teaching time. My project replaces manual roll calls with an AI camera system. The camera detects students' "
        "faces automatically, marks their attendance with exact time-stamps in seconds, and updates the college database without anyone touching a device.'"
    )

    # ==================== SLIDE 4: BACKGROUND OF THE PROJECT ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_top_template(s4, 4, 16)
    add_slide_title(s4, "Background: Classroom & Workplace Attendance Realities", "Evolution of attendance tracking mechanisms")

    bg_left = [
        "Paper Registers: The oldest method; highly prone to physical damage, lost register books, and fake signatures.",
        "RFID Smart Cards: Faster than paper, but students easily swap cards with friends, leading to proxy attendance.",
        "Fingerprint Biometrics: Requires physical contact, creates long bottlenecks outside classrooms, and fails on wet/dusty fingers.",
        "Mobile App Check-Ins: Easily bypassed using GPS spoofing apps or sharing OTP codes across WhatsApp."
    ]
    bg_right = [
        "The Need for Contactless Biometrics: Post-pandemic hygiene mandates touchless systems.",
        "Multi-Student Recognition: Modern deep learning models can detect and recognize multiple faces simultaneously in a single camera frame.",
        "Automated Administrative Reporting: Faculty need automated weekly and monthly percentage calculation without manual Excel entry.",
        "Conclusion: Face recognition is the only method that verifies the actual physical presence of the student without physical touch."
    ]
    create_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Legacy Attendance Methods", bg_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📜")
    create_card(s4, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "The Shift to Vision Biometrics", bg_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="👁️")

    s4.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'When we examine how attendance has evolved: Paper registers get damaged, RFID cards can be passed to friends, "
        "and fingerprint scanners form long queues and spread germs. Mobile check-ins are easily fooled by sharing OTPs. "
        "Computer vision face recognition is the best solution because a student cannot give their face to a friend—guaranteeing genuine presence.'"
    )

    # ==================== SLIDE 5: PROBLEM STATEMENT ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_top_template(s5, 5, 16)
    add_slide_title(s5, "Problem Statement: 4 Major Challenges", "Core problems in traditional attendance systems")

    p1 = [
        "Teachers spend 10 to 15 minutes of every 50-minute lecture calling roll numbers.",
        "Accumulates to over 60 wasted instructional hours per semester per class.",
        "Disrupts student attention and lecture flow."
    ]
    p2 = [
        "Friends answer roll calls or scan RFID cards for absent classmates.",
        "Signatures on physical attendance sheets are routinely forged.",
        "Distorts actual attendance percentages required for exam eligibility."
    ]
    p3 = [
        "Fingerprint scanners require one student at a time, causing long entry queues.",
        "High maintenance costs when optical sensors accumulate dust or grease.",
        "Unhygienic during flu and viral outbreak seasons."
    ]
    p4 = [
        "Staff spend hours manually entering attendance from paper registers into Excel/ERP portals.",
        "Parents receive absence notifications days later instead of in real time.",
        "High risk of human data-entry errors when calculating 75% eligibility."
    ]

    create_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Huge Instructional Time Loss", p1, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⏱️")
    create_card(s5, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Rampant Proxy Attendance", p2, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="🚫")
    create_card(s5, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Queue Delays & Hardware Friction", p3, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="⚠️")
    create_card(s5, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Manual Calculation & Late Alerts", p4, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📊")

    s5.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Staff, there are 4 major problems today: 1. Huge time wasted calling roll numbers every hour. 2. Rampant proxy attendance where "
        "friends answer for absent students or swap RFID cards. 3. Long queues and unhygienic fingerprint sensors. 4. Teachers having to "
        "manually calculate attendance percentages in Excel at the end of every month. My smart system solves all four.'"
    )

    # ==================== SLIDE 6: AIM AND OBJECTIVES ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_top_template(s6, 6, 16)
    add_slide_title(s6, "Aim & Specific Objectives", "What the project aims to accomplish")

    aim_items = [
        "To design and develop an automated, contactless, real-time Smart Attendance Monitoring System using deep-learning face recognition that detects multiple students, verifies identity with >= 95% accuracy in under 3 seconds, and automatically logs attendance to a centralized database without human intervention."
    ]
    create_card(s6, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.35), "PROJECT AIM", aim_items, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🎯")

    obj_left = [
        "Objective 1: Multi-Face Detection & Preprocessing",
        "  • Detect multiple human faces in live camera streams using OpenCV & deep learning.",
        "  • Handle variations in lighting, head pose, and facial expressions.",
        "Objective 2: Facial Feature Encoding & Recognition",
        "  • Generate 128-dimensional facial embedding vectors using deep neural models (FaceNet / dlib).",
        "  • Match embeddings against enrolled student database in real time."
    ]
    obj_right = [
        "Objective 3: Anti-Spoofing & Liveness Detection",
        "  • Detect and reject photo prints, phone screens, and video replays to prevent spoofing.",
        "Objective 4: Automated Logging & Faculty Dashboard",
        "  • Automatically record Roll No, Name, Date, and Timestamp into database.",
        "  • Provide a clean web dashboard for teachers with 1-click Excel export and automated SMS/email absent alerts."
    ]
    create_card(s6, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7), "Objectives (1 & 2): Vision & AI Recognition", obj_left, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="👁️")
    create_card(s6, Inches(6.8), Inches(3.1), Inches(5.733), Inches(3.7), "Objectives (3 & 4): Security & Dashboard", obj_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="💻")

    s6.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'My aim is simple: Build a fast, contactless face recognition attendance system that recognizes students with over 95% accuracy "
        "in under 3 seconds. My four objectives are: 1. Detect faces in real-time camera video. 2. Match facial features against student profiles. "
        "3. Add anti-spoofing so students cannot hold up mobile phone photos. 4. Automatically save attendance to a database with a clean teacher dashboard.'"
    )

    # ==================== SLIDE 7: LITERATURE REVIEW ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_top_template(s7, 7, 16)
    add_slide_title(s7, "Literature Review: Comparative Study", "Analysis of existing research and technological approaches")

    lit1 = [
        "Method: Viola-Jones Haar Cascade + Eigenfaces.",
        "Findings: Fast and lightweight on basic hardware.",
        "Drawback: High error rates under poor classroom lighting, tilted head poses, and glasses/masks."
    ]
    lit2 = [
        "Method: Radio Frequency Identification (RFID) card readers.",
        "Findings: Instant card reading with minimal computational cost.",
        "Drawback: Severe proxy issue—students easily carry multiple cards for absent friends."
    ]
    lit3 = [
        "Method: BLE Bluetooth Beacons & WiFi Proximity.",
        "Findings: Connects to students' smartphones automatically.",
        "Drawback: Students leave phones in class while leaving campus; high battery drain on phones."
    ]
    lit4 = [
        "Method: Deep Convolutional Neural Networks (CNN) & FaceNet 128D Embeddings.",
        "Findings: Robust to lighting changes, accessories, and camera angles with >95% accuracy.",
        "Advantage: Contactless, zero proxy, supports multi-person recognition simultaneously."
    ]

    create_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Traditional Haar Cascades", lit1, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📖")
    create_card(s7, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. RFID Hardware Tag Systems", lit2, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="🏷️")
    create_card(s7, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Bluetooth / WiFi Mobile Check-Ins", lit3, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📱")
    create_card(s7, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Deep Learning Face Biometrics (Our Choice)", lit4, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="⭐")

    s7.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'When reviewing previous research: Early methods like Haar Cascades struggled in low classroom lighting. "
        "RFID tags and Bluetooth beacons failed because students can pass cards or phones to friends. "
        "Modern deep learning using FaceNet 128-dimensional embeddings is the gold standard because it handles different lighting, "
        "tilts, and facial expressions while completely stopping proxy attendance.'"
    )

    # ==================== SLIDE 8: EXISTING SYSTEM ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_top_template(s8, 8, 16)
    add_slide_title(s8, "Existing System: How Attendance is Taken Today", "Current classroom and institutional workflows")

    e_left = [
        "Step 1: Faculty enters classroom carrying a physical paper register book.",
        "Step 2: Faculty pauses the lecture and calls out roll numbers 1 through 60 individually.",
        "Step 3: Students respond with 'Present' or 'Here'; faculty marks 'P' or 'A' in the grid.",
        "Step 4: Process takes 10 to 12 minutes every period; repeated 6 to 7 times daily."
    ]
    e_right = [
        "Step 5: Alternatively, students queue outside class at a single biometric wall scanner.",
        "Step 6: Each student presses their thumb onto the glass scanner (takes 4–6 seconds per student).",
        "Step 7: If a fingerprint fails due to sweat or dust, the student retries 3 to 4 times.",
        "Step 8: End of Month: Faculty manually counts marks and types percentages into college ERP portals."
    ]
    create_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Manual Paper Roll Call (Steps 1 to 4)", e_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📝")
    create_card(s8, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Biometric Scanner Bottleneck (Steps 5 to 8)", e_right, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="👆")

    s8.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'In the existing system: Teachers spend the first 10 minutes calling roll numbers 1 by 1. "
        "If fingerprint devices are used, 60 students stand in a long queue, each taking 5 seconds to scan. "
        "At the end of the month, teachers spend hours calculating attendance percentages by hand. It is slow, boring, and error-prone.'"
    )

    # ==================== SLIDE 9: LIMITATIONS OF EXISTING SYSTEM ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_top_template(s9, 9, 16)
    add_slide_title(s9, "Limitations of the Existing System", "Why the current methods are inefficient and flawed")

    lim1 = [
        "Easy for students to shout 'Present' for absent friends.",
        "Forged signatures on physical attendance sheets.",
        "Defeats the purpose of attendance monitoring for college accreditation."
    ]
    lim2 = [
        "10 to 15 minutes lost per period = 1 hour lost every single day.",
        "Reduces teaching coverage for syllabus completion.",
        "Disrupts classroom focus and discussion momentum."
    ]
    lim3 = [
        "Dozens of students touching the exact same fingerprint sensor surface.",
        "Sensors fail on sweaty, dusty, or cold fingers, causing repeated retries.",
        "Hardware repair costs when physical scanners break down."
    ]
    lim4 = [
        "Manual counting leads to calculation errors in 75% eligibility reports.",
        "Parents are not informed when students bunk lectures in real time.",
        "Paper registers are vulnerable to water damage, tears, and misplacement."
    ]

    create_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Rampant Proxy & Forgery", lim1, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="❌")
    create_card(s9, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Severe Instructional Time Loss", lim2, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⏳")
    create_card(s9, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Hardware Jams & Hygiene Risks", lim3, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⚠️")
    create_card(s9, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Human Errors & Delayed Alerts", lim4, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="📊")

    s9.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'To summarize the drawbacks: 1. Proxies and forged signatures. 2. Losing 1 hour of teaching time every day. "
        "3. Unhygienic sensors that jam when fingers are dusty. 4. Calculation mistakes and parents not getting timely alerts. "
        "My smart attendance system fixes all four problems completely.'"
    )

    # ==================== SLIDE 10: PROPOSED SYSTEM ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_top_template(s10, 10, 16)
    add_slide_title(s10, "Proposed System: Automated AI Face Attendance", "Our smart, modern solution")

    prop_left = [
        "1. Contactless Video Scanning: High-definition camera placed at classroom entrance or front podium scans faces seamlessly.",
        "2. Multi-Face Detection: Detects multiple student faces in a single video frame simultaneously.",
        "3. Deep Face Recognition: Generates unique 128-dimensional facial embedding vectors and matches against registered database.",
        "4. High Precision: Achieves over 95% recognition accuracy even with glasses, different hairstyles, and slight head tilts."
    ]
    prop_right = [
        "5. Instant Attendance Logging: Marks student present with exact date and timestamp in less than 2 seconds.",
        "6. Anti-Spoofing Security: Distinguishes live human faces from printed photos or mobile screen replays.",
        "7. Faculty Web Portal: Teachers view real-time live attendance grids with 1-click Excel export.",
        "8. Automated Absentee Alerts: Automatically sends SMS/WhatsApp notifications to parents of absent students."
    ]
    create_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Key Features of Proposed System", prop_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✨")
    create_card(s10, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Speed, Security & Automation", prop_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="⚡")

    s10.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'In my proposed system: A camera captures the students as they enter or sit. In less than 2 seconds, the deep learning model detects "
        "their faces, matches them with the student database, and marks them present with exact timestamps. It has anti-spoofing to stop photo cheating, "
        "provides an instant Excel report for teachers, and automatically messages parents if a student is absent.'"
    )

    # ==================== SLIDE 11: PROPOSED METHODOLOGY / ARCHITECTURE ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_top_template(s11, 11, 16)
    add_slide_title(s11, "Proposed Methodology & System Architecture", "Step-by-step pipeline of the Smart Attendance System")

    step_data = [
        ("STEP 01", "Video Capture", "Classroom HD webcam captures live video frames as students enter.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 02", "Face Detection", "OpenCV / YuNet model locates all human face bounding boxes in frame.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 03", "Face Alignment", "Normalizes eye/nose landmarks, adjusts brightness and rotation.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 04", "Feature Extraction", "Deep CNN model converts facial geometry into 128D embedding vectors.", CARD_GREEN_BG, CARD_GREEN_BD),
        ("STEP 05", "Database Matching", "Compares embeddings with enrolled student vectors using Euclidean distance.", CARD_GREEN_BG, CARD_GREEN_BD),
        ("STEP 06", "Logging & Dashboard", "Updates attendance database instantly and triggers SMS/Excel reports!", CARD_GREEN_BG, CARD_GREEN_BD),
    ]

    col_w = Inches(3.64)
    # Row 1
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

    # Row 2
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
        "'Here is the 6-step architecture: Step 1: Camera captures live video. Step 2: OpenCV detects all faces in the frame. "
        "Step 3: Align and crop face landmarks. Step 4: Convert facial features into 128D mathematical vectors. "
        "Step 5: Compare vectors with student database. Step 6: Log attendance automatically and display it on the faculty portal.'"
    )

    # ==================== SLIDE 12: TOOLS AND TECHNOLOGIES USED ====================
    s12 = prs.slides.add_slide(blank_layout)
    add_top_template(s12, 12, 16)
    add_slide_title(s12, "Tools & Technologies Used", "Hardware, software, and AI libraries chosen")

    t1 = [
        "Python 3.10+: Core programming language.",
        "OpenCV (cv2): Real-time computer vision & video stream handling.",
        "NumPy: High-speed matrix operations and vector math.",
        "Why chosen: Standard industry stack for computer vision applications."
    ]
    t2 = [
        "dlib / FaceNet: Deep metric learning for 128D facial embeddings.",
        "YuNet / Haar Cascade: Fast, lightweight face landmark detection.",
        "Liveness Detection: Anti-spoofing blink and texture verification.",
        "Why chosen: >95% accuracy while running smoothly on standard laptops."
    ]
    t3 = [
        "FastAPI / Flask: High-speed asynchronous Python REST API.",
        "SQLite / PostgreSQL: Structured student records and timestamp logs.",
        "Pandas: Automated Excel report generator (.xlsx / .csv).",
        "Why chosen: Reliable, lightweight, and supports instant data export."
    ]
    t4 = [
        "HTML5, CSS3, JavaScript / React: Responsive faculty web dashboard.",
        "Hardware: Standard 1080p USB Webcam or CCTV IP camera.",
        "Twilio / SMTP: Automated SMS & email notifications for absent alerts.",
        "Why chosen: Low cost, works with existing college computer infrastructure."
    ]

    create_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Core Programming & Vision", t1, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="⚙️")
    create_card(s12, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Deep Learning Face AI", t2, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="🧠")
    create_card(s12, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Backend API & Database", t3, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="💾")
    create_card(s12, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Web Dashboard & Hardware", t4, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="🖥️")

    s12.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'For my tech stack: I used Python and OpenCV for video processing, deep learning FaceNet and dlib for face recognition, "
        "FastAPI and SQLite for saving attendance logs, and a clean web dashboard for teachers with Excel export. "
        "It runs on any standard laptop with a normal USB webcam—no expensive equipment needed.'"
    )

    # ==================== SLIDE 13: WORK COMPLETED SO FAR ====================
    s13 = prs.slides.add_slide(blank_layout)
    add_top_template(s13, 13, 16)
    add_slide_title(s13, "Work Completed So Far (Our Results)", "Phase 1 deliverables and practical prototype achievements")

    r1 = [
        "Connected live webcam video stream with OpenCV.",
        "Detects multiple faces in real-time at 30 frames per second.",
        "Draws bounding boxes and labels around detected faces.",
        "Status: 100% Completed & Verified."
    ]
    r2 = [
        "Built enrollment module: captures 20 image samples per student.",
        "Generated and stored 128D facial feature vectors.",
        "Tested on test student profiles with high similarity confidence.",
        "Status: 100% Completed & Verified."
    ]
    r3 = [
        "System matches live camera faces against database vectors.",
        "Displays student Name and Register Number on screen in real time.",
        "Overcomes minor head rotations and glasses.",
        "Status: 100% Completed & Verified."
    ]
    r4 = [
        "System logs Register No, Name, Date, and Time into SQLite.",
        "Prevents duplicate entries within the same period (debouncing).",
        "Generates clean Excel spreadsheet (.csv) automatically.",
        "Status: 100% Completed & Verified."
    ]

    create_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Live Camera Stream & Detection", r1, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="✅")
    create_card(s13, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Student Dataset & Embedding Generation", r2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="✅")
    create_card(s13, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Real-Time Recognition & Matching", r3, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✅")
    create_card(s13, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Automated Attendance Logging", r4, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✅")

    s13.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'For Review 1, I have already built and tested a functional working prototype! I completed 4 key milestones: "
        "1. Real-time face detection from a webcam at 30 fps. 2. Student dataset creation and 128D facial vector generation. "
        "3. Live recognition displaying student names on screen. 4. Automatic logging into an Excel database while preventing duplicate marks.'"
    )

    # ==================== SLIDE 14: EXPECTED OUTCOMES ====================
    s14 = prs.slides.add_slide(blank_layout)
    add_top_template(s14, 14, 16)
    add_slide_title(s14, "Expected Outcomes: Big Benefits for Institutions", "Measurable quantitative and qualitative impact")

    o1 = [
        "Manual roll call: 10 to 15 minutes per lecture.",
        "Smart Attendance: Complete class marked in under 30 seconds.",
        "Saves over 60 teaching hours per classroom every semester."
    ]
    o2 = [
        "100% elimination of proxy attendance and roll call shouting.",
        "Biometric verification guarantees physical presence.",
        "Accurate attendance records for Anna University / AICTE compliance."
    ]
    o3 = [
        "100% contactless operation—zero touch of physical biometric hardware.",
        "Zero queue buildup outside class doors.",
        "Maintains high hygiene standards during viral seasons."
    ]
    o4 = [
        "Faculty views live attendance percentages with 1-click reports.",
        "Automated alerts sent to parents of absent students.",
        "Directly integrates with college management ERP software."
    ]

    create_card(s14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. 95% Time Savings for Teachers", o1, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="⚡")
    create_card(s14, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Zero Proxy & Fake Attendance", o2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🎯")
    create_card(s14, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. 100% Contactless & Clean", o3, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🔒")
    create_card(s14, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Automated Parent SMS & ERP Sync", o4, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📊")

    s14.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'The expected benefits are: 1. 95% time saved—taking attendance in 30 seconds instead of 15 minutes. "
        "2. Zero proxy attendance. 3. 100% contactless and hygienic. 4. Automatic Excel reporting and instant SMS messages to parents.'"
    )

    # ==================== SLIDE 15: PROJECT TIMELINE ====================
    s15 = prs.slides.add_slide(blank_layout)
    add_top_template(s15, 15, 16)
    add_slide_title(s15, "Project Timeline & Work Plan", "Roadmap across the three review stages")

    tm1 = [
        "Literature review on face recognition algorithms.",
        "Real-time webcam integration with OpenCV.",
        "Dataset creation & 128D facial vector generation.",
        "Core recognition & SQLite logging prototype.",
        "Current Status: Working prototype demonstrated in Review 1."
    ]
    tm2 = [
        "Implement anti-spoofing (eye-blink and liveness detection).",
        "Build Faculty Web Dashboard with attendance analytics.",
        "Add automated absentee SMS / Email notification module.",
        "Test with 50+ students under varied lighting conditions."
    ]
    tm3 = [
        "Optimize multi-face detection speed using GPU acceleration.",
        "Integrate with college ERP / database management systems.",
        "Benchmark accuracy metrics (Precision, Recall, F1-Score).",
        "Final thesis preparation and project demonstration."
    ]

    create_card(s15, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "Phase 1: Working Prototype [DONE]", tm1, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🏁")
    create_card(s15, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "Phase 2: Anti-Spoofing & Web Dashboard [MID REVIEW]", tm2, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🚀")
    create_card(s15, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.55), "Phase 3: ERP Integration & Final Benchmarking [FINAL REVIEW]", tm3, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="🌐")

    s15.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'Here is my 3-phase plan: Phase 1 is completed—I built the face recognition and automated logging prototype. "
        "In Phase 2 for the Mid Review, I will add anti-spoofing to prevent photo cheating and build the teacher web portal. "
        "In Phase 3 for the Final Review, I will optimize it for 50+ students simultaneously and connect it to college ERP systems.'"
    )

    # ==================== SLIDE 16: CONCLUSION & REFERENCES ====================
    s16 = prs.slides.add_slide(blank_layout)
    add_top_template(s16, 16, 16)
    add_slide_title(s16, "Conclusion & References", "Summary of our work")

    ref_items = [
        "1. F. Schroff, D. Kalenichenko, and J. Philbin, 'FaceNet: A Unified Embedding for Face Recognition and Clustering,' CVPR, 2015.",
        "2. OpenCV Computer Vision Library, 'Real-Time Face Detection and Feature Extraction,' 2023.",
        "3. D. E. King, 'Dlib-ml: A Machine Learning Toolkit,' Journal of Machine Learning Research, 2009.",
        "4. IEEE Access, 'Automated Attendance System using Computer Vision and Deep Learning,' 2023.",
        "5. Project GitHub Repository: https://github.com/dhanush-2006/smart-attendance"
    ]
    conc_items = [
        "Eliminates Manual Inefficiency: Replaces 15-minute roll calls with automated 2-second face recognition.",
        "Stops Proxy Attendance: Contactless biometric verification ensures 100% genuine presence.",
        "Affordable & Scalable: Works with standard webcams and laptops without costly proprietary hardware.",
        "Ready for Phase 2: Core AI engine is verified and working; ready for dashboard and anti-spoofing expansion."
    ]

    create_card(s16, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Key Academic References", ref_items, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📚")
    create_card(s16, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Concluding Summary", conc_items, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🏆")

    s16.notes_slide.notes_text_frame.text = (
        "SIMPLE EXPLANATION FOR STAFF:\n"
        "'In conclusion: The Smart Attendance Monitoring System saves time, stops proxy attendance, and automates daily reporting "
        "using deep learning face recognition. I have already built and verified the working prototype for Phase 1. "
        "Thank you respected staff and panel members, I am ready for your questions and guidance!'"
    )

    output_filename = "SMART_ATTENDANCE_MONITORING.pptx"
    prs.save(output_filename)
    print(f"Presentation successfully created: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_smart_attendance_presentation()
