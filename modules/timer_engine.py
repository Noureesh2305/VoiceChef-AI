import re
import time

def extract_time(text):
    total_seconds = 0
    pattern = r"(\d+)\s*(hours?|hrs?|hr|minutes?|mins?|min|seconds?|secs?|sec)"

    for value, unit in re.findall(pattern, text.lower()):
        value = int(value)
        if unit.startswith(("hour", "hr")):
            total_seconds += value * 3600
        elif unit.startswith(("minute", "min")):
            total_seconds += value * 60
        else:
            total_seconds += value

    return total_seconds or None


def format_seconds(seconds):
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        return f"{hours}h {minutes:02d}m {seconds:02d}s"
    if minutes:
        return f"{minutes}m {seconds:02d}s"
    return f"{seconds}s"

def start_timer(seconds):
    return time.time() + seconds
