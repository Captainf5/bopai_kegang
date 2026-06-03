---
name: bopai-kegang
description: Designs mobile-first enterprise training course outlines from short briefs. Invoke when users want fast curriculum drafts, industry customization, or direct outline generation from requirements or questionnaires.
---

# BoPai Kegang

Self-contained curriculum design Skill for Claude-style agents.

Use this Skill when the user wants a fast first draft of an enterprise training outline, especially from mobile chat, fragmented requirements, or questionnaire summaries.

This package is designed to be portable:

- no dependency on the original project folders
- can be published as a standalone GitHub folder
- can be copied into Trae or similar Skill-capable agents
- can also serve as a structured prompt pack for Codex-style agents

It includes four layers:

- core Skill files for fast outline generation
- `reference-pack/` for benchmarking and industry adaptation
- `delivery-pack/` for Word, PDF, HTML delivery assets
- `feishu-pack/` for questionnaire-to-brief support

## Use When

- The user wants a half-day, one-day, or multi-day course outline
- The user provides only a short brief and wants a fast draft
- The user needs industry customization such as port, airport, energy, retail, banking, logistics
- The user gives questionnaire text, notes, or table summaries and wants them turned into a course outline
- The user wants a first draft now and refinement later

## Default Mode

- Default to `Type B`: outline from client needs without formal questionnaire analysis
- Default output is `Markdown`
- Default to China-accessible tools first
- Default to “draft first, refine later”
- If non-critical fields are missing, make reasonable assumptions and list them under `待确认项`

## Blocking Questions

Only treat these as blocking:

1. Client or industry
2. Audience or roles
3. Duration
4. Tool or compliance limits

If these four are mostly clear, generate the first draft immediately.

## Execution Checklist

- [ ] Determine `Type A` or `Type B`
- [ ] Compress the input into a short brief
- [ ] Build the module and timing structure
- [ ] Output the full outline in Markdown
- [ ] Add `待确认项`
- [ ] Run quick self-check

Detailed flow: `WORKFLOW.md`

## Progressive Disclosure

Read only what is needed.

- Start with this file
- Read `WORKFLOW.md` for execution steps
- Read `OUTPUT-FORMAT.md` when drafting the final outline
- Read `CHECKLIST.md` before final output
- Read `EXAMPLES.md` only when an industry example or wording style is needed
- Read `reference-pack/` only when stronger customization or benchmarking is needed
- Read `delivery-pack/` only when the user asks for Word, PDF, HTML, or client delivery version
- Read `feishu-pack/` only when the user provides questionnaire or table summaries

Do not assume access to any external project files.

## Writing Rules

- Use client-facing wording, not internal jargon
- Do not expose labels such as “大展宏图”, “BOBO-123”, or “AI First”
- Do not write tea breaks, voting, icebreakers, or workshop operations unless explicitly requested
- Each module should include: `讲解要点` / `演示` / `学员练习` / `产出物`
- Each module should list at most 1 primary tool and 1 backup tool
- For PPT scenarios, prefer `iSlide` and `智谱GLM`

## Mobile-First Behavior

In short-chat or mobile scenarios:

1. Reduce user input into a 6-line brief
2. Generate the full first draft without over-questioning
3. Keep only 3-5 confirmation items at the end
4. Refine specific sections after feedback, not the whole outline

## Brief Template

```text
客户/行业：
学员/岗位：
时长：
目标：
重点模块：
限制：
```

## Output Order

1. 需求摘要
2. 课纲标题
3. 完整课纲 Markdown
4. 待确认项

## Delivery Capability

When the user asks for final delivery:

- use `delivery-pack/scripts/课纲排版toWord带图版.py` to generate Word
- use `delivery-pack/images/` for lecturer, slides, and现场图片
- use `delivery-pack/STYLE-GUIDE-WORD.md` to preserve enterprise-grade formatting
- use `delivery-pack/HTML-CARD-PROMPT.md` when HTML card delivery is preferred
- use `delivery-pack/scripts/docx_to_pdf.py` when PDF output is needed and the environment supports it

Do not skip delivery assets when the request is for a client-facing final file.

## References In This Package

- `WORKFLOW.md`
- `OUTPUT-FORMAT.md`
- `CHECKLIST.md`
- `EXAMPLES.md`
- `reference-pack/`
- `delivery-pack/`
- `feishu-pack/`
