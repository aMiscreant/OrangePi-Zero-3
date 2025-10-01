# utils/matcher.py
import hashlib
import time

# Debounce configuration
_last_triggered = {}
_DEBOUNCE_SECONDS = 0.5  # ignore repeats within 0.5s

def normalize_code(raw_code, length=16):
    """
    Normalize an IR code:
    - Remove non-hex characters
    - Lowercase
    - Truncate
    - Return SHA256 hash for matching
    """
    raw = "".join(c for c in raw_code.lower().strip() if c in "0123456789abcdef")
    truncated = raw[:length]
    return hashlib.sha256(truncated.encode()).hexdigest()


def match_code(raw_code, known_codes, norm_length=16):
    """
    Match a raw IR code against known codes.
    Returns the label if found and not recently triggered.
    """
    norm = normalize_code(raw_code, length=norm_length)
    now = time.time()

    # Debounce: ignore if triggered recently
    last_time = _last_triggered.get(norm, 0)
    if now - last_time < _DEBOUNCE_SECONDS:
        return None

    # Check all variants per label
    for label, variants in known_codes.items():
        for v in variants:
            if normalize_code(v, length=norm_length) == norm:
                _last_triggered[norm] = now
                return label

    return None
