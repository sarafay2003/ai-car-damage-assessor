# from ultralytics import YOLO
#
# model = YOLO('models/best.pt')
# results = model('bus.jpg')
# results[0].show()

#from ultralytics import YOLO
#
# model = YOLO('models/best.pt')
# results = model('Car_damage_detection-3/valid/images/SOME_IMAGE_NAME.jpg')
# results[0].show()

from ultralytics import YOLO

model = YOLO('models/best.pt')
results = model('Car_damage_detection-3/valid/images/003305_jpg.rf.6aadc1f0ab75b72eac663254c1a4630c.jpg')
results[0].show()