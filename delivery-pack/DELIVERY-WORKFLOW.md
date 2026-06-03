# Delivery Workflow

## Goal

Turn the final Markdown outline into client-ready delivery assets.

## Included Assets

- `STYLE-GUIDE-WORD.md`: enterprise Word styling rules
- `HTML-CARD-PROMPT.md`: HTML card delivery prompt
- `公文写作规范.md`: backup writing rules for formal client scenarios
- `课纲模板.docx`: base Word template
- `images/`: lecturer, slides, and training scene images
- `scripts/课纲排版toWord带图版.py`: Markdown to Word with images
- `scripts/docx_to_pdf.py`: Word to PDF helper

## Word Delivery

From the package root:

```bash
python delivery-pack/scripts/课纲排版toWord带图版.py --input "your-outline.md"
```

This generates:

```text
your-outline_带图.docx
```

## PDF Delivery

If the environment supports `docx2pdf` and has Word conversion capability:

```bash
python delivery-pack/scripts/docx_to_pdf.py --input "your-outline_带图.docx"
```

This generates:

```text
your-outline_带图.pdf
```

## HTML Delivery

If the user wants a shareable or screenshot-friendly format, follow:

- `HTML-CARD-PROMPT.md`

## Notes

- Keep `images/` beside the script folder so image insertion works
- Word generation depends on `python-docx`
- PDF generation depends on `docx2pdf` and a supported local environment
