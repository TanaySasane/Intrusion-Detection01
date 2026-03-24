"""
Retrain the Random Forest model using the KDD dataset.
This creates a new model compatible with the current sklearn version.
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# Column names for KDD dataset
columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'rerror_rate',
    'same_srv_rate', 'diff_srv_rate', 'label'
]

print("Loading dataset...")
# Load all class samples
dfs = []
for i in range(5):
    path = f'output_samples/class_{i}_samples.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        dfs.append(df)
        print(f"  class_{i}: {len(df)} samples")

# Also load random distributions
for i in range(1, 4):
    path = f'output_samples/random_distribution_{i}.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        dfs.append(df)
        print(f"  random_distribution_{i}: {len(df)} samples")

# Try loading the full KDD dataset
kdd_path = 'dataset/KDD_DATA.txt'
if os.path.exists(kdd_path):
    print(f"\nLoading full KDD dataset from {kdd_path}...")
    try:
        # KDD dataset has 42 columns, we use first 27 features + label
        all_cols = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
            'num_compromised', 'root_shell', 'su_attempted', 'num_file_creations',
            'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate', 'rerror_rate',
            'same_srv_rate', 'diff_srv_rate',
            'srv_serror_rate', 'srv_rerror_rate', 'same_srv_rate2', 'diff_srv_rate2',
            'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
            'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
            'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
            'dst_host_srv_rerror_rate', 'label', 'difficulty'
        ]
        kdd_df = pd.read_csv(kdd_path, header=None, names=all_cols)
        print(f"  Loaded {len(kdd_df)} rows")
        print(f"  Label distribution:\n{kdd_df['label'].value_counts().head(10)}")

        # Encode categorical columns
        from sklearn.preprocessing import LabelEncoder
        le_protocol = LabelEncoder()
        le_service = LabelEncoder()
        le_flag = LabelEncoder()
        le_label = LabelEncoder()

        kdd_df['protocol_type'] = le_protocol.fit_transform(kdd_df['protocol_type'].astype(str))
        kdd_df['service'] = le_service.fit_transform(kdd_df['service'].astype(str))
        kdd_df['flag'] = le_flag.fit_transform(kdd_df['flag'].astype(str))

        # Map attack types to 5 classes: 0=DoS, 1=Probe, 2=R2L, 3=U2R, 4=normal
        dos_attacks = ['back', 'land', 'neptune', 'pod', 'smurf', 'teardrop', 'apache2',
                       'udpstorm', 'processtable', 'worm', 'mailbomb']
        probe_attacks = ['ipsweep', 'nmap', 'portsweep', 'satan', 'mscan', 'saint']
        r2l_attacks = ['ftp_write', 'guess_passwd', 'imap', 'multihop', 'phf', 'spy',
                       'warezclient', 'warezmaster', 'sendmail', 'named', 'snmpgetattack',
                       'snmpguess', 'xlock', 'xsnoop', 'httptunnel']
        u2r_attacks = ['buffer_overflow', 'loadmodule', 'perl', 'rootkit', 'ps',
                       'sqlattack', 'xterm']

        def map_label(label):
            label = str(label).rstrip('.')
            if label == 'normal':
                return 4
            elif label in dos_attacks:
                return 0
            elif label in probe_attacks:
                return 1
            elif label in r2l_attacks:
                return 2
            elif label in u2r_attacks:
                return 3
            else:
                return 0  # default to DoS for unknown attacks

        kdd_df['label_encoded'] = kdd_df['label'].apply(map_label)

        feature_cols = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
            'num_compromised', 'root_shell', 'su_attempted', 'num_file_creations',
            'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate', 'rerror_rate',
            'same_srv_rate', 'diff_srv_rate'
        ]

        X = kdd_df[feature_cols].values
        y = kdd_df['label_encoded'].values

        print(f"\nTraining on {len(X)} samples with {X.shape[1]} features")
        print(f"Class distribution: {dict(zip(*np.unique(y, return_counts=True)))}")

    except Exception as e:
        print(f"Error loading KDD dataset: {e}")
        print("Falling back to sample data...")
        X, y = None, None
else:
    X, y = None, None

# Fallback to sample data if KDD not available
if X is None:
    print("\nUsing sample data for training...")
    combined = pd.concat(dfs, ignore_index=True)
    feature_cols = [c for c in combined.columns if c != 'label']
    X = combined[feature_cols].values
    y = combined['label'].values
    print(f"Training on {len(X)} samples")

# Train models
print("\nTraining Random Forest Classifier...")
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X, y)
print("  RF training complete!")

print("Training Decision Tree Classifier...")
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X, y)
print("  DT training complete!")

# Save models
os.makedirs('models', exist_ok=True)
with open('models/rf_classifier.pkl', 'wb') as f:
    pickle.dump(rf, f)
print("\nSaved: models/rf_classifier.pkl")

with open('models/dt_classifier.pkl', 'wb') as f:
    pickle.dump(dt, f)
print("Saved: models/dt_classifier.pkl")

# Quick test
test_sample = X[0:1]
pred = rf.predict(test_sample)
print(f"\nTest prediction: {pred} (expected: {y[0]})")
print("\nModels retrained and saved successfully!")
