# Approach

This pipeline cleans `inventory_raw.csv` into `inventory_clean.csv` and records issues in `anomalies.json`.
It follows the given instruction:  Use deterministic rules first; use LLMs only where rules are weak. 
LLM model choice: gpt-4o-mini

## Usage (two options)

**Deterministic run (rules only):**
```bash
python3 run.py --raw inventory_raw.csv --outdir out
```

**Enable LLM:**
```bash
export OPENAI_API_KEY=sk-********************************(please first set your gpt api key in your bash)
python3 run.py --raw inventory_raw.csv --outdir out --use-llm
```


## Steps
1. **Normalize & Validate**
   - IP: validate IPv4/IPv6 (`ipaddress`), derive `subnet_cidr` (IPv4: /24, IPv6: /64), compute `reverse_ptr`.
   - Hostname: check validity based on RFC‑952/1123 rules (lowercase, labels allowed chars).
   - FQDN: validate labels and overall length; check `fqdn_consistent` with `hostname`.
   - MAC: strip separators, verify 12 hex digits mac address, output colon‑separated uppercase.
   - Owner: extract `owner_email`, prettify name, infer `owner_team` using keyword hints.
   - Site: Normalize the site field to the company’s standard three-letter site codes (for example SJC or NYC) using a synonyms list.
2. **Classification**
   - Infer device_type using simple keyword rules from hostname, fqdn, role, owner_team, and site. Convert matches to a confidence score in [0.0–1.0].
   - If the score is < 0.6 and LLM usage is enabled, call the model with temperature = 0.2 and require a strict JSON response ({"device_type": "...", "confidence": ...}).
3. **Anomaly Reporting**
   - For any invalid or inconsistent field, append an entry to `anomalies.json` with `row_id`, `fields`, `issue_type`, `recommended_action`.
4. **Traceability**
   - Each output row includes a normalization_steps field: a semicolon-separated list of the cleaning/validation actions applied, in order.
5. **Reproducibility**
   - A single entry script, run.py, rebuilds all outputs. With LLM off (default) the run is fully deterministic; with LLM on(must provide a API key), calls are tightly constrained and logged to prompts.md.

## Notes
- If no subnet mask is provided, set subnet_cidr to /24 for IPv4 and /64 for IPv6. If the file includes a real subnet/netmask column, use that instead.
- Most processing uses deterministic rules. LLM calls are rare, optional, and logged in prompts.md when enabled; if LLM is disabled or no API key is present, no LLM prompts are logged.

