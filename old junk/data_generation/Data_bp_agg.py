# Data_bp_agg.py

import numpy as np
import Data_bp as cfg

layers  = cfg.layers
scores  = cfg.scores
country = cfg.country

# ============================================================
# Cluster-Definition (5 Cluster)
# ============================================================
clusters = {
    "A Data Ingestion & Connectivity": [
        "1 Echtzeit-Datenaufnahme (Real-Time Ingestion)",
        "2 Batch-Ingestion & ETL/ELT",
        "3 Konnektoren-Ökosystem & Marketplace",
    ],
    "B Storage & Processing": [
        "4 Data-Lakehouse-Architektur",
        "5 Datenformat-Flexibilität",
        "6 Storage-Tiering & Lifecycle-Management",
        "7 Skalierbarkeit (Compute & Storage)",
        "8 Stream-Processing & Complex Event Processing",
        "9 Analytische Query-Engine",
    ],
    "C Analytics & BI": [
        "10 BI- & Visualisierungs-Integration",
        "11 Ad-hoc-Exploration & Notebooks",
    ],
    "D AI & ML": [
        "12 ML-Plattform & AutoML",
        "13 MLOps, Modell-Lifecycle & Reproduzierbarkeit",
        "14 Feature Store",
        "15 Generative AI & LLM-Integration",
        "16 Modell-Erklärbarkeit & Fairness",
    ],
    "E Governance & Operations": [
        "17 Data Governance, Katalogisierung, Metadaten & Lineage",
        "18 Datenqualitätsmanagement",
        "19 Sicherheitsarchitektur & Zugriffskontrolle",
        "20 Resilienz & Disaster Recovery",
        "21 Edge-Computing & lokale Verarbeitung",
        "22 Multi-Cloud, Hybrid & Portabilität",
        "23 Infrastructure as Code & DataOps",
        "24 Monitoring, Observability & AIOps",
        "25 API-First & Entwicklerfreundlichkeit",
        "26 Cross-Organization Data Sharing",
    ],
}

# ============================================================
# Cluster-Scores berechnen (Ø pro Cluster pro Anbieter)
# ============================================================
cluster_scores = {}
for anbieter, krit_scores in scores.items():
    cluster_scores[anbieter] = {}
    for cluster_name, krit_list in clusters.items():
        vals = [krit_scores[k] for k in krit_list if k in krit_scores]
        cluster_scores[anbieter][cluster_name] = round(np.mean(vals), 2)

cluster_layers = list(clusters.keys())
