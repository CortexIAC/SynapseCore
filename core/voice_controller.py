import threading
from ai.router import chat
from core.voice import VoiceInput


class VoiceController:
    def __init__(self, runtime):
        self.runtime = runtime
        self.voice = VoiceInput()
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.loop, daemon=True).start()

    def stop(self):
        self.running = False

    def loop(self):
        import keyboard
        import speech_recognition as sr
        import time

        while self.running:
            # =========================
            # WAIT FOR ALT HOLD
            # =========================
            while not keyboard.is_pressed("alt"):
                time.sleep(0.05)

            app = getattr(self.runtime.state, "app", None)

            # =========================
            # LISTENING
            # =========================
            if app and hasattr(app, "set_voice_state"):
                app.set_voice_state("listening")

            self.runtime.debug("[VOICE STATE] listening")
            self.runtime.voice_log("[VOICE] Listening...")

            audio_data = []

            with sr.Microphone() as source:
                self.voice.recognizer.adjust_for_ambient_noise(source, duration=0.2)

                while keyboard.is_pressed("alt"):
                    try:
                        audio = self.voice.recognizer.listen(
                            source,
                            timeout=1,
                            phrase_time_limit=2
                        )
                        audio_data.append(audio)
                    except:
                        pass

            # wait for full release
            while keyboard.is_pressed("alt"):
                time.sleep(0.02)

            # =========================
            # PROCESSING
            # =========================
            if app and hasattr(app, "set_voice_state"):
                app.set_voice_state("processing")

            self.runtime.debug("[VOICE STATE] processing")
            self.runtime.voice_log("[VOICE] Processing...")

            if not audio_data:
                self.runtime.voice_log("[VOICE] No input")

                if app and hasattr(app, "set_voice_state"):
                    app.set_voice_state("idle")

                self.runtime.debug("[VOICE STATE] idle")
                continue

            combined = sr.AudioData(
                b"".join([a.get_raw_data() for a in audio_data]),
                audio_data[0].sample_rate,
                audio_data[0].sample_width
            )

            text = self.voice.transcribe(combined)

            if text in ["__ERROR__", "__UNKNOWN__"]:
                self.runtime.voice_log("[VOICE] Failed")

                if app and hasattr(app, "set_voice_state"):
                    app.set_voice_state("idle")

                self.runtime.debug("[VOICE STATE] idle")
                continue

            self.runtime.voice_log(f"[VOICE] {text}")

            response = chat(text, self.runtime.state)

            self.runtime.voice_log(f"[VOICE RESPONSE] {response}")

            # =========================
            # IDLE
            # =========================
            if app and hasattr(app, "set_voice_state"):
                app.set_voice_state("idle")

            self.runtime.debug("[VOICE STATE] idle")