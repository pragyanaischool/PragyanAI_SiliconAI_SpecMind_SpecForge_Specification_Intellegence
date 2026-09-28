"""
assets/generate_contract_ontology.py
Generates assets/contract_ontology_graph.png for PragyanAI-SpecForge.
Creates a high-density, 300-DPI equivalent schema diagram for Pydantic V2 hardware models.
"""

import os
from PIL import Image, ImageDraw, ImageFont


def get_font(size: int, bold: bool = False):
    """Attempt to load a crisp monospace or modern system font, fallback to default."""
    font_names = [
        # Linux / Ubuntu CI
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        # macOS
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/Courier New Bold.ttf"
        if bold
        else "/Library/Fonts/Courier New.ttf",
        # Windows
        "C:\\Windows\\Fonts\\consola.ttf"
        if not bold
        else "C:\\Windows\\Fonts\\consolab.ttf",
    ]
    for p in font_names:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_rounded_rect(
    draw, xy, radius, fill=None, outline=None, width=1, stroke_dash=None
):
    """Draws a clean rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(
        [x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width
    )


def draw_schema_card(
    draw, x, y, width, title, fields, border_color, badge_text, badge_color
):
    """Renders a standard Pydantic schema class box."""
    header_h = 44
    line_h = 24
    card_h = header_h + len(fields) * line_h + 16

    # Card background and border
    draw_rounded_rect(
        draw,
        (x, y, x + width, y + card_h),
        radius=10,
        fill=(13, 20, 36, 250),
        outline=border_color,
        width=2,
    )

    # Header section
    draw_rounded_rect(
        draw,
        (x, y, x + width, y + header_h),
        radius=10,
        fill=(19, 28, 46, 255),
        outline=None,
    )
    # Bottom square corners for header
    draw.rectangle([x, y + 20, x + width, y + header_h], fill=(19, 28, 46, 255))
    draw.line(
        [(x, y + header_h), (x + width, y + header_h)],
        fill=border_color,
        width=1,
    )

    # Title & Badge
    f_title = get_font(15, bold=True)
    f_badge = get_font(10, bold=True)
    f_field = get_font(12, bold=False)
    f_type = get_font(11, bold=False)

    draw.text((x + 16, y + 14), title, fill=(248, 250, 252, 255), font=f_title)

    # Badge pill
    badge_w = 90
    draw_rounded_rect(
        draw,
        (x + width - badge_w - 12, y + 12, x + width - 12, y + 32),
        radius=5,
        fill=(8, 14, 26, 255),
        outline=badge_color,
        width=1,
    )
    draw.text(
        (x + width - badge_w - 4, y + 16),
        badge_text,
        fill=badge_color,
        font=f_badge,
    )

    # Render Fields
    curr_y = y + header_h + 10
    for fname, ftype in fields:
        draw.text(
            (x + 16, curr_y), f"+ {fname}:", fill=(226, 232, 240, 255), font=f_field
        )
        draw.text(
            (x + width - 14 - (len(ftype) * 8), curr_y),
            ftype,
            fill=(100, 116, 139, 255),
            font=f_type,
        )
        curr_y += line_h

    return (
        x + width // 2,
        y,
        x + width // 2,
        y + card_h,
    )  # Return top and bottom anchors


def main():
    width, height = 2400, 1400
    img = Image.new("RGBA", (width, height), (7, 11, 18, 255))
    draw = ImageDraw.Draw(img)

    # Grid background lines
    for gx in range(0, width, 50):
        draw.line([(gx, 0), (gx, height)], fill=(15, 23, 42, 120), width=1)
    for gy in range(0, height, 50):
        draw.line([(0, gy), (width, gy)], fill=(15, 23, 42, 120), width=1)

    # Top Banner
    f_brand = get_font(26, bold=True)
    f_sub = get_font(14, bold=False)
    draw.text(
        (100, 60),
        "PRAGYANAI-SPECFORGE : PYDANTIC V2 HARDWARE ONTOLOGY",
        fill=(0, 242, 254, 255),
        font=f_brand,
    )
    draw.text(
        (100, 100),
        "Relational Schema Mapping, Strong Typing Constraints, and Downstream Verification Bindings",
        fill=(148, 163, 184, 255),
        font=f_sub,
    )
    draw.line(
        [(100, 130), (width - 100, 130)], fill=(30, 41, 59, 255), width=2
    )

    # 1. ROOT CONTAINER (Centered Top)
    root_x, root_y, root_w = 950, 170, 500
    root_fields = [
        ("module_name", "str"),
        ("description", "str"),
        ("reset_type", "Literal['sync_low', ...]"),
        ("ports", "List[PortModel]"),
        ("timing", "TimingModel"),
        ("fsms", "List[FSMModel]"),
        ("corner_cases", "List[CornerCaseModel]"),
        ("traceability", "List[RTMItem]"),
    ]
    rx_top, ry_top, rx_bot, ry_bot = draw_schema_card(
        draw,
        root_x,
        root_y,
        root_w,
        "HardwareSpecificationContract",
        root_fields,
        border_color=(0, 242, 254, 255),
        badge_text="Root Contract",
        badge_color=(0, 242, 254, 255),
    )

    # 2. LEVEL 2 SCHEMAS (Four Columns)
    # PortModel
    p_fields = [
        ("name", "str (e.g. s_axis_tdata)"),
        ("direction", "Literal['in','out','inout']"),
        ("width", "str (e.g. '[31:0]')"),
        ("clock_domain", "str (e.g. 'aclk')"),
        ("active_level", "Literal['high','low','edge']"),
        ("description", "str"),
    ]
    px_top, py_top, px_bot, py_bot = draw_schema_card(
        draw,
        100,
        540,
        500,
        "PortModel",
        p_fields,
        border_color=(56, 189, 248, 255),
        badge_text="Interface",
        badge_color=(56, 189, 248, 255),
    )

    # TimingModel
    t_fields = [
        ("fmax_mhz", "Optional[float]"),
        ("setup_time_ns", "Optional[float]"),
        ("hold_time_ns", "Optional[float]"),
        ("latency_cycles", "str"),
        ("throughput_cycles", "str"),
        ("is_cdc", "bool"),
        ("cdc_details", "Optional[str]"),
    ]
    tx_top, ty_top, tx_bot, ty_bot = draw_schema_card(
        draw,
        660,
        540,
        480,
        "TimingModel",
        t_fields,
        border_color=(147, 51, 234, 255),
        badge_text="STA & CDC",
        badge_color=(192, 132, 252, 255),
    )

    # FSMModel
    f_fields = [
        ("name", "str (e.g. 'READ_FSM')"),
        ("encoding", "Literal['one-hot','gray','bin']"),
        ("states", "List[str]"),
        ("transitions", "List[FSMTransitionModel]"),
        ("reset_state", "str"),
    ]
    fx_top, fy_top, fx_bot, fy_bot = draw_schema_card(
        draw,
        1200,
        540,
        520,
        "FSMModel",
        f_fields,
        border_color=(234, 179, 8, 255),
        badge_text="Control Path",
        badge_color=(250, 204, 21, 255),
    )

    # CornerCaseModel
    c_fields = [
        ("scenario_id", "str (e.g. 'CC_01')"),
        ("title", "str"),
        ("hazard_description", "str"),
        ("expected_behavior", "str"),
        ("sva_property", "str (SystemVerilog)"),
    ]
    cx_top, cy_top, cx_bot, cy_bot = draw_schema_card(
        draw,
        1780,
        540,
        520,
        "CornerCaseModel",
        c_fields,
        border_color=(239, 68, 68, 255),
        badge_text="DV & SVA",
        badge_color=(248, 113, 113, 255),
    )

    # Connect Root to Level 2 with Multi-branch Bus
    bus_y = 480
    draw.line([(rx_bot, ry_bot), (rx_bot, bus_y)], fill=(0, 242, 254, 255), width=2)
    draw.line(
        [(px_top, bus_y), (cx_top, bus_y)], fill=(0, 242, 254, 255), width=2
    )

    # Downward connectors with 1:N cardinality marks
    for x_target in [px_top, tx_top, fx_top, cx_top]:
        draw.line([(x_target, bus_y), (x_target, 540)], fill=(0, 242, 254, 255), width=2)
        draw.ellipse(
            [x_target - 4, 536, x_target + 4, 544], fill=(0, 242, 254, 255)
        )

    # Cardinality badges
    f_card = get_font(12, bold=True)
    draw.text((px_top - 36, 505), "1 : N", fill=(0, 242, 254, 255), font=f_card)
    draw.text((tx_top - 36, 505), "1 : 1", fill=(0, 242, 254, 255), font=f_card)
    draw.text((fx_top - 36, 505), "1 : N", fill=(0, 242, 254, 255), font=f_card)
    draw.text((cx_top - 36, 505), "1 : N", fill=(0, 242, 254, 255), font=f_card)

    # 3. LEVEL 3 CHILDREN (Transitions & Traceability)
    # FSMTransitionModel
    ft_fields = [
        ("from_state", "str"),
        ("to_state", "str"),
        ("condition", "str (Boolean logic)"),
    ]
    ftx_top, fty_top, _, _ = draw_schema_card(
        draw,
        1220,
        830,
        480,
        "FSMTransitionModel",
        ft_fields,
        border_color=(234, 179, 8, 200),
        badge_text="State Arc",
        badge_color=(250, 204, 21, 255),
    )
    draw.line([(fx_bot, fy_bot), (ftx_top, fty_top)], fill=(234, 179, 8, 255), width=2)
    draw.text(
        (fx_bot + 10, fy_bot + 40), "1 : N", fill=(234, 179, 8, 255), font=f_card
    )

    # RTM Traceability
    rtm_fields = [
        ("req_id", "str (e.g. 'REQ_042')"),
        ("target_type", "Literal['port','fsm','corner']"),
        ("mapped_element", "str"),
        ("source_paragraph", "str"),
    ]
    rtmx_top, rtmy_top, _, _ = draw_schema_card(
        draw,
        100,
        830,
        500,
        "RequirementsTraceabilityItem",
        rtm_fields,
        border_color=(16, 185, 129, 255),
        badge_text="Traceability",
        badge_color=(52, 211, 153, 255),
    )
    # Link from Port to Traceability
    draw.line(
        [(px_bot, py_bot), (rtmx_top, rtmy_top)],
        fill=(16, 185, 129, 255),
        width=2,
    )

    # 4. DOWNSTREAM ARTIFACT OUTPUTS (Bottom Stage)
    artifacts = [
        (
            100,
            1130,
            680,
            "Micro-Architecture Specification (.md / .docx)",
            "Automated Engineering MAS with Signal Dictionaries & FSM State Tables",
            (56, 189, 248, 255),
        ),
        (
            840,
            1130,
            680,
            "Synthesizable SystemVerilog Assertions (.sv)",
            "Formal Bind Modules for Clocked Concurrent Temporal Properties",
            (192, 132, 252, 255),
        ),
        (
            1580,
            1130,
            720,
            "Immutable JSON Contract Manifest (.json)",
            "Strict Machine-Readable Directives for Verilog Synthesizers & LLM Coders",
            (0, 242, 254, 255),
        ),
    ]

    f_art_title = get_font(14, bold=True)
    f_art_sub = get_font(11, bold=False)

    for ax, ay, aw, atitle, asub, acolor in artifacts:
        draw_rounded_rect(
            draw,
            (ax, ay, ax + aw, ay + 90),
            radius=8,
            fill=(10, 16, 30, 255),
            outline=acolor,
            width=1.5,
        )
        draw.text(
            (ax + 24, ay + 22), f"📦 {atitle}", fill=acolor, font=f_art_title
        )
        draw.text(
            (ax + 24, ay + 52), asub, fill=(148, 163, 184, 255), font=f_art_sub
        )

    # Save artifact
    os.makedirs("assets", exist_ok=True)
    output_path = "assets/contract_ontology_graph.png"
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Successfully generated {output_path} ({width}x{height})")


if __name__ == "__main__":
    main()
