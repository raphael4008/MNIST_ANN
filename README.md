# MNIST Digit Classifier from Scratch using NumPy

**A high-performance, production-ready implementation of an Artificial Neural Network for MNIST classification.**

This is a 4th-year university assignment for an Applied Computer Science course. It implements a 3-layer Multi-Layer Perceptron (MLP) using **only NumPy**, with advanced optimizations and comprehensive analysis tools.

---

## 🎯 Key Features

### ✅ **Advanced Architecture**
- **Input Layer:** 784 nodes (28×28 pixel images)
- **Hidden Layer:** 128 nodes with **ReLU** activation
- **Output Layer:** 10 nodes with **Softmax** activation
- **Weight Initialization:** He initialization for stable gradient flow

### ✅ **High-Performance Implementation**
- **Full Vectorization:** 100% vectorized NumPy operations—no Python loops for data processing
- **Float32 Precision:** Optimized memory usage without sacrificing accuracy
- **In-Place Operations:** Efficient gradient updates minimize memory allocation
- **Mini-Batch Training:** SGD with configurable batch sizes for optimal convergence

### ✅ **Training Features**
- **Categorical Cross-Entropy Loss:** Mathematically rigorous loss function
- **Learning Rate Decay:** Adaptive learning rate scheduling per epoch
- **Early Stopping:** Prevents overfitting by monitoring validation loss
- **Validation Monitoring:** 90/10 train/validation split

### ✅ **Comprehensive Analysis**
- **Learning Curves:** Visualize training/validation accuracy and loss over epochs
- **Confusion Matrix:** Detailed per-digit classification analysis
- **Performance Metrics:** Precision, Recall, F1-Score for each digit
- **Misclassification Analysis:** Identify common confusion patterns

---

## 📦 Installation & Setup

### 1. **Clone or Download the Project**
```bash
cd /path/to/Group4_MNIST_ANN
```

### 2. **Create a Virtual Environment (Recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Verify Data Files**
Ensure these files are in the project directory:
- `mnist_train.csv` (60,000 training samples)
- `mnist_test.csv` (10,000 test samples)

If missing, download from [Kaggle MNIST Dataset](https://www.kaggle.com/datasets/oddrationale/mnist-in-csv)

---

## 🚀 Usage

### **Running the Notebook**
```bash
jupyter notebook mnist_ann.ipynb
```

Then run cells sequentially:

1. **Cell 1-3:** Load and preprocess data
2. **Cell 4-5:** Define NeuralNetwork class
3. **Cell 6:** Train the network
4. **Cell 7-8:** Visualize learning curves and sample predictions
5. **Cell 9:** Generate confusion matrix
6. **Cell 10:** Advanced performance analysis

### **Expected Performance**
- **Training Accuracy:** ~98-99%
- **Validation Accuracy:** ~97-98%
- **Training Time:** ~1-2 minutes on standard CPU

---

## 🔬 Technical Highlights

### **Vectorized Forward Propagation**
```
Z¹ = W¹ @ X.T + b¹          [128, batch_size]
A¹ = ReLU(Z¹)               [128, batch_size]
Z² = W² @ A¹ + b²           [10, batch_size]
A² = Softmax(Z²)            [10, batch_size]
```

### **Efficient Backward Propagation**
```
dZ² = A² - Y.T              (Elegant closed-form: combines softmax + cross-entropy derivatives)
dW² = (1/m) × dZ² @ A¹.T
dZ¹ = (W².T @ dZ²) ⊙ ReLU'(Z¹)
```

### **Memory Efficiency**
- Total Parameters: 101,770
- Model Size: ~400 KB (float32)
- Batch Processing: Reduces memory footprint

---

## 📊 Project Structure

```
Group4_MNIST_ANN/
├── mnist_ann.ipynb              # Main notebook
├── mnist_train.csv              # Training data (60K samples)
├── mnist_test.csv               # Test data (10K samples)
├── requirements.txt             # Python dependencies
└── README.md                     # This file
```

---

## 🔐 Cybersecurity Connection: Adversarial Robustness

Understanding neural networks from scratch is crucial for cybersecurity:

- **Adversarial Attacks:** Imperceptible noise added to inputs can cause misclassification
- **Defense Mechanisms:** Understanding the mathematical foundations helps build robust models
- **Model Interpretability:** Knowing exact weights/operations reveals potential attack vectors

By implementing this network from first principles, you gain insights into:
- How small perturbations affect predictions
- Why certain digits are more vulnerable to misclassification
- How to design more resilient classification systems

---

## 📈 Performance Metrics

### Confusion Matrix Interpretation
- **Diagonal:** Correct predictions
- **Off-Diagonal:** Misclassifications
- **Common Issues:** 
  - 4↔9 confusion (similar shapes)
  - 3↔5 confusion (curved digits)

### Per-Class Metrics
| Metric | Formula |
|--------|---------|
| **Precision** | TP / (TP + FP) |
| **Recall** | TP / (TP + FN) |
| **F1-Score** | 2 × (Precision × Recall) / (Precision + Recall) |

---

## 🛠️ Optimization Opportunities

### **CPU-Bound Optimization**
For further speedup on CPU, consider:
1. **NumPy's BLAS/LAPACK:** Already used implicitly in matrix ops
2. **Einstein Summation (`np.einsum`):** For complex tensor operations
3. **Numba JIT Compilation:** Compile hot functions to machine code

### **GPU Acceleration**
To scale to larger networks, consider:
- **CuPy:** Drop-in NumPy replacement for NVIDIA GPUs
- **PyTorch/TensorFlow:** For production deployments

---

## 👥 Team: Group 4

Applied Computer Science Course | University Assignment

---

## 📝 License

This project is provided for educational purposes. Feel free to modify and extend it for learning.

---

## 🤝 Contributing

Want to improve this implementation? Consider:
- Adding L1/L2 regularization
- Implementing batch normalization
- Trying different activation functions
- Building an ensemble of models

Pull requests are welcome!
