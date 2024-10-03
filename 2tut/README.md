# KNN Implementation Tutorial

## Introduction (5-10 minutes)

Good morning, everyone! Today, we're going to implement a K-Nearest Neighbors (KNN) algorithm from scratch. We'll start with a basic implementation and gradually enhance it with type hints, private attributes, and Pydantic integration.

## KNN Overview (20 minutes)

[Briefly explain KNN algorithm, its use cases, and how it works]

- K-Nearest Neighbors is a simple, yet effective classification algorithm
- It works by finding the K nearest neighbors to a given data point and voting on the class
- Key concepts: distance metric, K value, majority voting

Let's dive into the implementation!

## Basic Implementation (30 minutes)

We'll start with a simple implementation without any bells and whistles.

```python
import numpy as np
from collections import Counter

class KNN:
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        predictions = [self._predict(x) for x in X]
        return np.array(predictions)

    def _predict(self, observation):
        distances = [np.sqrt(np.sum((observation - observation_)**2)) for observation_ in self.observations]
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common
```

[Explain each method and its purpose]

Let's test our implementation:

```python
X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
y_train = np.array([0, 0, 1, 1])
X_test = np.array([[2.5, 3.5]])

knn = KNN(k=3)
knn.fit(X_train, y_train)
predictions = knn.predict(X_test)
print(predictions)
```

[Run the code and explain the output]

## Break (5 minutes)

Let's take a quick break. When we return, we'll enhance our implementation.

## Adding Type Hints and Private Attributes (10 minutes)

Now, let's add type hints and private attributes to make our code more robust:

```python
import numpy as np
from collections import Counter
from typing import List, Union

class KNN:
    def __init__(self, k: int = 3):
        self.k = k
        self.__X_train: Union[np.ndarray, None] = None
        self.__y_train: Union[np.ndarray, None] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.__X_train = X
        self.__y_train = y

    def predict(self, X: np.ndarray) -> np.ndarray:
        predictions: List[int] = [self.__predict(x) for x in X]
        return np.array(predictions)

    def __predict(self, x: np.ndarray) -> int:
        distances: List[float] = [np.sqrt(np.sum((x - x_train)**2)) for x_train in self.__X_train]
        k_indices: np.ndarray = np.argsort(distances)[:self.k]
        k_nearest_labels: List[int] = [self.__y_train[i] for i in k_indices]
        most_common: List[tuple] = Counter(k_nearest_labels).most_common(1)
        return most_common
```

[Explain the benefits of type hints and private attributes]

## Integrating Pydantic (15-20 minutes)

Finally, let's use Pydantic to add data validation and improve our class structure:

```python
from pydantic import BaseModel, Field, validator

class KNNConfig(BaseModel):
    k: int = Field(default=3, ge=1)
    
    @validator('k')
    def k_must_be_odd(cls, v):
        if v % 2 == 0:
            raise ValueError('k must be odd')
        return v

class KNN(BaseModel):
    config: KNNConfig
    X_train: Union[np.ndarray, None] = None
    y_train: Union[np.ndarray, None] = None

    class Config:
        arbitrary_types_allowed = True

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.X_train = X
        self.y_train = y

    def predict(self, X: np.ndarray) -> np.ndarray:
        predictions: List[int] = [self._predict(x) for x in X]
        return np.array(predictions)

    def _predict(self, x: np.ndarray) -> int:
        distances: List[float] = [np.sqrt(np.sum((x - x_train)**2)) for x_train in self.X_train]
        k_indices: np.ndarray = np.argsort(distances)[:self.config.k]
        k_nearest_labels: List[int] = [self.y_train[i] for i in k_indices]
        most_common: List[tuple] = Counter(k_nearest_labels).most_common(1)
        return most_common
```

[Explain Pydantic features: data validation, config class, BaseModel]

Let's test our final implementation:

```python
config = KNNConfig(k=3)
knn = KNN(config=config)
knn.fit(X_train, y_train)
predictions = knn.predict(X_test)
print(predictions)
```

[Run the code and explain the output]

## Q&A and Discussion

Now, let's open the floor for any questions or discussions about the implementation or KNN in general.

[Address questions and facilitate discussion]

## Conclusion

Thank you all for your attention and participation. We've seen how to implement KNN from scratch and gradually improve it with Python's advanced features. Remember, this is just a starting point - there's always room for optimization and improvement!