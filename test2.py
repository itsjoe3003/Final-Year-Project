import cv2
import mediapipe as mp
from controller_test import Controller
import numpy as np

from test import RandomForestClassifier

gest_obj = RandomForestClassifier()




class MainClass():
   
  # mpHands = None
  # hands = None
  # mpDraw = None
   
  # def __init__(self):
  mpHands = mp.solutions.hands
  hands = mpHands.Hands(
              static_image_mode='store_true',
              max_num_hands=2,
              min_detection_confidence=0.7,
              min_tracking_confidence=0.5,
  )
  mpDraw = mp.solutions.drawing_utils

    
  def foo(self):

    cap = cv2.VideoCapture(0)

    while True:
  
      success, img = cap.read()
      img = cv2.flip(img, 1)

      imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      results = self.hands.process(imgRGB)

      if results.multi_hand_landmarks:
          Controller.hand_Landmarks = results.multi_hand_landmarks[0]
          self.mpDraw.draw_landmarks(img, Controller.hand_Landmarks, self.mpHands.HAND_CONNECTIONS)

        #   print(results)
          
          for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
              
              landmark_list = gest_obj.calc_landmark_list(imgRGB, hand_landmarks)
              pre_processed_landmark_list = gest_obj.pre_process_landmark(landmark_list)
              pre_processed_landmark_list = np.array(pre_processed_landmark_list).reshape(1,-1)

              hand_sign_id = gest_obj.predict(pre_processed_landmark_list)[0]

              # print(gest_obj.keypoint_labels[hand_sign_id])
          
              Controller.update_fingers_status()
              Controller.cursor_moving(gest_obj.keypoint_labels[hand_sign_id])
              Controller.detect_scrolling(gest_obj.keypoint_labels[hand_sign_id])
              # Controller.detect_zoomming(gest_obj.keypoint_labels[hand_sign_id])
              Controller.detect_clicking(gest_obj.keypoint_labels[hand_sign_id])
              Controller.detect_dragging(gest_obj.keypoint_labels[hand_sign_id])
      
  # img = cv2.resize(img, (1280, 720))
  # cv2.imshow('Hand Tracker', img)
      if cv2.waitKey(5) & 0xff == 27:
        break







# DragDrop
# rightclick
# leftclick
# doubleclick
# scroll up
# scroll down
# Zoom in 
# Zoom out