from imutils.video import VideoStream
import imutils, time, cv2

import argparse, sys, serial

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision


# Initialize the video stream and allow the camera sensor to warmup
vs = VideoStream(usePiCamera=1).start()
time.sleep(2.0)

def runML(model: str, camera_id: int, width: int, height: int, num_threads: int, data:dict, stop:list):
    global frame

    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()
  
    # Visualization parameters
    row_size = 22  # pixels
    left_margin = 24  # pixels
    text_color = (128, 0, 255)  # magenta # red
    font_size = 1.2
    font_thickness = 2
    fps_avg_frame_count = 10
  
    # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=model, use_coral=False, num_threads=num_threads)
    detection_options = processor.DetectionOptions(
        max_results=2, score_threshold=0.6)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    while True:
        if stop[0] == True:
            return
        frame = vs.read()

        counter += 1
        image = cv2.flip(frame, 0)
        image = cv2.resize(image, (width,height), interpolation = cv2.INTER_AREA)
    
        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create a TensorImage object from the RGB image.
        input_tensor = vision.TensorImage.create_from_array(rgb_image)

        # Run object detection estimation using the model. 
        # Brain of the operation, causal of 8 FPS.
        detection_result = detector.detect(input_tensor)

        # Draw keypoints and edges on input image
        image, grass_detected, bounding_box = utils.visualize(image, detection_result)

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
          end_time = time.time()
          fps = fps_avg_frame_count / (end_time - start_time)
          start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    font_size, text_color, font_thickness)

        cv2.waitKey(1)
        cv2.imshow('Live cam', image)

        data['Grass Detected'] = grass_detected
        data['Bounding Box'] = bounding_box
        #time.sleep(.1)

        
    #return grass_detected
        
# (Q)uit the program if key is pressed.
def endML():
    cv2.VideoCapture(0).release()
    cv2.destroyAllWindows()

def initML(fp = 'grass0.tflite'):
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default=fp)
  parser.add_argument(
      '--cameraId', help='Id of camera.', 
      required=False, type=int, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640) # SD:640x480 HD:1280x720
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480) # SD:640x480 HD:1280x720
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
  
  return parser.parse_args()

if __name__ == '__main__':
    import utils
    data = {}
    try:
        args = initML()
        runML(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,int(args.numThreads), lock)
        endML()
    except KeyboardInterrupt:
        vs.stop() # release the video stream pointer
else:
    import ml.utils as utils
        
    
