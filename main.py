from gpiozero import MotionSensor
from picamera import PiCamera
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import imutils
import cv2

pir = MotionSensor(17)
camera = PiCamera()
camera.rotation = 0
max_images = 5
image_buffer = []

# Email configuration for Outlook (sender)
sender_email = 'senderemail'  # Change this
sender_password = 'password'  # Change this or use an app-specific password
subject = 'Motion Detected!'
body = 'Motion has been detected. See the attached image.'

# Receiver's email (Gmail)
receiver_email = 'receiveremail'  # Change this

# Initialize HOG descriptor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def send_email(image_filename):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    body_text = MIMEText(body, 'plain')
    msg.attach(body_text)

    # Attach image
    with open(image_filename, 'rb') as image_file:
        image_data = image_file.read()
        image = MIMEImage(image_data, name='motion_image.jpg')
        msg.attach(image)

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)  # Outlook SMTP server and port
        server.starttls()
        server.login(sender_email, sender_password)  # Outlook email credentials
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email failed to send. Error: {e}")
    finally:
        server.quit()

def is_probably_human(frame):
    # Resize the frame for faster processing
    frame = imutils.resize(frame, width=min(400, frame.shape[1]))

    # Detect people in the frame
    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # Check if people are detected
    return len(rects) > 0

while True:
    pir.wait_for_motion()
    print("Motion detected!")

    # Capture image
    filename = "/home/pi/Desktop/" + (time.strftime("%y%b%d_%H:%M:%S")) + ".jpg"
    camera.capture(filename)
    image_buffer.append(filename)

    if len(image_buffer) > max_images:
        oldest_image = image_buffer.pop(0)
        # Optionally, you can delete the oldest image file
        # os.remove(oldest_image)

    # Read the captured image using OpenCV
    img = cv2.imread(filename)

    # Check if a person is detected in the image
    if is_probably_human(img):
        # Send email with the captured image
        send_email(filename)

    pir.wait_for_no_motion()