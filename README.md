# AI Car Damage Assessor

An AI-powered tool that detects visible car damage from a photo and generates an illustrative repair cost estimate, combining a custom fine-tuned computer vision model with a lightweight reasoning agent.

Upload a photo of a damaged car (and optionally describe the issue in your own words), and the app will detect the damage, classify its severity, flag anything it isn't confident about, and produce a written cost estimate.


## Overview

Most car-damage-assessment demos stop at "here's a bounding box." This project goes a step further: a small custom agent sits on top of the vision model's raw output and turns it into something a person can actually read — a structured report with severity levels, per-item cost ranges, a total estimate, and honest flags when the model isn't confident.

This was built as a personal portfolio project to get hands-on experience training a vision model from scratch (rather than only calling a pretrained API) and building a reasoning layer on top of model output, written without a heavy agent framework so the logic stays transparent and inspectable.

## Features

- **Photo-based damage detection** across 22 damage categories (dents, cracks, broken lights, shattered glass, flat tires, and more)
- **Optional text description** — add context the camera can't capture (e.g. "there's also a rattling noise")
- **Severity classification** — minor / moderate / major
- **Confidence flagging** — low-confidence detections are flagged for the user to confirm rather than stated as fact
- **Cost estimation** — a per-item and total illustrative repair cost range
- **Simple web interface** built with Streamlit — no command-line use required to run a scan

## Tech Stack

| Component | Choice | Why |
|---|---|---|
| Vision model | YOLOv8 (Ultralytics) | Fast to train, strong community support, good first real experience training a vision model |
| Agent layer | Custom Python logic | No LangChain/CrewAI — a transparent, hand-written reasoning step over the model's output |
| Frontend | Streamlit | Fast to build, lets the project focus on the model and agent rather than UI plumbing |
| Training | Google Colab (free GPU tier) | Local CPU training was estimated at ~100 hours for the full run; the same run took ~4.4 hours on a free T4 GPU |
| Dataset | [ClickITS Car Damage Detection](https://universe.roboflow.com/clickits/car_damage_detection-zztxm) (Roboflow Universe) | 8,000+ labeled images across 22 damage classes, CC BY 4.0 |

## How It Works

1. **Detection** — the uploaded photo is passed through a YOLOv8 model fine-tuned on the car-damage dataset, which returns bounding boxes, class labels, and confidence scores for each piece of damage found.
2. **Summarization** — `agent.py` converts each raw detection into a structured finding: damage type, severity, confidence, and an estimated cost range (from a static reference table).
3. **Reporting** — the findings are assembled into a readable report, combined with any optional text the user provided, and a total cost range is calculated. Detections below a confidence threshold are explicitly flagged rather than stated as certain.
4. **Display** — the Streamlit app shows the original photo with detection boxes drawn on it, followed by the full written report.

## Results

The model was fine-tuned for 50 epochs on 8,000+ labeled images across 22 damage classes.

| Metric | Score |
|---|---|
| mAP50 | 0.741 |
| Precision | 0.752 |
| Recall | 0.702 |

**Strongest classes** (mAP50 > 0.85): rear windscreen damage, side mirror damage, glass shatter, bonnet dent, door outer dent, pillar dent.

**Weakest classes** (mAP50 < 0.25): generic crack, generic dent, paint scratch.

## Known Limitations

- **Scratches and cracks are under-detected.** These were the most visually subtle damage types in the dataset and likely overlap conceptually with more specific classes. In manual testing, a photo with a clear long scratch down a door panel was misclassified as a low-confidence "tire flat" — the agent correctly flagged it as low-confidence rather than stating it as fact, but the underlying detection was still wrong. This is a dataset/label limitation rather than a pipeline bug, and is left undocumented-fixed intentionally rather than retrained, to keep the project's reported results honest.
- **Cost estimates are illustrative only.** They come from a static reference table, not live market pricing or an actual repair shop quote.
- **Not intended for real insurance claims or professional repair assessments.**

## Getting Started

### Prerequisites

- Python 3.10 or 3.11 recommended
- A trained model file (`best.pt`) — not included in this repo due to size; see [Model Weights](#model-weights) below

### Installation

```bash
git clone https://github.com/sarafay2003/ai-car-damage-assessor.git
cd ai-car-damage-assessor

python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### Model Weights

The trained model (`models/best.pt`) is not committed to this repository. Download it from the [Releases](../../releases) page (or train your own — see below) and place it at:

```
ai-car-damage-assessor/models/best.pt
```

### Running the App

```bash
streamlit run app.py
```

This opens the app in your browser at `localhost:8501`. Upload a photo, optionally add a description, and view the assessment.

### Training Your Own Model (optional)

1. Download the dataset from [Roboflow](https://universe.roboflow.com/clickits/car_damage_detection-zztxm) in YOLOv8 format
2. Run `train.py` (CPU training is impractically slow for this dataset size — a GPU environment such as Google Colab's free tier is strongly recommended)
3. Copy the resulting `best.pt` into `models/`

## Project Structure

```
ai-car-damage-assessor/
├── app.py                  # Streamlit web app
├── agent.py                # Detection → written estimate logic
├── train.py                # Model training script
├── test_trained_model.py   # CLI script for testing the trained model
├── models/                 # Trained model weights (not committed)
├── requirements.txt
├── PROJECT_SCOPE.md         # v1 scope and stretch goals
└── README.md
```

## Project Scope

See [`PROJECT_SCOPE.md`](./PROJECT_SCOPE.md) for the full v1 feature scope, stretch goals, and what was intentionally left out.

## Disclaimer

This is a personal portfolio project. Cost estimates are illustrative and should not be used for real insurance, legal, or professional repair decisions.
