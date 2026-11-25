import re

MAX_INPUT_LENGTH = 3000

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?rules",
    r"reveal\s+(your\s+)?(system|developer)\s+prompt",
    r"show\s+(your\s+)?(system|developer)\s+instructions",
    r"bypass\s+(your\s+)?safety",
    r"override\s+(all\s+)?instructions",
]

SECRET_PATTERNS = [
    r"(?i)\bpassword\s*[:=]\s*\S+",
    r"(?i)\bapi[_ -]?key\s*[:=]\s*\S+",
    r"\bsk-[A-Za-z0-9_-]{20,}\b",
    r"\b\d{5}-\d{7}-\d\b",
    r"(?<!\d)(?:\+92|0)3\d{9}(?!\d)",
]

def check_input(message):
    """Check user input before sending it to the model."""

    if not isinstance(message, str) or not message.strip():
        return False, "Please enter a valid message."

    if len(message) > MAX_INPUT_LENGTH:
        return False, "Your message is too long. Please shorten it."

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return False, "Your message contains a prohibited instruction."

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, message):
            return False, "Do not share passwords, API keys, or personal information."

    return True, "Input accepted."


def check_output(message):
    """Check model output for accidental secret disclosure."""

    if not isinstance(message, str):
        return False, "Invalid response."

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, message):
            return False, "Response blocked because it may contain sensitive information."

    return True, message
