from ultralytics import YOLO

model = YOLO('best.pt')
results = model.predict('image.png', device='mps')

# Process results list
for result in results:
    result.save(filename="teste.jpg")
    