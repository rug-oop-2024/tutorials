import numpy as np
from collections import Counter
from helper import *

class KNN:
    def __init__(self, k=3):
        self.k = k
        self.observations = None
        self.ground_truth = None
        self._parameters = {}

    def fit(self, observations, ground_truth):
        self._parameters = {
            "observations": observations,
            "ground_truth": ground_truth
        }

    def predict(self, observations):
        if self._parameters == {}:
            raise ValueError("Model not fitted. Call 'fit' with appropriate arguments before using 'predict'.")
        
        predictions = [self._predict_single(x) for x in observations]
        return np.array(predictions)

    def _predict_single(self, observation):
        distances = np.linalg.norm(self._parameters["observations"] - observation, axis=1)
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self._parameters["ground_truth"][i] for i in k_indices]
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]


class FruitClassifier(KNN):
    def __init__(self, k=3):
        super().__init__(k)


# Generate some random fruits
fruits, labels, apples, oranges = generate_fruits()

# Create and train the model
fruit_classifier = FruitClassifier(k=3)
fruit_classifier.fit(fruits, labels)

new_fruit = gen_random_fruit()

prediction = fruit_classifier.predict(new_fruit)
print(f"The new fruit is predicted to be: {prediction[0]}")

plot_fruits(apples, oranges, new_fruit, prediction)
