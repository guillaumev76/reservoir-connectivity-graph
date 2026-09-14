# Reservoir Connectivity from Production Data — a Graph-Based Approach

**Status: data loaded and cleaned, first exploration done (14/09/2026)**

First look at monthly oil production per well already shows F-12 and F-14 moving together for years (2008-2013), including a shared production dip mid-2012 — the first visual hint of connectivity, well before any graph is built. See `notebooks/01_monthly_oil_by_well.png`.

## What this is

A portfolio project applying graph analysis (NetworkX) and classical machine learning (scikit-learn) to reservoir connectivity, using the public Volve field dataset (Equinor). Wells are modeled as nodes; edges represent inferred hydraulic connectivity, weighted by production-behaviour correlation.

This project exists to demonstrate, with a real and checkable example, a skillset that a CV line cannot: applying data science tools to an actual subsurface engineering problem, end to end, with a defensible physical conclusion at the end.

## Why Volve

The Volve dataset (Equinor, North Sea, production 2008-2016) is public, well-documented, and widely used in the industry for exactly this kind of work. No confidential or employer data is used anywhere in this project.

## Plan

| Step | Content | Status |
|---|---|---|
| 1 | Get the data, understand structure, clean production series | **Done** — 7 wells, daily + monthly production, 2007-2016 |
| 2 | Build features: production correlation, pressure response, (fluid composition if available) | **In progress** |
| 3 | Build the NetworkX graph, weight edges, detect communities (compartments) | Not started |
| 4 | Compare detected compartments to Volve's published geological understanding | Not started |
| 5 | Add a scikit-learn layer: classify/predict compartment membership, quantify uncertainty | Not started |
| 6 | Clean up code, write the final README, publish to GitHub, post on LinkedIn | Not started |

## Data source

Production data (daily/monthly, well by well): [Kaggle — Volve production data](https://www.kaggle.com/datasets/lamyalbert/volve-production-data)

Full field dataset (logs, seismic, static models, ~40,000 files) if needed later: [Equinor Volve data sharing](https://www.equinor.com/energy/volve-data-sharing)

## Setup

```bash
pip install -r requirements.txt
```

## Structure

```
reservoir-connectivity-graph/
├── README.md
├── requirements.txt
├── data/
│   └── raw/          # downloaded data lands here, never committed (see .gitignore)
├── notebooks/         # exploration
└── src/                # cleaned-up, reusable code
```
