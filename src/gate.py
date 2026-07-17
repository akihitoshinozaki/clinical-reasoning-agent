def verify_spans(spans: list[str], note: str) -> list[bool]:
    """Returns True for each span if it appears verbatim (case-insensitive) in the note."""
    note_norm = note.lower()
    return [span.lower() in note_norm for span in spans]
