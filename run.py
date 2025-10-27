#!/usr/bin/env python3
"""
This script does:
- Loads the provided `inventory_raw.csv`
- Validates, normalizes, and enriches fields for DDI (DNS/DHCP/IPAM) workflows
- Emits `inventory_clean.csv` and `anomalies.json`
- Logs any LLM prompts into `prompts.md`.
- Writes short docs: approach.md, cons.md and ddi_ideas.md

Deterministic rules are used first; LLM is only used for weak/ambiguous cases.
The LLM call is triggered only if OPENAI_API_KEY is present *and*
the `--use-llm` flag is passed.

"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import ipaddress
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import pandas as pd

# ------------------------------
# Helpers: validation and utils
# ------------------------------

HOSTNAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
LABEL_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
MAC_HEX_RE = re.compile(r"^[0-9a-fA-F]{12}$")

SITE_MAP = {
    # canonical : known synonyms
    "SJC": ["sjc", "san jose", "sj"],
    "SFO": ["sfo", "san francisco", "sf"],
    "NYC": ["nyc", "new york", "ny"],
    "LON": ["lon", "london", "ldn"],
    "AMS": ["ams", "amsterdam"],
    "FRA": ["fra", "frankfurt"],
    "TYO": ["tyo", "tokyo"],
    "BLR": ["blr", "bengaluru", "bangalore"],
    "PEK": ["pek", "beijing"],
}

DEVICE_KEYWORDS = {
    "switch": ["switch", "sw", "dist", "edge", "core"],
    "router": ["router", "rtr", "gw", "gateway"],
    "firewall": ["firewall", "fw", "asa", "palo", "pa-"],
    "wireless_ap": ["ap", "wlc", "aironet", "arubaap"],
    "printer": ["printer", "prt", "prn", "hp-lj"],
    "server": ["server", "srv", "db", "sql", "web", "app", "kube", "k8s", "esx", "esxi"],
    "desktop": ["desktop", "dt"],
    "laptop": ["laptop", "lt", "mbp", "macbook", "thinkpad", "elitebook"],
    "load_balancer": ["f5", "ltm", "bigip", "netscaler", "avi-lb"],
    "nas": ["nas", "synology", "qnap", "isilon"],
    "camera": ["cam", "camera", "cctv"],
    "phone": ["phone", "voip", "sip"],
    "iot": ["sensor", "badge", "door", "lock", "iot"],
}

TEAM_KEYWORDS = {
    "netops": ["netops", "network", "noc"],
    "secops": ["secops", "security", "soc"],
    "devops": ["devops", "platform", "sre"],
    "it": ["it", "helpdesk", "desktop"],
    "eng": ["engineering", "dev", "qa", "test"],
    "sales": ["sales", "field", "se"],
    "hr": ["hr", "talent", "recruiting"],
    "finance": ["finance", "acct", "accounting"],
    "marketing": ["marketing", "mktg"],
    "ops": ["ops", "operations"],
}


def now_utc_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def safe_str(x) -> str:
    return "" if pd.isna(x) else str(x).strip()


def normalize_hostname(raw: str) -> Tuple[str, bool, List[str]]:
    steps = []
    s = safe_str(raw).lower()
    if s != raw:
        steps.append("hostname:lowercased")
    valid = bool(HOSTNAME_RE.match(s)) if s else False
    if not valid and s:
        steps.append("hostname:invalid_format")
    return s, valid, steps


def validate_fqdn(fqdn_raw: str) -> Tuple[str, bool, List[str]]:
    steps = []
    fqdn = safe_str(fqdn_raw).lower()
    if fqdn != fqdn_raw:
        steps.append("fqdn:lowercased")
    if not fqdn:
        return "", False, steps

    # Basic FQDN validation: labels 1-63 chars, overall <=253
    labels = fqdn.split(".")
    if len(fqdn) > 253 or any((len(l) == 0 or len(l) > 63 or not LABEL_RE.match(l)) for l in labels):
        steps.append("fqdn:invalid")
        return fqdn, False, steps
    return fqdn, True, steps


def fqdn_consistent_with_hostname(hostname: str, fqdn: str) -> bool:
    if not hostname or not fqdn:
        return False
    return fqdn.startswith(hostname + ".") or fqdn == hostname  # bare hostname case


def normalize_mac(mac_raw: str) -> Tuple[str, bool, List[str]]:
    steps = []
    s = safe_str(mac_raw)
    if not s:
        return "", False, steps

    hex_only = re.sub(r"[^0-9a-fA-F]", "", s)
    if hex_only != s:
        steps.append("mac:removed_separators")
    if len(hex_only) == 12 and MAC_HEX_RE.match(hex_only):
        norm = ":".join(hex_only[i:i+2] for i in range(0, 12, 2)).upper()
        steps.append("mac:normalized_colon_upper")
        return norm, True, steps
    else:
        steps.append("mac:invalid")
        return s.upper(), False, steps


def reverse_ptr_for_ip(ip_obj: ipaddress._BaseAddress) -> str:
    # ipaddress has reverse_pointer
    return ip_obj.reverse_pointer


def derive_subnet_for_ip(ip_obj: ipaddress._BaseAddress) -> str:
    # Without a provided mask, pick pragmatic defaults common in ops:
    # - IPv4: /24  (management/office networks)
    # - IPv6: /64  (typical LAN)
    if isinstance(ip_obj, ipaddress.IPv4Address):
        net = ipaddress.ip_network(f"{ip_obj}/24", strict=False)
        return str(net)
    else:
        net = ipaddress.ip_network(f"{ip_obj}/64", strict=False)
        return str(net)


def normalize_ip(ip_raw: str) -> Tuple[str, bool, int, str, str, List[str]]:
    steps = []
    s = safe_str(ip_raw)
    if not s:
        return "", False, 0, "", "", steps

    s = s.strip()
    try:
        ip_obj = ipaddress.ip_address(s)
        steps.append("ip:validated")
        version = ip_obj.version
        subnet = derive_subnet_for_ip(ip_obj)
        rptr = reverse_ptr_for_ip(ip_obj)
        return str(ip_obj), True, version, subnet, rptr, steps
    except ValueError:
        steps.append("ip:invalid")
        return s, False, 0, "", "", steps


def parse_owner(owner_raw: str) -> Tuple[str, str, str, List[str]]:
    steps = []
    s = safe_str(owner_raw)
    email = ""
    team = ""
    owner = ""

    if not s:
        return "", "", "", steps

    # Try email first
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", s)
    if email_match:
        email = email_match.group(0).lower()
        owner = email.split("@")[0].replace(".", " ").replace("_", " ").title()
        steps.append("owner:email_extracted")
    else:
        # Try formats like "Lastname, Firstname" or "First Last (team)"
        cleaned = re.sub(r"[\(\)\[\]]", " ", s).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        # team hint
        for tcanon, keys in TEAM_KEYWORDS.items():
            if any(k in cleaned.lower() for k in keys):
                team = tcanon
                steps.append("owner:team_inferred")
                break
        owner = cleaned.title()

    # If team not known via above, guess from email domain or tokens
    if not team:
        text = (s + " " + email).lower()
        for tcanon, keys in TEAM_KEYWORDS.items():
            if any(k in text for k in keys):
                team = tcanon
                steps.append("owner:team_inferred")
                break

    return owner, email, team, steps


def normalize_site(site_raw: str) -> Tuple[str, str, List[str]]:
    steps = []
    s = safe_str(site_raw)
    if not s:
        return "", "", steps
    s_norm = re.sub(r"[^a-zA-Z0-9\- ]", " ", s).strip().lower()
    s_norm = re.sub(r"\s+", " ", s_norm)
    # split off potential building/room (keep after canonical code)
    building = ""
    m = re.search(r"(bldg|bld|b)\s*(\d+)", s_norm)
    if m:
        building = f"-B{m.group(2)}"
        steps.append("site:building_tagged")

    # map to canonical
    for canon, keys in SITE_MAP.items():
        if s_norm == canon.lower() or any(s_norm == k for k in keys) or any(k in s_norm for k in keys):
            steps.append("site:normalized")
            return s, canon + building, steps
    # If three-letter code already
    if re.fullmatch(r"[A-Za-z]{3}", s.strip()):
        steps.append("site:assumed_three_letter_code")
        return s, s.strip().upper() + building, steps

    steps.append("site:unknown")
    return s, "", steps


def deterministic_device_guess(text: str) -> Tuple[str, float, List[str]]:
    steps = []
    t = text.lower()
    best = ("", 0.0)
    for dev, keys in DEVICE_KEYWORDS.items():
        score = 0.0
        for k in keys:
            if k in t:
                score += 1.0
        if score > best[1]:
            best = (dev, score)
    if best[1] > 0:
        steps.append("device:heuristic_match")
        # normalize score to [0, 1] roughly
        conf = min(1.0, 0.3 + best[1] * 0.15)
        return best[0], conf, steps
    return "", 0.0, steps


# ------------------------------
# LLM (optional)
# ------------------------------

def use_llm() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def call_llm_device_type(prompt: str, temperature: float = 0.2, timeout: int = 8) -> Optional[Dict]:
    """
    Very small direct HTTP call to OpenAI Chat Completions JSON API.
    Not required for core functionality; guarded by env var and try/except.
    Returns a dict with fields {"device_type": str, "confidence": float} if successful.
    """
    import json, os, time, urllib.request

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        body = {
            "model": "gpt-4o-mini",
            "temperature": temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "You are a deterministic network asset classifier. Reply in strict JSON."},
                {"role": "user", "content": prompt},
            ],
        }
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read())
        # Extract assistant content text
        content = payload["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        return None


def log_prompt(prompts_path: str, title: str, prompt: str, response: Optional[Dict], rationale: str):
    ts = dt.datetime.utcnow().isoformat() + "Z"
    with open(prompts_path, "a", encoding="utf-8") as f:
        f.write(f"## {title}\n")
        f.write(f"- timestamp: {ts}\n")
        f.write(f"- temperature: 0.2\n")
        f.write(f"- rationale: {rationale}\n")
        f.write("\n**Prompt**\n\n")
        f.write("```\n")
        f.write(prompt.strip() + "\n")
        f.write("```\n\n")
        f.write("**Response**\n\n")
        f.write("```\n")
        if response is None:
            f.write("{\"note\": \"no response (offline or LLM disabled)\"}\n")
        else:
            f.write(json.dumps(response, indent=2) + "\n")
        f.write("```\n\n---\n\n")


# ------------------------------
# Core processing
# ------------------------------

@dataclass
class Anomaly:
    row_id: int
    fields: List[str]
    issue_type: str
    recommended_action: str


def process(df: pd.DataFrame, prompts_path: str, enable_llm: bool) -> Tuple[pd.DataFrame, List[Anomaly]]:
    out_rows = []
    anomalies: List[Anomaly] = []

    # normalize column names for easier matching
    df_cols = {c.lower(): c for c in df.columns}
    def get(colname: str):
        # flexible getter; return empty string if missing
        return df[df_cols[colname]].astype(str) if colname in df_cols else pd.Series([""] * len(df))

    # try to find expected columns with fuzzy matches
    def pick(cols: List[str]) -> Optional[str]:
        for c in df.columns:
            if c.lower() in cols:
                return c
        return None

    col_ip = pick(["ip", "ip_address", "address"])
    col_host = pick(["hostname", "host", "shortname"])
    col_fqdn = pick(["fqdn", "name", "dns_name", "full_name"])
    col_mac = pick(["mac", "mac_address", "ether"])
    col_owner = pick(["owner", "user", "assigned_to", "responsible"])
    col_device = pick(["device_type", "type", "role"])
    col_site = pick(["site", "location", "office", "po", "dc"])
    col_src_id = pick(["source_row_id", "row_id", "id"])

    for idx, row in df.iterrows():
        steps_all: List[str] = []
        source_id = int(row[col_src_id]) if col_src_id and str(row[col_src_id]).strip().isdigit() else int(idx) + 1
        raw_ip = str(row[col_ip]) if col_ip else ""
        raw_host = str(row[col_host]) if col_host else ""
        raw_fqdn = str(row[col_fqdn]) if col_fqdn else ""
        raw_mac = str(row[col_mac]) if col_mac else ""
        raw_owner = str(row[col_owner]) if col_owner else ""
        raw_device = str(row[col_device]) if col_device else ""
        raw_site = str(row[col_site]) if col_site else ""

        # IP
        ip, ip_valid, ip_version, subnet_cidr, reverse_ptr, steps = normalize_ip(raw_ip)
        steps_all.extend(steps)
        if not ip_valid:
            anomalies.append(Anomaly(source_id, ["ip"], "invalid_ip", "Fix or remove invalid IP address."))

        # Hostname
        hostname, hostname_valid, steps = normalize_hostname(raw_host)
        steps_all.extend(steps)
        if raw_host and not hostname_valid:
            anomalies.append(Anomaly(source_id, ["hostname"], "invalid_hostname", "Use RFC‑952/1123 compliant hostname."))

        # FQDN
        fqdn, fqdn_valid, steps = validate_fqdn(raw_fqdn)
        steps_all.extend(steps)
        fqdn_consistent = hostname_valid and fqdn_valid and fqdn_consistent_with_hostname(hostname, fqdn)
        if raw_fqdn and not fqdn_valid:
            anomalies.append(Anomaly(source_id, ["fqdn"], "invalid_fqdn", "Ensure labels are 1–63 chars; only letters/digits/hyphens."))
        if hostname_valid and fqdn_valid and not fqdn_consistent:
            anomalies.append(Anomaly(source_id, ["hostname","fqdn"], "mismatch", "Make FQDN start with the hostname label."))

        # MAC
        mac, mac_valid, steps = normalize_mac(raw_mac)
        steps_all.extend(steps)
        if raw_mac and not mac_valid:
            anomalies.append(Anomaly(source_id, ["mac"], "invalid_mac", "Provide 12 hex digits; use colon notation."))

        # Owner
        owner, owner_email, owner_team, steps = parse_owner(raw_owner)
        steps_all.extend(steps)
        if not (owner or owner_email):
            anomalies.append(Anomaly(source_id, ["owner"], "missing_owner", "Add owner or owner_email for accountability."))

        # Site
        site, site_norm, steps = normalize_site(raw_site)
        steps_all.extend(steps)
        if site and not site_norm:
            anomalies.append(Anomaly(source_id, ["site"], "unknown_site", "Map to a canonical site code (e.g., SJC, NYC)."))

        # Device type
        # Start with deterministic heuristics using the best combined hint text
        hint_text = " ".join([raw_device, hostname, fqdn, owner_team, site]).strip()
        dev_guess, dev_conf, dev_steps = deterministic_device_guess(hint_text)
        steps_all.extend(dev_steps)

        device_type = dev_guess if dev_guess else ""
        device_conf = dev_conf if dev_guess else 0.0

        # If weak or unknown and LLM is allowed, try the LLM
        if (not device_type or device_conf < 0.6) and enable_llm and use_llm():
            prompt = f"""
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
{hint_text}

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
""".strip()
            response = call_llm_device_type(prompt, temperature=0.2)
            if response and isinstance(response, dict):
                device_type = str(response.get("device_type", device_type or "unknown"))
                device_conf = float(response.get("confidence", device_conf or 0.5))
            log_prompt(prompts_path, title="device_type classification", prompt=prompt,
                       response=response, rationale="LLM used only when heuristics were weak (<0.6).")
        elif not device_type:
            # LLM disabled or not requested: skip prompting; keep deterministic outcome only.
            device_type = "unknown"
            device_conf = max(device_conf, 0.3)

        # If still unknown but we have strong hostname tokens
        if not device_type and hostname:
            device_type = "server"
            device_conf = 0.4
            steps_all.append("device:default_server_when_unknown")

        # Assemble output row
        out_rows.append({
            "ip": ip,
            "ip_valid": bool(ip_valid),
            "ip_version": int(ip_version) if ip_version else "",
            "subnet_cidr": subnet_cidr,
            "hostname": hostname,
            "hostname_valid": bool(hostname_valid),
            "fqdn": fqdn,
            "fqdn_consistent": bool(fqdn_consistent),
            "reverse_ptr": reverse_ptr,
            "mac": mac,
            "mac_valid": bool(mac_valid),
            "owner": owner,
            "owner_email": owner_email,
            "owner_team": owner_team,
            "device_type": device_type,
            "device_type_confidence": round(float(device_conf), 3) if device_conf else 0.0,
            "site": site,
            "site_normalized": site_norm,
            "source_row_id": source_id,
            "normalization_steps": ";".join(steps_all),
        })

        # Device anomaly if still too weak
        if device_conf < 0.5:
            anomalies.append(Anomaly(source_id, ["device_type"], "low_confidence_device_type",
                                     "Review classification; add better hints (e.g., role, model)."))

    out_df = pd.DataFrame(out_rows, columns=[
        "ip", "ip_valid", "ip_version", "subnet_cidr",
        "hostname", "hostname_valid", "fqdn", "fqdn_consistent", "reverse_ptr",
        "mac", "mac_valid",
        "owner", "owner_email", "owner_team",
        "device_type", "device_type_confidence",
        "site", "site_normalized",
        "source_row_id", "normalization_steps"
    ])
    return out_df, anomalies


def write_anomalies(anomalies_path: str, anomalies: List[Anomaly]) -> None:
    payload = [{
        "row_id": a.row_id,
        "fields": a.fields,
        "issue_type": a.issue_type,
        "recommended_action": a.recommended_action,
    } for a in anomalies]
    with open(anomalies_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def ensure_docs(out_dir: str) -> Tuple[str, str, str, str]:
    """
    Create/overwrite short documentation files to satisfy deliverables.
    Returns the paths to: approach.md, cons.md, prompts.md, ddi_ideas.md
    """
    approach_p = os.path.join(out_dir, "approach.md")
    cons_p = os.path.join(out_dir, "cons.md")
    prompts_p = os.path.join(out_dir, "prompts.md")
    ideas_p = os.path.join(out_dir, "ddi_ideas.md")

    approach = """# Approach

