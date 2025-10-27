# LLM Prompts Log

- This file logs all prompts from my run with LLM option enabled. 
- gpt model temperature is set to  **0.2** and responses are formatted to **JSON**.
---

## device_type classification
- timestamp: 2025-10-27T22:20:51.089244Z
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
- timestamp: 2025-10-27T22:20:52.241821Z
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
  "confidence": 0.8
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:20:53.285790Z
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
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:20:54.266923Z
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
  "device_type": "camera",
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:20:57.060515Z
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
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:20:57.745854Z
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
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:20:59.181744Z
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
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:21:04.349472Z
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
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:21:05.750010Z
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
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:21:06.756557Z
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
  "confidence": 0.9
}
```

---

## device_type classification
- timestamp: 2025-10-27T22:21:07.395772Z
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
- timestamp: 2025-10-27T22:21:08.367544Z
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
- timestamp: 2025-10-27T22:21:09.419601Z
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
  "confidence": 0.9
}
```

---

