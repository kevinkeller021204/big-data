import pandas as pd
import plotly.graph_objects as go
import Data_bp as cfg

layers = cfg.layers
scores = cfg.scores
country = cfg.country

df = pd.DataFrame(scores).T[layers]
df["country"] = df.index.map(country)

def radar_chart_avg(title):
    fig = go.Figure()

    for c, color in [("USA", "#4A90D9"), ("DE", "#D94A4A")]:
        avg = df[df["country"] == c][layers].mean().tolist()
        fig.add_trace(go.Scatterpolar(
            r=avg + [avg[0]],
            theta=layers + [layers[0]],
            fill="toself",
            name=f"{c} Ø",
            opacity=0.55,
            line=dict(width=3, color=color),
        ))

    fig.update_layout(
        title=title,
        polar=dict(radialaxis=dict(visible=True, range=[0, 5], dtick=1)),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=70, b=120),
    )
    return fig

radar_chart_avg("Radar – DE vs. USA Durchschnitt (26 Kriterien)").show()