This pipeline cleans `inventory_raw.csv` into `inventory_clean.csv` and flags issues in `anomalies.json`.
It follows a **rules-first, LLM-second** strategy.

## Steps
1. **Normalize & Validate**
   - IP: validate IPv4/IPv6 (`ipaddress`), derive `subnet_cidr` (IPv4: /24, IPv6: /64 by default), compute `reverse_ptr`.
   - Hostname: RFC‑952/1123 checks (lowercase, labels allowed chars).
   - FQDN: validate labels and overall length; check `fqdn_consistent` with `hostname`.
   - MAC: strip separators, verify 12 hex digits, output colon‑separated uppercase.
   - Owner: extract `owner_email`, prettify name, infer `owner_team` using keyword hints.
   - Site: canonicalize to 3‑letter site codes (e.g., SJC, NYC) with a synonyms map.
2. **Classification**
   - Device type via keyword heuristics (hostname/fqdn/role/owner_team/site). Confidence scaled 0..1.
   - If heuristics are weak (<0.6) and an LLM is enabled, call it with temperature 0.2, JSON reply enforced.
3. **Anomaly Reporting**
   - For any invalid or inconsistent field, append an entry to `anomalies.json` with `row_id`, `fields`, `issue_type`, `recommended_action`.
4. **Traceability**
   - Each row carries a `normalization_steps` semi‑colon log for transparency.
