from fastapi import FastAPI
from src.gate import verify_spans

app = FastAPI()

# Hardcoded for the skeleton — replaced with real note input in M2
NOTE = "Patient presents with chest pain, shortness of breath, and elevated troponin."


def stub_proposer(note: str):
    """Fake LLM output: diagnosis + self-reported supporting spans.
    One span is real (in the note), one is hallucinated (not in the note),
    to prove the gate actually discriminates."""
    return [
        {
            "diagnosis": "Myocardial infarction",
            "spans": ["chest pain", "elevated troponin"],
        },
        {
            "diagnosis": "Pulmonary embolism",
            "spans": ["shortness of breath", "positive D-dimer"],
        },
    ]


@app.get("/diagnose")
def diagnose():
    candidates = stub_proposer(NOTE)
    cited = []
    withheld = []

    for c in candidates:
        results = verify_spans(c["spans"], NOTE)
        if all(results):
            cited.append({"diagnosis": c["diagnosis"], "evidence": c["spans"]})
        else:
            failed = [s for s, ok in zip(c["spans"], results) if not ok]
            withheld.append(
                {"diagnosis": c["diagnosis"], "reason": f"unverified spans: {failed}"}
            )

    return {"cited_diagnoses": cited, "missingness_report": withheld}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
