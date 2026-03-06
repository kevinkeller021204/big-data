import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.express as px
layers = [
    "1 Source/Physical Hardware",
    "2 Embedded/Firmware",
    "3 OT/Field Interface",
    "4 Edge Gateway/Protocol Adaptation",
    "5 Edge Compute Runtime",
    "6 Source Agents & Collectors",
    "7 App Instrumentation/Event Emission",
    "8 CDC (Change Event Generation)",
    "9 Local Buffering & Reliability",
    "10 Context/Semantics/Contracts",
    "11 Virtual/Algorithmic Generation",
    "12 Egress/Handoff (to Ingestion)",
]

# --- Provider Scores (0–5). EDIT THIS to match your assessment. ---
scores = {
    # USA hyperscalers
    "AWS": {
        "1 Source/Physical Hardware": 1,
        "2 Embedded/Firmware": 1,
        "3 OT/Field Interface": 3,
        "4 Edge Gateway/Protocol Adaptation": 4,
        "5 Edge Compute Runtime": 5,
        "6 Source Agents & Collectors": 5,
        "7 App Instrumentation/Event Emission": 5,
        "8 CDC (Change Event Generation)": 5,
        "9 Local Buffering & Reliability": 4,
        "10 Context/Semantics/Contracts": 3,
        "11 Virtual/Algorithmic Generation": 5,
        "12 Egress/Handoff (to Ingestion)": 5,
    },
    "Azure": {
        "1 Source/Physical Hardware": 1,
        "2 Embedded/Firmware": 1,
        "3 OT/Field Interface": 4,
        "4 Edge Gateway/Protocol Adaptation": 4,
        "5 Edge Compute Runtime": 5,
        "6 Source Agents & Collectors": 5,
        "7 App Instrumentation/Event Emission": 5,
        "8 CDC (Change Event Generation)": 4,
        "9 Local Buffering & Reliability": 5,
        "10 Context/Semantics/Contracts": 4,
        "11 Virtual/Algorithmic Generation": 5,
        "12 Egress/Handoff (to Ingestion)": 5,
    },
    "Google Cloud": {
        "1 Source/Physical Hardware": 1,
        "2 Embedded/Firmware": 1,
        "3 OT/Field Interface": 2,
        "4 Edge Gateway/Protocol Adaptation": 3,
        "5 Edge Compute Runtime": 4,
        "6 Source Agents & Collectors": 4,
        "7 App Instrumentation/Event Emission": 5,
        "8 CDC (Change Event Generation)": 5,
        "9 Local Buffering & Reliability": 3,
        "10 Context/Semantics/Contracts": 3,
        "11 Virtual/Algorithmic Generation": 5,
        "12 Egress/Handoff (to Ingestion)": 5,
    },

    # DE main providers
    "Stackable": {
        "1 Source/Physical Hardware": 0,
        "2 Embedded/Firmware": 0,
        "3 OT/Field Interface": 1,
        "4 Edge Gateway/Protocol Adaptation": 2,
        "5 Edge Compute Runtime": 4,
        "6 Source Agents & Collectors": 3,
        "7 App Instrumentation/Event Emission": 2,
        "8 CDC (Change Event Generation)": 4,
        "9 Local Buffering & Reliability": 3,
        "10 Context/Semantics/Contracts": 2,
        "11 Virtual/Algorithmic Generation": 2,
        "12 Egress/Handoff (to Ingestion)": 4,
    },
    "IONOS": {
        "1 Source/Physical Hardware": 1,
        "2 Embedded/Firmware": 0,
        "3 OT/Field Interface": 1,
        "4 Edge Gateway/Protocol Adaptation": 1,
        "5 Edge Compute Runtime": 4,
        "6 Source Agents & Collectors": 2,
        "7 App Instrumentation/Event Emission": 2,
        "8 CDC (Change Event Generation)": 2,
        "9 Local Buffering & Reliability": 2,
        "10 Context/Semantics/Contracts": 2,
        "11 Virtual/Algorithmic Generation": 3,
        "12 Egress/Handoff (to Ingestion)": 3,
    },
    "OTC": {
        "1 Source/Physical Hardware": 1,
        "2 Embedded/Firmware": 0,
        "3 OT/Field Interface": 1,
        "4 Edge Gateway/Protocol Adaptation": 1,
        "5 Edge Compute Runtime": 4,
        "6 Source Agents & Collectors": 2,
        "7 App Instrumentation/Event Emission": 2,
        "8 CDC (Change Event Generation)": 2,
        "9 Local Buffering & Reliability": 2,
        "10 Context/Semantics/Contracts": 2,
        "11 Virtual/Algorithmic Generation": 2,
        "12 Egress/Handoff (to Ingestion)": 3,
    },
}

country = {
    "AWS": "USA",
    "Azure": "USA",
    "Google Cloud": "USA",
    "Stackable": "DE",
    "IONOS": "DE",
    "OTC": "DE",
}
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
