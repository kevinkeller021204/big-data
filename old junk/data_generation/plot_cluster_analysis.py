# plot_cluster_analysis.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import Data_bp_agg as cfg

layers  = cfg.cluster_layers
scores  = cfg.cluster_scores
country = cfg.country

anbieter_list = list(scores.keys())
df = pd.DataFrame(scores).T[layers]
df["country"] = df.index.map(country)
df_num = df[layers]

# ============================================================
# PLOT 1: Grouped Bar – Cluster-Scores pro Anbieter
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(layers))
n = len(anbieter_list)
width = 0.13

for i, anb in enumerate(anbieter_list):
    vals = [scores[anb][l] for l in layers]
    color = '#4A90D9' if country[anb] == 'USA' else '#D94A4A'
    offset = (i - n / 2) * width + width / 2
    bars = ax.bar(x + offset, vals, width, label=anb, color=color,
                  alpha=0.6 + i * 0.05, edgecolor='white')

short_labels = [l.split(" ", 1)[1] for l in layers]
ax.set_xticks(x)
ax.set_xticklabels(short_labels, rotation=15, ha='right', fontsize=8)
ax.set_ylabel("Ø Cluster-Score (1–5)")
ax.set_title("Cluster-Scores pro Anbieter")
ax.set_ylim(0, 5.5)
ax.grid(axis='y', alpha=0.3)
ax.legend(loc='lower right', fontsize=8)

plt.tight_layout()
plt.savefig("cluster_grouped_bar.png", dpi=150)
plt.show()


# ============================================================
# PLOT 2: Heatmap Anbieter x Cluster
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))

matrix = df_num.values
short_labels = [l.split(" ", 1)[1] for l in layers]

im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=5)
ax.set_xticks(range(len(layers)))
ax.set_xticklabels(short_labels, rotation=20, ha='right', fontsize=8)
ax.set_yticks(range(len(anbieter_list)))
ax.set_yticklabels(anbieter_list, fontsize=9)

for i in range(len(anbieter_list)):
    for j in range(len(layers)):
        ax.text(j, i, f'{matrix[i, j]:.2f}', ha='center', va='center',
                fontsize=9, fontweight='bold',
                color='white' if matrix[i, j] < 2.5 else 'black')

plt.colorbar(im, ax=ax, shrink=0.8, label='Ø Score')
ax.set_title("Heatmap: Cluster-Scores pro Anbieter")
plt.tight_layout()
plt.savefig("cluster_heatmap.png", dpi=150)
plt.show()


# ============================================================
# PLOT 3: Radar – USA vs DE Durchschnitt pro Cluster
# ============================================================
fig = go.Figure()

for c, color in [("USA", "#4A90D9"), ("DE", "#D94A4A")]:
    avg = df_num[df["country"] == c].mean().tolist()
    fig.add_trace(go.Scatterpolar(
        r=avg + [avg[0]],
        theta=layers + [layers[0]],
        fill="toself",
        name=f"{c} Ø",
        opacity=0.55,
        line=dict(width=3, color=color),
    ))

fig.update_layout(
    title="Radar – USA vs. DE Cluster-Durchschnitt",
    polar=dict(radialaxis=dict(visible=True, range=[0, 5], dtick=1)),
    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    margin=dict(l=40, r=40, t=70, b=100),
)
fig.show()


# ============================================================
# PLOT 4: Boxplot – Score-Verteilung pro Cluster
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))

data_box = [df_num[l].tolist() for l in layers]
short_labels = [l.split(" ", 1)[1] for l in layers]

bp = ax.boxplot(data_box, labels=short_labels, patch_artist=True,
                widths=0.5, medianprops=dict(color='black', linewidth=2))

for patch in bp['boxes']:
    patch.set_facecolor('#7B68EE')
    patch.set_alpha(0.7)

means = [np.mean(d) for d in data_box]
ax.scatter(range(1, len(layers) + 1), means, marker='D', color='black',
           s=40, zorder=5, label='Mittelwert')

ax.set_ylabel("Ø Score (1–5)")
ax.set_title("Score-Verteilung pro Cluster (alle Anbieter)")
ax.set_xticklabels(short_labels, rotation=15, ha='right', fontsize=8)
ax.set_ylim(0, 5.5)
ax.grid(axis='y', alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig("cluster_boxplot.png", dpi=150)
plt.show()


# ============================================================
# PLOT 5: Gap-Analyse USA vs DE pro Cluster (horizontal bar)
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

gaps = []
usa_avgs = []
de_avgs  = []
for l in layers:
    usa = df_num[df["country"] == "USA"][l].mean()
    de  = df_num[df["country"] == "DE"][l].mean()
    gaps.append(round(usa - de, 2))
    usa_avgs.append(round(usa, 2))
    de_avgs.append(round(de, 2))

short_labels = [l.split(" ", 1)[1] for l in layers]
y_pos = range(len(layers))
colors_gap = ['#D94A4A' if g >= 2 else '#E8A838' if g >= 1 else '#4A90D9' for g in gaps]

bars = ax.barh(y_pos, gaps, color=colors_gap, edgecolor='white', height=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(short_labels, fontsize=9)
ax.set_xlabel("Gap (USA Ø – DE Ø)")
ax.set_title("Gap-Analyse pro Cluster: Wo DE zurückliegt")
ax.axvline(x=0, color='black', linewidth=0.8)
ax.grid(axis='x', alpha=0.3)

for i, (g, usa, de) in enumerate(zip(gaps, usa_avgs, de_avgs)):
    ax.text(g + 0.05, i, f'Δ {g:.2f}  (USA {usa} | DE {de})',
            va='center', fontsize=8)

plt.tight_layout()
plt.savefig("cluster_gap.png", dpi=150)
plt.show()


# ============================================================
# PLOT 6: Stacked Bar – USA vs DE Cluster-Scores nebeneinander
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(layers))
width = 0.35

usa_avg = [df_num[df["country"] == "USA"][l].mean() for l in layers]
de_avg  = [df_num[df["country"] == "DE"][l].mean()  for l in layers]

ax.bar(x - width/2, usa_avg, width, label='USA Ø', color='#4A90D9', alpha=0.8, edgecolor='white')
ax.bar(x + width/2, de_avg,  width, label='DE Ø',  color='#D94A4A', alpha=0.8, edgecolor='white')

for i, (u, d) in enumerate(zip(usa_avg, de_avg)):
    ax.text(i - width/2, u + 0.08, f'{u:.2f}', ha='center', fontsize=8, fontweight='bold')
    ax.text(i + width/2, d + 0.08, f'{d:.2f}', ha='center', fontsize=8, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels([l.split(" ", 1)[1] for l in layers], rotation=15, ha='right', fontsize=8)
ax.set_ylabel("Ø Cluster-Score (1–5)")
ax.set_title("USA vs. DE – Cluster-Durchschnitt im Vergleich")
ax.set_ylim(0, 5.8)
ax.grid(axis='y', alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig("cluster_usa_vs_de_bar.png", dpi=150)
plt.show()
