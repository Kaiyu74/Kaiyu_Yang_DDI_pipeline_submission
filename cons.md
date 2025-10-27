# Known Limitations / Trade‑offs

1) **Subnet inference.** When no mask is present, the pipeline assumes **/24 (IPv4)** and **/64 (IPv6)** to derive `subnet_cidr`. Real networks may differ; prefer an explicit subnet/netmask column when available.

2) **Device type classification.** Rules come first; the LLM is only called when heuristic confidence `< 0.6`. If the API key is missing or the API is unreachable, the model may not respond and the run falls back to a deterministic outcome (often `unknown` with low confidence), which is flagged in `anomalies.json`. Low temperature and JSON‑only reduce but don’t eliminate noise.

3) **Coarse taxonomy.** The allowed `device_type` set is intentionally broad (e.g., `server`, `router`, `switch`, `unknown`). Niche hardware (e.g., storage switches, hypervisors) may be collapsed to `server`/`unknown`.

4) **Site normalization.** The `SITE_MAP` synonym list is small and example‑driven. Unmapped locations yield an empty `site_normalized` and an `unknown_site` anomaly. Building/room tags are parsed heuristically and may miss local conventions.

5) **Owner parsing.** Email/name extraction and `owner_team` inference are keyword‑based only; there’s no HR/IdP directory lookup. Nicknames, contractors, and non‑standard formats can be misclassified.

6) **DNS name rules.** Hostname/FQDN checks cover ASCII RFC‑952/1123 patterns. IDNA/punycode and other non‑ASCII labels aren’t supported. `fqdn_consistent` is a simple prefix test and doesn’t consider split‑horizon DNS.

7) **MAC handling.** MACs are normalized to uppercase colon form and syntax‑validated, but no OUI/vendor enrichment is performed; spoofing or vendor hints aren’t detected.

8) **IP hygiene beyond syntax.** The pipeline validates address syntax and computes `reverse_ptr`, but it doesn’t detect duplicate IP/MAC entries, overlapping subnets, or DNS authority conflicts.

9) **Logging & privacy.** `prompts.md` records prompts/responses only when the LLM is actually invoked. Avoid placing sensitive data (e.g., secrets, customer names) in hints that feed the model.

10) **Reproducibility vs. reliance on LLM.** With LLM disabled, runs are fully deterministic. Enabling LLM introduces an external dependency and mild nondeterminism (mitigated by low temperature and a constrained label set).