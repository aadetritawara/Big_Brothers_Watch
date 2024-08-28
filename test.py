import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

model_path = 'blaze_face_short_range.tflite'

BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
FaceDetectorResult = mp.tasks.vision.FaceDetectorResult
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: FaceDetectorResult, output_image: mp.Image, timestamp_ms: int):
    if result.detections:
        x_value = get_x_value(result)
        print(f"X-coordinate of detected face: {x_value}")
    else:
        print("No face detected.")

options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

def get_x_value(detection_result):
    for detection in detection_result.detections:
        x = detection.bounding_box.origin_x + (detection.bounding_box.width/2)
        return x

with FaceDetector.create_from_options(options) as detector:
    cam = cv2.VideoCapture(1)  # Use the default webcam
    
    while cam.isOpened():
        success, img = cam.read()
        if not success:
            print("Failed to read frame")
            break

        # Convert the frame received from OpenCV to a MediaPipe’s Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        
        # Get the current time in milliseconds
        frame_timestamp_ms = int(time.time() * 1000)
        
        # Perform face detection asynchronously
        detector.detect_async(mp_image, frame_timestamp_ms)

        # Display the frame in an OpenCV window
        cv2.imshow('Video Feed', img)

        # Check for 'Esc' key press to exit
        if cv2.waitKey(1) == 27:
            print("Esc key pressed. Exiting loop...")
            break

    cam.release()
    cv2.destroyAllWindows()
