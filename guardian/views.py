from django.http import HttpResponse, FileResponse, StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt
from email.message import EmailMessage
from ultralytics import YOLO
import cv2
import tempfile
import threading
import smtplib
import os

# Create your views here.
def index(request):
	return render(request, "guardian/index.html")

@csrf_exempt
def upload_video(request):
    if (request.method == "POST"):
        file = request.FILES["file"]
        
        knife_detected = False\
        
        with tempfile.NamedTemporaryFile(suffix=".mp4") as temp:
            temp.write(file.read())

            # Handle the file upload
            cap = cv2.VideoCapture(temp.name)
            
            # Check if the file is a video
            if not cap.isOpened():
                return HttpResponse("File is not a video")
            
            model = YOLO('best.pt')
            results = model.predict(temp.name, device='mps')
            
            for result in results:
                for box in result.boxes:
                    prob = 0

                    for x in box.conf:
                        prob = float(x)

                        if (prob > 0.5):
                            for c in box.cls:
                                if(result.names[int(c)] == "knife"):
                                    print("Knife detected " +str(prob))
                                    knife_detected = True
                            
            if knife_detected:
                send_email()
                print("Email sent")
            
            cap.release()

            response = FileResponse(open(temp.name, 'rb'))
            response['knife_detected'] = knife_detected
            return response

def send_email():
    message = EmailMessage()
    message['Subject'] = 'Knife Detected'
    message['From'] = os.environ['EMAIL_FROM']
    message['To'] = os.environ['EMAIL_TO']
    message.set_content('Faca Detectada')
    
    server = smtplib.SMTP(os.environ['SMTP_HOST'], os.environ['SMTP_PORT'])
    server.starttls()
    server.login(os.environ['SMTP_LOGIN'], os.environ['SMTP_PASSWORD'])
    server.send_message(message)
    server.quit()
    return True
    
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
    
    def __del__(self):
        self.video.release()
        
    def get_frame(self):
        image = self.frame
        return image
    
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera, model):
    while True:
        knife_detected = True
        frame = camera.get_frame()
        results = model.predict(frame, device='mps')
        for result in results:
            for box in result.boxes:
                prob = 0

                for x in box.conf:
                    prob = float(x)

                    if (prob > 0.5):
                        for c in box.cls:
                            if(result.names[int(c)] == "knife"):
                                frame = result.plot()
                                knife_detected = True
            
        _, jpeg = cv2.imencode('.jpg', frame)     
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@gzip.gzip_page
def stream(request):
    try:
        model = YOLO('best.pt')
        response = StreamingHttpResponse(gen(VideoCamera(), model), content_type="multipart/x-mixed-replace;boundary=frame")
        return response
    except HttpResponseServerError as e:
        print("aborted")