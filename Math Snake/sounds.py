"""
Sound management module for Math Snake.

This module generates procedural sound effects using sine waves
and chords for various game events.
"""

import pygame
import numpy as np
from config import C5, E5, G5, C6

class SoundManager:
    """
    Manages all sound effects in the game using procedurally generated tones.
    
    Generates sounds from scratch using sine waves rather than loading audio files,
    providing eat, correct, wrong, victory, and collision sound effects.
    """
    
    def __init__(self):
        """
        Initialize the sound system and generate all game sounds.
        
        Sets up pygame mixer with:
        - frequency=22050: 22.05 kHz sample rate (standard for small games)
        - size=-16: 16-bit signed samples (CD-quality audio)
        - channels=2: stereo (left + right)
        - buffer=512: internal audio buffer size for low latency
        """
        # frequency=22050 => 22.05 kHz sample rate (standard for small games).
        # size=-16 => 16-bit signed samples (CD-quality audio).
        # channels=2 => stereo (left + right).
        # buffer=512 => internal audio buffer size.
        # this is the size of the internal audio buffer in samples.
        # think of it as a temporary storage area for audio data before it's sent to the sound card.
        # smaller buffer => lower latency (sound plays faster after calling .play()), 
        # but may risk audio glitches if CPU can't keep up.
        # larger buffer => more stable playback, but slightly higher delay between calling .play() and hearing the sound.
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.generate_sounds()
        
    def generate_tone(self, frequency, duration, volume=0.3):
        """
        Generate a pure tone using a sine wave.
        
        Creates a single-frequency sound with fade in/out envelope to prevent clicking.
        Uses the formula: y[n] = sin(2*pi*f*n/R) where:
        - f = frequency (cycles per second)
        - R = sample rate (samples per second)
        - n = sample index (time step)
        
        Args:
            frequency (float): Frequency of the tone in Hz
            duration (float): Length of the sound in seconds
            volume (float): Volume multiplier (0.0 to 1.0), default 0.3
            
        Returns:
            pygame.Sound: The generated sound object
        """
        sample_rate = 22050
        num_samples = int(sample_rate * duration)
        
        # generate sine wave
        # y[n] = sin(2*pi*f*n/R) = sin(2*pi*f*t)
        # f = freq (cyles per sec), R = sample rate (samples per sec)
        # n = samples index (time step [0,1,2,3,...])
        # t = n/R = time in seconds, convert index to time
        samples = np.sin(2 * np.pi * np.arange(num_samples) * frequency / sample_rate)
        
        # apply envelope (fade in/out) to avoid clicks
        #        n/F     , n < F
        # E[n] = 1       , F <= n <= N-F
        #        (N-n)/F , n > N-F
        # F = fade length, N = total samples
        envelope = np.ones(num_samples)
        fade_length = int(sample_rate * 0.01)
        envelope[:fade_length] = np.linspace(0, 1, fade_length)
        envelope[-fade_length:] = np.linspace(1, 0, fade_length)
        
        # x[n] = E[n] * y[n] * V
        samples = samples * envelope * volume
        
        # convert to 16-bit integer
        samples = (samples * 32767).astype(np.int16)
        
        # create stereo sound
        stereo_samples = np.column_stack((samples, samples))
        
        sound = pygame.sndarray.make_sound(stereo_samples)
        return sound
    
    def generate_chord(self, frequencies, duration, volume=0.2):
        """
        Generate a musical chord by combining multiple sine waves.
        
        Creates a harmonious sound by summing sine waves at different frequencies,
        then normalizes and applies fade in/out envelope.
        
        Args:
            frequencies (list): List of frequencies in Hz to combine
            duration (float): Length of the sound in seconds
            volume (float): Volume multiplier (0.0 to 1.0), default 0.2
            
        Returns:
            pygame.Sound: The generated chord sound object
        """
        sample_rate = 22050
        num_samples = int(sample_rate * duration)
        
        # generate and sum multiple sine waves
        samples = np.zeros(num_samples)
        for freq in frequencies:
            samples += np.sin(2 * np.pi * np.arange(num_samples) * freq / sample_rate)
        
        # normalize
        samples = samples / len(frequencies)
        
        # apply envelope
        envelope = np.ones(num_samples)
        fade_length = int(sample_rate * 0.01)
        envelope[:fade_length] = np.linspace(0, 1, fade_length)
        envelope[-fade_length:] = np.linspace(1, 0, fade_length)
        
        samples = samples * envelope * volume
        samples = (samples * 32767).astype(np.int16)
        stereo_samples = np.column_stack((samples, samples))
        
        sound = pygame.sndarray.make_sound(stereo_samples)
        return sound
    
    def generate_sounds(self):
        """
        Generate all game sound effects and store them in the sounds dictionary.
        
        Creates:
        - 'eat': 800Hz beep for collecting numbers
        - 'correct': C major chord for correct digit sequence
        - 'wrong': 150Hz buzz for incorrect digit
        - 'victory': C major chord with octave for winning
        - 'collision': Dual-frequency sound for wall/self collision
        """
        # eating number sound - beep
        self.sounds['eat'] = self.generate_tone(800, 0.1, 0.3)
        
        # correct number sound - C major chord
        self.sounds['correct'] = self.generate_chord([C5, E5, G5], 0.15, 0.25)
        
        # wrong number sound - low buzz
        self.sounds['wrong'] = self.generate_tone(150, 0.3, 0.4)
        
        # victory sound - C major chord with an added octave
        self.sounds['victory'] = self.generate_chord([C5, E5, G5, C6], 0.5, 0.3)
        
        # collision sound - low buzz with a sharp clickly edge
        self.sounds['collision'] = self.generate_chord([120, 800], 0.15, 0.35)
    
    def play(self, sound_name):
        """
        Play a sound effect by name.
        
        Args:
            sound_name (str): Name of the sound to play
                ('eat', 'correct', 'wrong', 'victory', 'collision')
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def stop_all(self):
        """Stop all currently playing sounds."""
        pygame.mixer.stop()