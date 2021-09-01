import os
import time

import moviepy.editor as moviepy
import tensorflow as tf
from django.conf import settings

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import flags
from . import utils as utils
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags_framework = 'tf'

flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags_weights = "./checkpoints/custom-416"

flags.DEFINE_integer('size', 416, 'resize images to')
flags_size = 416

flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags_tiny = False

flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags_model = 'yolov4'

flags.DEFINE_string('video', './data/video/video.mp4', 'path to input video 0 or set to 1  for webcam')
flags_video = 0

flags.DEFINE_string('output', None, 'path to output video')

flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags_output_format = 'XVID'

flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags_iou = 0.45

flags.DEFINE_float('score', 0.25, 'score threshold')
flags_score = 0.25

flags.DEFINE_boolean('dont_show', False, 'dont show video output')
flags_dont_show = False

count = 0

f = open(os.path.join(settings.BASE_DIR, "streamapp/demofile.txt"),
         "r")
count = int(f.read())
count = count + 1

f = open(os.path.join(settings.BASE_DIR, "streamapp/demofile.txt"),
         "w")
f.write(str(count))
f.close()
global output
output = os.path.join(settings.BASE_DIR, "streamapp/detections/results" + str(count) + ".avi")
mp4_output = os.path.join(settings.BASE_DIR, "streamapp/static/streamapp/results" + str(count) + ".mp4")

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(flags_tiny, flags_model)
input_size = 416
video_path = flags_video
out = None
saved_model_loaded = tf.saved_model.load(
    os.path.join(settings.BASE_DIR, "streamapp/checkpoints/custom-416"),
    tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']


class Model(object):
    def __init__(self):
        video1 = "C:/Users/Muhammad Ahsan/Desktop/seq4.avi"
        video2 = "C:/Users/Muhammad Ahsan/Desktop/v2.mp4"

        self.vid = cv2.VideoCapture(0)
        if output:
            # by default VideoCapture returns float instead of int
            width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.vid.get(cv2.CAP_PROP_FPS))
            codec = cv2.VideoWriter_fourcc(*flags_output_format)
            global out
            out = cv2.VideoWriter(output, codec, fps, (width, height))

    def __del__(self):
        # converting saved avi video to mp4
        out.release()
        if output:
            clip = moviepy.VideoFileClip(output)
            clip.write_videofile(mp4_output)

        # close all windows

        cv2.destroyAllWindows()

    def get_frame(self):

        while True:
            return_value, frame = self.vid.read()
            if return_value:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
            else:
                print('Video has ended or failed, try a different video format!')
                break

            frame_size = frame.shape[:2]
            image_data = cv2.resize(frame, (input_size, input_size))
            image_data = image_data / 255.
            image_data = image_data[np.newaxis, ...].astype(np.float32)
            start_time = time.time()

            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

            boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
                boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
                scores=tf.reshape(
                    pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                max_output_size_per_class=50,
                max_total_size=50,
                iou_threshold=flags_iou,
                score_threshold=flags_score
            )

            pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]

            image, b = utils.draw_bbox(frame, pred_bbox)

            fps = 1.0 / (time.time() - start_time)
            print("FPS: %.2f" % fps)
            result = np.asarray(image)
            result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #saving frames to make video
            if output:
                out.write(result)
            ret, jpeg = cv2.imencode('.jpg', result)
            return jpeg.tobytes(), b
