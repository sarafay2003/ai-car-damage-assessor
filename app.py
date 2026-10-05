import streamlit as st
from ultralytics import YOLO
from agent import summarize_detections, generate_estimate
from PIL import Image

st.set_page_config(page_title="AI Car Damage Assessor", page_icon="🚗")

st.title("🚗 AI Car Damage Assessor")
st.write("Upload a photo of car damage to get an instant assessment and repair cost estimate.")

@st.cache_resource
def load_model():
    return YOLO('models/best.pt')

model = load_model()

uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
description = st.text_area("Optional: describe the issue (e.g. 'there's also a rattling noise')", "")

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    with st.spinner("Analyzing damage..."):
        results = model(image)
        findings = summarize_detections(results)
        report = generate_estimate(findings, user_description=description if description else None)

    annotated_image = results[0].plot()  # returns a numpy array with boxes drawn
    st.image(annotated_image, caption="Detected Damage", use_container_width=True)

    st.subheader("Assessment Report")
    st.text(report)