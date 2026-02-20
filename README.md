# 🛰️ Project 01: Multi-Feature Traffic Classifier (v2.0)

## 📊 Pipeline Overview

This project processes a 2,000-row network traffic dataset using a complete ML pipeline:

1. **Standardization:** Normalizing feature scales using `StandardScaler`.
2. **Validation:** Evaluating model performance via an 80/20 train/test split.
3. **Visualization:** Generating model interpretability charts.

## 📉 Evaluation Summary

The model demonstrates high precision across all three traffic categories (IoT, Video, Web).

### Confusion Matrix

(Include the `confusion_matrix.png` here)
The matrix shows zero misclassifications, confirming that the statistical features chosen (IAT and Packet Length) are highly discriminative for these classes.

### Feature Importance

The most critical feature for classification was found to be **IAT_Max**, which effectively separates "bursty" IoT traffic from "constant" video streams.
