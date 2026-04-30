import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

# ─── DATASET: 1000 customers (Age vs Annual Spending) ───────────────────────
def generate_dataset(n=1000, seed=42):
    np.random.seed(seed)
    groups = [
        (22, 1800, 5, 300),   # Young low-income
        (35, 5500, 6, 800),   # Mid-age mid-income
        (52, 9500, 7, 1500),  # Senior high-income
    ]
    records = []
    per_group = n // len(groups)
    for age_mu, inc_mu, age_sd, inc_sd in groups:
        ages    = np.random.normal(age_mu, age_sd,  per_group).clip(18, 70).round(1)
        incomes = np.random.normal(inc_mu, inc_sd,  per_group).clip(500, 15000).round(0)
        for a, i in zip(ages, incomes):
            records.append({"age": float(a), "annual_spending": float(i)})
    remainder = n - len(records)
    for _ in range(remainder):
        records.append({"age": round(float(np.random.uniform(18,70)),1),
                        "annual_spending": round(float(np.random.uniform(500,15000)),0)})
    return records

# ─── MANUAL K-MEANS SIMULATION (100 points, 3 iterations) ───────────────────
def manual_kmeans_simulation():
    np.random.seed(7)
    n = 100
    ages    = np.concatenate([np.random.normal(22,4,34), np.random.normal(38,5,33), np.random.normal(55,5,33)]).clip(18,70).round(1)
    incomes = np.concatenate([np.random.normal(1800,300,34), np.random.normal(5000,700,33), np.random.normal(9200,800,33)]).clip(500,12000).round(0)
    idx = np.random.permutation(n)
    ages, incomes = ages[idx], incomes[idx]

    points = np.column_stack([ages, incomes]).tolist()

    # Initial centroids (manually chosen)
    centroids_history = []
    C = [[20.0, 1500.0], [38.0, 5000.0], [58.0, 9500.0]]
    centroids_history.append([list(c) for c in C])

    def euclidean(p, c):
        return round(np.sqrt((p[0]-c[0])**2 + (p[1]-c[1])**2), 2)

    iterations = []
    variance_per_iter = []

    for it in range(3):
        table = []
        clusters = [[], [], []]
        for p in points:
            dists = [euclidean(p, c) for c in C]
            assigned = int(np.argmin(dists))
            clusters[assigned].append(p)
            table.append({
                "age": p[0], "income": p[1],
                "d1": dists[0], "d2": dists[1], "d3": dists[2],
                "cluster": assigned + 1
            })

        # Variance (inertia)
        variance = 0
        for k, members in enumerate(clusters):
            for p in members:
                variance += euclidean(p, C[k])**2
        variance_per_iter.append(round(variance, 2))

        # New centroids
        new_C = []
        for k, members in enumerate(clusters):
            if members:
                new_C.append([round(np.mean([m[0] for m in members]),2),
                               round(np.mean([m[1] for m in members]),2)])
            else:
                new_C.append(C[k])

        iterations.append({"table": table, "centroids": [list(c) for c in C],
                            "new_centroids": new_C, "variance": round(variance, 2)})
        C = new_C
        centroids_history.append([list(c) for c in C])

    # Variance chart
    fig, ax = plt.subplots(figsize=(7, 3.5), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    ax.plot([1,2,3], variance_per_iter, marker='o', color='#22d3ee', linewidth=2.5, markersize=8)
    ax.fill_between([1,2,3], variance_per_iter, alpha=0.15, color='#22d3ee')
    for i, v in enumerate(variance_per_iter):
        ax.annotate(f'{v:,.0f}', (i+1, v), textcoords="offset points",
                    xytext=(0,10), ha='center', color='#f8fafc', fontsize=9)
    ax.set_xlabel('Iteration', color='#94a3b8')
    ax.set_ylabel('Variance (Inertia)', color='#94a3b8')
    ax.set_title('Variance Reduction per Iteration', color='#f8fafc', fontsize=12)
    ax.tick_params(colors='#94a3b8')
    ax.set_xticks([1,2,3])
    for spine in ax.spines.values(): spine.set_edgecolor('#334155')
    plt.tight_layout()
    buf = io.BytesIO(); plt.savefig(buf, format='png', dpi=120); buf.seek(0)
    variance_chart = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return {"points": points, "iterations": iterations,
            "variance_per_iter": variance_per_iter, "variance_chart": variance_chart}

# ─── FULL K-MEANS APPLICATION (1000 records) ────────────────────────────────
def apply_clustering():
    data = generate_dataset(1000)
    df = pd.DataFrame(data)

    X = df[['age','annual_spending']].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)
    df['cluster'] = labels + 1

    # Centroids in original scale
    centers_scaled = model.cluster_centers_
    centers_orig   = scaler.inverse_transform(centers_scaled)

    cluster_summary = df.groupby('cluster').agg(
        count=('age','count'),
        avg_age=('age','mean'),
        avg_spending=('annual_spending','mean')
    ).reset_index()
    cluster_summary = cluster_summary.round(2).to_dict('records')

    # Scatter plot
    colors = {1:'#22d3ee', 2:'#10b981', 3:'#f59e0b'}
    labels_map = {1:'Cluster 1', 2:'Cluster 2', 3:'Cluster 3'}
    fig, ax = plt.subplots(figsize=(9,5), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    for cl in [1,2,3]:
        mask = df['cluster'] == cl
        ax.scatter(df.loc[mask,'age'], df.loc[mask,'annual_spending'],
                   c=colors[cl], label=labels_map[cl], alpha=0.6, s=18)
    ax.scatter(centers_orig[:,0], centers_orig[:,1],
               c='white', marker='X', s=180, zorder=5, label='Centroids', edgecolors='black')
    ax.set_xlabel('Age', color='#94a3b8')
    ax.set_ylabel('Annual Spending (USD)', color='#94a3b8')
    ax.set_title('K-Means Clustering: Age vs Annual Spending', color='#f8fafc', fontsize=13)
    ax.tick_params(colors='#94a3b8')
    ax.legend(facecolor='#1e293b', labelcolor='#f8fafc', edgecolor='#334155')
    for spine in ax.spines.values(): spine.set_edgecolor('#334155')
    plt.tight_layout()
    buf = io.BytesIO(); plt.savefig(buf, format='png', dpi=130); buf.seek(0)
    scatter_chart = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    sample = df.sample(20, random_state=1).sort_values('cluster').to_dict('records')
    centers_list = [{"cluster": int(i+1),
                     "age": float(round(centers_orig[i][0],2)),
                     "annual_spending": float(round(centers_orig[i][1],2))} for i in range(3)]

    return {"sample": sample, "cluster_summary": cluster_summary,
            "centers": centers_list, "scatter_chart": scatter_chart, "total": len(df)}