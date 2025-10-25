"""
Speech recognition for voice input.
"""
from typing import Optional
import threading


class SpeechRecognizer:
    """Speech recognition for user voice input."""
    
    def __init__(self):
        """Initialize speech recognizer."""
        self.recognizer = None
        self.microphone = None
        self.is_listening = False
        self.available = False
        
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            
            # MAXIMUM sensitivity for better recognition
            self.recognizer.energy_threshold = 100  # VERY sensitive (default ~300)
            self.recognizer.dynamic_energy_threshold = False  # Disable adaptive to force low threshold
            self.recognizer.pause_threshold = 0.4  # Seconds of silence to consider end of phrase
            self.recognizer.phrase_threshold = 0.2  # Minimum seconds of speech
            self.recognizer.non_speaking_duration = 0.4  # Seconds of silence before considering complete
            
            self.microphone = sr.Microphone()
            
            # ULTRA-FAST calibration (or skip it entirely for speed)
            print("[AUDIO] Calibrating microphone... (fast mode)")
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
            except Exception as e:
                print(f"[AUDIO] Skipping calibration: {e}")
            
            self.available = True
            print("[AUDIO] ✓ Speech Recognition initialized (FAST MODE)")
            print(f"[AUDIO] Energy threshold: {self.recognizer.energy_threshold}")
            print(f"[AUDIO] Pause threshold: {self.recognizer.pause_threshold}s")
            
        except ImportError as e:
            print(f"[AUDIO] Missing package: {e}")
            print("[AUDIO] Install with: pip install pyaudio SpeechRecognition")
        except Exception as e:
            print(f"[AUDIO] Could not initialize speech recognition: {e}")
            print("[AUDIO] Voice input will be disabled")
    
    def listen_once(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for single voice command.
        
        Args:
            timeout: Max seconds to wait for speech
        
        Returns:
            Recognized text or None
        """
        if not self.available:
            print("[AUDIO] Speech recognition not available")
            return None
        
        try:
            import speech_recognition as sr
            
            print("[AUDIO] ========== STARTING AUDIO CAPTURE ==========")
            print("[AUDIO] Opening microphone...")
            with self.microphone as source:
                print(f"[AUDIO] Microphone ready! Energy threshold: {self.recognizer.energy_threshold}")
                print(f"[AUDIO] Timeout: {timeout}s | Phrase limit: 3s")
                print("[AUDIO]")
                print("[AUDIO] ⚡⚡⚡ SPEAK NOW - LOUD and CLEAR! ⚡⚡⚡")
                print("[AUDIO]")
                
                # Much shorter timeout and phrase limit for faster response
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
                print("[AUDIO] ✓✓✓ Audio captured successfully! ✓✓✓")
            
            print("[AUDIO] Sending to Google Speech Recognition API...")
            text = self.recognizer.recognize_google(audio)
            print("[AUDIO] ========================================")
            print(f"[AUDIO] ✓ SUCCESS! Recognized text: '{text}'")
            print("[AUDIO] ========================================")
            return text
            
        except sr.WaitTimeoutError:
            print("[AUDIO] Listening timeout")
            return None
        except sr.UnknownValueError:
            print("[AUDIO] Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"[AUDIO] Recognition service error: {e}")
            return None
        except Exception as e:
            print(f"[AUDIO] Error in speech recognition: {e}")
            return None
    
    def listen_continuous(self, callback):
        """
        Listen continuously in background.
        
        Args:
            callback: Function to call with recognized text
        """
        if not self.available:
            print("Speech recognition not available")
            return
        
        def background_listen():
            import speech_recognition as sr
            
            self.is_listening = True
            with self.microphone as source:
                while self.is_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1)
                        text = self.recognizer.recognize_google(audio)
                        callback(text)
                    except:
                        pass
        
        thread = threading.Thread(target=background_listen)
        thread.daemon = True
        thread.start()
    
    def stop_listening(self):
        """Stop continuous listening."""
        self.is_listening = False
    
    def is_available(self) -> bool:
        """Check if speech recognition is available."""
        return self.available

