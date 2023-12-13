# Raspberry Pi Motion Detection and Email Notification

This Python script is designed to run on a Raspberry Pi, using a motion sensor and PiCamera to detect motion, capture images, and send email notifications if a person is detected in the captured images using computer vision.

## Functionality Overview

### Hardware Components
- Utilizes a motion sensor connected to GPIO pin 17.
- Controls the Raspberry Pi Camera to capture images.

### Libraries Used
- `gpiozero`: Interfacing with the motion sensor.
- `picamera`: Access and control of the Raspberry Pi Camera.
- `time`: Handling time-related functionalities.
- `smtplib`, `email.mime`: Sending emails and constructing email content.
- `imutils`, `cv2` (OpenCV): Image processing and computer vision tasks.

### Components Initialization
- Initializes the motion sensor and camera.
- Configures camera rotation and manages captured images.

### Email Configuration
- Sets up email credentials for sender and receiver.
- Defines subject and body content for email notifications.

### Human Detection
- Utilizes OpenCV's HOG (Histogram of Oriented Gradients) descriptor for human detection.
- Sets up SVM (Support Vector Machine) detector for identifying people in captured images.

## Directory Structure

### Project Directory
