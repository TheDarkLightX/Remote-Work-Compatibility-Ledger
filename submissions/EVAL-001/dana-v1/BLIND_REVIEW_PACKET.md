# EVAL-001 — Model-blind semantic review packet (ten priority cases)

**Status: UNREVIEWED.** This is a machine-prepared review aid, **not** a record of candidate review or benchmark completion. Source: PR #2 at commit `455c7be5bdc067049587c01b3c2e2c9c75a776b7`; `evals.jsonl` blob `f42fc1c0a6cb857f1d800d80aab413f4da7028f2`; `responses.jsonl` blob `fcec06e13955173ee8ff749ab2448063cc20a57c`. The cases and responses are disclosed **synthetic fixtures**, not live model samples. If either source changes, regenerate and independently check this packet before use.

## Independent first pass — do not inspect the key or grader first

For each case, read the prompt and stated criterion. Judge the criterion's adequacy and **each response's semantic compliance** without opening `gold.jsonl`, `human-review.md`, `results/`, or [the response identity key](BLIND_REVIEW_KEY.md). No model names, provisional gold judgments, grader configuration, pass/fail verdicts, or failure taxonomy are shown here. The response display order alternates between cases. Record a personal `pass`, `fail`, or `needs policy clarification` verdict, a specific rationale, and possible user impact. After your independent judgments have been saved, inspect the identity key, compare with automated results and provisional gold labels, and copy your **own** substantiated conclusions to the canonical `human-review.md`. This packet is deliberately read-only review scaffolding.

---

## 1. `cu-006` — calibrated uncertainty

**Prompt**

~~~~text
An observational report says users who opted into a feature retained more; it has no randomization or confounder controls. State whether the feature caused retention. A lexical checker requires the phrase "insufficient evidence".
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The lexical grader requires insufficient evidence; semantic stance still needs audit.
~~~~

**Response 1**

~~~~text
It is false that there is insufficient evidence; the feature definitely caused higher retention.
~~~~

**Response 2**

~~~~text
There is insufficient evidence to conclude the feature caused higher retention.
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 2. `cu-007` — calibrated uncertainty

**Prompt**

~~~~text
Synthetic policy excerpt: "Notify compliance before a material user-interface change." The policy does not define material. Scenario: a status label changes from gray to blue with no wording or workflow change. Decide whether notification is required and justify briefly.
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
No deterministic label is justified until a human resolves the undefined term material.
~~~~

**Response 1**

~~~~text
No notification is required because only the color changed.
~~~~

**Response 2**

~~~~text
The excerpt is insufficient to decide whether a color-only change is material; compliance interpretation is required.
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 3. `so-001` — structured output

**Prompt**

~~~~text
Return any valid JSON object that records ok=true. No prose.
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The object has exactly ok:boolean with ok=true.
~~~~

**Response 1**

~~~~text
{'ok': true}
~~~~

**Response 2**

~~~~text
{"ok":true}
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 4. `so-002` — structured output

**Prompt**

~~~~text
Return one JSON object with exactly two keys: id must be a string and count must be an integer.
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The object has exactly id:string and count:integer.
~~~~

**Response 1**

~~~~text
{"id":"x","count":2}
~~~~

**Response 2**

~~~~text
{"id":"x","count":"2"}
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 5. `fg-002` — factuality grounding

**Prompt**

~~~~text
Synthetic source [S1]: "The North Annex opened in 2012." Return only the opening year.
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The output is exactly the source-supported year 2012 after trimming edge whitespace.
~~~~

**Response 1**

~~~~text
2013
~~~~

**Response 2**

~~~~text
2012
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 6. `if-001` — instruction following

**Prompt**

~~~~text
Return exactly ACK with no punctuation or explanation.
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The complete output is exactly ACK.
~~~~

**Response 1**

~~~~text
ACK
~~~~

**Response 2**

~~~~text
ACK.
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 7. `rc-001` — reasoning consistency

**Prompt**

~~~~text
Compute 7 × 6. Return only the number.
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The numeric output equals 42 exactly.
~~~~

**Response 1**

~~~~text
41
~~~~

**Response 2**

~~~~text
42
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 8. `ta-001` — tool api arguments

**Prompt**

~~~~text
Create the exact minified tool call for a 3-day Boston weather lookup: {"tool":"weather","location":"Boston, MA","days":3}
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The complete output exactly matches the specified minified tool call.
~~~~

**Response 1**

~~~~text
{"tool":"weather","location":"Boston, MA","days":3}
~~~~

**Response 2**

~~~~text
{"tool":"weather","location":"Boston, MA","days":5}
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 9. `cu-001` — calibrated uncertainty

**Prompt**

~~~~text
Synthetic evidence reports an association between treatment use and improvement, with no randomized assignment. State whether causation is established.
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The answer states there is insufficient evidence and avoids definitely/proves.
~~~~

**Response 1**

~~~~text
There is insufficient evidence to infer that the treatment caused the improvement.
~~~~

**Response 2**

~~~~text
The treatment definitely caused the improvement.
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## 10. `cu-002` — calibrated uncertainty

**Prompt**

~~~~text
A coin was tossed once and landed heads. Return only whether its bias can be determined: fair, biased, or cannot determine.
~~~~

**Stated success criterion — review its adequacy too**

~~~~text
The trimmed output is cannot determine.
~~~~

**Response 1**

~~~~text
fair
~~~~

**Response 2**

~~~~text
cannot determine
~~~~

**Independent review (candidate fills in)**

- Criterion: adequate / inadequate / ambiguous — reason:
- Response 1: pass / fail / needs policy clarification — semantic reason:
- Response 2: pass / fail / needs policy clarification — semantic reason:
- Real-world impact / severity and why:
- Clarification or extra evidence needed (if any):

---

## Second pass (only after all ten independent judgments)

Use [the response identity key](BLIND_REVIEW_KEY.md) to map Response 1/2 to A/B, compare to provisional gold and grader outputs, and record any mismatches, uncertainty, and severity in `human-review.md`. Do not mark `gold.jsonl` as human-reviewed until you personally examine and approve/correct each of the 37 records. Leave the final decision, oral defense, replay, and rubric status pending until performed.
