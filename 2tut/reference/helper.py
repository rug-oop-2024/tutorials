import numpy as np
import datetime

def generate_fruits():
    # Generate random points for apples and oranges
    np.random.seed(
        int(datetime.datetime.now().timestamp() % 2**32)
    )
    num_samples = 50  # number of samples for each fruit
    # Apples: smaller size, higher color intensity
    apples = np.random.rand(num_samples, 2)
    apples[:, 0] = apples[:, 0] * 3 + 2  # size between 2 and 5
    apples[:, 1] = apples[:, 1] * 3 + 6  # color intensity between 6 and 9
    # Oranges: larger size, lower color intensity
    oranges = np.random.rand(num_samples, 2)
    oranges[:, 0] = oranges[:, 0] * 3 + 6  # size between 6 and 9
    oranges[:, 1] = oranges[:, 1] * 3 + 2  # color intensity between 2 and 5

    fruits = np.vstack((apples, oranges))
    labels = ['Apple'] * num_samples + ['Orange'] * num_samples

    return fruits, labels, apples, oranges

def gen_random_fruit():
    # Predict a new fruit
    new_fruit = np.random.rand(1, 2)
    size = np.random.randint(2, 10)
    color_intensity = np.random.randint(2, 10)
    new_fruit[0, 0] = size
    new_fruit[0, 1] = color_intensity
    return new_fruit

def plot_fruits(apples, oranges, new_fruit, prediction):
    import matplotlib.pyplot as plt

    # Generate the chart
    plt.figure(figsize=(10, 6))

    # Plot apples
    plt.scatter(apples[:, 0], apples[:, 1], color='red', label='Apple', s=100)

    # Plot oranges
    plt.scatter(oranges[:, 0], oranges[:, 1], color='orange', label='Orange', s=100)

    # Plot the new fruit
    plt.scatter(new_fruit[0, 0], new_fruit[0, 1], color='green', label='New Fruit', s=200, marker='*')

    plt.title('Fruit Classification: Apples vs Oranges')
    plt.xlabel('Size')
    plt.ylabel('Color Intensity')
    plt.legend()

    # Add text annotation for the prediction
    plt.annotate(f"Predicted: {prediction[0]}", 
                xy=(new_fruit[0, 0], new_fruit[0, 1]), 
                xytext=(5, 5.5),
                arrowprops=dict(facecolor='black', shrink=0.05))

    plt.grid(False)
    plt.show()
