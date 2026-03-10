import pandas as pd
import plotly.graph_objects as go

# --- 12 Data-Generation Architekturschichten (nur Überschriften) ---
import Data_bp as cfg

layers = cfg.layers
scores = cfg.scores
country = cfg.country

df = pd.DataFrame(scores).T[layers]
df["country"] = df.index.map(country)

def radar_chart(providers, title, include_country_avg=False):
    fig = go.Figure()

    # provider traces
    for p in providers:
        r = df.loc[p, layers].tolist()
        fig.add_trace(go.Scatterpolar(
            r=r + [r[0]],
            theta=layers + [layers[0]],
            fill="toself",
            name=p,
            opacity=0.55,
        ))

    # optional: country average trace (DE/USA)
    if include_country_avg:
        for c in sorted(df.loc[providers, "country"].unique()):
            avg = df[df["country"] == c][layers].mean().tolist()
            fig.add_trace(go.Scatterpolar(
                r=avg + [avg[0]],
                theta=layers + [layers[0]],
                fill=None,
                name=f"{c} avg",
                line=dict(width=4),
            ))

    fig.update_layout(
        title=title,
        polar=dict(radialaxis=dict(visible=True, range=[0, 5], dtick=1)),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=70, b=120),
    )
    return fig

usa_providers = [p for p in df.index if df.loc[p, "country"] == "USA"]
de_providers  = [p for p in df.index if df.loc[p, "country"] == "DE"]
all_providers = list(df.index)

# --- 3 useful radar charts ---
radar_chart(usa_providers, "Radar – USA Anbieter (Data Generation Layer Coverage)", include_country_avg=False).show()
radar_chart(de_providers,  "Radar – DE Anbieter (Data Generation Layer Coverage)",  include_country_avg=False).show()
radar_chart(all_providers, "Radar – Alle Anbieter (inkl. DE/USA Durchschnitt)",     include_country_avg=True).show()
