---
name: tone
description: Author, rewrite, and review course transcripts in transcript/ using the KodeFood teleprompter teaching voice. Use every time the user asks to create, draft, update, edit, or review any lecture transcript, video script, demo script, or lab runbook.
---

# Course Transcript Tone & Teleprompter Guide

Apply this skill **every time** you create or edit a transcript under `transcript/`. Detailed before/after examples and section nuances live in [tone.md](tone.md).

## 1. Core Persona & Voice

- **Primary persona (Sections 001–008):** A calm senior platform engineer guiding a junior engineer through one real production problem — **KodeFood** (processing vendor menu photos into captions and `accepted`/`rejected` catalog decisions on AWS Batch with GPUs).
- **Section 009 variation:** A concise magazine-explainer voice — one clear global through-line (supply chain, power, geopolitics, regulations, economics) that still reconnects to the KodeFood Batch job (`RUNNABLE` in Tokyo, Spot capacity, scale-to-zero).
- **Gradual build-up ("Why" before "What"):** Never open with dry definitions, service manuals, or config fields. Start with a practical question, operational symptom, or scaling tension in the first 15–20 seconds, explain *why* the problem exists and how real companies think about it, and only then introduce the AWS mechanism.

## 2. Strict Boundary by Lecture Type

**Videos teach the thinking. Demos show the doing. Labs let the learner do it themselves.**

| Type | Purpose | Rules |
|------|---------|-------|
| `Video` | Concept, *why*, architecture, company reality, tradeoffs, diagnostic mental model | **No line-by-line code explanation.** **No CLI command narration.** Minimize raw identifiers, env vars, and long resource names in spoken lines — say *"the job script"*, *"the input prefix"*, *"the output CSV"*, *"the job role"* unless the exact token is the lesson itself (`RUNNABLE`, `descriptions.csv`, `12288` vs `16384` MiB). |
| `Demo` | Instructor console/code walkthrough | Include `## Teaching goal`, `## Before you record`, `## Demo script (spoken flow)`, `## What not to do in this demo`, and `## Checkpoint for students`. |
| `Lab` | Learner hands-on runbook | Include `## Lab goal`, `## Prerequisites`, `## Steps`, `## Deliverable`, `## Cleanup`, and `## Common issues`. |

## 3. Teleprompter & Pacing Rules

1. **Runtime & word count ceiling (never cross 4 minutes):**
   - Standard `Video` (`~2 minutes`): **220–300 spoken words** (at ~130 wpm).
   - Denser architecture or comparison `Video` (`~3 minutes`): **300–380 spoken words** (hard max: 420 words).
2. **Breathable paragraph layout:**
   - Keep paragraphs to **2–4 lines** with **one idea per paragraph**.
   - Avoid long comma chains and multi-clause sentences.
3. **Dynamic vocal cadence (avoid flat reading):**
   - Mix medium setup sentences (12–20 words) with short, punchy contrast lines that create natural vocal emphasis on a teleprompter:
     - *"One folder in. One result out."*
     - *"If there is no container yet, there is no application failure yet."*
     - *"That is a data-contract problem, not a GPU problem."*
   - Never stack a queue name, job definition, env var, and CLI command into a single spoken breath.

## 4. The 5-Beat `Video` Script Flow

Structure every `Video` transcript around these five beats (without rigid headings in the spoken body):

1. **Hook / Question (first 15–20s):** Connect softly from the previous lecture and pose a "why" question or real operational symptom (*"Why separate storage logic from GPU processing at all?"* / *"When a Batch job feels slow, the first question is not 'is Python slow?'"*).
2. **Slow Build & Tradeoff:** Walk through the naive path vs. what changes at scale. Explain the reasoning before naming the mechanism.
3. **How It's Done in a Company (Diagnostic Lens + Industry Anchor):**
   - Explain what breaks in production and how engineers isolate the fault layer (data path vs. model path; orchestrator vs. host vs. workload IAM; placement vs. runtime).
   - Include **at most one learner prediction or diagnostic check** per script (*"Let's make one prediction..."*, *"Notice that the application has not started yet."*).
   - In **~50% of scripts** (where backed by a link in `Further reading`), weave in **1 short industry anchor sentence** using the right company/system name for that topic (e.g., **DoorDash** for catalog/menu imagery quality, **Uber / Michelangelo** for separating storage/compute or small retryable tasks, **Netflix** for offline batch scoring, **Airbnb / Bighead** for storage lineage). State it as a natural pattern or public engineering reference — never as an academic citation dump or unverified claim.
4. **Core Mental Model:** Distill the lesson into one crisp operating principle or analogy (e.g., *recipe = job definition, one run = job, line = queue, kitchen = compute environment*).
5. **Varied Forward Handoff:** Bridge cleanly into the next lecture, demo, or lab. **Never** use repetitive closings like *"That's it here for..."*. Rotate between a forward question, a one-line takeaway + next step, or a direct demo/lab handoff.

## 5. Required Markdown Template

### `Video` Transcript Template

```markdown
# Video <NNN> — <Lecture Title>

**Section:** <NNN> — <Section Name>
**Lecture#:** <NNN>
**Sheet title:** <Exact Lecture Name from CSV>
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** <30-char topic code from CSV>

---

<Spoken teleprompter script: 6–10 short paragraphs, 220–300 words, no subheadings in spoken body>

---

## Further reading (not spoken)

- [<Source Title>](<https://...>) — <short note on what this backs>
- [<Source Title>](<https://...>) — <short note on what this backs>
```

## 6. Pre-Finish Checklist

Before saving any transcript:
- [ ] Spoken word count is **220–300 words** (~2 min) or **300–380 words** (~3 min), well under 4 minutes.
- [ ] Opens with a "why" question, tension point, or symptom within the first 2 paragraphs.
- [ ] Contains **no** line-by-line code explanations or CLI command readouts in `Video` scripts.
- [ ] Includes a "how companies really operate / debug this" lens.
- [ ] Paragraphs are 2–4 lines each and pass a single-take read-aloud check.
- [ ] Closing transitions naturally to the next lecture without formulaic *"That's it here..."* phrasing.
- [ ] `## Further reading (not spoken)` includes 2–4 real links supporting the technical and industry claims.
