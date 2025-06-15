import numpy as np
import joblib

class KeyPointClassifier(object):
    def __init__(self, model_path=r'keypoint_classifier_rf.joblib'):
        self.model = joblib.load(model_path)

    def __call__(self, landmark_list):

        result_index = self.model.predict([landmark_list])[0]

        return result_index
