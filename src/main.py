from src.gate import verify_spans

if __name__ == "__main__":
    note = "Patient presents with chest pain and shortness of breath."
    spans = ["chest pain", "fever"]
    print(verify_spans(spans, note))
