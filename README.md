# Clinical Reasoning Agent

An evidence-gated differential diagnosis system that **withholds diagnoses lacking retrievable supporting evidence**, targeting the trust problem in clinical decision support.

## Problem

LLMs in clinical decision support produce confident-sounding diagnoses without traceable justification. In clinical contexts, a confidently-wrong output is more dangerous than a system that abstains — because clinicians may act on it. Reducing hallucination to zero is not feasible; the practical problem is **distinguishing supported from unsupported outputs and suppressing the latter**.

## Approach

Three-agent LangGraph pipeline:

1. **Proposer** — generates candidate differential diagnoses from a clinical note
2. **Retriever** — searches for supporting evidence (note-internal spans + PubMed abstracts) per candidate
3. **Gate** — withholds any candidate whose retrieved evidence falls below an explicit threshold

The system outputs:
- **Cited diagnoses** — surviving candidates with their supporting evidence citations
- **Missingness report** — withheld candidates with the reason for withholding

The contribution is not "more accurate diagnoses." It is **honesty through structural abstention**.

## Architecture

```
Clinical Note
     ↓
[FastAPI /diagnose]
     ↓
┌─ LangGraph ──────────────────┐
│  Proposer → Retriever → Gate │
└──────────────────────────────┘
     ↓
Cited diagnoses + Missingness report
```

## Tech Stack

- Python 3.x
- LangGraph (agent orchestration)
- FastAPI (API layer)
- PubMed API / local abstract corpus (evidence retrieval)
- Anthropic API (Proposer LLM)

## Evaluation

Planned evaluation on MTSamples clinical notes:
- **Abstention–accuracy tradeoff** with gate ablation
- Measurement: % of unsupported diagnoses withheld vs. coverage retained

## Status

🚧 Work in progress. Walking skeleton (v0) under development.

## Setup

```bash
pip install -r requirements.txt
python main.py
```