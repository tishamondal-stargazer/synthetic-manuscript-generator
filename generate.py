
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import textwrap
import json
import re

PROJECT_DIR = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_DIR / "dataset"

SCRIPTS = {
    "Devanagari": {
        "source": PROJECT_DIR / "sources" / "devanagari_md.md",
        "font": str(PROJECT_DIR / "fonts" / "NotoSansDevanagari-Regular.ttf"),
        "folder": "devanagari",
    },
    "Modi": {
        "source": PROJECT_DIR / "sources" / "Modi_md.md",
        "font": str(PROJECT_DIR / "fonts" / "NotoSansModi-Regular.ttf"),
        "folder": "modi",
    },
    "Sharada": {
        "source": PROJECT_DIR / "sources" / "sharada_md.part01",
        "font": str(PROJECT_DIR / "fonts" / "NotoSansSharada-Regular.ttf"),
        "folder": "sharada",
    },
}

WIDTH, HEIGHT = 1200, 1600
IMAGES_PER_SCRIPT = 100
SPLITS = {"train": 85, "validation": 10, "test": 5}
SEED = 42


def load_passages(path):
    lines = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    passages = []
    for line in lines:
        # Keep passages manageable for page layout.
        line = re.sub(r"\s+", " ", line)
        if len(line) <= 220:
            passages.append(line)
        else:
            words = line.split()
            chunk = ""
            for word in words:
                if len(chunk) + len(word) + 1 > 180:
                    if chunk:
                        passages.append(chunk)
                    chunk = word
                else:
                    chunk = f"{chunk} {word}".strip()
            if chunk:
                passages.append(chunk)

    if not passages:
        raise ValueError(f"No usable text found in {path}")

    return passages


def make_paper(seed):
    rng = random.Random(seed)
    base = rng.randint(215, 239)
    image = Image.new("RGB", (WIDTH, HEIGHT), (base, base - 8, base - 25))
    pixels = image.load()

    # Subtle paper grain.
    for y in range(HEIGHT):
        for x in range(WIDTH):
            noise = rng.randint(-8, 8)
            pixels[x, y] = (
                max(0, min(255, base + noise)),
                max(0, min(255, base - 8 + noise)),
                max(0, min(255, base - 25 + noise)),
            )

    draw = ImageDraw.Draw(image, "RGBA")

    # Aged edges and faint stains.
    for _ in range(55):
        x = rng.randint(0, WIDTH - 1)
        y = rng.randint(0, HEIGHT - 1)
        radius = rng.randint(12, 65)
        alpha = rng.randint(5, 22)
        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=(115, 75, 35, alpha),
        )

    # Light horizontal creases.
    for _ in range(5):
        y = rng.randint(80, HEIGHT - 80)
        draw.line((45, y, WIDTH - 45, y + rng.randint(-3, 3)),
                  fill=(100, 70, 40, 28), width=rng.randint(1, 3))

    return image


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def render_folio(script, config, passage, index, split, seed):
    rng = random.Random(seed)
    image = make_paper(seed)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(config["font"], 42)
    small_font = ImageFont.truetype(config["font"], 27)

    margin_x = 115
    top = 180
    max_width = WIDTH - 2 * margin_x

    # Decorative page border.
    draw.rectangle(
        (55, 55, WIDTH - 55, HEIGHT - 55),
        outline=(105, 72, 38),
        width=3,
    )

    # Folio title and number.
    draw.text((margin_x, 90), f"MANUSCRIPT - {script.upper()}", font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 24), fill=(105, 55, 30))
    draw.text((WIDTH - 220, 90), f"Folio {index + 1:03d}",
              font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 24),
              fill=(105, 55, 30))

    lines = wrap_text(draw, passage, font, max_width)
    y = top

    # Keep a margin for the footer; avoid text overflow.
    max_body_lines = max(1, (HEIGHT - 300 - top) // 58)
    for line in lines[:max_body_lines]:
        ink = rng.choice([
            (55, 35, 25),
            (72, 42, 28),
            (83, 50, 33),
        ])
        draw.text((margin_x, y), line, font=font, fill=ink)
        y += 58

    # Small side annotation.
    annotation = "✦"
    draw.text((WIDTH - 125, top + 80), annotation,
              font=small_font, fill=(125, 65, 35))

    # Subtle blur to soften digital edges.
    image = image.filter(ImageFilter.GaussianBlur(radius=0.25))

    return image, lines[:max_body_lines]


def create_dataset(test_only=False):
    rng = random.Random(SEED)

    for script, config in SCRIPTS.items():
        passages = load_passages(config["source"])
        rng.shuffle(passages)

        if test_only:
            split_plan = {"test": 2}
        else:
            split_plan = SPLITS

        passage_index = 0

        for split, count in split_plan.items():
            out_dir = DATASET_DIR / config["folder"] / split
            out_dir.mkdir(parents=True, exist_ok=True)

            for local_index in range(count):
                passage = passages[passage_index % len(passages)]
                passage_index += 1

                global_index = (
                    sum(split_plan[s] for s in list(split_plan)[:list(split_plan).index(split)])
                    + local_index
                )

                image, rendered_lines = render_folio(
                    script, config, passage, global_index, split,
                    SEED + global_index + passage_index
                )

                stem = f"{config['folder']}_{global_index + 1:03d}"
                image_path = out_dir / f"{stem}.png"
                md_path = out_dir / f"{stem}.md"

                image.save(image_path)

                annotation = f"""---
script: {script}
split: {split}
image: {image_path.name}
source_file: {config['source'].name}
generator: Synthetic Manuscript Generator
---

# Folio {global_index + 1:03d}

## Source text

{passage}

## Rendered lines

""" + "\n".join(f"- {line}" for line in rendered_lines)

                md_path.write_text(annotation, encoding="utf-8")

                print("Created:", image_path.name)


if __name__ == "__main__":
    create_dataset(test_only=False)
