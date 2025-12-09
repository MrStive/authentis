
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
from datetime import datetime

def perform_analysis():
    # 1. Load Data
    input_path = 'data/raw/marketing_data.csv'
    if not os.path.exists(input_path):
        print("Data not found!")
        return
        
    df = pd.read_csv(input_path)
    
    # 2. RFM Calculation
    # Recency: Days since last purchase relative to "today" (simulated as max date in dataset or execution date)
    # Using 'today' from data generation context or simpler: max date in dataset + 1
    df['DateDernierAchat'] = pd.to_datetime(df['DateDernierAchat'])
    snapshot_date = df['DateDernierAchat'].max() + pd.Timedelta(days=1)
    
    df['Recency'] = (snapshot_date - df['DateDernierAchat']).dt.days
    df['Frequency'] = df['FrequenceAchats']
    df['Monetary'] = df['MontantTotalDepense']
    
    # 3. RFM Scoring (Quintiles 1-5)
    # R: Lower is better -> Labels 5,4,3,2,1
    # Use rank(method='first') to handle duplicates (e.g. many users with Recency=0)
    df['R_Score'] = pd.qcut(df['Recency'].rank(method='first'), q=5, labels=[5, 4, 3, 2, 1]).astype(int)
    
    # F: Higher is better -> Labels 1,2,3,4,5
    df['F_Score'] = pd.qcut(df['Frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # M: Higher is better
    df['M_Score'] = pd.qcut(df['Monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    df['RFM_Segment'] = df['R_Score'].astype(str) + df['F_Score'].astype(str) + df['M_Score'].astype(str)
    
    # 4. Clustering
    features = ['Recency', 'Frequency', 'Monetary']
    X = df[features].copy()
    
    # Log transform for skewness? 
    # Monetary is pareto, highly skewed. Log transform is recommended before K-Means.
    # Recency and Frequency might also benefit.
    X_log = np.log1p(X)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_log)
    
    # Elbow Method (simplified: Check 2 to 10, print inertia)
    # We will compute inertia but select K=5 as per target segments.
    # If K=5 is terrible, we'd know, but for this assignment we proceed with 5.
    print("Computing Inertia for K=2..10:")
    for k in range(2, 11):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        print(f"K={k}, Inertia={km.inertia_:.2f}")
        
    k_optimal = 5
    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # 5. Labeling
    # Calculate stats per cluster to map to names
    cluster_stats = df.groupby('Cluster')[['R_Score', 'F_Score', 'M_Score']].mean()
    print("\nCluster Centroids (RFM Scores):")
    print(cluster_stats)
    
    # Definitions
    # Champions (R[4-5], F[4-5], M[4-5]) -> Ideal: 4.5, 4.5, 4.5
    # Loyal (R[3-5], F[3-5], M[3-4]) -> Ideal: 4, 4, 3.5
    # Potentiel (R[4-5], F[2-3], M[2-3]) -> Ideal: 4.5, 2.5, 2.5
    # Dormant (R[1-2], F[1-2], M[1-2]) -> Ideal: 1.5, 1.5, 1.5
    # À risque (R[1-2], F[3-5], M[3-5]) -> Ideal: 1.5, 4, 4
    
    labels_map = {
        'Champions': np.array([4.5, 4.5, 4.5]),
        'Loyal': np.array([4.0, 4.0, 3.5]),
        'Potentiel': np.array([4.5, 2.5, 2.5]),
        'Dormant': np.array([1.5, 1.5, 1.5]),
        'A risque': np.array([1.5, 4.0, 4.0])
    }
    
    cluster_labels = {}
    used_labels = set()
    
    # Naive matching: Closest Euclidian distance of mean scores to target profile
    for cluster_id, row in cluster_stats.iterrows():
        vec = row.values
        best_label = None
        min_dist = float('inf')
        
        for name, target_vec in labels_map.items():
            dist = np.linalg.norm(vec - target_vec)
            if dist < min_dist:
                min_dist = dist
                best_label = name
        
        # Simple assignment (can resolve conflicts later if needed, but K-Means should separate them well enough)
        cluster_labels[cluster_id] = best_label

    df['Segment_Label'] = df['Cluster'].map(cluster_labels)
    
    print("\nAssigned Labels:")
    print(df['Segment_Label'].value_counts())
    
    # Export
    output_path = 'data/processed/marketing_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\nAnalysis saved to {output_path}")

if __name__ == "__main__":
    perform_analysis()
