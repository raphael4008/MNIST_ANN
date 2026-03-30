"""MNIST ANN (NumPy-only)

A lightweight educational implementation of a 1-hidden-layer neural network
for MNIST-like tabular pixel inputs (784 features, 10 classes).
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class TrainHistory:
    epochs: List[int]
    train_loss: List[float]
    train_acc: List[float]
    val_loss: List[float]
    val_acc: List[float]
    epoch_seconds: List[float]


class NeuralNetwork:
    """Simple 784 -> hidden -> 10 ANN with ReLU + Softmax."""

    def __init__(
        self,
        input_size: int = 784,
        hidden_size: int = 128,
        output_size: int = 10,
        init_scale: float = 1.0,
        seed: Optional[int] = 42,
    ) -> None:
        if seed is not None:
            np.random.seed(seed)

        self.input_size = int(input_size)
        self.hidden_size = int(hidden_size)
        self.output_size = int(output_size)

        he_std_1 = np.sqrt(2.0 / self.input_size) * init_scale
        he_std_2 = np.sqrt(2.0 / self.hidden_size) * init_scale

        self.W1 = (np.random.randn(self.hidden_size, self.input_size) * he_std_1).astype(np.float32)
        self.b1 = np.zeros((self.hidden_size, 1), dtype=np.float32)
        self.W2 = (np.random.randn(self.output_size, self.hidden_size) * he_std_2).astype(np.float32)
        self.b2 = np.zeros((self.output_size, 1), dtype=np.float32)

        self.dW1 = np.zeros_like(self.W1)
        self.db1 = np.zeros_like(self.b1)
        self.dW2 = np.zeros_like(self.W2)
        self.db2 = np.zeros_like(self.b2)

        self.Z1: Optional[np.ndarray] = None
        self.A1: Optional[np.ndarray] = None
        self.Z2: Optional[np.ndarray] = None
        self.A2: Optional[np.ndarray] = None

    @staticmethod
    def relu(z: np.ndarray) -> np.ndarray:
        return np.maximum(0.0, z)

    @staticmethod
    def relu_derivative(z: np.ndarray) -> np.ndarray:
        return (z > 0).astype(np.float32)

    @staticmethod
    def softmax(z: np.ndarray) -> np.ndarray:
        z_shifted = z - np.max(z, axis=0, keepdims=True)
        exp_scores = np.exp(z_shifted)
        return exp_scores / np.sum(exp_scores, axis=0, keepdims=True)

    def forward(self, x: np.ndarray) -> np.ndarray:
        x_t = x.T.astype(np.float32, copy=False)
        self.Z1 = self.W1 @ x_t + self.b1
        self.A1 = self.relu(self.Z1)
        self.Z2 = self.W2 @ self.A1 + self.b2
        self.A2 = self.softmax(self.Z2)
        return self.A2

    def cross_entropy_loss(self, y_hat: np.ndarray, y_onehot: np.ndarray) -> float:
        m = y_onehot.shape[0]
        y_t = y_onehot.T.astype(np.float32, copy=False)
        eps = 1e-12
        return float(-np.sum(y_t * np.log(y_hat + eps)) / m)

    @staticmethod
    def get_predictions(y_hat: np.ndarray) -> np.ndarray:
        return np.argmax(y_hat, axis=0)

    @staticmethod
    def get_accuracy(predictions: np.ndarray, y_onehot: np.ndarray) -> float:
        true_labels = np.argmax(y_onehot, axis=1)
        return float(np.mean(predictions == true_labels))

    def backward(self, x: np.ndarray, y_onehot: np.ndarray) -> None:
        if self.A2 is None or self.A1 is None or self.Z1 is None:
            raise RuntimeError("Call forward() before backward().")

        m = x.shape[0]
        y_t = y_onehot.T.astype(np.float32, copy=False)

        dZ2 = self.A2 - y_t
        self.dW2 = (dZ2 @ self.A1.T) / m
        self.db2 = np.sum(dZ2, axis=1, keepdims=True) / m

        dA1 = self.W2.T @ dZ2
        dZ1 = dA1 * self.relu_derivative(self.Z1)
        self.dW1 = (dZ1 @ x.astype(np.float32, copy=False)) / m
        self.db1 = np.sum(dZ1, axis=1, keepdims=True) / m

    def update_parameters(self, learning_rate: float) -> None:
        lr = np.float32(learning_rate)
        self.W1 -= lr * self.dW1
        self.b1 -= lr * self.db1
        self.W2 -= lr * self.dW2
        self.b2 -= lr * self.db2

    def predict(self, x: np.ndarray) -> np.ndarray:
        y_hat = self.forward(x)
        return self.get_predictions(y_hat)

    def evaluate(self, x: np.ndarray, y_onehot: np.ndarray) -> Tuple[float, float]:
        y_hat = self.forward(x)
        loss = self.cross_entropy_loss(y_hat, y_onehot)
        acc = self.get_accuracy(self.get_predictions(y_hat), y_onehot)
        return loss, acc

    def fit(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        x_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 20,
        learning_rate: float = 0.01,
        batch_size: int = 128,
        shuffle: bool = True,
        verbose: bool = True,
    ) -> TrainHistory:
        n = x_train.shape[0]

        history = TrainHistory(
            epochs=[],
            train_loss=[],
            train_acc=[],
            val_loss=[],
            val_acc=[],
            epoch_seconds=[],
        )

        for epoch in range(1, epochs + 1):
            t0 = time.perf_counter()

            if shuffle:
                idx = np.random.permutation(n)
                x_epoch = x_train[idx]
                y_epoch = y_train[idx]
            else:
                x_epoch = x_train
                y_epoch = y_train

            for start in range(0, n, batch_size):
                end = min(start + batch_size, n)
                xb = x_epoch[start:end]
                yb = y_epoch[start:end]

                y_hat = self.forward(xb)
                _ = self.cross_entropy_loss(y_hat, yb)
                self.backward(xb, yb)
                self.update_parameters(learning_rate)

            train_loss, train_acc = self.evaluate(x_train, y_train)
            val_loss, val_acc = self.evaluate(x_val, y_val)
            dt = time.perf_counter() - t0

            history.epochs.append(epoch)
            history.train_loss.append(train_loss)
            history.train_acc.append(train_acc)
            history.val_loss.append(val_loss)
            history.val_acc.append(val_acc)
            history.epoch_seconds.append(dt)

            if verbose:
                print(
                    f"Epoch {epoch:02d}/{epochs} | "
                    f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} | "
                    f"val_loss={val_loss:.4f} val_acc={val_acc:.4f} | "
                    f"time={dt:.2f}s"
                )

        return history


def one_hot_encode(labels: np.ndarray, num_classes: int = 10) -> np.ndarray:
    labels = labels.astype(np.int64)
    out = np.zeros((labels.shape[0], num_classes), dtype=np.float32)
    out[np.arange(labels.shape[0]), labels] = 1.0
    return out


def train_val_split(
    x: np.ndarray,
    y: np.ndarray,
    val_ratio: float = 0.1,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    np.random.seed(seed)
    n = x.shape[0]
    idx = np.random.permutation(n)
    val_n = int(n * val_ratio)

    val_idx = idx[:val_n]
    train_idx = idx[val_n:]

    return x[train_idx], y[train_idx], x[val_idx], y[val_idx]


def normalize_pixels(x: np.ndarray) -> np.ndarray:
    return (x.astype(np.float32) / 255.0).astype(np.float32)


def labels_and_pixels_from_csv_array(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    y = data[:, 0].astype(np.int64)
    x = data[:, 1:].astype(np.float32)
    return y, x
