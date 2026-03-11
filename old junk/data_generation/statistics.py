import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.stats import skew, entropy
import Data_bp as cfg

layers = cfg.layers
scores = cfg.scores
country = cfg.country

df = pd.DataFrame(scores).T[layers]
df["country"] = df.index.map(country)
df_num = df[layers]

# ============================================================
# 1) Deskriptive Statistik pro Anbieter
# ============================================================
stats = pd.DataFrame({
    "Ø Score": df_num.mean(axis=1).round(2),
    "Median": df_num.median(axis=1),
    "Std": df_num.std(axis=1).round(2),
    "Min": df_num.min(axis=1),
    "Max": df_num.max(axis=1),
    "Range": (df_num.max(axis=1) - df_num.min(axis=1)),
    "CV (σ/μ)": (df_num.std(axis=1) / df_num.mean(axis=1)).round(3),
    "Skewness": df_num.apply(lambda row: skew(row), axis=1).round(2),
    "Scores ≥ 4": (df_num >= 4).sum(axis=1),
    "Scores ≤ 2": (df_num <= 2).sum(axis=1),
    "Dominanz (1. Platz)": (df_num == df_num.max(axis=0)).sum(axis=1),
})
stats["Region"] = df["country"]
print("=" * 70)
print("DESKRIPTIVE STATISTIK PRO ANBIETER")
print("=" * 70)
print(stats.to_string())

# ============================================================
# 2) Regionaler Vergleich
# ============================================================
print("\n" + "=" * 70)
print("REGIONALER VERGLEICH")
print("=" * 70)
for region in ["USA", "DE"]:
    sub = df_num[df["country"] == region]
    print(f"\n{region}:  Ø={sub.values.mean():.2f}  Std={sub.values.std():.2f}  "
          f"Median={np.median(sub.values):.1f}")

# ============================================================
# 3) Kriterien-Analyse (wo differenzieren sich Anbieter?)
# ============================================================
krit_stats = pd.DataFrame({
    "Ø Score": df_num.mean().round(2),
    "Std": df_num.std().round(2),
    "Min": df_num.min(),
    "Max": df_num.max(),
    "USA Ø": df_num[df["country"] == "USA"].mean().round(2),
    "DE Ø": df_num[df["country"] == "DE"].mean().round(2),
})
krit_stats["Gap (USA–DE)"] = (krit_stats["USA Ø"] - krit_stats["DE Ø"]).round(2)
krit_stats = krit_stats.sort_values("Gap (USA–DE)", ascending=False)

print("\n" + "=" * 70)
print("KRITERIEN-ANALYSE (sortiert nach Gap USA–DE)")
print("=" * 70)
print(krit_stats.to_string())

# ============================================================
# 4) Korrelation & Distanzmatrix (Vorstufe Clustering)
# ============================================================
print("\n" + "=" * 70)
print("PEARSON-KORRELATION (Anbieter-Profile)")
print("=" * 70)
corr = df_num.T.corr().round(2)
print(corr.to_string())

print("\n" + "=" * 70)
print("EUKLIDISCHE DISTANZMATRIX")
print("=" * 70)
dist = pd.DataFrame(
    squareform(pdist(df_num.values, metric='euclidean')),
    index=df_num.index, columns=df_num.index
).round(2)
print(dist.to_string())

print("\n" + "=" * 70)
print("COSINE SIMILARITY")
print("=" * 70)
cos_dist = pd.DataFrame(
    squareform(pdist(df_num.values, metric='cosine')),
    index=df_num.index, columns=df_num.index
)
cos_sim = (1 - cos_dist).round(3)
print(cos_sim.to_string())
