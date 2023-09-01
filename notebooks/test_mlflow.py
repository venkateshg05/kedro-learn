"""Trains and evaluate a simple MLP
on the Reuters newswire topic classification task.
"""
import numpy as np, os
from tensorflow import keras
from tensorflow.keras.datasets import reuters
from tensorflow.keras.layers import Activation, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer

# The following import and function call are the only additions to code required
# to automatically log metrics and parameters to MLflow.
import mlflow
from datetime import datetime

# mlflow.tensorflow.autolog()

mlflow.log_artifact(local_path=os.path.join("data", "01_raw", "ds-11.csv"))
max_words = 1000
batch_size = 32
epochs = 3

print("Loading data...")
(x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=max_words, test_split=0.2)

print(len(x_train), "train sequences")
print(len(x_test), "test sequences")

num_classes = np.max(y_train) + 1
print(num_classes, "classes")

print("Vectorizing sequence data...")
tokenizer = Tokenizer(num_words=max_words)
x_train = tokenizer.sequences_to_matrix(x_train, mode="binary")
x_test = tokenizer.sequences_to_matrix(x_test, mode="binary")
print("x_train shape:", x_train.shape)
print("x_test shape:", x_test.shape)

print("Convert class vector to binary class matrix (for use with categorical_crossentropy)")
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

print("Building model...")
model = Sequential()
model.add(Dense(512, input_shape=(max_words,)))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation("softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

history = model.fit(
    x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.1
)
mlflow.tensorflow.log_model(
    model=model, 
    artifact_path=os.path.join("data", "06_models") #../data/06_models
    )
score = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)
print("Test score:", score[0])
print("Test accuracy:", score[1])

mlflow.log_metric("Test score", score[0])
mlflow.log_metric("Test accuracy", score[1])
mlflow.log_param("time of prediction", str(datetime.now()))
mlflow.set_tag("modeltag", 2023)