# Basic severity/cost reference — static for now, can be refined later
DAMAGE_COSTS = {
    "Front-Windscreen-Damage": ("major", 200, 500),
    "Headlight-Damage": ("moderate", 80, 200),
    "Rear-windscreen-Damage": ("major", 200, 450),
    "RunningBoard-Dent": ("minor", 50, 150),
    "Sidemirror-Damage": ("minor", 40, 120),
    "Signlight-Damage": ("minor", 30, 90),
    "Taillight-Damage": ("moderate", 70, 180),
    "bonnet-dent": ("moderate", 150, 400),
    "crack": ("minor", 50, 150),
    "dent": ("minor", 80, 200),
    "doorouter-dent": ("moderate", 150, 350),
    "fender-dent": ("moderate", 120, 300),
    "front-bumper-dent": ("moderate", 100, 300),
    "glass shatter": ("major", 250, 600),
    "lamp broken": ("moderate", 60, 150),
    "medium-Bodypanel-Dent": ("moderate", 150, 350),
    "paint-scratch": ("minor", 30, 100),
    "pillar-dent": ("major", 200, 500),
    "quaterpanel-dent": ("major", 200, 450),
    "rear-bumper-dent": ("moderate", 100, 300),
    "roof-dent": ("major", 250, 600),
    "tire flat": ("minor", 20, 80),
}

CONFIDENCE_THRESHOLD = 0.5  # below this, flag as uncertain

def summarize_detections(results):
    """Takes YOLO results and returns a list of structured findings."""
    findings = []
    boxes = results[0].boxes
    names = results[0].names

    for box in boxes:
        class_id = int(box.cls[0])
        class_name = names[class_id]
        confidence = float(box.conf[0])

        severity, cost_low, cost_high = DAMAGE_COSTS.get(class_name, ("unknown", 0, 0))

        findings.append({
            "type": class_name,
            "confidence": round(confidence, 2),
            "severity": severity,
            "cost_range": (cost_low, cost_high),
            "low_confidence": confidence < CONFIDENCE_THRESHOLD
        })

    return findings


def generate_estimate(findings, user_description=None):
    """Turns structured findings into a written estimate."""
    if not findings:
        return "No damage was detected in this image."

    lines = ["Damage Assessment Report", "=" * 30, ""]

    total_low, total_high = 0, 0

    for f in findings:
        flag = " (low confidence — please confirm)" if f["low_confidence"] else ""
        lines.append(
            f"- {f['type']} ({f['severity']} severity, {int(f['confidence']*100)}% confidence){flag}"
        )
        lines.append(f"  Estimated cost: ${f['cost_range'][0]}–${f['cost_range'][1]}")
        total_low += f['cost_range'][0]
        total_high += f['cost_range'][1]

    lines.append("")
    lines.append(f"Estimated total repair cost: ${total_low}–${total_high}")

    if user_description:
        lines.append("")
        lines.append(f"Additional context provided: \"{user_description}\"")

    lines.append("")
    lines.append("Note: This is an illustrative estimate only, not a real repair quote.")

    return "\n".join(lines)