import os
from ultralytics import YOLO

model = YOLO('best.pt')
results = model.predict('image.png', device=os.environ['device'])

# Process results list
for result in results:
    result.save(filename="teste.jpg")
    