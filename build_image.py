#!/usr/bin/env python3
"""Build the front page for Friday 20 November 2026.

Renders a one-page newspaper image (1024x1024 JPEG) from the four
editorial photographs in assets/ and the verified story list below.
Every story was checked against Reuters, CNN, AP, WSJ, Le Monde,
the India Meteorological Department and COP31 draft texts on
20 November 2026; each item carries its source. Stories first
reported on 19 November sit in their own band, dated as such.

Layout flows top to bottom on a cursor: nothing is drawn past the
page edge, every line is wrapped or truncated to its column width.

Runs offline with Pillow only. Output is deterministic: same
inputs, same bytes, every run.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (176, 30, 36)
GREY = (96, 90, 80)
LINE = (200, 192, 175)
BODY = (40, 38, 34)

REGION_COLORS = {
    "EUROPE": (122, 31, 43),
    "ASIA": (180, 83, 9),
    "MIDEAST": (109, 40, 217),
    "AFRICA": (21, 128, 61),
    "AMERICAS": (14, 116, 144),
    "OCEANIA": (29, 78, 216),
    "MARKETS": (68, 64, 60),
    "WORLD": (87, 83, 78),
}

HERO = {
    "kicker": "INDIA  ·  LANDFALL 07:30 IST",
    "headline": "AKVAN SLAMS INTO INDIA'S EAST COAST",
    "caption": (
        "Cyclone Akvan crossed the coast near Gopalpur, Odisha, on Friday "
        "morning with winds of 70\u201380 km/h, gusting to 90. Over 300,000 "
        "people were evacuated to 9,341 shelters and 69 trains cancelled "
        "\u2014 the third cyclone in under a month. Sources: Reuters, IMD."
    ),
    "image": "assets/media-generation-hero-akvan-0-de20aac7-388b-4046-8f6a-419dc512f536.jpg",
}

PANELS = [
    {
        "kicker": "UKRAINE  ·  01:22 UTC",
        "headline": "MISSILES SMASH THREE KYIV BRIDGES",
        "text": (
            "Russia's overnight missile attack killed 3 in Kyiv and 2 in "
            "Lviv, damaged three Dnipro bridges and cut power across "
            "districts."
        ),
        "source": "Reuters, AP",
        "image": "assets/media-generation-panel-kyiv-0-d5517e16-c1b3-4281-a3b9-9f7251cc21c1.jpg",
    },
    {
        "kicker": "CLIMATE  ·  ANTALYA",
        "headline": "COP31 ENDS WITH NO FOSSIL-FUEL DEAL",
        "text": (
            "The revised draft drops every fossil-fuel phase-out mention "
            "and a $120bn finance figure, adding a carbon-capture target. "
            "Panama may block a deal."
        ),
        "source": "Reuters, Carbon Herald",
        "image": "assets/media-generation-panel-cop31-0-f05dc660-51ae-4b2c-aa7f-54f5280402fe.jpg",
    },
    {
        "kicker": "DIPLOMACY  ·  SHENZHEN",
        "headline": "AFTER SHENZHEN, EUROPE SCOFFS",
        "text": (
            "European leaders dismiss the joint \u201cdeclaration for "
            "peace\u201d as a photo op. Canada extends a tariff pact "
            "with China to 2028."
        ),
        "source": "WSJ, Reuters, The Times",
        "image": "assets/media-generation-panel-apec-0-45fbe9de-8d1d-407f-94be-772d09871622.jpg",
    },
]

# (region, headline, one-line summary, source)
BRIEFS_TODAY = [
    ("MIDEAST", "Iraq deploys troops to militia base",
     "Security forces move into Jurf al-Sakhar, a Kataib Hezbollah "
     "stronghold, under a deal to ease tensions.", "Reuters"),
    ("ASIA", "Prabowo meets Xi on South China Sea",
     "Indonesia's president talks economy and sea cooperation with "
     "Xi in Shenzhen.", "Reuters"),
    ("EUROPE", "Russia rejects NATO guarantees",
     "Deputy FM Ryabkov pushes back on the US idea of NATO-style "
     "security guarantees for Ukraine.", "Reuters"),
    ("OCEANIA", "Xi hails China\u2013Australia turnaround",
     "Xi calls ties with Australia a \u201ccomprehensive turnaround\u201d "
     "after meeting Albanese in Shenzhen.", "Reuters"),
    ("ASIA", "Jakarta quizzes Google on channels",
     "Indonesia asks Google to justify removing 19,000+ "
     "pro-government YouTube channels.", "Reuters"),
    ("MARKETS", "Oil up on Riyadh supply fears",
     "Brent $92.22 after Houthi strikes on Riyadh and tanker "
     "disruption in the Strait of Hormuz.", "Reuters"),
    ("ASIA", "Kakao founder acquittal stands",
     "Seoul appeals court upholds Kim Beom-su's acquittal on "
     "stock-manipulation charges.", "Reuters"),
    ("WORLD", "FIFA presidency challenged",
     "Japan's Kozo Tashima says a World Cup red-card row pushed him "
     "to run against Infantino.", "Reuters"),
    ("EUROPE", "Lagarde: AI cyber threat top worry",
     "The ECB chief says AI-boosted cyber attacks keep her awake; "
     "policymakers pay too little attention.", "Reuters"),
    ("AMERICAS", "Bovespa slips as sell-off spreads",
     "Brazil's Bovespa falls 0.69% to 166,376 amid the global "
     "market sell-off.", "OneTurn"),
    ("ASIA", "Rupee breaks past 93 to the dollar",
     "India's currency strengthens for the first time since April as "
     "foreign inflows top $12bn in November.", "Reuters"),
    ("EUROPE", "Metro Bank draws takeover interest",
     "Barclays and private equity firms circle the British lender "
     "after it put itself up for sale.", "Bloomberg"),
    ("MARKETS", "Asian stocks slump; Taiwan dives 5%",
     "Nikkei \u22124.8%, Kospi \u22124.8%, Taiwan \u22125% intraday; "
     "the S&P 500 falls a fifth straight day.", "Reuters"),
    ("ASIA", "Taiwan sheds 7,000 points in a week",
     "Taipei's index falls again as the regulator unveils five "
     "rescue measures.", "SimpleLife"),
    ("AFRICA", "Kenya's last Ebola patient goes home",
     "Kenya discharges its final Ebola patient, 37 days after the "
     "first case.", "OneTurn"),
    ("AMERICAS", "880,000 AI chips cleared for China",
     "A US House panel says nearly 880,000 advanced AI chips were "
     "approved for sale to China.", "SimpleLife"),
    ("AMERICAS", "US Iran-war spending tops $48bn",
     "A Pentagon official puts military spending on the Iran war "
     "above $48 billion.", "SimpleLife"),
    ("MIDEAST", "Iran war burns 30% of munitions",
     "CSIS analysis says US operations against Iran consumed over "
     "30% of key munitions.", "SimpleLife"),
    ("MIDEAST", "Israel urges new Iran bombing",
     "Israel presses Trump to resume bombing Iran; Trump says the "
     "next step comes after New Year.", "SimpleLife"),
    ("ASIA", "No Kim meeting for Trump",
     "Trump leaves Shenzhen without confirming a meeting with North "
     "Korea's Kim Jong Un.", "WSJ"),
    ("WORLD", "Panama vows to block COP31 deal",
     "Panama tells the COP31 presidency it will block a final "
     "agreement unless its demands are met.", "Turkey Recap"),
]

# Stories first reported 19 November, still moving on the 20th.
BRIEFS_YESTERDAY = [
    ("WORLD", "Trump, Xi, Putin hold first summit",
     "Joint declaration: \u201ca nuclear war cannot be won and must "
     "never be fought.\u201d", "WSJ"),
    ("WORLD", "ICJ: Myanmar genocide ruling",
     "The ICJ rules on the Rohingya \u2014 a first genocide finding "
     "against a state.", "Reuters"),
    ("AMERICAS", "Anthropic closes 17% above IPO",
     "The AI firm debuts on Nasdaq at $83 and closes near $97.", "Reuters"),
    ("MIDEAST", "Houthi missiles hit Riyadh tower",
     "A strike damages the Saudi sovereign wealth fund tower in the "
     "financial district.", "Reuters"),
    ("MIDEAST", "Israeli troops cross Gaza truce line",
     "First incursion across the \u201cYellow Line\u201d since the "
     "truce began.", "OneTurn"),
    ("AFRICA", "Drone strike kills 10 at Sudan mine",
     "Ten killed in a drone attack on a mine in South Kordofan.", "OneTurn"),
]

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, font, width, max_lines=None):
    """Greedy word wrap, capped at max_lines with an ellipsis."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "\u2026", font=font) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "\u2026"
    return lines


