# Workflow

## Goal

Turn a short requirement into a usable enterprise training outline with as few dialogue rounds as possible.

## Step 1: Determine Type

- `Type A`: the user provides questionnaire results, learner data, or structured survey findings
- `Type B`: the user provides only business needs, industry direction, or training goals

Default to `Type B` unless strong questionnaire evidence exists.

## Step 2: Capture Minimum Inputs

Prioritize only these:

- client or industry
- audience or roles
- duration
- tool or compliance limits

If they are mostly clear, stop asking and continue.

## Step 3: Build a Short Brief

Compress the information to:

```text
客户/行业：
学员/岗位：
时长：
目标：
重点模块：
限制：
```

## Step 4: Create the Skeleton

Use four client-facing sections inside the course agenda:

1. AI趋势与业务场景
2. 核心工具实战
3. 工作流与成果串联
4. 落地行动与总结

The four sections must stay in this order.

## Step 5: Allocate Time

- Trend section: 10-15%
- Tool practice section: 40-50%
- Workflow section: 20-30%
- Landing and action section: 10-15%

Adjust by duration, but keep the overall balance.

## Step 6: Industry Adaptation

Replace generic content with real business scenes from the user's industry.

Good industry adaptation should include:

- 3 or more real tasks from the target industry
- tools that fit compliance and device constraints
- outputs that learners can actually take away

When needed, benchmark against one or two files from `reference-pack/`, not the whole folder.

## Step 7: Draft the Output

Follow `OUTPUT-FORMAT.md`.

Required output order:

1. 需求摘要
2. 课纲标题
3. 完整课纲 Markdown
4. 待确认项

## Step 8: Produce Delivery Files

If the user needs final delivery:

- create Word with `delivery-pack/scripts/课纲排版toWord带图版.py`
- keep style aligned with `delivery-pack/STYLE-GUIDE-WORD.md`
- use `delivery-pack/images/` so the document remains client-ready
- if PDF is required, run `delivery-pack/scripts/docx_to_pdf.py` where supported
- if HTML card delivery is preferred, follow `delivery-pack/HTML-CARD-PROMPT.md`

## Step 9: Refine After Feedback

When the user replies with more details, update only the affected parts:

- course positioning
- industry cases
- tool stack
- time allocation
- outputs and preparation

## Step 10: Questionnaire Branch

If the user provides a questionnaire, use `feishu-pack/` to normalize the brief before revising the outline.