5. **Reproducibility**
   - Single entry point `run.py` regenerates outputs deterministically (LLM optional and guarded).

## Notes
- `subnet_cidr` defaults are common ops defaults when the mask isn’t present; if a Subnet column is provided, the script can be extended to prefer it.
- LLM usage is minimal and logged in `prompts.md`. Deterministic transforms dominate.
"""

    cons = """# Known Limitations / Trade‑offs

1. **Subnet inference** — Without an explicit netmask, `/24` for IPv4 and `/64` for IPv6 are heuristics. Real networks may differ.
2. **LLM fragility** — Even at low temperature, classification can be noisy or ambiguous; offline fallback avoids nondeterminism but may under‑classify.
3. **Limited site dictionary** — `SITE_MAP` covers common sites only. Unknown locations will be flagged for manual mapping.
4. **Sparse owner parsing** — Owner extraction heuristics won’t resolve nicknames or external contractors without a proper directory integration.
5. **Hostname/FQDN edge cases** — Split‑horizon DNS, IDNA/punycode, and non‑ASCII labels aren’t modeled.
6. **No OUI vendor check** — MAC vendors could improve device hints; omitted to keep the core deterministic and local.
"""

    prompts_header = """# LLM Prompts Log

All prompts below are issued only when deterministic rules are weak. Temperature is **0.2** and responses are constrained to **JSON** for reproducibility.
If the environment lacks an API key or --use-llm is not provided, no LLM prompts are logged and heuristics are used instead.
"""

    ideas = """# DDI Enrichment Ideas (Optional)

