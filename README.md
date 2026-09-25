
# Synthetic Manuscript Generator

A Python project that generates synthetic manuscript-style images and Markdown annotations in Devanagari, Modi, and Sharada scripts.

The project creates manuscript-style pages with aged-paper textures, decorative borders, script-specific text, and corresponding Markdown annotations.

## Dataset

This project contains 300 generated images across three scripts:

| Script | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| Devanagari | 85 | 10 | 5 | 100 |
| Modi | 85 | 10 | 5 | 100 |
| Sharada | 85 | 10 | 5 | 100 |
| **Total** | **255** | **30** | **15** | **300** |

Each image has a corresponding Markdown annotation containing metadata, source text, and rendered lines.

The generated dataset is publicly available on Hugging Face:

[View the Synthetic Manuscript Generator Dataset](https://huggingface.co/datasets/tisha-mondal/synthetic-manuscript-generator)

## Features

- Synthetic manuscript-style page generation
- Support for Devanagari, Modi, and Sharada scripts
- Aged-paper appearance with subtle texture and stains
- Traditional decorative page borders
- Script-specific fonts
- Variation in ink colour
- PNG images with Markdown annotations
- Separate training, validation, and test splits

## Repository Structure

```text
synthetic-manuscript-generator/
├── fonts/
│   ├── NotoSansDevanagari-Regular.ttf
│   ├── NotoSansModi-Regular.ttf
│   └── NotoSansSharada-Regular.ttf
├── sources/
│   ├── devanagari_md.md
│   ├── Modi_md.md
│   ├── sharada_md.part01
│   ├── sharada_md.part02
│   └── sharada_md.part03
├── generate.py
├── README.md
└── synthetic-manuscript-source.zip
```

The Sharada source text is stored in three parts because of file-size limitations. The generator reads the parts together.

## Generated Dataset Structure

Running the generator creates the following structure:

```text
dataset/
├── devanagari/
│   ├── train/
│   ├── validation/
│   └── test/
├── modi/
│   ├── train/
│   ├── validation/
│   └── test/
└── sharada/
    ├── train/
    ├── validation/
    └── test/
```

Each split folder contains PNG images and matching Markdown annotation files.

## Requirements

- Python 3
- Pillow

Install the required Python library:

```bash
pip install pillow
```

## Run

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Install the required library using the command above.
4. Run the generator:

```bash
python generate.py
```

The generated images and Markdown annotations will be saved in the `dataset/` directory.

## Validation

The generated dataset was checked for the expected split counts and valid PNG files.

- Total images: 300
- Total Markdown annotations: 300
- Images per script: 100
- Train split: 85 images per script
- Validation split: 10 images per script
- Test split: 5 images per script

## Note

This is a synthetic dataset created for experimentation and research. It is not a collection of historical manuscript scans.

## Links

- **GitHub Repository:** https://github.com/tishamondal-stargazer/synthetic-manuscript-generator
- **Hugging Face Dataset:** https://huggingface.co/datasets/tisha-mondal/synthetic-manuscript-generator
