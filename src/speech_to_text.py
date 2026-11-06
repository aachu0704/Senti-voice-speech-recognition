import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import speech_recognition.audio as sr_audio
import shutil

# Use Mac-compatible FLAC converter
sr_audio.get_flac_converter = lambda: shutil.which("flac") or "flac"


def record_audio(filename="recording.wav", duration=10, sample_rate=44100):
    print("Recording... Speak now!")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()
    wav.write(filename, sample_rate, recording)

    print("Recording finished!")
    return filename


def recognize_speech():
    filename = record_audio(duration=10)
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "Could not understand the audio."

    except sr.RequestError:
        return "Speech recognition service is unavailable."

    except Exception as e:
        return f"Recording error: {str(e)}"
