from ultralytics import YOLO
import gradio as gr
from PIL import Image

model = YOLO("best.pt")

def predict(image):
    results = model(image, conf=0.25)
    result = results[0]

    names = model.names
    boxes = result.boxes

    disease_detected = False

    if boxes is not None and len(boxes) > 0:
        for cls in boxes.cls:
            class_name = names[int(cls)]
            if "Unhealthy" in class_name:
                disease_detected = True
                break

    # IMPORTANT FIX HERE
    if disease_detected:
        output_img = result.plot()   # numpy array (BGR)
        output_img = Image.fromarray(output_img[..., ::-1])  # convert BGR → RGB
        status = "⚠️ Disease Detected"
    else:
        output_img = image
        status = "✅ Healthy Plant"

    return output_img, status


demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs=[
        gr.Image(type="pil"),
        gr.Textbox()
    ],
    title="Plant Disease Detector"
)

demo.launch()
