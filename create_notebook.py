import json


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }

cells = [
    md("""# MNIST ANN From Scratch (NumPy Only)

This notebook is a complete assignment submission for building and analyzing a simple Artificial Neural Network (ANN) on MNIST CSV data using **NumPy only**.

## What we will learn
- What **inputs (784)**, **hidden nodes**, **weights**, **learning rate**, and **epochs** are
- How **forward pass** and **backpropagation** update work
- How to track **accuracy per epoch** (learning curve)
- How changing **hidden nodes** and **initialization scale** affects accuracy and speed

## Rule
- No PyTorch / TensorFlow / Keras
"""),
    code("""import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mnist_ann import NeuralNetwork, one_hot_encode, train_val_split, normalize_pixels

np.random.seed(42)
plt.style.use('seaborn-v0_8-whitegrid')
print('Libraries loaded. Seed fixed to 42.')
"""),
    md("""## Data Loading (CSV or ZIP)

This cell supports either direct CSV files or zipped CSV files:
- `mnist_train.csv` or `mnist_train.csv.zip`
- `mnist_test.csv` or `mnist_test.csv.zip`

Each row format:
- Column 0: label (0-9)
- Columns 1..784: grayscale pixel values (0-255)
"""),
    code("""ROOT = Path('.')

def resolve_csv(csv_name: str, zip_name: str) -> Path:
    csv_path = ROOT / csv_name
    zip_path = ROOT / zip_name

    if csv_path.exists():
        return csv_path

    if zip_path.exists():
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(ROOT)
        if csv_path.exists():
            return csv_path

    raise FileNotFoundError(f'Could not find {csv_name} or {zip_name}')

def load_mnist_csv(path: Path) -> pd.DataFrame:
    # Read raw then drop optional header row like: label,pixel1,...
    df = pd.read_csv(path, header=None)
    first_value = str(df.iloc[0, 0]).strip().lower()
    if 'label' in first_value:
        df = df.iloc[1:].reset_index(drop=True)
    return df

train_csv = resolve_csv('mnist_train.csv', 'mnist_train.csv.zip')
test_csv = resolve_csv('mnist_test.csv', 'mnist_test.csv.zip')

train_df = load_mnist_csv(train_csv)
test_df = load_mnist_csv(test_csv)

# Handle CSVs that include a header row like: label,pixel1,...
if str(train_df.iloc[0, 0]).lower() == 'label':
    train_df = train_df.iloc[1:].reset_index(drop=True)
if str(test_df.iloc[0, 0]).lower() == 'label':
    test_df = test_df.iloc[1:].reset_index(drop=True)

print(f'Train shape: {train_df.shape}')
print(f'Test shape:  {test_df.shape}')
"""),
    code("""# Robust cleaning: keep only rows with numeric labels
train_label_num = pd.to_numeric(train_df.iloc[:, 0], errors='coerce')
test_label_num = pd.to_numeric(test_df.iloc[:, 0], errors='coerce')

train_df = train_df[train_label_num.notna()].reset_index(drop=True)
test_df = test_df[test_label_num.notna()].reset_index(drop=True)

train_data = train_df.values
test_data = test_df.values

y_train_raw = train_data[:, 0].astype(np.int64)
X_train_raw = train_data[:, 1:].astype(np.float32)
y_test_raw = test_data[:, 0].astype(np.int64)
X_test_raw = test_data[:, 1:].astype(np.float32)

X_train_all = normalize_pixels(X_train_raw)
X_test = normalize_pixels(X_test_raw)

Y_train_all = one_hot_encode(y_train_raw, num_classes=10)
Y_test = one_hot_encode(y_test_raw, num_classes=10)

X_train, Y_train, X_val, Y_val = train_val_split(X_train_all, Y_train_all, val_ratio=0.1, seed=42)

print('X_train:', X_train.shape, 'Y_train:', Y_train.shape)
print('X_val:  ', X_val.shape, 'Y_val:  ', Y_val.shape)
print('X_test: ', X_test.shape, 'Y_test: ', Y_test.shape)
"""),
    md("""## Core ANN Concepts

- **Inputs (784):** each MNIST image is 28x28 pixels, flattened to 784 features.
- **Hidden nodes:** number of neurons in the hidden layer. More nodes can model more complex patterns but increase compute cost.
- **Weights:** learnable parameters connecting neurons; they store what the network learns.
- **Learning rate (`lr`):** step size for weight updates.
- **Epochs:** one full pass through all training samples.

Forward pass equations:

$$
Z_1 = W_1 X + b_1,\quad A_1 = ReLU(Z_1)
$$
$$
Z_2 = W_2 A_1 + b_2,\quad \hat{Y} = Softmax(Z_2)
$$

Backprop update idea:
1. Compute prediction error at output.
2. Propagate that error backwards through weights.
3. Compute gradients for each parameter.
4. Update parameters with gradient descent.
"""),
    code("""BASE_INPUT = 784
BASE_HIDDEN = 128
BASE_OUTPUT = 10
BASE_LR = 0.01
BASE_EPOCHS = 12
BASE_BATCH = 128
BASE_INIT_SCALE = 1.0

model = NeuralNetwork(
    input_size=BASE_INPUT,
    hidden_size=BASE_HIDDEN,
    output_size=BASE_OUTPUT,
    init_scale=BASE_INIT_SCALE,
    seed=42,
)

history = model.fit(
    X_train,
    Y_train,
    X_val,
    Y_val,
    epochs=BASE_EPOCHS,
    learning_rate=BASE_LR,
    batch_size=BASE_BATCH,
    verbose=True,
)

print('Baseline training finished.')
print(f'Best val acc: {max(history.val_acc):.4f}')
print(f'Average epoch time: {np.mean(history.epoch_seconds):.2f}s')
"""),
    code("""fig, axes = plt.subplots(1, 3, figsize=(18, 4))

axes[0].plot(history.epochs, history.train_acc, marker='o', label='Train Acc')
axes[0].plot(history.epochs, history.val_acc, marker='s', label='Val Acc')
axes[0].set_title('Accuracy per Epoch')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()

axes[1].plot(history.epochs, history.train_loss, marker='o', label='Train Loss')
axes[1].plot(history.epochs, history.val_loss, marker='s', label='Val Loss')
axes[1].set_title('Loss per Epoch')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Cross-Entropy Loss')
axes[1].legend()

axes[2].plot(history.epochs, history.epoch_seconds, marker='d', color='tab:purple')
axes[2].set_title('Epoch Time (Speed)')
axes[2].set_xlabel('Epoch')
axes[2].set_ylabel('Seconds')

plt.tight_layout()
plt.show()
"""),
    code("""def confusion_matrix_np(y_true, y_pred, num_classes=10):
    cm = np.zeros((num_classes, num_classes), dtype=np.int64)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
    return cm

y_test_pred = model.predict(X_test)
y_test_true = np.argmax(Y_test, axis=1)
test_acc = np.mean(y_test_pred == y_test_true)
print(f'Test accuracy: {test_acc:.4f}')

cm = confusion_matrix_np(y_test_true, y_test_pred, num_classes=10)

plt.figure(figsize=(7, 6))
plt.imshow(cm, cmap='Blues')
plt.title('Confusion Matrix (Test)')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.colorbar()
plt.xticks(range(10))
plt.yticks(range(10))
plt.tight_layout()
plt.show()
"""),
    code("""def run_experiment(hidden_size=128, init_scale=1.0, lr=0.01, epochs=8, batch_size=128, seed=42):
    exp_model = NeuralNetwork(
        input_size=784,
        hidden_size=hidden_size,
        output_size=10,
        init_scale=init_scale,
        seed=seed,
    )
    exp_history = exp_model.fit(
        X_train,
        Y_train,
        X_val,
        Y_val,
        epochs=epochs,
        learning_rate=lr,
        batch_size=batch_size,
        verbose=False,
    )
    return {
        'hidden_size': hidden_size,
        'init_scale': init_scale,
        'lr': lr,
        'batch_size': batch_size,
        'best_val_acc': float(np.max(exp_history.val_acc)),
        'last_val_acc': float(exp_history.val_acc[-1]),
        'avg_epoch_sec': float(np.mean(exp_history.epoch_seconds)),
        'final_train_acc': float(exp_history.train_acc[-1]),
    }, exp_history
"""),
    code("""hidden_sizes = [32, 64, 128, 256]
rows_hidden = []

for hs in hidden_sizes:
    row, _ = run_experiment(hidden_size=hs, init_scale=1.0, lr=0.01, epochs=8, batch_size=128, seed=42)
    rows_hidden.append(row)

hidden_df = pd.DataFrame(rows_hidden).sort_values('hidden_size').reset_index(drop=True)
hidden_df
"""),
    code("""fig, ax = plt.subplots(1, 2, figsize=(12, 4))

ax[0].plot(hidden_df['hidden_size'], hidden_df['best_val_acc'], marker='o')
ax[0].set_title('Hidden Size vs Best Val Accuracy')
ax[0].set_xlabel('Hidden Nodes')
ax[0].set_ylabel('Best Val Accuracy')

ax[1].plot(hidden_df['hidden_size'], hidden_df['avg_epoch_sec'], marker='s', color='tab:orange')
ax[1].set_title('Hidden Size vs Avg Epoch Time')
ax[1].set_xlabel('Hidden Nodes')
ax[1].set_ylabel('Seconds / Epoch')

plt.tight_layout()
plt.show()
"""),
    code("""init_scales = [0.25, 0.5, 1.0, 2.0]
rows_init = []

for s in init_scales:
    row, _ = run_experiment(hidden_size=128, init_scale=s, lr=0.01, epochs=8, batch_size=128, seed=42)
    rows_init.append(row)

init_df = pd.DataFrame(rows_init).sort_values('init_scale').reset_index(drop=True)
init_df
"""),
    code("""fig, ax = plt.subplots(1, 2, figsize=(12, 4))

ax[0].plot(init_df['init_scale'], init_df['best_val_acc'], marker='o')
ax[0].set_title('Init Scale vs Best Val Accuracy')
ax[0].set_xlabel('Initialization Scale')
ax[0].set_ylabel('Best Val Accuracy')

ax[1].plot(init_df['init_scale'], init_df['avg_epoch_sec'], marker='s', color='tab:green')
ax[1].set_title('Init Scale vs Avg Epoch Time')
ax[1].set_xlabel('Initialization Scale')
ax[1].set_ylabel('Seconds / Epoch')

plt.tight_layout()
plt.show()
"""),
    code("""batch_sizes = [32, 64, 128, 256]
learning_rates = [0.001, 0.01, 0.05]
rows_speed = []

for bs in batch_sizes:
    for lr in learning_rates:
        row, _ = run_experiment(hidden_size=128, init_scale=1.0, lr=lr, epochs=6, batch_size=bs, seed=42)
        rows_speed.append(row)

speed_df = pd.DataFrame(rows_speed).sort_values(['batch_size', 'lr']).reset_index(drop=True)
speed_df
"""),
    code("""pivot_acc = speed_df.pivot(index='batch_size', columns='lr', values='best_val_acc')
pivot_time = speed_df.pivot(index='batch_size', columns='lr', values='avg_epoch_sec')

fig, ax = plt.subplots(1, 2, figsize=(13, 4))

im1 = ax[0].imshow(pivot_acc.values, aspect='auto', cmap='viridis')
ax[0].set_title('Best Val Accuracy Heatmap')
ax[0].set_xlabel('Learning Rate')
ax[0].set_ylabel('Batch Size')
ax[0].set_xticks(range(len(pivot_acc.columns)), labels=[str(c) for c in pivot_acc.columns])
ax[0].set_yticks(range(len(pivot_acc.index)), labels=[str(i) for i in pivot_acc.index])
plt.colorbar(im1, ax=ax[0])

im2 = ax[1].imshow(pivot_time.values, aspect='auto', cmap='magma_r')
ax[1].set_title('Avg Epoch Time Heatmap (s)')
ax[1].set_xlabel('Learning Rate')
ax[1].set_ylabel('Batch Size')
ax[1].set_xticks(range(len(pivot_time.columns)), labels=[str(c) for c in pivot_time.columns])
ax[1].set_yticks(range(len(pivot_time.index)), labels=[str(i) for i in pivot_time.index])
plt.colorbar(im2, ax=ax[1])

plt.tight_layout()
plt.show()
"""),
    md("""## Report (Short Answers)

### 1) What are inputs (784), hidden nodes, weights, learning rate, and epochs?
- **Inputs (784):** flattened pixel features for each 28x28 image.
- **Hidden nodes:** neurons in the hidden layer that learn intermediate patterns (edges, curves, digit parts).
- **Weights:** learned numeric strengths of connections; they encode what the model has learned.
- **Learning rate:** update step size for gradient descent.
- **Epochs:** number of full passes over the training set.

### 2) How do forward pass and backprop update work?
- Forward pass computes predictions layer by layer: affine transform -> ReLU -> affine transform -> softmax.
- Backprop computes gradients of loss w.r.t. each parameter using chain rule.
- Parameters are updated by gradient descent: $\\theta \\leftarrow \\theta - \\eta \\nabla_\\theta L$.

### 3) How do we track accuracy per epoch (learning curve)?
- After each epoch, evaluate train/validation accuracy and append to history arrays.
- Plot accuracy vs epoch to see whether the model is learning, plateauing, overfitting, or underfitting.

### 4) Effect of hidden nodes on accuracy and speed
- Increasing hidden nodes often improves best accuracy up to a point.
- Too many hidden nodes increase epoch time and may show diminishing returns.

### 5) Effect of initialization scale on accuracy
- Very small scales can slow learning (weak activations/gradients).
- Very large scales can destabilize learning.
- Moderate scale near He initialization (1.0 multiplier here) is usually most stable.

### 6) Speed considerations summary
- Larger batch size usually gives faster epochs (fewer updates), but too large can reduce generalization.
- Learning rate too small is slow to converge; too large can overshoot. A middle value often works best.
"""),
    md("""## Final Conclusions

- A NumPy-only ANN can reach strong MNIST performance while keeping full mathematical transparency.
- Learning curves are essential for understanding training behavior, not just final accuracy.
- Hidden size and initialization scale materially affect both accuracy and speed.
- Practical model design is a trade-off between compute budget (time) and predictive performance.

### Optional screenshot checklist
- Learning curve plot (accuracy/loss)
- Hidden-size comparison plot
- Init-scale comparison plot
- Speed heatmaps
"""),
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.13"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = "/home/bantu/Documents/MNIST_ANN/mnist_ann.ipynb"
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print(out)
print("cells", len(cells))
