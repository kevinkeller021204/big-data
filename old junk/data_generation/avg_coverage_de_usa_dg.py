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

country_avg = (long_df
    .groupby(["country", "layer"], as_index=False)["score"]
    .mean()
)

fig = px.bar(
    country_avg,
    x="layer",
    y="score",
    color="country",
    barmode="group",
    title="DE vs USA – durchschnittliche Abdeckung je Data-Generation-Layer",
)
fig.update_layout(xaxis_tickangle=35, yaxis_range=[0,5])
fig.show()

