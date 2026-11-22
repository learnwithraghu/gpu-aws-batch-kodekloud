# Section 04 — Topics Plan

**Section Name:** `04 — Building the ML Menu Satisfaction Scorer`  
*(Alternative concise name: `04 — Automating Menu Photo Review with an ML Scorer`)*

**Scope:** Build and test a minimal ML scoring script (`score_menu.py`) locally against dish photos, apply the `8.0` satisfaction threshold (`APPROVED` vs `REJECTED`), and test reading from S3 before moving this workload onto AWS Batch in Section 05.

## Play order (Theory, Demo, and Lab)

| # | Type | Topic Title | Focus |
|---|------|-------------|-------|
| 001 | Video (Theory) | From Manual 24-Hour Review to Automated Menu Scoring | Why KodeFood replaces manual menu-team checks with an automated photo satisfaction score. |
| 002 | Video (Theory) | How the Menu Satisfaction Model Turns Pixels into a 1–10 Score | Extracting brightness, contrast, and sharpness features from an image and scoring with weights and bias. |
| 003 | Demo | `[Demo]` Building and Running the ML Menu Scorer Locally with `uv` | Walk through `04-menu-scorer/score_menu.py` and run `uv run 04-menu-scorer/score_menu.py` on `images/`. |
| 004 | Video (Theory) | Designing the 8.0 Quality Gate: Approved vs Rejected Decisions | Why threshold selection matters in catalog pipelines and how `< 8.0` rejection messages differ from `>= 8.0` approvals. |
| 005 | Lab | `[Lab]` Score Sample Dish Photos and Tune the 8.0 Threshold Locally | Learners run the scorer locally with `uv`, inspect `< 8.0` vs `>= 8.0` outcomes, and test their own photos. |
| 006 | Video (Theory) | Separating Storage from Scoring: Preparing the Model to Read from S3 | Keeping `score_image()` independent of where image bytes live (local folder vs S3 bucket from Step 03), setting up Step 05 on AWS Batch. |
| 007 | Demo | `[Demo]` Testing the Menu Scorer Against Uploaded S3 Dish Photos (`--s3`) | Run `uv run 04-menu-scorer/score_menu.py --s3` against `kodefood-menu-uploads-kodekloud` and preview the handoff to AWS Batch in Section 05. |

## Topic summaries

1. **Video — From Manual 24-Hour Review to Automated Menu Scoring**  
   Connects directly from Step 03 (photos landing in S3). Explains what slows down manual review and why a fast, consistent ML quality score unblocks restaurant onboarding.

2. **Video — How the Menu Satisfaction Model Turns Pixels into a 1–10 Score**  
   Introduces the minimal ML pipeline in plain terms: resizing to grayscale, measuring three visual signals (brightness, contrast, sharpness), and combining them with learned weights + bias into a `1.0–10.0` score.

3. **`[Demo]` Building and Running the ML Menu Scorer Locally with `uv`**  
   Shows `04-menu-scorer/score_menu.py`, explains how PEP 723 metadata lets `uv run` handle dependencies automatically, and runs the script on the sample photos in `images/` to show both `[REJECTED]` and `[APPROVED]` outputs.

4. **Video — Designing the 8.0 Quality Gate: Approved vs Rejected Decisions**  
   Explains why a continuous ML score needs a clear business decision boundary (`8.0`) and actionable feedback when a dish photo is rejected (`< 8.0`) vs accepted (`>= 8.0`).

5. **`[Lab]` Score Sample Dish Photos and Tune the 8.0 Threshold Locally**  
   Hands-on exercise where students run `uv run 04-menu-scorer/score_menu.py`, test a custom folder of food photos, and observe how changing `THRESHOLD` shifts which photos are approved or rejected.

6. **Video — Separating Storage from Scoring: Preparing the Model to Read from S3**  
   Highlights why `load_local_images()` and `load_s3_images()` feed the exact same `score_image()` function—so moving from a laptop to an AWS Batch container in Section 05 requires zero changes to the scoring logic.

7. **`[Demo]` Testing the Menu Scorer Against Uploaded S3 Dish Photos (`--s3`)**  
   Runs `uv run 04-menu-scorer/score_menu.py --s3` against the S3 bucket created in Step 03 (`kodefood-menu-uploads-kodekloud`) and hands off to Section 05: running this scorer automatically on AWS Batch.
