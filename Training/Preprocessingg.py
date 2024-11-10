import json
from feature_engine.pipeline import Pipeline
from Training.EventDetection import EventDetector
from Training.EventExtraction import EventFeatureExtractor

class PreProcessor:
    def __init__(self):
        pass

    def preprocess(self,data):
        piepln = Pipeline([("Event Detection",EventDetector()),
                          ("Feature Extraction",EventFeatureExtractor())])
        transformed_data = piepln.fit_transform(data)

        return transformed_data