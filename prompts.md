# LLM Prompts Log

- This file logs all prompts from this run.
- Temperature: **0.2**; responses are formatted in **JSON**.


---

## device_type classification
- timestamp: 2025-10-27T21:07:13.788254Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:13.912607Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:14.045331Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:14.192828Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:14.395415Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:14.546298Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:14.706880Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:14.856915Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:15.015286Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:15.141075Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:15.301480Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:15.498691Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

## device_type classification
- timestamp: 2025-10-27T21:07:15.603861Z
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
{"note": "no response (offline or LLM disabled)"}
```

---

