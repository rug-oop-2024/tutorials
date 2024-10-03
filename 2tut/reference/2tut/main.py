import numpy as np
from collections import Counter

class KNN:
    def __init__(self, k=3):
        self.k = k
        self.observations = None
        self.ground_truth = None
        self._parameters = {}

    def fit(self, observations, ground_truth):
        self.observations = observations
        self.ground_truth = ground_truth
        self._parameters = {
            "observations": observations,
            "ground_truth": ground_truth
        }

    def predict(self, observations):
        predictions = [self._predict_single(x) for x in observations]
        return predictions

    def _predict_single(self, observation):
        # TODO: predict a single point
        # steps:
        # step1: calc distance between observation and ever other point
        distances = np.linalg.norm(self._parameters["observations"] - observation, axis=1)
        # step2: sort the array of the distances and take first k
        k_indices = np.argsort(distances)[:self.k]
        # step3: check the label aka ground truth of those points
        k_nearest_labels = [self._parameters["ground_truth"][i] for i in k_indices]
        #### now we have k =3, 3 labels inside an array ####
        # step4: take most common label and return it to the caller
        most_common = Counter(k_nearest_labels).most_common()
        return most_common[0][0]

class FruitClassifier(KNN):
    def __init__(self, k=3):
        super().__init__(k)