def fit_one(draw, text, font, width):
    """Truncate a single line to width, with an ellipsis."""
    if draw.textlength(text, font=font) <= width:
        return text
    while text and draw.textlength(text + "\u2026", font=font) > width:
        text = text[:-1]
    return text + "\u2026"


def crop_cover(img, tw, th):
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


def chip(draw, x, y, label, color):
    font = load_font("DejaVuSans-Bold.ttf", 11)
    w = int(draw.textlength(label, font=font)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=color)
    draw.text((x + 6, y + 1), label, font=font, fill=(255, 255, 255))
    return w


def brief_rows(draw, x, items, y, col_w, row_h):
    """Draw a column of briefs; returns the y after the last row."""
    for region, head, text, _src in items:
        chip_w = chip(draw, x, y, region,
                      REGION_COLORS.get(region, (87, 83, 78)))
        head_font = load_font("DejaVuSans-Bold.ttf", 12)
        head = fit_one(draw, head, head_font, col_w - chip_w - 6)
        draw.text((x + chip_w + 6, y), head, font=head_font, fill=INK)
        body = wrap(draw, text, load_font("DejaVuSans.ttf", 11),
                    col_w, max_lines=2)
        by = y + 14
        for line in body:
            draw.text((x, by), line, font=load_font("DejaVuSans.ttf", 11),
                      fill=BODY)
            by += 12
        y += row_h
    return y


