# main.py
import os
import json
import anthropic

# DeepSeek を Anthropic 互換エンドポイントで使う
client = anthropic.Anthropic(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/anthropic",
)

# (1) note を1個 hardcode。MTSamples はまだ要らない。
NOTE = """58yo male, 3-day history of productive cough, fever 38.9C,
left-sided pleuritic chest pain. Smoker. Crackles on left lower lobe."""


# (2) Proposer: 候補診断と、note 内の根拠 span を出させる
def propose(note: str) -> list[dict]:
    prompt = f"""You are a clinical reasoning assistant. Given the note below,
list candidate differential diagnoses. For EACH candidate, quote the exact
span(s) from the note that support it. If a candidate has no supporting span,
return an empty evidence list for it. Do not invent spans not present.

Return ONLY valid JSON, no prose, no markdown fences, in this exact shape:
[{{"diagnosis": "...", "evidence": ["exact span copied from the note", "..."]}}]

NOTE:
\"\"\"{note}\"\"\""""

    resp = client.messages.create(
        model="deepseek-chat",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    return json.loads(text)


# (3) Gate: 根拠が閾値未満の候補は withhold する（今は placeholder）
MIN_EVIDENCE = 1


def gate(candidates: list[dict]) -> tuple[list[dict], list[dict]]:
    cited, withheld = [], []
    for c in candidates:
        if len(c.get("evidence", [])) >= MIN_EVIDENCE:
            cited.append(c)
        else:
            withheld.append(c)
    return cited, withheld


# (4) 1回だけ実行
if __name__ == "__main__":
    candidates = propose(NOTE)
    cited, withheld = gate(candidates)

    print("=== CITED DIAGNOSES ===")
    for c in cited:
        print(f"- {c['diagnosis']}")
        for e in c["evidence"]:
            print(f"    evidence: {e}")

    print("\n=== MISSINGNESS REPORT (withheld) ===")
    for c in withheld:
        print(f"- {c['diagnosis']} (withheld: no supporting evidence)")
