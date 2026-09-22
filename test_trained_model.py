from ultralytics import YOLO

model = YOLO('models/best.pt')
results = model('bus.jpg')
results[0].show()