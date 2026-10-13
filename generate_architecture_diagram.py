import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram(output_path="proposed_architecture_diagram.png"):
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
        # Draw rounded rectangle
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

    # Box 1: Ingestion
    draw_box(
        2, 23, 20, 16, C_BLUE, B_BLUE,
        "1. Document Ingestion",
        ["• Multi-Page e-Aadhaar PDF", "• Front & Back PVC Scans", "• Drag & Drop File Chips", "• pypdfium2 300 DPI Render"]
    )

    # Box 2A: Face Detection
    draw_box(
        26, 23, 22, 16, C_PURPLE, B_PURPLE,
        "2A. Deep Neural Face Crop",
        ["• OpenCV YuNet ONNX (232KB)", "• 92%+ Confidence Face Box", "• 40% Margin Passport Crop", "• HSV Skin Density >= 2.0%"]
    )

    # Box 2B: Bilingual OCR
    draw_box(
        26, 3, 22, 16, C_BLUE, B_BLUE,
        "2B. Bilingual OCR Engine",
        ["• EasyOCR (PyTorch-based)", "• Multi-Script Recognition", "• Word & Box Coordinates", "• Concatenated Text Stream"]
    )

    # Box 3: Local SLM Reasoner
    draw_box(
        52, 3, 22, 16, C_AMBER, B_AMBER,
        "3. Local SLM Reasoner",
        ["• Meta Llama 3.2 (3B) Model", "• Local Ollama (Port 11434)", "• Zero Cloud Telemetry", "• Strict JSON Schema Output"]
    )

    # Box 4: Regex Normalizer
    draw_box(
        52, 23, 22, 16, C_GREEN, B_GREEN,
        "4. Rule Normalization",
        ["• 12-Digit UID vs 14-Digit Enrol", "• Disclaimer Footers Scrubbed", "• Door No / Street Splitting", "• DOB -> YYYY-MM-DD Format"]
    )

    # Box 5: DOM Autofill Dashboard
    draw_box(
        78, 13, 20, 16, C_SLATE, B_SLATE,
        "5. ECI Form 6 DOM Engine",
        ["• Reactive Field Injection", "• Dropdown Sync (Relation)", "• Passport Photo Preview", "• Mandatory User Review"]
    )

    # Arrows
    draw_arrow(22, 31, 26, 31, B_BLUE)         # Box 1 -> Box 2A
    draw_arrow(12, 23, 12, 11, B_BLUE)         # Box 1 down
    draw_arrow(12, 11, 26, 11, B_BLUE)         # -> Box 2B
    draw_arrow(48, 11, 52, 11, B_BLUE)         # Box 2B -> Box 3
    draw_arrow(63, 19, 63, 23, B_AMBER)        # Box 3 up -> Box 4
    draw_arrow(48, 31, 52, 31, B_PURPLE)       # Box 2A -> Box 4
    draw_arrow(74, 31, 78, 25, B_GREEN)        # Box 4 -> Box 5
    draw_arrow(74, 11, 78, 17, B_AMBER)        # Box 3 -> Box 5

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Architecture diagram created: {output_path}")

if __name__ == "__main__":
    create_architecture_diagram()
