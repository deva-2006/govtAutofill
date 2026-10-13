import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_attendance_architecture_diagram(output_path="smart_attendance_architecture_diagram.png"):
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('white')

    # Color definitions
    C_BLUE = '#EFF6FF'
    B_BLUE = '#2563EB'
    C_GREEN = '#F0FDF4'
    B_GREEN = '#16A34A'
    C_PURPLE = '#FAF5FF'
    B_PURPLE = '#9333EA'
    C_AMBER = '#FFFBEB'
    B_AMBER = '#D97706'
    C_SLATE = '#F8FAFC'
    B_SLATE = '#475569'

    def draw_box(x, y, w, h, bg_col, bd_col, title, subtitle_lines):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.5,rounding_size=1.2",
            facecolor=bg_col, edgecolor=bd_col, linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Title
        ax.text(
            x + w/2, y + h - 2.2, title,
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A',
            fontfamily='sans-serif'
        )
        # Separator line
        ax.plot([x + 1, x + w - 1], [y + h - 3.8, y + h - 3.8], color=bd_col, lw=0.75)
        
        # Subtitle lines
        for idx, line in enumerate(subtitle_lines):
            ax.text(
                x + w/2, y + h - 5.5 - (idx * 2.1), line,
                ha='center', va='center', fontsize=7.2, color='#334155',
                fontfamily='sans-serif'
            )

    def draw_arrow(x1, y1, x2, y2, color='#475569'):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>", color=color, lw=1.5,
                mutation_scale=12, shrinkA=0, shrinkB=0
            )
        )

    # Box 1: Video Capture
    draw_box(
        2, 23, 20, 16, C_BLUE, B_BLUE,
        "1. Video Capture",
        ["• Classroom 1080p Webcam", "• Real-Time Video Stream", "• Frame Extraction (30 FPS)", "• Illumination Normalization"]
    )

    # Box 2A: Face Detection
    draw_box(
        26, 23, 22, 16, C_PURPLE, B_PURPLE,
        "2A. Face Detection",
        ["• OpenCV YuNet / Haar", "• Multi-Face Bounding Boxes", "• Eye & Nose Landmarks", "• Facial Crop & Alignment"]
    )

    # Box 2B: Anti-Spoofing
    draw_box(
        26, 3, 22, 16, C_BLUE, B_BLUE,
        "2B. Anti-Spoofing Filter",
        ["• Liveness & Texture Check", "• Eye-Blink Verification", "• Rejects Phone Replays", "• Rejects Printed Photos"]
    )

    # Box 3: Feature Extraction
    draw_box(
        52, 23, 22, 16, C_AMBER, B_AMBER,
        "3. Feature Extraction",
        ["• Deep CNN (FaceNet / dlib)", "• 128D Embedding Vectors", "• Geometric Invariance", "• Metric Learning Mapping"]
    )

    # Box 4: Database Matching
    draw_box(
        52, 3, 22, 16, C_GREEN, B_GREEN,
        "4. Database Matching",
        ["• Euclidean Distance Calc", "• Similarity Thresholding", "• Student Profile Verification", "• Debounce Duplicate Filter"]
    )

    # Box 5: Dashboard & Logging
    draw_box(
        78, 13, 20, 16, C_SLATE, B_SLATE,
        "5. Automated Logging",
        ["• SQLite / PostgreSQL Log", "• Real-Time Faculty UI", "• 1-Click Excel / CSV Export", "• Parent Absentee SMS"]
    )

    # Arrows
    draw_arrow(22, 31, 26, 31, B_BLUE)         # Box 1 -> Box 2A
    draw_arrow(37, 23, 37, 19, B_PURPLE)       # Box 2A down -> Box 2B
    draw_arrow(48, 31, 52, 31, B_PURPLE)       # Box 2A -> Box 3
    draw_arrow(48, 11, 52, 11, B_BLUE)         # Box 2B -> Box 4
    draw_arrow(63, 23, 63, 19, B_AMBER)        # Box 3 -> Box 4
    draw_arrow(74, 11, 78, 18, B_GREEN)        # Box 4 -> Box 5
    draw_arrow(74, 31, 78, 24, B_AMBER)        # Box 3 -> Box 5

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Smart Attendance Architecture diagram created: {output_path}")

if __name__ == "__main__":
    create_attendance_architecture_diagram()
