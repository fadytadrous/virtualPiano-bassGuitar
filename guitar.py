import  numpy as np
from IPython.display import display
from IPython.display import Audio
import sounddevice as sd
import simpleaudio as sa

notes_range = np.arange(-9,3)
A_freq = 440
notes_freq=np.zeros(12)
for i in range(len(notes_range)):
    notes_freq[i] = A_freq*2**(notes_range[i]/12)
fs = 44100
def karplus_strong(wavetable, n_samples):
    """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging."""
    samples = []
    current_sample = 0
    previous_value = 0
    while len(samples) < n_samples:
        wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)
freqs = np.logspace(0, 1, num=13, base=2) * 55

for freq in freqs:
    wavetable_size = fs // int(freq)
    wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
    sample = karplus_strong(wavetable, 1 * fs)
    sd.play(sample, fs)