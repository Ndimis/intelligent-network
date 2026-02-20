import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_and_preprocess(path):
    """
    Loads the network dataset, cleans anomalies, and scales features.
    """
    # 1. Load the dataset
    df = pd.read_csv(path)
    
    # 2. Clean data (Handle missing/infinite values common in network captures)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    
    # 3. Label Encoding (Convert 'IoT', 'Video', 'Web' to numbers)
    le = LabelEncoder()
    df['label_enc'] = le.fit_transform(df['label'])
    
    # 4. Feature Selection
    X = df[['fwd_max', 'bwd_mean', 'iat_max', 'duration', 'pkt_count']]
    y = df['label_enc']
    
    # 5. Feature Scaling (Ensures metrics with different units don't bias the model)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, le, scaler