import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage

def visualize_pca_projection(df: pd.DataFrame, numerical_features: list, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes a 2D PCA projection of scaled numerical features.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(5000, len(df)))
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_sample)
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(scaled_data)
        ax.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.5, s=1)
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})')
        ax.set_title('PCA Projection', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'PCA failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()



def visualize_tsne_projection(df: pd.DataFrame, numerical_features: list, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes a 2D t-SNE projection of scaled numerical features.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(5000, len(df)))
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_sample)
        tsne = TSNE(n_components=2, random_state=42, perplexity=30)
        tsne_result = tsne.fit_transform(scaled_data[:1000])
        ax.scatter(tsne_result[:, 0], tsne_result[:, 1], alpha=0.5, s=1)
        ax.set_xlabel('t-SNE 1')
        ax.set_ylabel('t-SNE 2')
        ax.set_title('t-SNE Projection', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 't-SNE failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def visualize_kmeans_clustering(df: pd.DataFrame, numerical_features: list, k: int = 4, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes K-Means clustering results on a 2D PCA projection of scaled numerical features.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <k> (int): Number of clusters for K-Means (default: 4).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(5000, len(df)))
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_sample)
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(scaled_data)
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(scaled_data)
        ax.scatter(pca_result[:, 0], pca_result[:, 1], c=labels, cmap='Set1', alpha=0.5, s=1)
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_title(f'K-Means (k={k})', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'K-Means failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def visualize_dbscan_clustering(df: pd.DataFrame, numerical_features: list, eps: float = 0.5, min_samples: int = 5, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes DBSCAN clustering results on a 2D PCA projection of scaled numerical features.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <eps> (float): The maximum distance between two samples for DBSCAN (default: 0.5).
    <min_samples> (int): The number of samples in a neighborhood for DBSCAN (default: 5).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(5000, len(df)))
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_sample)
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        db_labels = dbscan.fit_predict(scaled_data)
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(scaled_data)
        ax.scatter(pca_result[:, 0], pca_result[:, 1], c=db_labels, cmap='Set2', alpha=0.5, s=1)
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_title('DBSCAN Clustering', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'DBSCAN failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def visualize_pca_scree_plot(df: pd.DataFrame, numerical_features: list, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the explained variance ratio for PCA components using a scree plot.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(5000, len(df)))
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_sample)
        pca_full = PCA()
        pca_full.fit(scaled_data)
        ax.plot(range(1, 7), pca_full.explained_variance_ratio_[:6], 'bo-')
        ax.set_xlabel('Component')
        ax.set_ylabel('Explained Variance Ratio')
        ax.set_title('PCA Scree Plot', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'Scree plot failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def visualize_silhouette_scores(df: pd.DataFrame, numerical_features: list, k_range: range = range(2, 8), output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes silhouette scores for different numbers of K-Means clusters.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <k_range> (range): Range of cluster numbers to evaluate (default: range(2, 8)).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(5000, len(df)))
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_sample)
        silhouette_scores = []
        for k in k_range:
            km = KMeans(n_clusters=k, random_state=42)
            labels = km.fit_predict(scaled_data)
            score = silhouette_score(scaled_data, labels)
            silhouette_scores.append(score)
        ax.plot(k_range, silhouette_scores, 'go-')
        ax.set_xlabel('Number of Clusters')
        ax.set_ylabel('Silhouette Score')
        ax.set_title('Optimal Cluster Selection', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'Silhouette failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def visualize_pca_feature_importance(df: pd.DataFrame, numerical_features: list, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the feature importance for the first PCA component using a bar plot.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(5000, len(df)))
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_sample)
        pca = PCA(n_components=1)
        pca.fit(scaled_data)
        feature_importance = np.abs(pca.components_[0])
        ax.bar(range(len(numerical_features)), feature_importance)
        ax.set_xticks(range(len(numerical_features)))
        ax.set_xticklabels(numerical_features, rotation=45)
        ax.set_ylabel('Importance')
        ax.set_title('PC1 Feature Importance', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'Feature importance failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def visualize_hierarchical_dendrogram(df: pd.DataFrame, numerical_features: list, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes a hierarchical clustering dendrogram for scaled numerical features.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(100, len(df)))
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_sample)
        linkage_matrix = linkage(scaled_data, method='ward')
        dendrogram(linkage_matrix, ax=ax, truncate_mode='level', p=3)
        ax.set_title('Hierarchical Clustering Dendrogram', fontweight='bold')
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'Dendrogram failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()