import io
import re

def speak(text):
    """
    Convert text to speech and return audio bytes for Streamlit.
    """
    try:
        from gtts import gTTS
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Text-to-speech needs the gTTS package. Install it with: pip install gTTS"
        ) from exc

    # Clean text (remove unicode / symbols)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    tts = gTTS(text=text, lang="en")
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)

    return audio_bytes
