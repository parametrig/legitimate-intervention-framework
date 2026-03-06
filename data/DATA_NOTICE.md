# Data Notice

## Dataset Migration

The LIF datasets previously hosted in this directory have been consolidated into a **Risk Intelligence API**.

### Affected Files
- `lif_exploits_final.csv` (705 exploit records, 2011–2025)
- `lif_exploits_raw.csv` (unprocessed exploit data)
- `lif_all_interventions.csv` (130+ intervention records)
- `lif_intervention_metrics.csv` (aggregate metrics)
- `lif_stats.json` (summary statistics)

### Why
Consolidating them into a single API ensures:
- **Data integrity**: Single source of truth, avoiding stale copies.
- **Contractual Stability**: The LIF website explicitly queries a canonical "public snapshot" layer (`/public/lif/*`).

### How to Access

**API Endpoint**: Data is publicly served via the Parametrig API at:
- `https://api.parametrig.com/auk/v1/public/lif/exploits` (705 records)
- `https://api.parametrig.com/auk/v1/public/lif/interventions` (137 records)

**Local Fallbacks**: For offline development, the `web/data/*.json` files are automatically synchronized with this canonical schema.

**For Paper Reviewers**: The ArXiv paper ([arXiv:2602.12260](https://arxiv.org/abs/2602.12260)) references these datasets. Contact the authors for academic access.

---

*Parametrig — Risk research-and-engineering lab*
