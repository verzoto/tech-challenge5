from ultralytics import YOLO

model = YOLO('yolo11n.pt')
results = model.train(data='model.yaml', epochs=10, device="mps")