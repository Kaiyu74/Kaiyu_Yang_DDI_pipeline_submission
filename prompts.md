# LLM Prompts Log

All prompts below are issued only when deterministic rules are weak. Temperature is **0.2** and responses are constrained to **JSON** for reproducibility.
If the environment lacks an API key or --use-llm is not provided, no LLM prompts are logged and heuristics are used instead.

---

## device_type classification
- timestamp: 2025-10-27T22:49:37.722772Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
server host01 nan devops BLR Campus

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "server",
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:38.259753Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
nan host-02 host-02.local ops HQ Bldg 1

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "server",
  "confidence": 0.7
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:38.832520Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
printer printer-01 nan it HQ

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "printer",
  "confidence": 1.0
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:39.466711Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
iot iot-cam01 nan sales Lab-1

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "iot",
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:40.586112Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
nan local-test nan  nan

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "unknown",
  "confidence": 0.1
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:41.219511Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
nan host-apipa nan  nan

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "unknown",
  "confidence": 0.7
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:41.916575Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
nan badhost nan  nan

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "unknown",
  "confidence": 0.5
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:42.889573Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
nan neg nan  nan

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "unknown",
  "confidence": 0.1
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:43.703663Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
nan bcast nan  nan

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "unknown",
  "confidence": 0.6
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:44.729341Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
nan netid nan  nan

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "unknown",
  "confidence": 0.2
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:45.278194Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
router dns-google nan  DC-1

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "router",
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:45.784786Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
server host-10 nan  nan

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "server",
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:49:46.510436Z
- temperature: 0.2
- rationale: LLM used only when heuristics were weak (<0.6).

**Prompt**

```
You are classifying a network asset into a broad device_type for DDI (DNS/DHCP/IPAM) workflows.
Given the hints below, return a JSON object with keys "device_type" and "confidence" (0..1).

Hints (free-form text):
nan missing-ip nan  nan

Allowed device_type values (choose the best single label):
["switch","router","firewall","wireless_ap","printer","server","desktop","laptop","load_balancer","nas","camera","phone","iot","unknown"]

Respond in strict JSON only.
```

**Response**

```
{
  "device_type": "unknown",
  "confidence": 0.8
}
```

---

