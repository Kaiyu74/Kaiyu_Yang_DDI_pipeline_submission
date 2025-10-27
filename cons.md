# Known Limitations / Trade‑offs

1) **Subnet inference.** When no mask is present, the pipeline assumes **/24 (IPv4)** and **/64 (IPv6)** to derive `subnet_cidr`. Real networks may differ; prefer an explicit subnet/netmask column when available.

2) **Device type classification.** Rules come first; the LLM is only called when heuristic confidence `< 0.6`. If the API key is missing or the API is unreachable, the model may not respond and the run falls back to a deterministic outcome (often `unknown` with low confidence), which is flagged in `anomalies.json`. Low temperature and JSON‑only reduce but don’t eliminate noise.

3) **Coarse taxonomy.** The allowed `device_type` set is intentionally broad (e.g., `server`, `router`, `switch`, `unknown`). Niche hardware (e.g., storage switches, hypervisors) may be collapsed to `server`/`unknown`.

4) **Site normalization.** The `SITE_MAP` synonym list is small and example‑driven. Unmapped locations yield an empty `site_normalized` and an `unknown_site` anomaly. Building/room tags are parsed heuristically and may miss local conventions.

5) **Owner parsing.** Email/name extraction and `owner_team` inference are keyword‑based only; there’s no HR/IdP directory lookup. Nicknames, contractors, and non‑standard formats can be misclassified.

6) **MAC handling.** MACs are normalized to uppercase colon form and syntax‑validated, but no OUI/vendor enrichment is performed; spoofing or vendor hints aren’t detected.
