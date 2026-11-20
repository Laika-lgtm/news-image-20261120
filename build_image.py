#!/usr/bin/env python3
"""Build the 1024x1024 front-page image for news-image-20261120.

Hero artwork was generated in-session (AI image, no text). All headlines
and labels are drawn here with PIL so every word is crisp and accurate.
Output: entry.png (JPEG bytes under the .png name, allowed by RULES.txt:
the file is told apart by its first bytes; the name stays entry.png).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)      # off-white paper
NAVY = (27, 42, 74)
GOLD = (201, 162, 39)
RED = (176, 58, 46)
INK = (20, 20, 20)
GREY = (90, 90, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.text((W // 2, 18), "THE WORLD TODAY", font=font(SERIF_B, 58),
           fill=NAVY, anchor="ma")
    d.text((W // 2, 86), "FRIDAY, 20 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=RED, anchor="ma")
    d.line([(28, 122), (W - 28, 122)], fill=NAVY, width=3)

    # --- hero band (AI artwork, no text in it) ---
    hero = Image.open("assets/media-generation-hero-summit-0-2d877a3d-9b2b-49fe-9985-8abf486c03a1.png").convert("RGB")
    hw, hh = hero.size
    target_w, target_h = 968, 330
    scale = max(target_w / hw, target_h / hh)
    hero = hero.resize((int(hw * scale + 0.5), int(hh * scale + 0.5)), Image.LANCZOS)
    x0 = (hero.width - target_w) // 2
    y0 = (hero.height - target_h) // 2
    hero = hero.crop((x0, y0, x0 + target_w, y0 + target_h))
    img.paste(hero, (28, 134))
    d.rectangle([28, 134, 28 + 968, 134 + 330], outline=NAVY, width=3)
    # caption strip over hero bottom, text centred in the strip
    d.rectangle([28, 434, 28 + 968, 464], fill=NAVY)
    d.text((W // 2, 449), "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
           font=font(SANS_B, 20), fill=(255, 255, 255), anchor="mm")

    # --- story rows ---
    stories = [
        ("01", "SUMMIT IN SHENZHEN",
         "Trump, Xi and Putin issue a joint peace declaration after their first trilateral talks."),
        ("02", "WORLD COURT: GENOCIDE",
         "The ICJ rules Myanmar committed genocide against the Rohingya, by 9 votes to 6."),
        ("03", "ANTHROPIC GOES PUBLIC",
         "The first frontier AI company lists on Nasdaq; shares jump on debut."),
        ("04", "UKRAINE: TALKS AND DRONES",
         "Europe is ready to join peace talks; the UK pledges 1,000+ drones in a £260m package."),
    ]
    y = 486
    row_h = 118
    for num, head, summ in stories:
        # number chip
        d.rectangle([28, y + 8, 88, y + 68], fill=NAVY)
        d.text((58, y + 16), num, font=font(SANS_B, 30), fill=GOLD, anchor="ma")
        # headline
        d.text((104, y + 6), head, font=font(SERIF_B, 29), fill=INK, anchor="la")
        # summary, wrapped to 2 lines
        lines = wrap(d, summ, font(SANS, 21), 892)[:2]
        ly = y + 44
        for ln in lines:
            d.text((104, ly), ln, font=font(SANS, 21), fill=(45, 45, 45), anchor="la")
            ly += 27
        y += row_h
        if num != "04":
            d.line([(28, y - 8), (W - 28, y - 8)], fill=(200, 192, 175), width=2)

    # --- footer ---
    d.line([(28, 972), (W - 28, 972)], fill=NAVY, width=3)
    d.text((W // 2, 984), "20 NOVEMBER 2026  •  SHENZHEN  •  THE HAGUE  •  NEW YORK  •  KYIV",
           font=font(SANS_B, 18), fill=GREY, anchor="ma")

    img.save("entry.png", format="JPEG", quality=90, optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
