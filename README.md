# 📊 Production Graph RAG for the Enterprise
## Vector RAG vs. SQL+RAG vs. Spanner Graph RAG: A Food Safety Supply Chain Showdown

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Vertex_AI_%26_Spanner-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![DACH AI Summit](https://img.shields.io/badge/DACH_AI_Summit_2026-Frankfurt-FF8800)](https://cloud.withgoogle.com/summits/dach)

This repository contains the official hands-on materials for the **Google Cloud DACH AI Summit (Frankfurt)** session on **Production Graph RAG for the Enterprise**. 

This demo contrasts three distinct architectures (Vector RAG, SQL+RAG, and Spanner Graph RAG) under a high-stakes, time-sensitive **food contamination crisis**—specifically, an *E. coli O157:H7* outbreak traced through a complex multi-hop supply chain.

---

## 🚨 The Monday Morning Crisis Scenario

> **Time:** Monday, March 4th, 2026. 8:47 AM.
> **Location:** Frankfurt am Main, Germany.
> **Trigger:** The *Gesundheitsamt Frankfurt* (public health authority) calls. *E. coli O157:H7* has been confirmed in romaine lettuce from Farm "Grünfeld Hof", Batch `#L-2024-0312` (shipped March 3rd). 
> **The Mission:** Trace which restaurants and supermarkets in Frankfurt received this batch, determine consumer exposure, identify a compromised warehouse with a refrigeration failure, and compile a regulatory audit trail. **You have 2 hours before a public panic.**

### The Supply Chain Topology
```
Farm "Grünfeld Hof" (Hessen) 
  → Batch #L-2024-0312 (120kg romaine lettuce, shipped 2024-03-03)
    → Distributor "FreshLog GmbH" (received 2024-03-04)
      ├→ Warehouse "Lager West" ⚠️ REFRIGERATION FAILURE Mar 3-4 overnight
      │   ├→ REWE Konstablerwache (40kg, delivered Mar 5)
      │   ├→ EDEKA Sachsenhausen (25kg, delivered Mar 5)  
      │   ├→ Restaurant Margarete (8kg, delivered Mar 4)
      │   └→ Seven Swans (5kg, delivered Mar 5)
      └→ [also handled Tomatoes batch T-2024-0455 through same warehouse]
    → Distributor "BioFrisch AG" (received 2024-03-04)
      └→ Alnatura Bockenheim (15kg, delivered Mar 6) → NOT YET SOLD ✅
```

---

## 🧠 The Epiquant (Epistemic-Quantitative) Paradigm

Standard Vector RAG is **epistemically blind** and **quantitatively illiterate** when applied to enterprise supply chains, financial transactions, or network routing. This project demonstrates how **Spanner Graph RAG** solves these limits by applying **EQLS (Epistemic-Quantitative Lattice Store)** principles:

1. **Epistemic Tracking**: The ability to distinguish *what was true in the world* (Valid Time) from *what was recorded in the database* (System Time) for bi-temporal audits.
2. **Quantitative Flows**: The ability to propagate, subtract, and aggregate numerical values (e.g., kilograms of lettuce split across distributors) to calculate exposure.
3. **Lattice Topology**: The ability to perform multi-hop, variable-depth path traversals across directed networks instead of flat keyword proximity matching.
4. **Structural Pivots**: The ability to link disjoint documents sharing common nodes (e.g., unrelated tomatoes and lettuce passing through the same compromised warehouse).

---

## ⚔️ The 3 RAG Architectures

The notebook implements and evaluates three architectures on the exact same dataset to answer the seven escalating crisis questions:

| Architecture | Data Storage Model | Query / Retrieval Method | Best Suited For |
| :--- | :--- | :--- | :--- |
| **1. Vector RAG** | In-Memory / Vector Store | Semantic similarity search using `gemini-embedding-2` | Unstructured knowledge bases, FAQs, prose search. |
| **2. SQL + RAG** | Relational Database (Spanner) | Gemini Text-to-SQL generation & relational query execution | Flat queries, transactional lookups, single-table metrics. |
| **3. Spanner Graph RAG** | Property Graph (Spanner Graph) | GQL (Graph Query Language) + Gemini Graph RAG Agent | Complex networks, path traversals, bi-temporal compliance, causal reasoning. |

---

## 📈 Comparison Scorecard

Our 7 escalating questions test different structural and mathematical capabilities:

| # | Crisis Question | Vector RAG | SQL + RAG | Spanner Graph RAG |
| :--- | :--- | :---: | :---: | :---: |
| **Q1** | Direct Retailer Tracing | ⚠️ *Unreliable* (Top-k omissions) | ✅ *Success* | ✅ **Perfect** |
| **Q2** | Deep Supply Chain Traversal | ❌ *Fails* (Broken paths) | ⚠️ *Complex Joins* | ✅ **Perfect (Path)** |
| **Q3** | Warehouse Temporal Filtering | ❌ *Fails* (No date logic) | ✅ *Success* | ✅ **Perfect** |
| **Q4** | Lateral Pivot (Secondary Blast Radius) | ❌ *Fails* | ⚠️ *SQL Nightmares* | ✅ **Perfect (Lateral)** |
| **Q5** | Multi-Hop Common Source Discovery | ❌ *Fails* | ❌ *Fails* (Too complex) | ✅ **Perfect (GQL)** |
| **Q6** | Structured Regulatory Audit Trail | ❌ *Fails* (Returns prose) | ⚠️ *Text Output* | ✅ **Perfect (Provenance)** |
| **Q7** | Bi-Temporal Compliance Audit | ❌ *Fails* (No time-travel) | ❌ *Fails* | ✅ **Perfect (System vs. Valid)** |

---

## 🚀 Setup & Execution Instructions

### Option A: Run in Google Colab (Recommended)
This notebook is fully optimized to run in cloud environments. 

1. Click the open-in-colab badge inside the notebook or upload the `.ipynb` file to [Google Colab](https://colab.research.google.com) or [Vertex AI Workbench](https://cloud.google.com/vertex-ai-workbench).
2. Provisioned Spanner databases are automatically shared for official session participants.

### Option B: Local Jupyter Environment Setup

#### 1. Prerequisites & CLI Installation
Ensure you have the Google Cloud SDK installed and configured:
```bash
# Verify gcloud CLI
gcloud --version

# Log in to set up Application Default Credentials (ADC)
gcloud auth application-default login
```

#### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone git@github.com:salekh/cloud-summit-dach-2026.git
cd cloud-summit-dach-2026

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install required dependencies
pip install -r -q --index-url https://pypi.org/simple/ \
  google-cloud-spanner \
  google-cloud-aiplatform \
  google-cloud-storage \
  plotly \
  pyvis \
  networkx \
  "google-genai[pyopenssl]>=2.4.0" \
  langchain-google-spanner
```

#### 3. Start Jupyter
```bash
jupyter notebook notebooks/production_graphrag_enterprise.ipynb
```

---

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

*Copyright 2026 Google LLC. This is not an official Google product. It is a technical demonstration developed for the Google Cloud DACH AI Summit.*
