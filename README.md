# Synthetic Manuscript Generator

A Python project that generates synthetic manuscript-style images and Markdown annotations.

## Dataset

This project contains 300 generated images across three scripts:
- Devanagari: 100 images
- Modi: 100 images
- Sharada: 100 images

Each script is split into:
- Train: 85 images
- Validation: 10 images
- Test: 5 images

Each image has a corresponding Markdown annotation.

## Features

- Synthetic manuscript-style page generation
- Aged-paper appearance
- Traditional page border
- Script-specific text
- PNG images with Markdown annotations

## Folder Structure

```text
dataset/
  devanagari/
    train/
    validation/
    test/
  modi/
    train/
    validation/
    test/
  sharada/
    train/
    validation/
    test/
```

Each split folder contains PNG images and matching Markdown files.

## Run

Run the generator from the project directory:

```bash
python generate.py
```

## Validation

The generated dataset was checked for expected split counts and valid PNG files.
Total: 300 images and 300 Markdown annotations.

## Note

This is a synthetic dataset for experimentation and research. It is not a collection of historical manuscript scans.