from ultralytics import YOLO

model = YOLO('yolov8n.pt')
# model.train(
#     data='Car_damage_detection-3/data.yaml',
#     epochs=50,
#     imgsz=640,
#     batch=8
# )

model.train(
    data='Car_damage_detection-3/data.yaml',
    epochs=1,
    imgsz=640,
    batch=8
)