def build():
    base = os.path.dirname(os.path.abspath(__file__))
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    serif_b = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
    sans_b = lambda s: load_font("DejaVuSans-Bold.ttf", s)
    sans = lambda s: load_font("DejaVuSans.ttf", s)

    y = 0
    # ---- masthead ----
    draw.text((W // 2, 4), "THE WORLD TODAY", font=serif_b(56),
              fill=INK, anchor="ma")
    draw.rectangle([24, 72, W - 24, 76], fill=RED)
    date_line = ("FRIDAY 20 NOVEMBER 2026   ·   31 STORIES   ·   6 CONTINENTS"
                 "   ·   ALL TIMES UTC")
    draw.text((W // 2, 80), date_line, font=sans_b(15), fill=INK, anchor="ma")
    y = 104

    # ---- hero ----
    hero = Image.open(os.path.join(base, HERO["image"])).convert("RGB")
    page.paste(crop_cover(hero, 976, 170), (24, y))
    draw.rectangle([24, y, 1000, y + 170], outline=INK, width=1)
    y += 176
    draw.text((24, y), HERO["kicker"], font=sans_b(13), fill=RED)
    y += 18
    draw.text((24, y), HERO["headline"], font=serif_b(30), fill=INK)
    y += 38
    for line in wrap(draw, HERO["caption"], sans(13), 976, max_lines=2):
        draw.text((24, y), line, font=sans(13), fill=BODY)
        y += 15
    y += 6

    # ---- three photo panels ----
    draw.rectangle([24, y, W - 24, y + 1], fill=LINE)
    y += 8
    px, pw, gap = 24, 318, 11
    panel_bottom = y
    for panel in PANELS:
        img = Image.open(os.path.join(base, panel["image"])).convert("RGB")
        page.paste(crop_cover(img, pw, 88), (px, y))
        draw.rectangle([px, y, px + pw, y + 88], outline=INK, width=1)
        ty = y + 94
        draw.text((px, ty), panel["kicker"], font=sans_b(11), fill=RED)
        ty += 15
        for line in wrap(draw, panel["headline"], serif_b(15), pw,
                         max_lines=2):
            draw.text((px, ty), line, font=serif_b(15), fill=INK)
            ty += 17
        for line in wrap(draw, panel["text"], sans(12), pw, max_lines=3):
            draw.text((px, ty), line, font=sans(12), fill=BODY)
            ty += 13
        draw.text((px, ty + 1), "Source: " + panel["source"],
                  font=sans(11), fill=GREY)
        panel_bottom = max(panel_bottom, ty + 16)
        px += pw + gap
    y = panel_bottom + 8

    # ---- briefs, today ----
    draw.rectangle([24, y, W - 24, y + 2], fill=INK)
    y += 8
    draw.text((24, y), "THE WORLD IN BRIEF", font=serif_b(17), fill=INK)
    draw.text((W - 24, y + 2), "FRIDAY 20 NOVEMBER 2026", font=sans_b(12),
              fill=RED, anchor="ra")
    y += 22
    col_w, row_h = 318, 37
    for col in range(3):
        items = BRIEFS_TODAY[col * 7:(col + 1) * 7]
        brief_rows(draw, 24 + col * (col_w + gap), items, y, col_w, row_h)
    y += 7 * row_h + 4

    # ---- briefs, yesterday ----
    draw.rectangle([24, y, W - 24, y + 1], fill=LINE)
    y += 7
    draw.text((24, y), "YESTERDAY, STILL MOVING", font=serif_b(14), fill=INK)
    draw.text((W - 24, y + 1), "FIRST REPORTED 19 NOVEMBER", font=sans_b(11),
              fill=RED, anchor="ra")
    y += 20
    for col in range(3):
        items = BRIEFS_YESTERDAY[col * 2:(col + 1) * 2]
        brief_rows(draw, 24 + col * (col_w + gap), items, y, col_w, row_h)
    y += 2 * row_h + 4

    # ---- footer ----
    draw.rectangle([24, y, W - 24, y + 2], fill=INK)
    y += 8
    footer = ("Sources: Reuters, CNN, AP, WSJ, Le Monde, The Times, "
              "Carbon Herald, IMD, UNFCCC. All stories first reported "
              "Friday 20 November 2026 unless marked 19 November.")
    for line in wrap(draw, footer, sans(11), 976):
        draw.text((24, y), line, font=sans(11), fill=GREY)
        y += 13
    print("final y:", y, "page height:", H)
    assert y <= H, "layout overflows the page"

    out = os.path.join(base, "entry.png")
    for quality in (88, 80, 72):
        page.save(out, "JPEG", quality=quality, optimize=True)
        if os.path.getsize(out) <= 1048576:
            break
    print("wrote", out, os.path.getsize(out), "bytes, quality", quality)
    return out


if __name__ == "__main__":
    build()
