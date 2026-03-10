import pandas as pd
import plotly.express as px
import Data_bp as cfg

layers = cfg.layers
scores = cfg.scores
country = cfg.country



# Reuse: layers, scores, country from the radar snippet
df = pd.DataFrame(scores).T.reset_index().rename(columns={"index": "provider"})
df["country"] = df["provider"].map(country)

long_df = df.melt(
    id_vars=["provider", "country"],
    var_name="layer",
    value_name="score"
)


# Pivot: rows=provider, cols=layer
heat = long_df.pivot_table(index="provider", columns="layer", values="score", aggfunc="mean")

# optional: Anbieter nach Gesamt-Score sortieren
order = heat.sum(axis=1).sort_values(ascending=False).index
heat = heat.loc[order]

fig = px.imshow(
    heat,
    color_continuous_scale="Blues",
    zmin=0, zmax=5,
    title="Provider Heatmap – Data Generation Layer Coverage (0–5)"
)
fig.update_layout(
    xaxis_title="Layer",
    yaxis_title="Provider",
    margin=dict(l=90, r=30, t=70, b=140),
)
fig.show()
