# AI Car Damage Assessor — Project Scope

## Overview
A tool that assesses car damage from a photo (and optionally a text description),
then uses an AI agent to generate a repair cost estimate with reasoning.

Users upload an image of damage → a fine-tuned vision model detects and labels
the damage → an agent combines this with any text description the user provides
to produce a written, reasoned estimate.

## Why This Project
- First hands-on experience training a vision model (not just calling an API)
- Distinct from prior RAG/retrieval-based projects — this is detection + reasoning
- Combines multimodal input (image + text) through an agent, built from scratch
  rather than a heavy framework, to demonstrate understanding of agent mechanics

## Tech Stack
- **Vision model:** YOLOv8 (Ultralytics) — fine-tuned on a public car-damage dataset
- **Agent layer:** Custom lightweight agent (function calling, no LangChain/CrewAI)
- **Frontend:** Streamlit
- **Dataset:** Public car-damage dataset (Kaggle / Roboflow Universe), YOLO format

## V1 Scope (must finish)
1. Photo upload → YOLOv8 detection (damage type, location, confidence score)
2. Optional text description field, combined with detection results
3. Custom agent: takes detection output + text → produces a written estimate with reasoning
4. Severity scoring (minor / moderate / major) based on detection output
5. Confidence flagging — low-confidence detections are flagged to the user instead of guessed
6. Streamlit UI — upload photo, enter description, view annotated image + estimate

## Stretch Goals (only after V1 is fully working)
- PDF export of the estimate
- Multi-image support — combine multiple angles of the same damage into one estimate
- Repair vs. replace recommendation from the agent

## Explicitly Out of Scope (for now)
- History / comparison of assessments over time
- Live/real-time pricing API integration
- Any claim of real insurance-grade or professional repair-shop accuracy

## Known Limitations / Notes for README
- Cost estimates are illustrative only, not real repair-shop quotes
- Static/simple price reference data will go stale — not real market pricing
- Not intended for use on real insurance claims or professional assessments
