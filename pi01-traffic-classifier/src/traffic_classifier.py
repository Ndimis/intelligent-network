import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, confusion_matrix
from load_and_preprocess import load_and_preprocess


def train_and_evaluate(X, y, le):
    # 80/20 Split for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    return model, X_test, y_test

if __name__ == "__main__":
    X, y, le, sc = load_and_preprocess('data/network_traffic.csv')
    model, X_test, y_test = train_and_evaluate(X, y, le)
    
    # Save Confusion Matrix Chart
    cm = confusion_matrix(y_test, model.predict(X_test))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
    disp.plot(cmap='Blues')
    plt.title('Traffic Classification Confusion Matrix')
    plt.savefig('docs/confusion_matrix.png')

def save_visualizations(model, X_test, y_test, feature_names, label_names):
    """
    Generates and saves the Confusion Matrix and Feature Importance charts.
    """
    # 1. Save Confusion Matrix
    plt.figure(figsize=(10, 7))
    cm = confusion_matrix(y_test, model.predict(X_test))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_names)
    disp.plot(cmap='Blues')
    plt.title('Traffic Classification: Confusion Matrix')
    plt.savefig('docs/confusion_matrix.png')
    plt.close()

    # 2. Save Feature Importance Chart
    plt.figure(figsize=(10, 7))
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.bar(range(len(importances)), importances[indices], align="center", color='skyblue')
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
    plt.title("Network Feature Importance")
    plt.ylabel("Importance Score")
    plt.tight_layout()
    plt.savefig('docs/feature_importance.png')
    plt.close()
    print("Charts saved to docs/ folder.")

if __name__ == "__main__":
    # Assuming you have the load_and_preprocess function from previous steps
    X, y, le, sc = load_and_preprocess('data/network_traffic.csv')
    
    # Split and Train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Generate charts for the portfolio
    save_visualizations(
        model, 
        X_test, 
        y_test, 
        feature_names=['fwd_max', 'bwd_mean', 'iat_max', 'duration', 'pkt_count'],
        label_names=le.classes_
    )