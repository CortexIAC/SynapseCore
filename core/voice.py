import speech_recognition as sr
import time


class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_once(self):
        try:
            with sr.Microphone() as source:
                print("[VOICE] Listening...")

                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

                # 🔥 prevent last word cutoff
                time.sleep(0.3)

                return audio

        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print("[VOICE ERROR]", e)
            return None

    def transcribe(self, audio):
        if not audio:
            return "__ERROR__"

        try:
            # noinspection PyUnresolvedReferences
            return self.recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            return "__UNKNOWN__"
        except Exception as e:
            print("[VOICE ERROR]", e)
            return "__ERROR__"