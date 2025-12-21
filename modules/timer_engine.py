import re
import time

def extract_time(text):
    match = re.search(r'(\d+)\s*(minute|minutes|min|second|seconds)', text.lower())
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        return value * 60 if "min" in unit else value
    return None

def start_timer(seconds):
    return time.time() + seconds
