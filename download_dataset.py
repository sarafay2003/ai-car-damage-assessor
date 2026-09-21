
from roboflow import Roboflow

rf = Roboflow(api_key="0XTIRiCVokTZykL1Cmfx")
project = rf.workspace("clickits").project("car_damage_detection-zztxm")
version = project.version(3)
dataset = version.download("yolov8")
