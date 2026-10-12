import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_clearpath_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Exact Inspiration Color Palette
    TOP_BLUE = RGBColor(26, 86, 219)       # #1A56DB Vibrant Blue Stripe
    NAVY_DARK = RGBColor(15, 23, 42)       # #0F172A Primary Headings
    BLUE_PILL_TXT = RGBColor(30, 64, 175)  # #1E40AF Capsule Text
    BLUE_PILL_BG = RGBColor(239, 246, 255) # #EFF6FF Capsule Fill
    BLUE_PILL_BD = RGBColor(191, 219, 254) # #BFDBFE Capsule Border
    
    TEXT_DARK = RGBColor(30, 41, 59)       # #1E293B Body Text
    TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B Secondary Text
    
    CARD_BLUE_BG = RGBColor(240, 247, 255) # #F0F7FF Soft Blue Card
    CARD_BLUE_BD = RGBColor(191, 219, 254)
    
    CARD_RED_BG = RGBColor(255, 241, 242)  # #FFF1F2 Soft Red Card (Problems/Limits)
    CARD_RED_BD = RGBColor(254, 205, 211)
    
    CARD_GREEN_BG = RGBColor(240, 253, 244)# #F0FDF4 Soft Green Card (Outcomes/Success)
    CARD_GREEN_BD = RGBColor(187, 247, 208)
    
    CARD_WHITE_BG = RGBColor(255, 255, 255)
    CARD_WHITE_BD = RGBColor(226, 232, 240)
    TABLE_HEADER_BG = RGBColor(239, 246, 255)

    def add_top_bar(slide, slide_num, total_slides=16, category="B.TECH ARTIFICIAL INTELLIGENCE & DATA SCIENCE | FIRST REVIEW"):
        # Top Blue Line
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = TOP_BLUE
        stripe.line.fill.background()

        # Capsule Tag on Top-Left
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.24), Inches(6.2), Inches(0.38))
        pill.fill.solid()
        pill.fill.fore_color.rgb = BLUE_PILL_BG
        pill.line.color.rgb = BLUE_PILL_BD
        pill.line.width = Pt(1)

        ptb = slide.shapes.add_textbox(Inches(0.9), Inches(0.25), Inches(6.0), Inches(0.35))
        ptf = ptb.text_frame
        ptf.word_wrap = True
        pp = ptf.paragraphs[0]
        pp.text = category
        pp.font.size = Pt(10.5)
        pp.font.bold = True
        pp.font.color.rgb = BLUE_PILL_TXT

        # Slide Number on Top-Right
        snum_box = slide.shapes.add_textbox(Inches(10.8), Inches(0.24), Inches(1.8), Inches(0.35))
        stf = snum_box.text_frame
        sp = stf.paragraphs[0]
        sp.alignment = PP_ALIGN.RIGHT
        sp.text = f"Slide {slide_num} of {total_slides}"
        sp.font.size = Pt(11)
        sp.font.bold = True
        sp.font.color.rgb = TEXT_MUTED

    def add_header(slide, title_text, subtitle_text=""):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.70), Inches(11.733), Inches(0.8))
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
    add_top_bar(s1, 1, 16, "B.TECH AI & DATA SCIENCE | FINAL YEAR PROJECT FIRST REVIEW")

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.733), Inches(2.3))
    t_tf = t_box.text_frame
    t_tf.word_wrap = True
    
    tp1 = t_tf.paragraphs[0]
    tp1.text = "CLEARPATH AI: AI Based Accident Detection and Traffic Diversion System"
    tp1.font.size = Pt(26)
    tp1.font.bold = True
    tp1.font.color.rgb = NAVY_DARK
    tp1.space_after = Pt(8)

    tp2 = t_tf.add_paragraph()
    tp2.text = "Detecting Road Accidents from CCTV Footage, Inferring Incidents via Nearby Cameras, and Recommending Real-Time Alternative Routes"
    tp2.font.size = Pt(14)
    tp2.font.color.rgb = TEXT_MUTED

    # Bottom Two Inspiration Cards
    # Left Card: Institution & Dept
    c_inst = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.75), Inches(5.6), Inches(2.9))
    c_inst.fill.solid()
    c_inst.fill.fore_color.rgb = CARD_BLUE_BG
    c_inst.line.color.rgb = CARD_BLUE_BD
    c_inst.line.width = Pt(1.2)

    itb = s1.shapes.add_textbox(Inches(1.05), Inches(3.95), Inches(5.1), Inches(2.5))
    itf = itb.text_frame
    itf.word_wrap = True
    
    ip1 = itf.paragraphs[0]
    ip1.text = "🎓  INSTITUTION DETAILS"
    ip1.font.size = Pt(13)
    ip1.font.bold = True
    ip1.font.color.rgb = BLUE_PILL_TXT
    ip1.space_after = Pt(8)

    ip2 = itf.add_paragraph()
    ip2.text = "Rajalakshmi Institute of Technology"
    ip2.font.size = Pt(17)
    ip2.font.bold = True
    ip2.font.color.rgb = NAVY_DARK
    ip2.space_after = Pt(6)

    inst_items = [
        "Department of Artificial Intelligence and Data Science",
        "Degree: B.Tech. AI & Data Science",
        "Academic Year: 2026–2027",
        "Stage: Undergraduate Project Review - I"
    ]
    for it in inst_items:
        p = itf.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(3)

    # Right Card: Team Members with Registration Numbers
    c_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.75), Inches(5.733), Inches(2.9))
    c_team.fill.solid()
    c_team.fill.fore_color.rgb = CARD_BLUE_BG
    c_team.line.color.rgb = CARD_BLUE_BD
    c_team.line.width = Pt(1.2)

    ttb = s1.shapes.add_textbox(Inches(7.05), Inches(3.95), Inches(5.2), Inches(2.5))
    ttf = ttb.text_frame
    ttf.word_wrap = True
    
    tp_team = ttf.paragraphs[0]
    tp_team.text = "👥  PROJECT MEMBERS"
    tp_team.font.size = Pt(13)
    tp_team.font.bold = True
    tp_team.font.color.rgb = BLUE_PILL_TXT
    tp_team.space_after = Pt(10)

    members = [
        ("Afrin Reshma C", "2117230070006"),
        ("Akshay A", "2117230070009"),
        ("Devadharshini R", "2117230070026")
    ]
    for name, regno in members:
        p = ttf.add_paragraph()
        p.text = f"{name}   ({regno})"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p.space_after = Pt(8)

    s1.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 1):\n"
        "Good morning respected evaluators and staff. We are Afrin Reshma, Akshay, and Devadharshini from the "
        "Department of Artificial Intelligence and Data Science, Rajalakshmi Institute of Technology. "
        "Today, we are presenting our First Review on the project: 'CLEARPATH AI – AI Based Accident Detection and "
        "Traffic Diversion System'. Our goal is to detect road accidents automatically from CCTV feeds, infer incidents "
        "from nearby cameras when direct video is absent, and guide drivers to alternative routes before they get stuck in traffic."
    )

    # ==================== SLIDE 2: TABLE OF CONTENTS ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_top_bar(s2, 2, 16)
    add_header(s2, "Table of Contents", "Presentation outline and agenda")

    toc_col1 = [
        "1. Introduction",
        "2. Background of the Project",
        "3. Problem Statement",
        "4. Aim and Objectives",
        "5. Literature Review",
        "6. Existing System",
        "7. Limitations of Existing System"
    ]
    toc_col2 = [
        "8. Proposed System",
        "9. Proposed Methodology / Architecture",
        "10. Tools and Technologies Used",
        "11. Work Completed So Far",
        "12. Expected Outcomes",
        "13. Project Timeline and Work Plan",
        "14. References and Conclusion"
    ]
    create_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Part 1: Problem & Existing Work", toc_col1, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📋")
    create_card(s2, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Part 2: Proposed Solution & Roadmap", toc_col2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🚀")

    s2.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 2):\n"
        "Here is our agenda for today. First, we outline the road safety context, project background, problem statement, "
        "aim and objectives, literature study, and limitations of existing traffic setups. Second, we explain our proposed "
        "CLEARPATH AI system, architecture, technology stack, initial progress, timeline, and conclusion."
    )

    # ==================== SLIDE 3: INTRODUCTION ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_top_bar(s3, 3, 16)
    add_header(s3, "1. Introduction", "Overview of road accident delays and AI-driven solutions")

    intro_left = [
        "Road accidents are a major cause of sudden traffic congestion, emergency delays, and increased road safety risks in urban areas.",
        "Traditional traffic monitoring systems rely on manual calls or slow human reporting, failing to alert approaching drivers in time.",
        "When an accident happens, incoming drivers continue towards the affected road without knowing about the blockage, worsening the jam."
    ]
    intro_right = [
        "Artificial Intelligence and Computer Vision can analyze CCTV footage automatically to detect road accidents in real time.",
        "CLEARPATH AI aims to detect accidents, evaluate nearby road traffic conditions, and compute alternative routes.",
        "The system sends early diversion alerts to drivers through a mobile app so they can divert before reaching the accident site."
    ]
    create_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "The Urban Traffic Problem", intro_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🚗")
    create_card(s3, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "The CLEARPATH AI Solution", intro_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="💡")

    s3.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 3):\n"
        "To introduce our project: When an accident occurs on an urban road, it often takes 15 to 30 minutes before emergency services "
        "and traffic police are notified. In that time, hundreds of vehicles enter the road, causing heavy gridlock. "
        "CLEARPATH AI uses Computer Vision on CCTV footage to automatically detect crashes, assess traffic, and immediately recommend "
        "alternative routes to drivers on a mobile app."
    )

    # ==================== SLIDE 4: BACKGROUND OF THE PROJECT ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_top_bar(s4, 4, 16)
    add_header(s4, "2. Background of the Project", "Current CCTV monitoring infrastructure and gaps")

    bg_left = [
        "CCTV cameras are now widely installed across city intersections and highways to monitor vehicle flow.",
        "Modern deep learning vision models like YOLO can detect vehicles, recognize abnormal collisions, and monitor road density.",
        "However, existing smart city systems mainly focus on passive video recording, vehicle counting, or static incident alerts."
    ]
    bg_right = [
        "Traffic congestion quickly builds up because drivers continue driving into the accident zone without diversion advice.",
        "An intelligent system must combine automated accident detection with active traffic analysis and dynamic route recommendations.",
        "Key Innovation: CLEARPATH AI also proposes analyzing nearby CCTV cameras to infer possible incidents even when direct camera footage is unavailable."
    ]
    create_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "CCTV Vision & Monitoring", bg_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📹")
    create_card(s4, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Need for Unified Diversion", bg_right, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🔄")

    s4.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 4):\n"
        "Looking at the background: Cities have thousands of CCTV cameras, but they are used mostly for recording or post-incident review. "
        "Moreover, cameras are not available on every single corner. If an accident occurs in a blind spot, nearby cameras show abnormal traffic "
        "stopping suddenly. CLEARPATH AI is designed to use both direct crash detection and nearby-camera traffic inference to trigger re-routing."
    )

    # ==================== SLIDE 5: PROBLEM STATEMENT ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_top_bar(s5, 5, 16)
    add_header(s5, "3. Problem Statement", "Major pain points and formal problem definition")

    prob_items = [
        "Late Accident Detection: Crashes are detected late, causing massive delays and slowing emergency responses.",
        "Delayed Driver Information: Commuters receive accident alerts only after already entering the blocked corridor.",
        "Incomplete Camera Coverage: CCTV cameras are not installed at every blind spot or accident-prone stretch.",
        "Lack of Nearby-Camera Inference: Existing systems fail to detect incidents by analyzing abnormal stoppages from adjacent cameras.",
        "Missing Automatic Re-Routing: Standard monitoring systems post warnings but fail to suggest feasible alternate routes."
    ]
    create_card(s5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(2.7), "Identified Pain Points", prob_items, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⚠️")

    prob_def = [
        "To develop an AI-based accident detection and traffic diversion system that detects road accidents using CCTV footage, identifies possible incidents through nearby-camera traffic analysis, and provides early alerts with automated alternative-route recommendations."
    ]
    create_card(s5, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.3), "Problem Definition", prob_def, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, title_col=NAVY_DARK, icon_text="🎯")

    s5.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 5):\n"
        "Our problem statement highlights five major issues: delayed accident detection, alerts arriving after entering the jam, "
        "camera blind spots, lack of indirect inference, and no automatic re-routing. Therefore, our formal definition is to build an "
        "end-to-end AI platform that detects accidents, infers blind-spot events from neighboring cameras, and automatically pushes "
        "alternative routes to drivers."
    )

    # ==================== SLIDE 6: AIM AND OBJECTIVES ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_top_bar(s6, 6, 16)
    add_header(s6, "4. Aim and Objectives", "Primary goal and key measurable technical objectives")

    aim_items = [
        "To develop an intelligent AI-based system for detecting road accidents, monitoring traffic congestion, and recommending alternative routes to approaching drivers."
    ]
    create_card(s6, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.35), "AIM OF THE PROJECT", aim_items, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🎯")

    obj_left = [
        "Detect road accidents automatically using CCTV footage and computer vision.",
        "Monitor vehicle movement and analyze real-time traffic density.",
        "Identify possible incidents using abnormal traffic patterns from nearby cameras.",
        "Determine the exact accident location and identify the affected road segment."
    ]
    obj_right = [
        "Generate alternative routes using road-network information and routing algorithms.",
        "Send early accident notifications through a cross-platform mobile application.",
        "Develop an interactive admin dashboard for traffic authorities to monitor incidents and alerts.",
        "Evaluate system efficiency in reducing travel delays and congestion."
    ]
    create_card(s6, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7), "Detection & Inference Objectives", obj_left, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="🔍")
    create_card(s6, Inches(6.8), Inches(3.1), Inches(5.733), Inches(3.7), "Routing & Notification Objectives", obj_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="📱")

    s6.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 6):\n"
        "Our primary aim is to detect accidents, monitor congestion, and re-route drivers. We have divided our work into specific objectives: "
        "First, automatic accident detection using computer vision. Second, traffic density analysis. Third, nearby camera pattern inference. "
        "Fourth, road mapping. Fifth, routing with Dijkstra or A*. Sixth, mobile alerts via Flutter. And seventh, an admin dashboard."
    )

    # ==================== SLIDE 7: LITERATURE REVIEW (TABLE) ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_top_bar(s7, 7, 16)
    add_header(s7, "5. Literature Review", "Analysis of recent research papers and identified research gap")

    # Table layout
    table_shape = s7.shapes.add_table(4, 3, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.8))
    table = table_shape.table
    table.columns[0].width = Inches(3.8)
    table.columns[1].width = Inches(4.0)
    table.columns[2].width = Inches(3.933)

    headers = ["Research Paper", "Methodology", "Research Gap Relevant to Our Project"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TABLE_HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

    rows_data = [
        ("Real-Time Event-Driven Road Traffic Monitoring System Using CCTV Video Analytics\n(IEEE Access, 2023)",
         "Uses deep learning and CCTV video analytics for traffic-event detection and density estimation.",
         "Does not focus on automatic traffic diversion or driver route recommendations."),
        ("Passable: An Intelligent Traffic Light System with Integrated Incident Detection and Vehicle Alerting\n(MDPI Sensors, 2025)",
         "Integrates accident detection, congestion monitoring, adaptive traffic signals, and driver alerts.",
         "Does not primarily provide accident-triggered alternative-route calculation to bypass blocked roads."),
        ("Deep Learning System for Vehicular Re-Routing and Congestion Avoidance\n(MDPI Applied Sciences, 2019)",
         "Uses deep learning for congestion prediction and alternative-route generation.",
         "Does not integrate CCTV-based accident detection as its main operational feature.")
    ]

    for row_idx, r_data in enumerate(rows_data):
        for col_idx, val in enumerate(r_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_WHITE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_DARK

    gap_text = [
        "Research Gap: Existing literature addresses either CCTV accident detection OR vehicular re-routing as separate systems. CLEARPATH AI bridges this gap by integrating CCTV accident detection, nearby-camera incident inference, and automatic traffic diversion with real-time driver mobile alerts."
    ]
    create_card(s7, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.2), "Identified Research Gap", gap_text, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="⭐")

    s7.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 7):\n"
        "We surveyed three recent, high-impact papers from IEEE Access and MDPI. The 2023 IEEE paper detects traffic events from CCTV "
        "but provides no re-routing. The 2025 MDPI paper focuses on adaptive traffic lights without alternative road calculation. "
        "The 2019 MDPI paper computes vehicle re-routing but lacks CCTV accident vision. Our research gap is combining all three into a single system."
    )

    # ==================== SLIDE 8: EXISTING SYSTEM ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_top_bar(s8, 8, 16)
    add_header(s8, "6. Existing System", "Current traffic management approaches and monitoring tools")

    ex_left = [
        "CCTV Infrastructure: Traffic control rooms monitor vehicle movement using stationary surveillance cameras.",
        "Computer Vision for Counting: Standard deep learning models perform vehicle counting, speed estimation, and lane tracking.",
        "Incident Logging: When an accident is manually observed by operators, an incident log is created in the traffic center."
    ]
    ex_right = [
        "Adaptive Traffic Signals: Some smart traffic systems adjust green-light timing at junctions based on congestion levels.",
        "Passive Notifications: Variable Message Signs (VMS boards) or radio announcements provide general traffic updates.",
        "Fragmented Solutions: Accident detection, density calculation, and GPS navigation apps function as completely separate, disconnected tools."
    ]
    create_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Monitoring & Surveillance Tools", ex_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📹")
    create_card(s8, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Signal Control & Notification", ex_right, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🚦")

    s8.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 8):\n"
        "In the existing system, city authorities monitor CCTV screens manually or use basic vehicle-counting vision models. "
        "Traffic signal timings may adjust slightly, and message boards display general delays. However, accident detection and GPS re-routing "
        "exist as completely separate islands with no real-time automated connection."
    )

    # ==================== SLIDE 9: LIMITATIONS OF EXISTING SYSTEM ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_top_bar(s9, 9, 16)
    add_header(s9, "7. Limitations of the Existing System", "Critical bottlenecks and operational weaknesses")

    l1 = [
        "Accident detection strictly depends on having direct CCTV camera coverage.",
        "If a crash happens 200 meters away from a camera, the system is completely blind."
    ]
    l2 = [
        "Existing systems cannot identify incidents by observing sudden stoppages on adjacent cameras.",
        "Blind-spot accidents go unnoticed until long traffic queues form."
    ]
    l3 = [
        "Alerts reach drivers too late—typically after they have already joined the stationary traffic jam.",
        "Radio broadcasts and roadside boards are too generic for targeted commuter navigation."
    ]
    l4 = [
        "Alerts warn of an accident but do not calculate a suitable, unblocked alternative route.",
        "Adjacent road congestion is ignored during diversions, causing secondary gridlocks."
    ]

    create_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Direct Coverage Dependency", l1, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="❌")
    create_card(s9, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Blind-Spot Blindness", l2, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="❌")
    create_card(s9, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. Delayed Driver Notifications", l3, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⏳")
    create_card(s9, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Lack of Integrated Re-Routing", l4, bg_col=CARD_RED_BG, bd_col=CARD_RED_BD, icon_text="⚠️")

    s9.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 9):\n"
        "Here are the four limitations: First, 100% dependency on direct camera visibility. Second, blind-spot failures where indirect "
        "patterns are ignored. Third, alerts reaching drivers far too late. And fourth, notifying drivers without offering a smart, computed alternative route."
    )

    # ==================== SLIDE 10: PROPOSED SYSTEM ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_top_bar(s10, 10, 16)
    add_header(s10, "8. Proposed System: CLEARPATH AI", "Key capabilities and proposed innovations")

    p_left = [
        "AI-Powered Vision: CLEARPATH AI processes CCTV feeds using OpenCV and YOLOv11 for vehicle and accident detection.",
        "Congestion Monitoring: Analyzes vehicle movement and flow rate to detect sudden, abnormal traffic density spikes.",
        "Nearby-Camera Inference: When an accident occurs away from direct camera views, neighboring camera data is analyzed to infer the incident.",
        "Accident Location Mapping: Automatically maps the detected crash to the specific street and road network segment."
    ]
    p_right = [
        "Dynamic Alternative Routing: Calculates the optimal alternative route around the accident using Dijkstra or A* algorithms.",
        "Mobile App Guidance: Pushes instant notifications and turn-by-turn diversion routes to approaching drivers via Flutter app.",
        "Admin Monitoring Dashboard: Provides traffic authorities with a centralized live map of incidents, traffic levels, and active diversions.",
        "Proactive Traffic Relief: Diverts traffic before congestion accumulates, reducing delay times and improving overall road safety."
    ]
    create_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Computer Vision & Incident Inference", p_left, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🤖")
    create_card(s10, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), "Routing, Mobile Alerts & Dashboard", p_right, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="📱")

    s10.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 10):\n"
        "CLEARPATH AI solves these limitations with an integrated platform: YOLOv11 detects collisions; nearby cameras detect congestion "
        "spikes when direct views are missing; routing algorithms calculate alternative roads; and our Flutter app alerts approaching drivers "
        "in real time while traffic police monitor the situation on an admin dashboard."
    )

    # ==================== SLIDE 11: PROPOSED METHODOLOGY / ARCHITECTURE ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_top_bar(s11, 11, 16)
    add_header(s11, "9. Proposed Methodology & System Architecture", "End-to-end pipeline from video feed to mobile re-routing")

    # Workflow Step Cards in 2 Rows (like user's Slide 5 inspiration)
    wf_steps = [
        ("STEP 01", "CCTV Video Ingestion", "Capture live or recorded traffic video streams.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 02", "OpenCV Video Processing", "Extract and preprocess video frames for AI analysis.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 03", "YOLOv11 Detection", "Detect vehicles, collisions, and stopped traffic.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 04", "Incident Confirmation", "Confirm accident and map coordinates to road network.", CARD_GREEN_BG, CARD_GREEN_BD),
        ("STEP 05", "Nearby-Camera Analysis", "Assess adjacent camera flow for congestion inference.", CARD_GREEN_BG, CARD_GREEN_BD),
        ("STEP 06", "Dijkstra / A* Routing", "Compute alternative diversion routes for approaching traffic.", CARD_GREEN_BG, CARD_GREEN_BD),
        ("STEP 07", "Driver Mobile Alerts", "Push early notifications and maps via Flutter app.", CARD_BLUE_BG, CARD_BLUE_BD),
        ("STEP 08", "Admin Dashboard", "Log incident in Firebase and display status on monitor.", CARD_BLUE_BG, CARD_BLUE_BD),
    ]

    col_w = Inches(2.78)
    # Row 1: Steps 1 to 4
    for i in range(4):
        s_num, s_title, s_desc, bg_c, bd_c = wf_steps[i]
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.98), Inches(1.6), col_w, Inches(2.5))
        c.fill.solid()
        c.fill.fore_color.rgb = bg_c
        c.line.color.rgb = bd_c
        c.line.width = Pt(1.2)

        tb = s11.shapes.add_textbox(Inches(0.9 + i * 2.98), Inches(1.75), col_w - Inches(0.2), Inches(2.2))
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
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = NAVY_DARK
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = s_desc
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = TEXT_DARK

    # Row 2: Steps 5 to 8
    for i in range(4):
        s_num, s_title, s_desc, bg_c, bd_c = wf_steps[i + 4]
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.98), Inches(4.3), col_w, Inches(2.5))
        c.fill.solid()
        c.fill.fore_color.rgb = bg_c
        c.line.color.rgb = bd_c
        c.line.width = Pt(1.2)

        tb = s11.shapes.add_textbox(Inches(0.9 + i * 2.98), Inches(4.45), col_w - Inches(0.2), Inches(2.2))
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
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = NAVY_DARK
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = s_desc
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = TEXT_DARK

    s11.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 11):\n"
        "Here is the 8-step methodology of our architecture: 1. Video ingestion from CCTV. 2. Frame processing in OpenCV. "
        "3. YOLOv11 accident and vehicle detection. 4. Location mapping. 5. Neighboring camera traffic analysis. "
        "6. Re-routing using Dijkstra or A*. 7. Pushing alerts to the Flutter mobile app. 8. Real-time logging on the admin dashboard."
    )

    # ==================== SLIDE 12: TOOLS AND TECHNOLOGIES USED (TABLE) ====================
    s12 = prs.slides.add_slide(blank_layout)
    add_top_bar(s12, 12, 16)
    add_header(s12, "10. Tools and Technologies Used", "Technology choices and their specific operational purpose")

    table_shape12 = s12.shapes.add_table(10, 2, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
    t12 = table_shape12.table
    t12.columns[0].width = Inches(3.5)
    t12.columns[1].width = Inches(8.233)

    cell_h0 = t12.cell(0, 0)
    cell_h0.fill.solid()
    cell_h0.fill.fore_color.rgb = TABLE_HEADER_BG
    p = cell_h0.text_frame.paragraphs[0]
    p.text = "Technology / Tool"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    cell_h1 = t12.cell(0, 1)
    cell_h1.fill.solid()
    cell_h1.fill.fore_color.rgb = TABLE_HEADER_BG
    p = cell_h1.text_frame.paragraphs[0]
    p.text = "Purpose & Operational Role in CLEARPATH AI"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    tech_data = [
        ("Python", "Core programming language for AI model training, logic, and backend processing."),
        ("OpenCV", "CCTV video stream decoding, frame extraction, and visual preprocessing."),
        ("YOLOv11", "State-of-the-art object detection model for vehicle tracking and accident classification."),
        ("FastAPI", "High-performance asynchronous backend framework for microservices and API endpoints."),
        ("Flutter", "Cross-platform mobile application development for driver navigation and alert screens."),
        ("Firebase", "Real-time NoSQL database to store active accident locations and road congestion data."),
        ("Google Maps API", "Road network mapping, geocoding, and interactive turn-by-turn navigation overlay."),
        ("Firebase Cloud Messaging (FCM)", "Instant push notifications sent to approaching drivers' mobile phones."),
        ("Dijkstra / A* Algorithm", "Graph-based routing algorithms for calculating optimal alternative bypass routes.")
    ]

    for r_idx, (t_name, t_purp) in enumerate(tech_data):
        c0 = t12.cell(r_idx + 1, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = CARD_WHITE_BG
        p = c0.text_frame.paragraphs[0]
        p.text = t_name
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TOP_BLUE

        c1 = t12.cell(r_idx + 1, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = CARD_WHITE_BG
        p = c1.text_frame.paragraphs[0]
        p.text = t_purp
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    s12.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 12):\n"
        "Here is our complete technology stack: Python and OpenCV handle video processing; YOLOv11 performs accident detection; "
        "FastAPI coordinates the backend; Dijkstra/A* compute alternative paths; Google Maps API and Flutter present the navigation "
        "to drivers; and Firebase handles live data and cloud messaging."
    )

    # ==================== SLIDE 13: WORK COMPLETED SO FAR ====================
    s13 = prs.slides.add_slide(blank_layout)
    add_top_bar(s13, 13, 16)
    add_header(s13, "11. Work Completed So Far", "Initial project milestones achieved during Phase 1")

    w1 = [
        "Finalized project title: CLEARPATH AI.",
        "Formulated the core problem statement and research scope.",
        "Defined 7 specific project objectives covering detection, routing, and mobile notification."
    ]
    w2 = [
        "Conducted literature survey analyzing recent IEEE Access (2023) and MDPI (2025, 2019) research papers.",
        "Identified the specific research gap in combining CCTV vision with dynamic traffic diversion."
    ]
    w3 = [
        "Prepared the complete 8-step system architecture and dataflow pipeline.",
        "Finalized the multi-camera inference strategy for blind-spot accident detection."
    ]
    w4 = [
        "Selected tools and libraries: YOLOv11, OpenCV, FastAPI, Flutter, Firebase, and Dijkstra/A*.",
        "Current Status: Project planning and architectural design completed at Review 1. Model training and app integration are next."
    ]

    create_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "1. Title & Problem Definition", w1, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="✅")
    create_card(s13, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "2. Literature Review & Gap", w2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="✅")
    create_card(s13, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "3. System Architecture Design", w3, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✅")
    create_card(s13, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "4. Technology Selection & Status", w4, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="✅")

    s13.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 13):\n"
        "At this First Review stage, we have finalized the project title, problem statement, and objectives; completed the IEEE and MDPI "
        "literature review; designed the 8-step system architecture; and selected our technology stack. System design and planning are complete, "
        "and we are now ready for model training and implementation in Phase 2."
    )

    # ==================== SLIDE 14: EXPECTED OUTCOMES ====================
    s14 = prs.slides.add_slide(blank_layout)
    add_top_bar(s14, 14, 16)
    add_header(s14, "12. Expected Outcomes", "Target capabilities and real-world system deliverables")

    o1 = [
        "Automatic detection of road accidents from CCTV video feeds.",
        "Continuous traffic congestion monitoring through vehicle movement analysis.",
        "Identification of possible blind-spot incidents using abnormal traffic patterns on nearby cameras."
    ]
    o2 = [
        "Early accident notifications delivered directly to approaching drivers before entering congested zones.",
        "Automated alternative-route recommendations generated to bypass the affected road segment."
    ]
    o3 = [
        "User-friendly Flutter mobile application displaying live accident alerts and interactive diversion maps.",
        "Centralized web-based admin dashboard for traffic authorities to monitor accidents, roads, and active alerts."
    ]
    o4 = [
        "Measurable reduction in urban traffic congestion and vehicle delay times.",
        "Faster emergency response coordination and improved overall commuter safety, subject to testing."
    ]

    create_card(s14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55), "AI Vision & Incident Inference", o1, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="👁️")
    create_card(s14, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55), "Dynamic Re-Routing & Alerts", o2, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🗺️")
    create_card(s14, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.55), "Mobile App & Admin Dashboard", o3, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="📱")
    create_card(s14, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.55), "Traffic & Safety Benefits", o4, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="🚦")

    s14.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 14):\n"
        "Our expected outcomes are: automatic accident detection from CCTV; nearby-camera blind spot inference; early mobile notifications; "
        "automatic alternative route calculation; a Flutter driver application; an admin monitoring dashboard; and significant reductions "
        "in urban traffic delay times."
    )

    # ==================== SLIDE 15: PROJECT TIMELINE AND WORK PLAN (TABLE) ====================
    s15 = prs.slides.add_slide(blank_layout)
    add_top_bar(s15, 15, 16)
    add_header(s15, "13. Project Timeline and Work Plan", "Phase breakdown across the project lifecycle")

    table_shape15 = s15.shapes.add_table(6, 3, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.6))
    t15 = table_shape15.table
    t15.columns[0].width = Inches(2.2)
    t15.columns[1].width = Inches(2.5)
    t15.columns[2].width = Inches(7.033)

    t15_headers = ["Phase", "Duration", "Planned Work & Milestones"]
    for c_i, h_t in enumerate(t15_headers):
        cell = t15.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TABLE_HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_t
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

    t15_rows = [
        ("Phase 1", "Week 1", "Literature survey, problem identification, requirement analysis, and Review 1 preparation."),
        ("Phase 2", "Weeks 2–4", "Traffic dataset collection, CCTV video preprocessing, and YOLOv11 accident detection model training."),
        ("Phase 3", "Weeks 5–6", "FastAPI backend development, nearby-camera inference logic, and Dijkstra/A* routing algorithm implementation."),
        ("Phase 4", "Weeks 7–8", "Flutter mobile app UI, Firebase database setup, Google Maps API, and FCM alert notifications integration."),
        ("Phase 5", "Weeks 9–10", "End-to-end system testing, performance evaluation, thesis documentation, and Final Project Review.")
    ]

    for r_i, (ph, dur, wk) in enumerate(t15_rows):
        c0 = t15.cell(r_i + 1, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = CARD_WHITE_BG
        p = c0.text_frame.paragraphs[0]
        p.text = ph
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = TOP_BLUE

        c1 = t15.cell(r_i + 1, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = CARD_WHITE_BG
        p = c1.text_frame.paragraphs[0]
        p.text = dur
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

        c2 = t15.cell(r_i + 1, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = CARD_WHITE_BG
        p = c2.text_frame.paragraphs[0]
        p.text = wk
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK

    future_scope = [
        "Future Scope: Integration with city-wide live traffic police CCTV feeds, advanced deep-learning congestion prediction, and automated integration with dynamic traffic signal controllers."
    ]
    create_card(s15, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.4), "Future Scope & Long-Term Vision", future_scope, bg_col=CARD_BLUE_BG, bd_col=CARD_BLUE_BD, icon_text="🔭")

    s15.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 15):\n"
        "Our work plan is structured into 5 phases over 10 weeks. Phase 1 is completed. Weeks 2 to 4 focus on dataset collection "
        "and YOLOv11 model training. Weeks 5 and 6 cover backend and routing algorithms. Weeks 7 and 8 involve the Flutter mobile app and "
        "Firebase integration. Weeks 9 and 10 conclude with end-to-end testing, documentation, and the final review."
    )

    # ==================== SLIDE 16: REFERENCES AND CONCLUSION ====================
    s16 = prs.slides.add_slide(blank_layout)
    add_top_bar(s16, 16, 16)
    add_header(s16, "14. References and Conclusion", "Academic sources, summary, and next milestones")

    ref_items = [
        "[1] M. Tahir, Y. Qiao, N. Kanwal, B. Lee, and M. N. Asghar, 'Real-Time Event-Driven Road Traffic Monitoring System Using CCTV Video Analytics,' IEEE Access, vol. 11, pp. 139097–139111, 2023, doi: 10.1109/ACCESS.2023.3340144.",
        "[2] O. Alzamzami, Z. Alsaggaf, R. AlMalki, R. Alghamdi, A. Babour, and L. Al Khuzayem, 'Passable: An Intelligent Traffic Light System with Integrated Incident Detection and Vehicle Alerting,' Sensors, vol. 25, no. 18, Art. no. 5760, 2025, doi: 10.3390/s25185760.",
        "[3] P. Perez-Murueta et al., 'Deep Learning System for Vehicular Re-Routing and Congestion Avoidance,' Applied Sciences, vol. 9, no. 13, Art. no. 2717, 2019, doi: 10.3390/app9132717."
    ]
    conc_items = [
        "CLEARPATH AI proposes an intelligent approach to accident detection and traffic diversion.",
        "Combines CCTV-based AI accident detection, nearby-camera traffic analysis, alternative-route recommendations, and early driver alerts.",
        "The proposed system aims to reduce traffic congestion, improve incident awareness, and support safer road travel.",
        "The next stage focuses on AI model development, route-planning integration, mobile application development, and system evaluation."
    ]

    create_card(s16, Inches(0.8), Inches(1.6), Inches(5.6), Inches(3.6), "References", ref_items, bg_col=CARD_WHITE_BG, bd_col=CARD_WHITE_BD, icon_text="📚")
    create_card(s16, Inches(6.8), Inches(1.6), Inches(5.733), Inches(3.6), "Conclusion", conc_items, bg_col=CARD_GREEN_BG, bd_col=CARD_GREEN_BD, icon_text="🏆")

    # Thank You Banner at Bottom (Inspired by Slide 12 in user images)
    ty_card = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.4))
    ty_card.fill.solid()
    ty_card.fill.fore_color.rgb = CARD_BLUE_BG
    ty_card.line.color.rgb = CARD_BLUE_BD
    ty_card.line.width = Pt(1.2)

    ty_tb = s16.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.333), Inches(1.3))
    ty_tf = ty_tb.text_frame
    ty_tf.word_wrap = True
    
    p_ty1 = ty_tf.paragraphs[0]
    p_ty1.alignment = PP_ALIGN.CENTER
    p_ty1.text = "🚩  THANK YOU!"
    p_ty1.font.size = Pt(18)
    p_ty1.font.bold = True
    p_ty1.font.color.rgb = TOP_BLUE
    p_ty1.space_after = Pt(4)

    p_ty2 = ty_tf.add_paragraph()
    p_ty2.alignment = PP_ALIGN.CENTER
    p_ty2.text = "We welcome your questions, feedback, and guidance. | Team: Afrin Reshma C, Akshay A, Devadharshini R (Dept. of AI & DS)"
    p_ty2.font.size = Pt(11.5)
    p_ty2.font.color.rgb = NAVY_DARK

    s16.notes_slide.notes_text_frame.text = (
        "SPEAKER NOTES (SLIDE 16):\n"
        "In conclusion: CLEARPATH AI provides an integrated solution to detect road accidents from CCTV, infer incidents from "
        "neighboring cameras, and proactively re-route approaching drivers to prevent city-wide gridlock. "
        "We are ready to move into Phase 2 for model training and development. Thank you respected staff, we welcome your questions and suggestions."
    )

    output_filename = "CLEARPATH_AI_Project_Presentation.pptx"
    prs.save(output_filename)
    print(f"CLEARPATH AI presentation successfully generated: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_clearpath_presentation()
