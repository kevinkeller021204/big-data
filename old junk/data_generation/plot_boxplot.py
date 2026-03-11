import numpy as np
import matplotlib.pyplot as plt
import Data_bp as cfg

layers = cfg.layers
scores = cfg.scores
country = cfg.country
anbieter_list = list(scores.keys())


# ============================================================
# PLOT 1: Boxplot pro Anbieter
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))

data_box = [list(scores[a].values()) for a in anbieter_list]
colors_box = ['#4A90D9' if country[a] == 'USA' else '#D94A4A' for a in anbieter_list]

bp = ax.boxplot(data_box, labels=anbieter_list, patch_artist=True, widths=0.5,
                medianprops=dict(color='black', linewidth=2))

for patch, c in zip(bp['boxes'], colors_box):
    patch.set_facecolor(c)
    patch.set_alpha(0.8)

means = [np.mean(d) for d in data_box]
ax.scatter(range(1, len(anbieter_list) + 1), means, marker='D', color='black',
           s=40, zorder=5, label='Mittelwert')

ax.set_ylabel("Score (1–5)")
ax.set_title("Score-Verteilung pro Anbieter (26 Kriterien)")
ax.set_ylim(0, 5.5)
ax.grid(axis='y', alpha=0.3)
ax.legend(handles=[
    plt.Rectangle((0, 0), 1, 1, fc='#4A90D9', alpha=0.8),
    plt.Rectangle((0, 0), 1, 1, fc='#D94A4A', alpha=0.8),
    plt.Line2D([0], [0], marker='D', color='black', linestyle='None', markersize=6),
], labels=['USA', 'DE', 'Mittelwert'], loc='lower left')

plt.tight_layout()
plt.savefig("boxplot_pro_anbieter.png", dpi=150)
plt.show()


# ============================================================
# PLOT 2: Generelle Score-Verteilung USA vs DE
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

usa_scores = []
de_scores = []
for a in anbieter_list:
    vals = list(scores[a].values())
    if country[a] == "USA":
        usa_scores.extend(vals)
    else:
        de_scores.extend(vals)

bp = ax.boxplot([usa_scores, de_scores], labels=["USA (n=78)", "DE (n=78)"],
                patch_artist=True, widths=0.4,
                medianprops=dict(color='black', linewidth=2))

bp['boxes'][0].set_facecolor('#4A90D9')
bp['boxes'][0].set_alpha(0.8)
bp['boxes'][1].set_facecolor('#D94A4A')
bp['boxes'][1].set_alpha(0.8)

for i, vals in enumerate([usa_scores, de_scores], 1):
    ax.scatter(i, np.mean(vals), marker='D', color='black', s=50, zorder=5)
    ax.annotate(f'Ø {np.mean(vals):.2f}', (i, np.mean(vals)),
                textcoords="offset points", xytext=(25, 0), fontsize=10, fontweight='bold')

ax.set_ylabel("Score (1–5)")
ax.set_title("Generelle Score-Verteilung: USA vs. DE Cloud-Anbieter")
ax.set_ylim(0, 5.8)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("boxplot_usa_vs_de.png", dpi=150)
plt.show()