- **PTR auto‑generation policy**: Suggest PTR naming templates based on hostname/Site conventions; flag deviations.
- **Conflict detector**: Cross‑check duplicated MAC/IP, overlapping subnets, and DNS uniqueness constraints.
- **Owner resolution via directory**: Integrate with HR/IdP to resolve owner/team definitively and update stale owners automatically.
- **Device inventory join**: Correlate with CMDB or switch port telemetry to raise confidence in device_type.
- **Policy advice**: Recommend subnet sizes from utilization stats and projected growth.
"""

    with open(approach_p, "w", encoding="utf-8") as f:
        f.write(approach)
    with open(cons_p, "w", encoding="utf-8") as f:
        f.write(cons)
    # create/append prompts header once
    if not os.path.exists(prompts_p) or os.path.getsize(prompts_p) == 0:
        with open(prompts_p, "w", encoding="utf-8") as f:
            f.write(prompts_header)
            f.write("\n---\n\n")
    with open(ideas_p, "w", encoding="utf-8") as f:
        f.write(ideas)

    return approach_p, cons_p, prompts_p, ideas_p


def main():
    ap = argparse.ArgumentParser(description="Infoblox — data cleaning: rules-first, LLM-second")
    ap.add_argument("--raw", default="inventory_raw.csv", help="Path to input inventory_raw.csv")
    ap.add_argument("--outdir", default=".", help="Directory to write outputs")
    ap.add_argument("--use-llm", action="store_true", help="Enable LLM calls when OPENAI_API_KEY is present")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    approach_p, cons_p, prompts_p, ideas_p = ensure_docs(args.outdir)

    try:
        df = pd.read_csv(args.raw)
    except Exception as e:
        raise SystemExit(f"Failed to read {args.raw}: {e}")

    out_df, anomalies = process(df, prompts_p, enable_llm=args.use_llm)

    # Write outputs
    clean_p = os.path.join(args.outdir, "inventory_clean.csv")
    anomalies_p = os.path.join(args.outdir, "anomalies.json")

    out_df.to_csv(clean_p, index=False)
    write_anomalies(anomalies_p, anomalies)

    # Also write a small README for convenience
    readme_p = os.path.join(args.outdir, "README_generated.txt")
    with open(readme_p, "w", encoding="utf-8") as f:
        f.write("Generated at: " + dt.datetime.utcnow().isoformat() + "Z\n")
        f.write("Files:\n")
        f.write("  - inventory_clean.csv\n")
        f.write("  - anomalies.json\n")
        f.write("  - approach.md\n")
        f.write("  - cons.md\n")
        f.write("  - prompts.md\n")
        f.write("  - ddi_ideas.md (optional)\n")

    print(f"Wrote: {clean_p}")
    print(f"Wrote: {anomalies_p}")
    print(f"Wrote docs into: {args.outdir}")

if __name__ == "__main__":
    main()
