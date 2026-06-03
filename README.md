# BoPai Kegang

Current version: `v1.0.0`

A portable, mobile-first Skill package for generating enterprise training outlines and delivering client-ready Word, PDF, and HTML assets.

This package is extracted as a standalone Skill so it can be:

- published to GitHub as an independent folder or repository
- copied into Trae under `.trae/skills/`
- reused by other Claude-style agents
- used as a structured prompt pack by Codex-style agents

## What Is Included

### Core

- `SKILL.md`: main entry and invocation rules
- `WORKFLOW.md`: execution workflow
- `OUTPUT-FORMAT.md`: client-facing output structure
- `CHECKLIST.md`: quality guardrails
- `EXAMPLES.md`: trigger and industry examples

### Reference Pack

- `reference-pack/经典课纲/`: all classic outlines
- `reference-pack/定制课纲/`: only Huarun and power-related custom outlines

### Delivery Pack

- `delivery-pack/scripts/课纲排版toWord带图版.py`: Markdown to Word with images
- `delivery-pack/scripts/docx_to_pdf.py`: Word to PDF conversion helper
- `delivery-pack/images/`: lecturer, slides, classroom, and device images
- `delivery-pack/STYLE-GUIDE-WORD.md`: Word styling rules
- `delivery-pack/HTML-CARD-PROMPT.md`: HTML card prompt
- `delivery-pack/课纲模板.docx`: Word base template

### Feishu Pack

- `feishu-pack/QUESTIONNAIRE-SKILL.md`
- `feishu-pack/QUESTIONNAIRE-WORKFLOW.md`

## How To Use In Trae

Copy this folder to:

```text
.trae/skills/bopai-kegang/
```

Then let the agent invoke the Skill when users ask for:

- enterprise training outlines
- industry-customized course agendas
- questionnaire-to-outline conversion
- final Word or PDF delivery files

## How To Use In Codex-Style Agents

Codex does not use the exact same Skill mechanism, but this package still works well as a prompt bundle:

1. Use `SKILL.md` as the main system or task instruction
2. Read `WORKFLOW.md` and `OUTPUT-FORMAT.md` during drafting
3. Read `reference-pack/` when stronger customization is needed
4. Read `delivery-pack/` when final delivery files are required

## Word And PDF Delivery

Install dependencies:

```bash
pip install -r delivery-pack/requirements.txt
```

Generate Word:

```bash
python delivery-pack/scripts/课纲排版toWord带图版.py --input "your-outline.md"
```

Generate PDF:

```bash
python delivery-pack/scripts/docx_to_pdf.py --input "your-outline_带图.docx"
```

## Publish To GitHub

Recommended repository name:

```text
bopai-kegang
```

Recommended publish path:

```text
portable-skills/bopai-kegang
```

If you want, this folder can be published:

- as a standalone GitHub repository
- as a subfolder inside an existing repository

## Notes

- This package is intentionally self-contained and does not require the original PC-side project folders
- It preserves delivery capability by bundling scripts, images, and style rules
- It preserves benchmarking capability by bundling selected reference outlines
