import pandas as pd
import plotly.express as px
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


def bucket(s):
    if s >= 4: return "strong (4–5)"
    if s >= 2: return "medium (2–3)"
    return "weak (0–1)"

tmp = long_df.copy()
tmp["bucket"] = tmp["score"].apply(bucket)

summary = (tmp
    .groupby(["provider", "bucket"], as_index=False)
    .size()
    .rename(columns={"size":"layer_count"})
)

# Reihenfolge nach #strong
strong_counts = (tmp[tmp["score"]>=4]
    .groupby("provider")["layer"]
    .count()
    .sort_values(ascending=False)
)
provider_order = strong_counts.index.tolist()

fig = px.bar(
    summary,
    x="provider",
    y="layer_count",
    color="bucket",
    category_orders={"provider": provider_order},
    title="Provider Summary – Anzahl Layer nach Reifegrad"
)
fig.update_layout(yaxis_title="Anzahl Layer", xaxis_title="Provider")
fig.show()
