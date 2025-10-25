"""
Text-to-speech output for audio feedback.
"""
import threading
from config.settings import settings


class TTSEngine:
    """Text-to-speech engine for audio output."""
    
    def __init__(self, use_online: bool = None):
        """
        Initialize TTS engine.
        
        Args:
            use_online: Use gTTS (online) vs pyttsx3 (offline). If None, uses settings.
        """
        self.use_online = use_online if use_online is not None else settings.use_online_tts
        self.engine = None
        self.available = False
        
        if not self.use_online:
            # Try to initialize offline pyttsx3
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', settings.tts_rate)
                self.engine.setProperty('volume', settings.tts_volume)
                
                # Use female voice if available
                voices = self.engine.getProperty('voices')
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                
                self.available = True
                print("✓ TTS Engine initialized (offline mode)")
                
            except Exception as e:
                print(f"Warning: Could not initialize pyttsx3: {e}")
                print("TTS will be disabled. Install pyttsx3 for offline TTS.")
        else:
            # Online mode (gTTS)
            try:
                import gtts
                self.available = True
                print("✓ TTS Engine initialized (online mode)")
            except Exception as e:
                print(f"Warning: Could not import gTTS: {e}")
                print("TTS will be disabled.")
    
    def speak(self, text: str, blocking: bool = False):
        """
        Speak text aloud.
        
        Args:
            text: Text to speak
            blocking: Wait for speech to finish
        """
        if not text or not self.available:
            return
        
        print(f"🔊 Speaking: {text}")
        
        try:
            if self.use_online:
                self._speak_gtts(text)
            else:
                if blocking:
                    self.engine.say(text)
                    self.engine.runAndWait()
                else:
                    # Run in separate thread to avoid blocking
                    thread = threading.Thread(target=self._speak_async, args=(text,))
                    thread.daemon = True
                    thread.start()
        except Exception as e:
            print(f"Error in TTS: {e}")
    
    def _speak_async(self, text: str):
        """Speak in async mode (pyttsx3)."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in async TTS: {e}")
    
    def _speak_gtts(self, text: str):
        """Speak using gTTS (online)."""
        try:
            from gtts import gTTS
            from playsound import playsound
            import tempfile
            import os
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file)
            
            # Play audio
            playsound(temp_file)
            
            # Cleanup
            os.remove(temp_file)
            
        except Exception as e:
            print(f"Error in gTTS: {e}")
    
    def stop(self):
        """Stop current speech."""
        if not self.use_online and self.engine:
            try:
                self.engine.stop()
            except:
                pass
    
    def is_available(self) -> bool:
        """Check if TTS is available."""
        return self.available

