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
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            print("Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.available = True
            print("✓ Speech Recognition initialized")
            
        except Exception as e:
            print(f"Warning: Could not initialize speech recognition: {e}")
            print("Voice input will be disabled. Install pyaudio and speechrecognition.")
    
    def listen_once(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for single voice command.
        
        Args:
            timeout: Max seconds to wait for speech
        
        Returns:
            Recognized text or None
        """
        if not self.available:
            print("Speech recognition not available")
            return None
        
        try:
            import speech_recognition as sr
            
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            print("🔄 Recognizing...")
            text = self.recognizer.recognize_google(audio)
            print(f"✅ Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏱️ Listening timeout")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Recognition service error: {e}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
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

