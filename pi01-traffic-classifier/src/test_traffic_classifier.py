import pytest
import numpy as np
import pandas as pd
import os
# Importing from your newly separated modules
from load_and_preprocess import load_and_preprocess
from traffic_classifier import train_and_evaluate

DATA_PATH = 'data/network_traffic.csv'

@pytest.fixture(scope="module")
def ml_assets():
    """
    Fixture to load data and train the model once for the entire test session.
    """
    if not os.path.exists(DATA_PATH):
        pytest.skip(f"Dataset not found at {DATA_PATH}. Please generate data first.")
    
    # Load and clean data
    X, y, le, sc = load_and_preprocess(DATA_PATH)
    
    # Train and evaluate to get the model
    model, X_test, y_test = train_and_evaluate(X, y, le)
    
    return {
        "model": model,
        "encoder": le,
        "scaler": sc,
        "X_test": X_test
    }

def test_preprocessing_integrity(ml_assets):
    """
    Verify that the scaler and encoder are correctly initialized.
    """
    sc = ml_assets["scaler"]
    le = ml_assets["encoder"]
    
    assert sc.mean_.shape[0] == 5  # Check for 5 features
    assert len(le.classes_) == 3   # Check for IoT, Video, Web

def test_video_traffic_prediction(ml_assets):
    """
    Operational test: Does a high-bandwidth, low-latency signature 
    result in a 'Video' classification?
    """
    model = ml_assets["model"]
    sc = ml_assets["scaler"]
    le = ml_assets["encoder"]

    # Typical Video Signature: [fwd_max, bwd_mean, iat_max, duration, pkt_count]
    # Large packets (1450), fast arrival (0.01s), high count (600)
    raw_input = np.array([[1450, 1100, 0.01, 5.0, 600]])
    
    # Wrap in a DataFrame to keep feature names consistent
    feature_names = ['fwd_max', 'bwd_mean', 'iat_max', 'duration', 'pkt_count']
    df_input = pd.DataFrame(raw_input, columns=feature_names)
    
    # Scale the DataFrame instead of the raw array
    scaled_input = sc.transform(df_input)
    
    pred_idx = model.predict(scaled_input)[0]
    pred_label = le.inverse_transform([pred_idx])[0]
    
    assert pred_label == 'Video'

def test_iot_traffic_prediction(ml_assets):
    """
    Operational test: Does a low-bandwidth, high-latency signature 
    result in an 'IoT' classification?
    """
    model = ml_assets["model"]
    sc = ml_assets["scaler"]
    le = ml_assets["encoder"]

    # Typical IoT Signature: Small packets (64), high idle time (2.5s), low count (5)
    raw_input = np.array([[64, 40, 2.5, 15.0, 5]])
    scaled_input = sc.transform(raw_input)
    
    pred_idx = model.predict(scaled_input)[0]
    pred_label = le.inverse_transform([pred_idx])[0]
    
    assert pred_label == 'IoT'