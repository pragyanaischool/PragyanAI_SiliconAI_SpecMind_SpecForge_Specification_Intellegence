"""
assets/generate_png_assets.py
Generates branding_banner.png and contract_ontology_graph.png using Pillow.
Run: python assets/generate_png_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets", exist_ok=True)

def create_banner():
    width, height = 1200, 260
    img = Image.new("RGBA", (width, height), (7, 11, 18, 255))
    draw = ImageDraw.Draw(img)

    # Gradient border on bottom
    for i in range(width):
        ratio = i / width
        r = int(0 * (1 - ratio) + 0 * ratio)
        g = int(242 * (1 - ratio) + 120 * ratio)
        b = int(254 * (1 - ratio) + 255 * ratio)
        draw.line([(i, height - 3), (i, height - 1)], fill=(r, g, b, 255))

    # Grid background lines
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height - 4)], fill=(19, 28, 46, 120), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(19, 28, 46, 120), width=1)

    # Text rendering
    draw.text((60, 48), "PRAGYANAI", fill=(0, 242, 254, 255))
    draw.text((60, 80), "SPECFORGE STUDIO", fill=(255, 255, 255, 255))
    draw.text((60, 140), "Autonomous Hardware Specification Intelligence & Design Contract Synthesis", fill=(148, 163, 184, 255))
    draw.text((60, 168), "Pydantic V2 Type Contracts • SystemVerilog Assertions • Formal Verification Planning", fill=(100, 116, 139, 255))

    # Right side decorative IC badge
    draw.rectangle([(980, 50), (1140, 210)], outline=(0, 242, 254, 180), width=2, fill=(15, 23, 42, 220))
    draw.text((1015, 120), "SILICON\nCONTRACT", fill=(0, 242, 254, 255))

    img.save("assets/branding_banner.png", "PNG")
    print("Created assets/branding_banner.png")

def create_ontology():
    width, height = 900, 520
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)

    # Core Root Node
    draw.rectangle([(320, 30), (580, 95)], fill=(7, 11, 18, 255), outline=(0, 242, 254, 255), width=2)
    draw.text((345, 48), "HardwareContract (Root)", fill=(0, 242, 254, 255))
    draw.text((360, 68), "Pydantic V2 Container", fill=(148, 163, 184, 255))

    # Child Entities
    boxes = [
        ("PortModel", 50, 170, "Interface Signals & Busses"),
        ("TimingModel", 270, 170, "Fmax, CDC & Latencies"),
        ("FSMModel", 490, 170, "States & Transition Matrix"),
        ("CornerCaseModel", 710, 170, "Hazards & SVA Assertions")
    ]

    for title, x, y, subtitle in boxes:
        draw.line([(450, 95), (x + 80, y)], fill=(0, 242, 254, 160), width=2)
        draw.rectangle([(x, y), (x + 160, y + 65)], fill=(30, 41, 59, 255), outline=(56, 189, 248, 200), width=1)
        draw.text((x + 15, y + 12), title, fill=(248, 250, 252, 255))
        draw.text((x + 10, y + 36), subtitle, fill=(148, 163, 184, 255))

    # Lower dependencies (RTM & SVA Outputs)
    draw.line([(130, 235), (130, 320)], fill=(56, 189, 248, 160), width=2)
    draw.rectangle([(50, 320), (210, 380)], fill=(7, 11, 18, 255), outline=(148, 163, 184, 200), width=1)
    draw.text((65, 335), "Traceability Link", fill=(226, 232, 240, 255))
    draw.text((65, 355), "Section <-> Port", fill=(100, 116, 139, 255))

    draw.line([(790, 235), (790, 320)], fill=(56, 189, 248, 160), width=2)
    draw.rectangle([(710, 320), (870, 380)], fill=(7, 11, 18, 255), outline=(168, 85, 247, 200), width=1)
    draw.text((725, 335), "SVA Bind Engine", fill=(192, 132, 252, 255))
    draw.text((725, 355), "SystemVerilog File", fill=(100, 116, 139, 255))

    img.save("assets/contract_ontology_graph.png", "PNG")
    print("Created assets/contract_ontology_graph.png")

if __name__ == "__main__":
    create_banner()
    create_ontology()
